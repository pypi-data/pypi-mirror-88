import json
import re
from typing import Optional
from urllib.parse import unquote_plus, parse_qs

from . import exceptions, types

#  https://stackoverflow.com/questions/6903823/regex-for-youtube-id
_ID_REGEX_P = r"([^\"&?\/\s]{11})"
_ID_REGEX = re.compile(_ID_REGEX_P)
_ID_FROM_URL_REGEX = re.compile(rf"(?:youtube\.com/(?:[^/]+/.+/|(?:v|e(?:mbed)?)/|.*[?&]v=)|youtu\.be/){_ID_REGEX_P}")

_PL_RESPONSE_REGEX = re.compile(r"ytInitialPlayerResponse\\s*=\\s*({.+?})\\s*;\\s*(?:var\\s+meta|</script|\\n)")


def search(url: str) -> types.Result:
    id_ = _get_id_from_url(url).strip()
    player_response = _get_player_response1(_req_sync(f"https://www.youtube.com/get_video_info?video_id={id_}"))
    try:
        result = _get_result(player_response)
    except exceptions.VideoNotAvailableException:
        player_response = _get_player_response2(
            _req_sync(f"https://www.youtube.com/watch?v={id_}&gl=US&hl=en&has_verified=1&bpctr=9999999999"))
        result = _get_result(player_response)
    return result


async def search_async(url: str) -> types.Result:
    id_ = _get_id_from_url(url).strip()
    player_response = _get_player_response1(await _req_async(f"https://www.youtube.com/get_video_info?video_id={id_}"))
    try:
        result = _get_result(player_response)
    except exceptions.VideoNotAvailableException:
        player_response = _get_player_response2(
            await _req_async(f"https://www.youtube.com/watch?v={id_}&gl=US&hl=en&has_verified=1&bpctr=9999999999"))
        result = _get_result(player_response)
    return result


def _get_id_from_url(url):
    if not isinstance(url, str):
        raise exceptions.WrongUrlException(f"url must be str, got {type(url)}")
    if res := _ID_FROM_URL_REGEX.search(url):
        return res.group(1)
    if res := _ID_REGEX.search(url):  # only id
        return res.group(1)
    raise exceptions.WrongUrlException()


async def _req_async(url):
    try:
        import aiohttp
    except ImportError:
        raise Exception("Please install aiohttp (pip install aiohttp) to use async search")
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.text()


def _req_sync(url):
    try:
        import requests
    except ImportError:
        raise Exception("Please install requests (pip install requests)")
    return requests.get(url).text


def _get_player_response1(video_info):
    video_info = unquote_plus(video_info)
    return _get_player_response(video_info, ("player_response=", "&"))


def _get_player_response2(video_info):
    return _get_player_response(video_info, ("ytInitialPlayerResponse = ", ";</script>"))


def _get_player_response(video_info, split_by):
    if split_by[0] not in video_info:
        raise exceptions.WrongUrlException()
    player_response_string = video_info.split(split_by[0])[1].split(split_by[1])[0]
    player_response = json.loads(player_response_string)
    return player_response


def _get_result(player_response):
    if (status := player_response['playabilityStatus'])['status'] != 'OK':
        raise exceptions.VideoNotAvailableException(
            status['status'],
            status['errorScreen']['playerErrorMessageRenderer']['reason'],
            status['errorScreen']['playerErrorMessageRenderer'].get('subreason', "")
        )

    streaming_data = player_response['streamingData']
    video_details = player_response['videoDetails']

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
    if not (url := format_.get('url', None)):
        if not (cipher := format_.get('cipher') or format_.get('signatureCipher')):
            return None
        cipher = parse_qs(cipher)
        if 'sig' not in cipher:
            return None
        url = cipher['url'][0] + '&signature=' + cipher['sig'][0]

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
        url=url,
        video=video,
        audio=audio,
        bitrate=format_['bitrate'],
    )
