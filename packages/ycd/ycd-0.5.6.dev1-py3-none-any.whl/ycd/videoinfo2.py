import httpx
import time
from .exceptions import InvalidVideoIdException, UnknownConnectionError
from .util import extract_video_id
from . settings import Settings



API_ENDPOINT = "https://www.googleapis.com/youtube/v3/videos?part=snippet,contentDetails&fields=items(id,snippet(channelId,title,channelTitle,publishedAt),contentDetails(duration))"




class VideoInfo:
    '''
    VideoInfo object retrieves YouTube video information.

    Parameter
    ---------
    video_id : str

    Exception
    ---------
    InvalidVideoIdException :
        Occurs when video_id does not exist on YouTube.
    '''

    def __init__(self, video_id):
        self.video_id = extract_video_id(video_id)
        self.client = httpx.Client(http2=True)
        self.api_key = Settings().config['api_key']
        err = None
        for _ in range(3):
            try:
                text = self._get_page_text(self.video_id)
                self._parse(text)
                break
            except (InvalidVideoIdException, UnknownConnectionError) as e:
                raise e
            except Exception as e:
                err = e
                time.sleep(2)
                pass
        else:
            raise err

    def _get_page_text(self, video_id):

        err = None
        for _ in range(3):
            try:
                resp = self.client.get(API_ENDPOINT+f"&id={video_id}&key={self.api_key }")
                resp.raise_for_status()
                break
            except httpx.HTTPError as e:
                err = e
                time.sleep(3)
        else:
            raise UnknownConnectionError(str(err))

        return resp.json()

    def _parse(self, text):
        self.duration = text[0]["contentDetails"]["duration"]
        self.channelId = text[0]["snippet"]["channelId"]
        self.channelTitle = text[0]["snippet"]["channelTitle"]
        self.title=text[0]["snippet"]["title"]
 
    def get_duration(self):
        return self.duration

    def get_title(self):
        return self.title

    def get_channel_id(self):
        return self.channelId

    def get_channel_name(self):
        return self.channelTitle



