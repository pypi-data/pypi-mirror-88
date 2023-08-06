from dataclasses import dataclass
from typing import List, Optional, Dict


@dataclass
class Video:
    width: int = None
    height: int = None
    quality: str = None
    fps: int = None

    @property
    def resolution(self):
        return f"{self.width}*{self.height}"

    def __str__(self):
        return f"🖼 {self.resolution: <9} {self.quality: <5} {self.fps}fps"


@dataclass
class Audio:
    sample_rate: int = None
    channels: int = None
    quality: str = None

    @property
    def quality_short(self):
        return self.quality.split('_')[-1][0]

    def __str__(self):
        return f" 🔊 {self.quality_short}Q"


@dataclass
class Format:
    url: str = None
    video: Optional[Video] = None
    audio: Optional[Audio] = None
    bitrate: int = None

    def __str__(self):
        return (str(self.video) if self.video else f"🔳 {'':#<21}") + \
               (str(self.audio) if self.audio else " 🔇   ")


@dataclass
class Result:
    title: str = None
    author: str = None
    length: int = None
    description: str = None
    formats: List[Format] = None
    thumbnails: Dict[str, str] = None
