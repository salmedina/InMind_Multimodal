#!/usr/bin/env python

import os
import yaml
import urllib
import json
import pprint

def is_valid_file(parser, arg):
  """
  Check if arg is a valid file that already exists on the file system.
  """
  arg = os.path.abspath(arg)
  if not os.path.exists(arg):
    parser.error("The file %s does not exist!" % arg)
  else:
    return arg

def get_parser():
  """Get parser object for this script"""
  from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
  parser = ArgumentParser(description=__doc__,
                          formatter_class=ArgumentDefaultsHelpFormatter)
  parser.add_argument("-k", "--key",
                      dest="key_filename",
                      type=lambda x: is_valid_file(parser, x),
                      help="YAML FILE with the API key",
                      metavar="FILE")
  parser.add_argument("-u", "--username",
                      dest="username",
                      type=str,
                      help="YouTube query username")
  parser.add_argument("-pl", "--playlist",
                      dest="playlist",
                      type=str,
                      help="YouTube query playlist from queried username")
  parser.add_argument("-o", "--output",
                      dest="out_filename",
                      type=str,
                      help="Text FILE where the video url's will be stored")
  return parser

def load_api_key(key_filename):
    loaded_dict = yaml.load(open(key_filename, 'r'))
    return loaded_dict['key']

def get_channel_id(api_key, username):
    channel_id = ''
    searchUrl = 'https://www.googleapis.com/youtube/v3/search'
    params = {'q': username, 'key': api_key, 'part': 'snippet', 'type': 'channel'}
    url = '%s?%s' % (searchUrl, urllib.urlencode(params))
    response = urllib.urlopen(url).read()
    data = json.loads(response)

    for i in data['items']:
        if i['snippet']['channelTitle'].lower() == username.lower():
            channel_id = i['snippet']['channelId']
            break

    return channel_id

def get_playlist_id(api_key, channel_id, playlist_name):
    playlist_id = ''
    playlistUrl = 'https://www.googleapis.com/youtube/v3/playlists'

    params = {'key': api_key,
              'part': 'snippet', 'channelId': channel_id}
    url = '%s?%s' % (playlistUrl, urllib.urlencode(params))
    response = urllib.urlopen(url).read()
    data = json.loads(response)

    while len(data['items']) > 0 and playlist_id=='':
        for i in data['items']:
            print i['snippet']['title']
            if i['snippet']['title'].lower() == playlist_name.lower():
                playlist_id = i['id']
                break
        if 'nextPageToken' in data:
            params['pageToken'] = data['nextPageToken']
            url = '%s?%s' % (playlistUrl, urllib.urlencode(params))
            response = urllib.urlopen(url).read()
            data = json.loads(response)
        else:
            break


    return playlist_id

def get_playlist_video_info(api_key, playlist_id):
    pItemsUrl = 'https://www.googleapis.com/youtube/v3/playlistItems'
    params = {'key': api_key, 'playlistId': playlist_id, 'part': 'snippet', 'maxResults': 50}
    url = '%s?%s' % (pItemsUrl, urllib.urlencode(params))
    response = urllib.urlopen(url).read()
    data = json.loads(response)

    video_info = []

    while len(data['items']) > 1:
        for i in data['items']:
            tmp = {}
            tmp['title'] = i['snippet']['title']
            tmp['desc'] = i['snippet']['description']
            tmp['id'] = i['snippet']['resourceId']['videoId']
            video_info.append(tmp)

        if 'nextPageToken' in data:
            params['pageToken'] = data['nextPageToken']
            url = '%s?%s' % (pItemsUrl, urllib.urlencode(params))
            response = urllib.urlopen(url).read()
            data = json.loads(response)
        else:
            break

    return video_info


def get_video_watch_links(api_key, video_info):
    watchUrl = 'https://www.youtube.com/watch?v='
    urls = []
    for video in video_info:
        url = '%s%s' % (watchUrl, video['id'])
        urls.append(url)

    return urls

def get_video_urls(api_key, username, playlist, output):
    channel_id = get_channel_id(api_key, username)
    playlist_id = get_playlist_id(api_key, channel_id, playlist)
    video_info = get_playlist_video_info(api_key, playlist_id)
    video_urls = get_video_watch_links(api_key, video_info)

    out_file = open(output, 'w')
    out_txt = '\n'.join(video_urls)
    out_file.write(out_txt)
    out_file.close()

if __name__ == "__main__":
    args = get_parser().parse_args()

    api_key = load_api_key(args.key_filename)
    get_video_urls(api_key, args.username, args.playlist, args.out_filename)
