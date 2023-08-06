
# youtubeless
Get youtube video information and download links by url!

btw i don't know why u need to use this instead of youtube-dl ¯\_(ツ)_/¯

Usage
-----

    import youtubeless
    
    try:
        res = youtubeless.search("https://www.youtube.com/watch?v=UOSF9YCfTB8")
    except youtubeless.WrongUrlException:
        print(f"You give me wrong url :/.")
    except youtubeless.VideoNotAvailableException as ex:
        print(f"Oh no, this video not available because of {ex}")
    else:
        print(f"Oh, {res.author}, i like this boy!")
        if not res.formats:
            print("There is no downloadable formats")
        else:
            print("There are so many download links... Which one should I choose?")
            print(*[f"{f} {f.url}" for f in res.formats], sep='\n')  # all types have __str__ method!

    
    
It has sync and async search methods:
 - **search_async** - requires `aiohttp` installed
 - **search** - requires `requests` installed

**They are not installed with library by default!**


Installation
------------

To install youtubeless, simply:

    $ pip install youtubeless


And don't forget to install aiohttp
 
    $ pip install aiohttp

 or requests 
 
    $ pip install requsts
