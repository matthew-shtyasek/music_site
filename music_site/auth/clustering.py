import random
import redis
import pickle

from Lib import copy
from django.db import connection


class Vector:
    def __init__(self, coordinates):
        self.coordinates = coordinates

    def get_length(self):
        result = 0
        for coordinate in self.coordinates.values():
            result += coordinate ** 2
        return result ** 0.5

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        try:
            result = self.coordinates[list(self.coordinates.keys())[self.index]]
        except IndexError:
            raise StopIteration
        self.index += 1
        return result

    def __mul__(self, other):
        if isinstance(other, self.__class__):
            if len(self.coordinates) != len(other.coordinates):
                raise AttributeError('Векторы не совпадают по размерности')
            result = 0
            for scoord, ocoord in zip(self, other):
                result += scoord * ocoord
        else:
            result = Vector(list())
            for scoord in self:
                result.coordinates.append(scoord * other)
        return result

    def cos(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError('Объект не является вектором')
        return (self * other) / (self.get_length() * other.get_length())

    def get_distance(self, other):
        return 1 - self.cos(other)


class NormalizedVector(Vector):
    def __init__(self, coordinates):
        super().__init__(coordinates)
        self.normalize()

    def normalize(self):
        minimum = min(self.coordinates.values())
        maximum = max(self.coordinates.values())
        for key, value in self.coordinates.items():
            self.coordinates[key] = (value - minimum) / (maximum - minimum)


class Clustering:
    def __init__(self, prepared_dict=None, fields=None, weights=None, load=False):
        if weights and len(weights) != len(fields):
            raise IndexError('fields и weights не совпадают по размерам!')

        self.objects = prepared_dict
        self.fields = fields
        self.centers = list()
        self.clusters = list()

        if load:
            r = redis.StrictRedis()
            _keys = r.keys('center_cluster_*')
            keys = list(map(lambda key: int(str(key, encoding='utf-8').rsplit('_', maxsplit=1)[-1]), _keys))
            for key in sorted(keys):
                _center = r.get(f'center_cluster_{key}')
                self.centers.append(pickle.loads(_center))
                _cluster = r.sinter(f'cluster_{key}')
                self.clusters.append(list(map(int, _cluster)))

        if weights:
            self.weights = weights
        else:
            self.weights = [1 / len(fields) for i in fields]

    def calculate(self, count_clusters=2):
        while count_clusters > 0:
            temp_value = random.choice(list(self.objects.values()))
            while temp_value in self.centers:
                temp_value = random.choice(list(self.objects.values()))
            self.centers.append(temp_value)
            count_clusters -= 1
        prev_centers = None
        id_clusters = []

        while not prev_centers or prev_centers != self.centers:
            prev_centers = copy.deepcopy(self.centers)
            self.clusters = [list() for i in self.centers]
            id_clusters = [list() for i in self.centers]

            for id, point in self.objects.items():
                point_minimum_index = 0
                prev_temp = None
                for center_index in range(len(self.centers)):
                    temp = self.get_absolute_distance(point, self.centers[center_index])
                    if prev_temp is None or temp < prev_temp:
                        point_minimum_index = center_index
                        prev_temp = temp
                id_clusters[point_minimum_index].append(id)
                self.clusters[point_minimum_index].append(point)
            self.recalculate_centers()
        r = redis.StrictRedis()
        for center, cluster_index in zip(self.centers, range(len(self.clusters))):
            pickled_center = pickle.dumps(center)
            r.set(f'center_cluster_{cluster_index}', pickled_center)
            r.delete(f'cluster_{cluster_index}')
            r.sadd(f'cluster_{cluster_index}', *id_clusters[cluster_index])

    def recalculate_centers(self):
        if len(self.clusters) != len(self.centers):
            raise IndexError('Количество кластеров не равно количеству центров кластеров!')
        for index, cluster in zip(range(len(self.centers)), self.clusters):
            self.centers[index] = self.get_mean_inner_dicts(cluster)

    def get_similar_user_pks(self, user_dict):
        minimum_distance = self.get_absolute_distance(self.centers[0], user_dict)
        result = self.clusters[0]
        for index, center in zip(range(len(self.centers)), self.centers):
            temp_distance = self.get_absolute_distance(center, user_dict)
            if temp_distance < minimum_distance:
                minimum_distance = temp_distance
                result = self.clusters[index]
        return result

    def get_dimension_distance(self, obj1, obj2, field):
        vector1 = NormalizedVector(obj1[field])
        vector2 = NormalizedVector(obj2[field])

        return vector1.get_distance(vector2)

    def get_absolute_distance(self, obj1, obj2):
        result = 0
        for field, weight in zip(self.fields, self.weights):
            result += weight * self.get_dimension_distance(obj1, obj2, field)
        return result

    def get_minimum_absolute_distance(self, obj1):
        result = {self.objects[0]: self.get_absolute_distance(obj1, self.objects[0])}
        for obj2 in self.objects:
            if obj1 == obj2:
                continue
            temp = self.get_absolute_distance(obj1, obj2)
            if temp < list(result.values())[0]:
                result = {obj2: temp}

    def union_inner_dicts(self, dictionary):
        result = self.union_dicts(*dictionary.values())
        return result

    def union_dicts(self, *dictionaries):
        def get_sum(result, dictionary):
            for k,v in dictionary.items():
                if isinstance(v, dict):
                    if k not in result:
                        result[k] = dict()
                    result[k] = get_sum(result[k], v)
                elif k in result:
                    result[k] += v
                else:
                    result[k] = v
            return result

        result = dict()
        for dictionary in dictionaries:
            get_sum(result, dictionary)
        return result

    def get_mean_dicts(self, *dictionaries):
        def get_mean(dictionary):
            for key, value in dictionary.items():
                if isinstance(value, dict):
                    dictionary[key] = get_mean(value)
                else:
                    dictionary[key] = value / len(dictionaries)
            return dictionary

        result = self.union_dicts(*dictionaries)
        result = get_mean(result)
        return result

    def get_mean_inner_dicts(self, obj):
        if isinstance(obj, dict):
            return self.get_mean_dicts(*obj.values())
        elif isinstance(obj, list) or isinstance(obj, tuple) or isinstance(obj, set):
            return self.get_mean_dicts(*obj)
        else:
            raise TypeError('Объект должен быть словарём, списком, кортежем или множеством!')


def columns_to_list(data):
    result = list()
    for columns in data:
        for i in range(len(columns)):
            if len(result) == i:
                result.append(list())
            result[i].append(columns[i])
    return result


def normalize_dates(dates):
    result = dict()
    for date in dates:
        if date not in result:
            result[date] = 0
        result[date] += 1
    maximum = max(result.values())
    minimum = min(result.values())

    for key, value in result.items():
        result[key] = normalize_number(value, minimum, maximum)

    return result


def normalize_number(number, minimum, maximum):
    try:
        return (number - minimum) / (maximum - minimum)
    except ZeroDivisionError:
        return 1.0


def get_minimum_maximum_date_by_songs(cursor, songs):
    cursor.execute('''SELECT MIN(written), MAX(written)
                        FROM musics_song
                        WHERE id IN %s''', [tuple(songs)])
    result = columns_to_list(cursor.fetchall())
    return [date[0].year - date[0].year % 10 for date in result]


def count_equals_elements(lst):
    result = dict()
    for item in lst:
        if not item in result:
            result[item] = 1
        result[item] += 1
    return result


def get_similar_user_pks(pk):
    user_dict = prepare_clustering([pk])[pk]
    c = Clustering(load=True, fields=['s', 'g', 'y'])
    result = c.get_similar_user_pks(user_dict)
    result.remove(pk)
    return result


def get_all_user_pks():
    with connection.cursor() as cursor:
        cursor.execute('''SELECT id FROM custom_auth_customuser''')
    return columns_to_list(cursor.fetchall())[0]


def prepare_clustering(users_pk):
    users_dict = dict()
    with connection.cursor() as cursor:
        cursor.execute('''SELECT s.id, a.genre_id, cast(date_part('year', s.written) as int) - MOD(cast(date_part('year', s.written) as int), 10)
                            FROM musics_song as s INNER JOIN musics_album as a
                            ON s.album_id = a.id''')
        all_songs, all_genres, all_years = columns_to_list(cursor.fetchall())

        for user_pk in users_pk:
            try:
                cursor.execute('''SELECT s.id, a.genre_id, cast(date_part('year', s.written) as int)
                                - MOD(cast(date_part('year', s.written) as int), 10)
                                FROM musics_song as s INNER JOIN musics_album as a
                              ON s.album_id = a.id
                                WHERE s.id IN
                              (SELECT DISTINCT song_id
                                FROM profiles_playlist_songs
                                WHERE playlist_id IN
                              (SELECT id
                                FROM profiles_playlist
                                WHERE owner_id=%s))''',
                               str(user_pk))
            except TypeError:
                continue
            try:
                songs, genres, years = columns_to_list(cursor.fetchall())
            except ValueError:
                continue
            genres = count_equals_elements(genres)
            genres = {genre: genres[genre] if genre in genres else 0 for genre in all_genres}
            min_genre = min(genres.values())
            max_genre = max(genres.values())
            years = count_equals_elements(years)
            years = {year: years[year] if year in years else 0 for year in all_years}
            min_year = min(years.values())
            max_year = max(years.values())

            songs = {song: int(song in songs) for song in all_songs}
            genres = {genre: normalize_number(count, min_genre, max_genre) for genre, count in genres.items()}
            years = {year: normalize_number(count, min_year, max_year) for year, count in years.items()}

            users_dict[user_pk] = {'s': songs,
                                   'g': genres,
                                   'y': years}
    return users_dict


"""
from auth.clustering import *
from django.db import connection
cursor = connection.cursor()
cursor.execute('SELECT id FROM custom_auth_customuser')
users_pk = columns_to_list(cursor.fetchall())[0]
users_dict = prepare_clustering(users_pk)
c = Clustering(users_dict, ['s', 'g', 'y'])
c.calculate()
"""
