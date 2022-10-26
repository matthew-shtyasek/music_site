from django.contrib import admin

from profiles.models import Playlist


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    fields = (
        'name',
        'icon',
        'owner',
        'songs',
        'subscribers',
        'public',
        'created',
        'updated',
    )

    readonly_fields = (
        'created',
        'updated',
    )

    list_display = (
        'name',
        'icon',
        'owner',
        'public',
        'created',
        'updated',
    )

    list_editable = (
        'public',
    )

    list_filter = (
        'public',
        'created',
        'updated',
    )

    search_fields = (
        'name',
        'owner',
        'songs',
    )
