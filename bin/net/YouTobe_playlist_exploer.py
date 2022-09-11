from pytube.contrib.playlist import Playlist

def search(url: str) :

    playlist = Playlist(url=url)
    list = playlist.video_urls

    return [list]