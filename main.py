import sys
import os
import ctypes

ctypes.windll.kernel32.SetConsoleTitleW("Music Player [Shan]")
# Add the environment path
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(dir_path, 'env'))
sys.path.append(os.path.join(dir_path, 'env', 'lib', 'site-packages'))

import urllib.request
import urllib
import re
import pafy
from utils import printProgressBar, play_stream


while True:
    print("> ", end='')
    request = input()
    if request.strip() == 'exit':
        sys.exit()
    
    search_query = '+'.join(request.strip().split())

    html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + search_query)
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    video_url = "https://www.youtube.com/watch?v=" + video_ids[0]

    video = pafy.new(video_url)
    streams_dict = dict()
    for stream in video.allstreams:
        streams_dict[stream.get_filesize()] = stream

    if not streams_dict:
        print("No stream found!")
        sys.exit()

    total_streams = streams_dict.items()

    stream_audios = []
    stream_videos = []
    for s in total_streams:
        if s[1].mediatype == 'audio':
            stream_audios.append(s)
        else:
            stream_videos.append(s)

    streams = sorted(stream_audios) + sorted(stream_videos)

    streams_count = len(streams)
    stream_index = 0
    while stream_index < streams_count:
        try:
            selected_stream = streams[stream_index][1]
            # if stream_index == 9:
            #     ret = play_stream(streams[0][1])
            # else:
            #     ret = play_stream(selected_stream)
            ret = play_stream(selected_stream)
            if ret == -1:
                raise Exception("vlc is unable to play this stream")
            else:
                break
        except Exception:
            print("\r                                                  \r", end='', flush=True)
            print(stream_index+1, "Error occured! Going to the next stream url...", end='', flush=True)
            stream_index += 1

    if stream_index == streams_count:
        print("\nUnable to play any stream url for this request!")