import pafy
import os

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
  parser.add_argument("-i", "--input",
                      dest="input_filename",
                      type=lambda x: is_valid_file(parser, x),
                      help="Text file with video urls list",
                      metavar="FILE")
  parser.add_argument("-s", "--savedir",
                      dest="save_dir",
                      type=str,
                      help="Directory where the videos will be downloaded")

  return parser

def download_videos(input_filename, save_dir):
    WATCH_URL = 'https://www.youtube.com/watch?v='
    input_file = open(input_filename, 'r')
    urls = input_file.readlines()

    for url in urls:
        video = pafy.new(url)
        for stream in video.streams:
            # Saves the first (smallest) mp4 format that it finds
            if stream.extension == 'mp4':
                save_filename = '%s.mp4'%(url.strip().replace(WATCH_URL, ''))
                save_file_path = os.path.join(save_dir, save_filename)
                stream.download(save_file_path)
                break

if __name__ == "__main__":
    args = get_parser().parse_args()

    download_videos(args.input_filename, args.save_dir)
