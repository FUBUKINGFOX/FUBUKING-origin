from pytube.contrib.playlist import Playlist

def search(url: str) :

    playlist = Playlist(url=url).video_urls

    return playlist