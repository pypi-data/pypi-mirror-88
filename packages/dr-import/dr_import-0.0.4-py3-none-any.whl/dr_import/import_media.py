#!/usr/bin/python3

import os
from datetime import datetime,timedelta
from dateutil.parser import parse
import tempfile
import time
import uuid
import yaml

import tator
from tator.transcode.upload import upload_file
from tator.transcode.make_thumbnails import make_thumbnails
from tator.transcode.transcode import make_video_definition
from tator.transcode.make_fragment_info import make_fragment_info
from tator.openapi.tator_openapi.models import CreateResponse


def filenameToTime(path):
    """Assuming filename is {uuid}.ext convert to datetime """
    filename=os.path.basename(path)
    uuid_str=os.path.splitext(filename)[0].split('_')[-1]
    uid=uuid.UUID(uuid_str)
    date=datetime(1582, 10, 15) + timedelta(microseconds=uid.time//10)
    return date

if __name__=="__main__":
    parser = tator.get_parser()
    parser.add_argument("--type-id",
                        required=True,
                        type=int)
    parser.add_argument("--section-lookup",
			type=str)
    parser.add_argument("--skip-archival",
                        action="store_true")
    parser.add_argument("--trip-id",
                        required=True,
                        type=str)
    parser.add_argument('--date-start',
                        type=str,
                        required=True)
    parser.add_argument('--date-end',
                        type=str,
                        required=True)

    parser.add_argument("directory")
    args = parser.parse_args()
    start_date = parse(args.date_start)
    end_date = parse(args.date_end)
    api = tator.get_api(args.host, args.token)

    media_type = api.get_media_type(args.type_id)
    project = media_type.project

    uploaded_count=0
    skipped_count=0
    start_time = datetime.now()
    upload_gid = str(uuid.uuid1())
    section_lookup = {}
    if args.section_lookup:
        with open(args.section_lookup,'r') as fp:
            section_lookup = yaml.safe_load(fp)

    print(f"Processing {args.directory}")

    all_media = api.get_media_list(project, type=args.type_id)
    print(f"Downloaded {len(all_media)} records")
    for root, dirs,files in os.walk(args.directory):
        looking_for=['archival.mp4','360.mp4','streaming.mp4']
        found = set(looking_for).intersection(set(files))
        if len(found) == 0:
            print(f"No streaming/archival found in {root}")
            continue
        media_file = list(found)[0]
        media_path = os.path.join(root,media_file)
        this_camera = os.path.basename(os.path.dirname(root))
        # Make media element to get ID


        time_str=os.path.basename(root)
        recording_date = parse(time_str.replace('_',':'))
        if recording_date < start_date or recording_date > end_date:
            print(f"Skipping {time_str}")
            continue

        sensor=os.path.basename(os.path.dirname(root))
        # Format = [pk_]YYYY-MM-DDTHH_MM_SS.ZZZZZ
        encoded=time_str
        fname = f"{time_str}.mp4"
        date_code = encoded.split('T')[0]
        time_code = encoded.split('T')[1]
        date_comps = date_code.split('_')[-1].split('-')
        time_comps = time_code.split('_')
        date=datetime(year=int(date_comps[0]),
                      month=int(date_comps[1]),
                      day=int(date_comps[2]),
                      hour=int(time_comps[0]),
                      minute=int(time_comps[1]),
                      second=int(float(time_comps[2])))

        # Assign section name based on alias rules.
        if sensor in section_lookup:
            section=section_lookup[sensor]
        else:
            section=sensor

        existing=False
        for previous in all_media:
            camera = previous.attributes.get('Camera',
                                             None)
            if previous.name == fname and camera == this_camera:
                existing=True

        if existing:
            print(f"{media_path}: Found Existing")
            skipped_count+=1
            continue
        uploaded_count+=1

        attributes={"Camera": this_camera,
                    "Date": date_code,
                    "Time": time_code,
                    "Trip": args.trip_id}

        md5sum = tator.util.md5sum(media_path)
        spec ={
            'type': args.type_id,
            'section': section,
            'name': fname,
            'md5': md5sum,
            'gid': upload_gid,
            'uid': str(uuid.uuid1())
        }
        if attributes:
            spec.update({'attributes': attributes})

        response = api.create_media(project, media_spec=spec)
        assert isinstance(response, CreateResponse)
        media_id = response.id

        try:
            with tempfile.TemporaryDirectory() as td:
                try:
                    thumb_path = os.path.join(td,f"{uuid.uuid4()}.jpg")
                    thumb_gif_path = os.path.join(td, f"{uuid.uuid4()}.gif")
                    make_thumbnails(args.host, args.token, media_id,
                                media_path, thumb_path,thumb_gif_path)
                except Exception as e:
                    print("Thumbnail error")
                    continue
        except Exception as e:
            print("WARNING: Could not delete file..")
            print(e)
        # Now process each file
        def upload_path(path):
            full_path=os.path.join(root,path)
            file_type = os.path.splitext(path)[0]
            if file_type == "archival":
                if args.skip_archival is True:
                    return True
                url = upload_file(full_path, api)
                spec = {
                    'media_files': {'archival': [{
                        **make_video_definition(full_path),
                        'url': url,
                    }]}
                }
                # Move video file with the api.
                response = api.move_video(media_id, move_video_spec=spec)
            elif file_type == "streaming":
                url = upload_file(full_path, api)
                with tempfile.TemporaryDirectory() as td:
                    segments_path = os.path.join(td,"{uuid.uuid4()}.json")
                    make_fragment_info(full_path, segments_path)
                    segments_url = upload_file(segments_path, api)
                # Construct move video spec.
                spec = {
                    'media_files': {'streaming': [{
                        **make_video_definition(full_path),
                        'url': url,
                        'segments_url': segments_url,
                    }]}
                }
                response = api.move_video(media_id, move_video_spec=spec)
            elif file_type == "360":
                url = upload_file(full_path, api)
                with tempfile.TemporaryDirectory() as td:
                    segments_path = os.path.join(td,"{uuid.uuid4()}.json")
                    make_fragment_info(full_path, segments_path)
                    segments_url = upload_file(segments_path, api)
                # Construct move video spec.
                spec = {
                    'media_files': {'streaming': [{
                        **make_video_definition(full_path),
                        'url': url,
                        'segments_url': segments_url,
                    }]}
                }
                response = api.move_video(media_id, move_video_spec=spec)


            print(f"{path}: Upload as {time_str} to {section} -- {attributes}")
            return True

        # Fault tolerant loop
        for idx,path in enumerate(files):
            done = False
            if os.path.splitext(path)[-1] == ".mp4":
                while not done:
                    try:
                        done = upload_path(path)
                    except Exception as exception:
                        print(f"Encountered error ({exception}), sleeping and retrying.")
                        time.sleep(5)


    print(f"Skipped {skipped_count} files")
    print(f"Uploaded {uploaded_count} files")
