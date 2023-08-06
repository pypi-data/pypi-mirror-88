#!/usr/bin/python3

import argparse
import tator
from collections import defaultdict
from dateutil.parser import parse
import os
from pprint import pprint
import datetime
import tqdm
import uuid

if __name__=="__main__":
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument('--host', type=str,default='https://www.tatorapp.com')
  parser.add_argument('--token', type=str,required=True)
  parser.add_argument('--multi-type-id', type=int, required=True)
  parser.add_argument('--quality', default=360, type=int)
  parser.add_argument('trip_id')
  args = parser.parse_args()

  start_date=parse(args.start_date)
  end_date=parse(args.end_date)

  api = tator.get_api(args.host, args.token)

  media_type = api.get_media_type(args.multi_type_id)
  project = media_type.project

  media_list = api.get_media_list(project, attribute=f"Trip::{args.trip_id}")
  time_joined=defaultdict(lambda:[])
  print(f"Processing {len(media_list)} media files")
  for media in tqdm.tqdm(media_list):
    try:
      video_start_str=os.path.splitext(media.name)[0].replace('_',':')
      date = parse(video_start_str)
    except:
      print(f"Bad Date {media.attributes.get('Date',None)}")
      continue
    if date >= start_date and date <= end_date:
      video_start_str=os.path.splitext(media.name)[0].replace('_',':')
      camera_ip = section_map.get(media.attributes.get('Camera'),
                                  None)
      # Round to the nearest whole second
      video_start = parse(video_start_str)
      seconds = int(datetime.datetime.timestamp(video_start))
      video_start = datetime.datetime.fromtimestamp(seconds)
      time_joined[video_start].append(media)

  print("Linking up")
  for name,medias in tqdm.tqdm(time_joined.items()):
    # Sort by IP address
    medias.sort(key=lambda x:x.attributes['Camera'])
    media_ids = [x.id for x in medias]
    print(name)
    print(media_ids)
    tator.util.make_multi_stream(api,
                                 args.multi_type_id,
                                 [2,2],
                                 name.isoformat(),
                                 media_ids,
                                 section=args.trip_id,
                                 quality=args.quality)
    

  
  
