from os import environ
from dotenv import load_dotenv

load_dotenv()

db = None


class Radio:
    spradio_stream_url = 'https://radio.uuuuuno.net/radio/8000/radio.mp3'
    eldaradio_stream_url = 'http://emgspb.hostingradio.ru/eldoradio128.mp3'
    uuuuunoradio_stream_url = 'http://radio.uuuu.uno/listen/unoradio/radio.mp3'
    bear_theme_stream_url = 'tema-medvedya.mp3'

    ban_video_url = 'https://www.youtube.com/watch?v=XeoS-zsGVCs'

    spradio_icon_url = 'https://radio.uuuuuno.net/static/uploads/browser_icon/192.1653387216.png'


class Discord:
    TOKEN = environ.get('TOKEN')

    command_prefix = '!;'

    notify_time_auto_delete = 5
    radio_request_song_time = 5.0
    notify_help_time_auto_delete = 30

    admin_ids = [471286011851177994, 437610383310716930]
    reports_new_songs_channel_id = 1019222057462022195
    bans = []


class Database:
    host = environ.get('DB_HOST')
    port = int(environ.get('DB_PORT'))

    user = environ.get('DB_USER')
    password = environ.get('DB_PASSWORD')

    database = 'spradio'


class PasteBin:
    key = environ.get('PASTEBIN_KEY')
