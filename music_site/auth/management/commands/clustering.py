from django.core.management import BaseCommand

from auth import clustering


class Command(BaseCommand):
    help = '''clustering [--weights="0.33,0.33,0.33"] [--count=clusters 5]'''

    def handle(self, *args, **options):
        try:
            weights = list(map(float, options['weights'].split(',')))
            count_clusters = int(options['countclusters'])
        except:
            self.stderr.write('Ошибка, введены неверные данные!')
            return
        self.stdout.write('Кластеризация запущена')
        users_pk = clustering.get_all_user_pks()
        users_dict = clustering.prepare_clustering(users_pk)
        c = clustering.Clustering(prepared_dict=users_dict,
                                  fields=['s', 'g', 'y'],
                                  weights=weights)
        c.calculate(count_clusters)
        self.stdout.write('Кластеризация выполнена!')

    def add_arguments(self, parser):
        parser.add_argument(
            '-w',
            '--weights',
            type=str,
            default='0.34,0.33,0.33',
            help='Задаёт веса для полей, используемых при кластеризации',
        )

        parser.add_argument(
            '-c',
            '--countclusters',
            type=int,
            default=5,
            help='Задаёт кол-во кластеров, на которое мы разбиваем множество пользователей',
        )
