import redis
import re

from musics.models import Song

r = redis.StrictRedis('localhost')


def get_recommended_songs(user, max_songs=-1):
    _song_ids = r.sinter(f'user:playlists:{user.id}')
    if not _song_ids:
        return []

    song_ids = list(map(lambda string: f'{string.decode("utf-8")}:z', _song_ids))
    tempkey = ''.join(song_ids)
    r.zunionstore(tempkey, song_ids)
    _recom_song_ids = list(map(lambda song_id: song_id.decode('utf-8'), r.zrangebyscore(tempkey, '-inf', '+inf')[::-1]))
    _recom_song_ids = list(filter(lambda song_id: bytes(song_id, 'utf-8') not in _song_ids, _recom_song_ids))
    r.delete(tempkey)
    recom_song_ids = list(map(lambda song_id: int(re.match(r'(.*:){1,2}(\d*)(:.*)*', song_id).group(2)), _recom_song_ids))
    return Song.objects.filter(id__in=recom_song_ids)
