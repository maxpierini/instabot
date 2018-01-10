import os
from tqdm import tqdm
from . import delay


def upload_video(self, video, thumbnail, caption=''):
    delay.small_delay(self)
    self.logger.info("Started uploading '{video}'".format(video=video))
    if not super(self.__class__, self).uploadVideo(video, thumbnail, caption):
        self.logger.info("Video '%s' is not %s ." % (video, 'uploaded'))
        return False
    self.logger.info("Video '{video}' uploaded".format(video=video))
    return True

def download_video(self, media_id, path='video/', filename=None, description=False):
    delay.small_delay(self)
    if not os.path.exists(path):
        os.makedirs(path)
    if description:
        media = self.get_media_info(media_id)[0]
        caption = media['caption']['text']
        with open('{path}{0}_{1}.txt'.format(media['user']['username'], media_id, path=path), encoding='utf8', mode='w') as f:
            f.write(caption)
    video = super(self.__class__, self).downloadVideo(media_id, filename, False, path)
    if video:
        return video
    if video == False:
        return "not_a_video"
    self.logger.info("Media with %s is not %s ." % (media_id, 'downloaded'))
    return False

def download_videos(self, medias, path, description=False):
    broken_items = []
    if len(medias) == 0:
        self.logger.info("Nothing to downloads.")
        return broken_items
    self.logger.info("Going to check %d medias and downloading videos only..." % (len(medias)))
    for media in tqdm(medias):
        if not self.download_video(media, path, description=description):
            delay.error_delay(self)
            broken_items = medias[medias.index(media):]
            break
    return broken_items
