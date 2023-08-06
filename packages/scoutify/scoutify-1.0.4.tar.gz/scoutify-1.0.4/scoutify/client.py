import requests as rq
"""
    Main class of client object
"""
SPOTIFY_API_BASE_URL = 'https://api.spotify.com/v1'


class Scoutify(object):
    def __init__(
            self,
            access_token=None,
            client_id=None,
            client_secret=None,
            redirect_url=None,
    ):
        self._access_token = access_token
        self._client_id = client_id
        self._client_secret = client_secret
        self._redirect_url = redirect_url
        self._header = None

    def __get__(self, instance, owner):
        return self

    def __str__(self):
        return self._client_id

    def set_access_token(self, access_token):
        self._access_token = access_token
        self._header = {'Authorization': 'Bearer {}'.format(access_token)}

    def search(self, search_type, q):
        if not self._header:
            return "No token available"
        search_url = "{}/{}".format(SPOTIFY_API_BASE_URL, 'search')
        if search_type.lower() not in ['artist', 'track', 'album', 'playlist']:
            print('Invalid search type')
            return
        params = {'type': search_type.lower(), 'q': q.lower()}
        resp = rq.get(search_url, params=params, headers=self._header)
        return resp.json()

    def several_artists(self, artist_ids):
        if not self._header:
            return "No token available"
        url = "{}/{}".format(SPOTIFY_API_BASE_URL, 'artists')
        params = {'ids': ",".join(artist_ids)}
        resp = rq.get(url, params=params, headers=self._header)
        return resp.json()

    def several_album(self, albums_ids):
        if not self._header:
            return "No token available"
        url = "{}/{}".format(SPOTIFY_API_BASE_URL, 'albums')
        params = {'ids': ",".join(albums_ids)}
        resp = rq.get(url, params=params, headers=self._header)
        return resp.json()

    def several_track(self, tracks_ids):
        if not self._header:
            return "No token available"
        url = "{}/{}".format(SPOTIFY_API_BASE_URL, 'tracks')
        params = {'ids': ",".join(tracks_ids)}
        resp = rq.get(url, params=params, headers=self._header)
        return resp.json()

    def playlist(self, playlist_ids):
        if not self._header:
            return "No token available"
        url = "{}/{}/{}".format(SPOTIFY_API_BASE_URL, 'playlists', playlist_ids)
        resp = rq.get(url, headers=self._header)
        return resp.json()
    
    def playlist_tracks(self, playlist_ids):
        if not self._header:
            return "No token available"
        url = "{}/{}/{}/{}".format(SPOTIFY_API_BASE_URL, 'playlists', playlist_ids, 'tracks')
        resp = rq.get(url, headers=self._header)
        return resp.json()
    
    def current_user_playlists(self):
        if not self._header:
            return "No token available"
        url = "{}/{}/{}".format(SPOTIFY_API_BASE_URL, 'me', 'playlists')
        resp = rq.get(url, headers=self._header)
        return resp.json()
    
    def user_playlists(self, user_ids):
        if not self._header:
            return "No token available"
        url = "{}/{}/{}/{}".format(SPOTIFY_API_BASE_URL, 'users', user_ids, 'playlists')
        resp = rq.get(url, headers=self._header)
        return resp.json()


