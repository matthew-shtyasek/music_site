from django.contrib import admin

from musics.models import Song, Musician, MusicGroup, Genre, Album


@admin.register(Musician)
class MusicianAdmin(admin.ModelAdmin):
    fields = ('pk',
              'first_name',
              'last_name',
              'patronymic',
              'slug',
              'photo',
              'description',
              'date_of_birth',
              'date_of_death')
    readonly_fields = ('pk',)
    list_display = ('name',
                    'slug',
                    'date_of_birth',
                    'date_of_death')
    list_filter = ('date_of_birth',
                   'date_of_death')
    search_fields = ('last_name',
                     'first_name',
                     'patronymic',
                     'slug')
    prepopulated_fields = {'slug': ('first_name', 'last_name')}
    list_editable = ('slug',)


@admin.register(MusicGroup)
class MusicGroupAdmin(admin.ModelAdmin):
    fields = ('pk',
              'name',
              'slug',
              'photo',
              'description',
              'musicians',
              'date_of_birth',
              'date_of_death')
    readonly_fields = ('pk',)
    list_display = ('name',
                    'slug',
                    'date_of_birth',
                    'date_of_death')
    list_filter = ('date_of_birth',
                   'date_of_death')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name', )}
    list_editable = ('slug',)


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    fields = ('name',
              'slug',
              'description',
              'album',
              'album_genre',
              'album_artist',
              'track',
              'written',
              'created',
              'updated')
    list_display = ('name',
                    'slug',
                    'album',
                    'album_genre',
                    'album_artist',
                    'written',
                    'created',
                    'updated')
    list_filter = ('album__genre',
                   'written',
                   'created',
                   'updated')
    search_fields = ('name',
                     'slug',
                     'album',
                     'album__genre')
    prepopulated_fields = {'slug': ('name', )}
    readonly_fields = ('album_artist',
                       'album_genre',
                       'created',
                       'updated')
    list_editable = ('slug',
                     'album')


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    fields = ('name',
              'slug',
              'image',
              'artist_type',
              'artist_id',
              'genre',
              'is_single',
              'released',
              'created',
              'updated')
    list_display = ('name',
                    'slug',
                    'artist',
                    'genre',
                    'is_single',
                    'released',
                    'created',
                    'updated')
    list_editable = ('genre',
                     'is_single',
                     'released')
    list_filter = ('genre',
                   'is_single',
                   'released',
                   'created',
                   'updated')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created',
                       'updated')
    search_fields = ('name',
                     'slug',
                     'genre')


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    fields = ('name',
              'slug')
    list_display = ('name',
                    'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
