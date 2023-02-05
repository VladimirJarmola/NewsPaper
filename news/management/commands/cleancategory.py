from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from news.models import Post, Category


class Command(BaseCommand):
    help = 'Команда очищает указанную категорию. ' \
           'Обязательным аргументом передается название категории!'

    def add_arguments(self, parser):
        parser.add_argument('cleancategory', type=str)

    def handle(self, *args, **options):
        answer = input(f'Вы правда хотите удалить все статьи '
                       f'в категории {options["cleancategory"]}? yes/no  ')

        if answer != 'yes':
            self.stdout.write(self.style.ERROR('Отменено'))
        else:
            try:
                category = Category.objects.get(
                    name_category=options['cleancategory']
                )
                Post.objects.filter(category=category).delete()
                self.stdout.write(self.style.SUCCESS(
                    f'Все новости в категории '
                    f'{category.name_category} успешно удалены'
                )
                )
            except ObjectDoesNotExist:
                self.stdout.write(self.style.ERROR(
                    f'Не удалось найти категорию {options["cleancategory"]}'))
