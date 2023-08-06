class MusiclessException(Exception):
    pass


class WrongUrlException(MusiclessException):
    pass


class VideoNotAvailableException(MusiclessException):
    pass
