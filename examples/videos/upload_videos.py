import sys
import os
import argparse

sys.path.append(os.path.join(sys.path[0], '../../'))
from instabot import Bot

import captions_for_medias

parser = argparse.ArgumentParser(add_help=True)
parser.add_argument('-u', type=str, help="username")
parser.add_argument('-p', type=str, help="password")
parser.add_argument('-proxy', type=str, help="proxy")
parser.add_argument('-video', type=str, help="video name")
parser.add_argument('-caption', type=str, help="caption for video")
args = parser.parse_args()

bot = Bot()
bot.login()

posted_videos_file = "videos.txt"

posted_video_list = []
caption = ''

if not os.path.isfile(posted_videos_file):
    with open(posted_videos_file, 'w'):
        pass
else:
    with open(posted_videos_file, 'r') as f:
        posted_video_list = f.read().splitlines()

# Get the filenames of the videos in the path ->
if not args.video:
    import glob
    videos = [os.path.basename(x) for x in glob.glob("media/*.mp4")]
    from random import shuffle
    shuffle(videos)
else:
    videos = [args.video]
videos = list(set(videos) - set(posted_video_list))
if len(videos) == 0:
    if not args.video:
        bot.logger.warn("NO MORE VIDEOS TO UPLOAD")
        exit()
    else:
        bot.logger.error("The video `{}` has already been posted".format(videos[0]))
try:
    for video in videos:
        bot.logger.info("Checking {}".format(video))
        if args.caption:
            caption = args.caption
        else:
            if captions_for_medias.CAPTIONS.get(video):
                caption = captions_for_medias.CAPTIONS[video]
            else:
                try:
                    caption = raw_input("No caption found for this media. Type the caption now: ")
                except NameError:
                    caption = input("No caption found for this media. Type the caption now: ")
        bot.logger.info("Uploading video `{video}` with caption: `{caption}`".format(video=video, caption=caption))
        if not bot.upload_video(os.path.dirname(os.path.realpath(__file__)) + "/media/" + video, caption=caption):
            bot.logger.error("Something went wrong...")
            break
        posted_video_list.append(video)
        with open(posted_videos_file, 'a') as f:
            f.write(video + "\n")
        bot.logger.info("Succesfully uploaded: " + video)
        break
except Exception as e:
    bot.logger.error("\033[41mERROR...\033[0m")
    bot.logger.error(str(e))
