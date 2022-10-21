# Generated by Django 3.2.15 on 2022-10-21 07:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Запись добавлена')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Запись изменена')),
                ('name', models.CharField(blank=True, max_length=64, verbose_name='Название альбома')),
                ('slug', models.SlugField(max_length=64, verbose_name='Человекопонятная ссылка')),
                ('image', models.ImageField(upload_to='album_covers/%Y/%m/%d/', verbose_name='Обложка альбома')),
                ('artist_id', models.PositiveIntegerField(verbose_name='ID исполнителя')),
                ('is_single', models.BooleanField(verbose_name='Сингл')),
                ('released', models.DateField(verbose_name='Выпущен')),
                ('artist_type', models.ForeignKey(limit_choices_to={'model__in': ('musician', 'musicgroup')}, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
            options={
                'verbose_name': 'Альбом',
                'verbose_name_plural': 'Альбомы',
                'ordering': ('name', 'created'),
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='Жанр')),
                ('slug', models.SlugField(unique=True, verbose_name='Человекопонятная ссылка')),
            ],
            options={
                'verbose_name': 'Жанр',
                'verbose_name_plural': 'Жанры',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Musician',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Запись добавлена')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Запись изменена')),
                ('slug', models.SlugField(unique=True, verbose_name='Человекопонятная ссылка')),
                ('description', models.TextField(blank=True, verbose_name='Биография')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='photos/%Y/%m/%d', verbose_name='Фотография')),
                ('date_of_birth', models.DateField(verbose_name='Дата рождения')),
                ('date_of_death', models.DateField(blank=True, null=True, verbose_name='Дата смерти')),
                ('first_name', models.CharField(max_length=64, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=64, verbose_name='Фамилия')),
                ('patronymic', models.CharField(blank=True, max_length=64, verbose_name='Отчество')),
            ],
            options={
                'verbose_name': 'Музыкант',
                'verbose_name_plural': 'Музыканты',
                'ordering': ('last_name',),
            },
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Запись добавлена')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Запись изменена')),
                ('name', models.CharField(max_length=200, verbose_name='Название')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('track', models.FileField(upload_to='songs/%Y/%m/%d/', verbose_name='Трек')),
                ('slug', models.SlugField(unique=True, verbose_name='Человекопонятная ссылка')),
                ('written', models.DateField(verbose_name='Написана')),
                ('album', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='musics.album', verbose_name='Альбом')),
            ],
            options={
                'verbose_name': 'Песня',
                'verbose_name_plural': 'Песни',
                'ordering': ('written', 'name'),
            },
        ),
        migrations.CreateModel(
            name='MusicGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Запись добавлена')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Запись изменена')),
                ('slug', models.SlugField(unique=True, verbose_name='Человекопонятная ссылка')),
                ('description', models.TextField(blank=True, verbose_name='Биография')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='photos/%Y/%m/%d', verbose_name='Фотография')),
                ('date_of_birth', models.DateField(verbose_name='Дата рождения')),
                ('date_of_death', models.DateField(blank=True, null=True, verbose_name='Дата смерти')),
                ('name', models.CharField(max_length=200, verbose_name='Название')),
                ('musicians', models.ManyToManyField(related_name='music_groups', to='musics.Musician', verbose_name='Музыканты')),
            ],
            options={
                'verbose_name': 'Группа',
                'verbose_name_plural': 'Группы',
                'ordering': ('name',),
            },
        ),
        migrations.AddField(
            model_name='album',
            name='genre',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='musics.genre', verbose_name='Жанр'),
        ),
    ]
