from datetime import datetime


class Song:
    def __init__(self, playing: dict):
        self.__full_title = playing['song']['text']
        self.__title = playing['song']['title']
        self.__author = playing['song']['artist']
        self.__lyrics = playing['song']['lyrics']

        self.__art = playing['song']['art']

        self.__played_at = datetime.fromtimestamp(playing['played_at'])

        self.__duration = playing['duration']

    @property
    def full_title(self) -> str:
        return self.__full_title

    @property
    def title(self) -> str:
        return self.__title

    @property
    def author(self) -> str:
        return self.__author

    @property
    def played_at(self) -> datetime:
        return self.__played_at

    @property
    def duration(self) -> int:
        return self.__duration

    @property
    def lyrics(self) -> str:
        return self.__lyrics

    @property
    def art(self) -> str:
        return self.__art


class Information:
    def __init__(self, json: dict):
        self.__previous_playing = Song(json['song_history'][0])
        self.__now_playing = Song(json['now_playing'])
        self.__playing_next = Song(json['playing_next'])

        self.__listeners = json['station']['mounts'][0]['listeners']['total']

    @property
    def previous_playing(self) -> Song:
        return self.__previous_playing

    @property
    def now_playing(self) -> Song:
        return self.__now_playing

    @property
    def playing_next(self) -> Song:
        return self.__playing_next

    @property
    def listeners(self) -> int:
        return self.__listeners
