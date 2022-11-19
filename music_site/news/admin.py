from django.contrib import admin

from news.models import News, Comment


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    fields = ('title',
              'slug',
              'body',
              'image',
              'author',
              'published',
              'created',
              'updated')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created',
                       'updated')
    list_display = ('title',
                    'slug',
                    'author',
                    'published',
                    'created',
                    'updated')
    search_fields = ('title',
                     'slug',
                     'body',
                     'author')
    list_filter = ('published',
                   'created',
                   'updated')
    list_editable = ('published',)
    ordering = ('-created',
                '-updated',
                'title')

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'author', None) is None:
            obj.author = request.user
        obj.save()


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    fields = ('text',
              'author',
              'news',
              'published',
              'created',
              'updated')
    readonly_fields = ('created',
                       'updated')
    list_display = ('author',
                    'news',
                    'published',
                    'created',
                    'updated')
    search_fields = ('author',
                     'news')
    list_filter = ('published',
                   'created',
                   'updated')
    list_editable = ('published',)
    ordering = ('-created',
                '-updated')

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'author', None) is None:
            obj.author = request.user
        obj.save()
