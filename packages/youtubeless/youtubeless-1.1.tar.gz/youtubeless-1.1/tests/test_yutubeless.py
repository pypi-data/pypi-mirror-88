import pytest

from youtubeless import search, search_async, exceptions


# links from https://stackoverflow.com/questions/6903823/regex-for-youtube-id

URL_NORMAL = [
    "NLqAF9hrVbY",
    "http://www.youtube.com/user/Scobleizer#p/u/1/1p3vcRhsYGo",
    "http://youtu.be/NLqAF9hrVbY",
    "http://www.youtube.com/embed/NLqAF9hrVbY",
    "https://www.youtube.com/embed/NLqAF9hrVbY",
    "http://www.youtube.com/v/NLqAF9hrVbY?fs=1&hl=en_US",
    "http://www.youtube.com/watch?v=NLqAF9hrVbY",
    "http://www.youtube.com/user/Scobleizer#p/u/1/1p3vcRhsYGo",
    "http://www.youtube.com/ytscreeningroom?v=NRHVzbJVx8I",
    "http://www.youtube.com/user/Scobleizer#p/u/1/1p3vcRhsYGo",
    "http://www.youtube.com/watch?v=JYArUl0TzhA&feature=featured",
    "https://www.youtube.com/watch?v=WvV5TbJc9tQ"
]
URL_BROKEN = [
    "https://www.youtube.com/watch?vasd=BaMcFghlVEASDU",
    "https://www.youtube.com",
    "https://www.youtu.be",
    "https://www.youtube.com/BaMcFghlVEU",
    "",
]

URL_NOT_AVAILABLE = [
    "https://www.youtube.com/watch?v=BaMcFghlVEASDU",
    "http://www.youtube.com/sandalsResorts#p/c/54B8C800269D7C1B/0/FJUvudQsKCM",  # private video
]


@pytest.mark.parametrize("url", URL_NORMAL)
def test_search(url):
    search(url)


@pytest.mark.asyncio
@pytest.mark.parametrize("url", URL_NORMAL)
async def test_async_search(url):
    await search_async(url)


@pytest.mark.parametrize("url", URL_BROKEN)
def test_search_wrong_url(url):
    with pytest.raises(exceptions.WrongUrlException):
        search(url)


@pytest.mark.asyncio
@pytest.mark.parametrize("url", URL_BROKEN)
async def test_async_search_wrong_url(url):
    with pytest.raises(exceptions.WrongUrlException):
        await search_async(url)


@pytest.mark.parametrize("url", URL_NOT_AVAILABLE)
def test_search_unavailable(url):
    with pytest.raises(exceptions.VideoNotAvailableException):
        search(url)


@pytest.mark.asyncio
@pytest.mark.parametrize("url", URL_NOT_AVAILABLE)
async def test_async_search_unavailable(url):
    with pytest.raises(exceptions.VideoNotAvailableException):
        await search_async(url)
