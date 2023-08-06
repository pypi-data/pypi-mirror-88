import json
import re
from typing import Optional
from urllib.parse import unquote_plus

from . import exceptions, types

#  https://stackoverflow.com/questions/6903823/regex-for-youtube-id
_ID_REGEX_P = r"([^\"&?\/\s]{11})"
_ID_REGEX = re.compile(_ID_REGEX_P)
_ID_FROM_URL_REGEX = re.compile(rf"(?:youtube\.com/(?:[^/]+/.+/|(?:v|e(?:mbed)?)/|.*[?&]v=)|youtu\.be/){_ID_REGEX_P}")


def search(url: str) -> types.Result:
    id_ = _get_id_from_url(url).strip()
    video_info = _get_video_info_sync(id_)
    result = _get_result(video_info)
    return result


async def search_async(url: str) -> types.Result:
    id_ = _get_id_from_url(url).strip()
    video_info = await _get_video_info_async(id_)
    result = _get_result(video_info)
    return result


def _get_id_from_url(url):
    if not isinstance(url, str):
        raise exceptions.WrongUrlException(f"url must be str, got {type(url)}")
    if res := _ID_FROM_URL_REGEX.search(url):
        return res.group(1)
    if res := _ID_REGEX.search(url):  # only id
        return res.group(1)
    raise exceptions.WrongUrlException()


async def _get_video_info_async(id_):
    try:
        import aiohttp
    except ImportError:
        raise Exception("Please install aiohttp (pip install aiohttp) to use async search")
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://www.youtube.com/get_video_info?video_id={id_}") as resp:
            return await resp.text()


def _get_video_info_sync(id_):
    try:
        import requests
    except ImportError:
        raise Exception("Please install requests (pip install requests)")
    return requests.get(f"https://www.youtube.com/get_video_info?video_id={id_}").text


def _get_result(video_info):
    video_info = unquote_plus(video_info)
    if "player_response" not in video_info:
        raise exceptions.WrongUrlException()
    player_response_string = video_info.split("player_response=")[1].split("&")[0]
    player_response_json = json.loads(player_response_string)
    if (status := player_response_json['playabilityStatus'])['status'] != 'OK':
        raise exceptions.VideoNotAvailableException(
            status['status'],
            status['errorScreen']['playerErrorMessageRenderer']['reason'],
            status['errorScreen']['playerErrorMessageRenderer'].get('subreason', "")
        )

    streaming_data = player_response_json['streamingData']
    video_details = player_response_json['videoDetails']

    formats = list(filter(None, map(
        _parse_format,
        streaming_data['formats'] + streaming_data['adaptiveFormats']
    )))

    thumbnails = {
        f"{t['width']}x{t['height']}": t['url']
        for t in video_details['thumbnail']['thumbnails']
    }

    return types.Result(
        video_id=video_details['videoId'],
        title=unquote_plus(video_details['title']),
        author=unquote_plus(video_details['author']),
        length=video_details['lengthSeconds'],
        description=unquote_plus(video_details['shortDescription']),
        formats=formats,
        thumbnails=thumbnails
    )


def _parse_format(format_) -> Optional[types.Format]:
    if 'url' not in format_:
        return None

    video, audio = None, None
    if 'width' in format_:
        video = types.Video(
            width=format_['width'],
            height=format_['height'],
            quality=format_['qualityLabel'],
            fps=format_['fps']
        )
    if 'audioQuality' in format_:
        audio = types.Audio(
            sample_rate=format_['audioSampleRate'],
            channels=format_['audioChannels'],
            quality=format_['audioQuality'],
        )

    return types.Format(
        url=format_['url'],
        video=video,
        audio=audio,
        bitrate=format_['bitrate'],
    )
