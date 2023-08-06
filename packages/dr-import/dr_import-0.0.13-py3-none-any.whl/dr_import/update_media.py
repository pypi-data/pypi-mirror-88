#!/usr/bin/env python3

import argparse
import os
import subprocess
import tator
import tqdm
import tempfile

from tator.transcode.upload import upload_file
from tator.transcode.make_thumbnails import make_thumbnails
from tator.transcode.transcode import make_video_definition
from tator.transcode.make_fragment_info import make_fragment_info
from tator.openapi.tator_openapi.models import CreateResponse

if __name__=="__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--host', type=str,default='https://www.tatorapp.com')
    parser.add_argument('--token', type=str)
    parser.add_argument('--type-id', type=int)
    parser.add_argument('--target-fps', type=int, default=15)
    parser.add_argument('--workflow-mode', action='store_true')
    args = parser.parse_args()

    if args.workflow_mode:
        api = tator.get_api("https://www.tatorapp.com",
                            os.getenv('TATOR_AUTH_TOKEN'))
    else:
        api = tator.get_api(args.host, args.token)

    if args.workflow_mode:
        # Infer arguments from workflow env
        media_ids_str = os.getenv('TATOR_MEDIA_IDS')
        media_ids = [int(m) for m in media_ids_str.split(',')]
        print(media_ids_str)
        print(media_ids)
        media_first = api.get_media(media_ids[0])
        media_type_id = media_first.meta
        media_type = api.get_media_type(media_type_id)
        project = os.getenv('TATOR_PROJECT_ID')
        media_list = api.get_media_list(project, type=args.type_id, media_id=media_ids)
    else:
        media_type = api.get_media_type(args.type_id)
        project = media_type.project
        media_list = api.get_media_list(project, type=args.type_id)

    bad_fps = []
    need_360 = []
    print(f"Processing {len(media_list)}")
    for media in media_list:
        if media.fps != args.target_fps:
            bad_fps.append(media)
            continue
        if media.media_files:
            streaming = media.media_files.streaming
        else:
            streaming = []
        available = [x.resolution[0] for x in streaming]
        print(f"{available} {360 in available}")
        if not 360 in available and len(available) > 0:
            need_360.append(media)

    #print(f"Bad fps: {len(bad_fps)}")
    print(f"Needs 360 Transcode: {len(need_360)}")

    for video in tqdm.tqdm(need_360):
        with tempfile.TemporaryDirectory() as td:
            source_file = os.path.join(td, "source.mp4")
            transcoded_file = os.path.join(td, "360.mp4")
            segments_file = os.path.join(td, "segments.json")
            print(f"Downloading {media.name}")
            for progress in tator.util.download_media(api, video, source_file):
                print(f"\r{progress}%",end='')

            cmd = [
                "ffmpeg", "-y",
                "-i", source_file,
                "-an",
                "-metadata:s", "handler_name=tator",
                "-g", "25",
                "-preset", "fast",
                "-movflags",
                "faststart+frag_keyframe+empty_moov+default_base_moof",
                "-tune", "fastdecode",
                "-vcodec", "libx264",
                "-crf", "28",
                "-pix_fmt", "yuv420p",
                "-vf", "scale=-2:360",
                transcoded_file
            ]

            subprocess.run(cmd)

            make_fragment_info(transcoded_file, segments_file)
            media_url = upload_file(transcoded_file, api)
            segments_url = upload_file(segments_file, api)
            spec = {
                    'media_files': {'streaming': [{
                        **make_video_definition(transcoded_file),
                        'url': media_url,
                        'segments_url': segments_url,
                    }]}
            }
            response = api.move_video(video.id, move_video_spec=spec)
            print(f"Updated {video.id}") 

    
        
    
