from django.contrib import admin

from musics.models import Song, Musician, MusicGroup


@admin.register(Musician)
class MusicianAdmin(admin.ModelAdmin):
    fields = ('first_name',
              'last_name',
              'patronymic',
              'slug',
              'description',
              'date_of_birth',
              'date_of_death')
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
    fields = ('name',
              'slug',
              'description',
              'musicians',
              'date_of_birth',
              'date_of_death')
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
              'artist_type',
              'artist_id',
              'track',
              'written',
              'created',
              'updated')
    list_display = ('name',
                    'slug',
                    'written',
                    'created',
                    'updated')
    list_filter = ('written',
                   'created',
                   'updated')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name', )}
    readonly_fields = ('created', 'updated')
    list_editable = ('slug', )
