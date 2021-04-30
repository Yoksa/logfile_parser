import requests
from datetime import datetime

from ...models import Log
from django.core.management.base import BaseCommand

"""
    Предполагается, что формат лога одинаковый, сама ссылка корректна, 
    а файл не повреждён. Для проверки этих условий программу надо дополнить.
    Так же нет проверки на дубликат файла и/или логов в нём, т.е. одинаковые
    данные будут записаны.
    Работает для количества элементов лога 11 и 12.
    Делал без использования регулярных выражений.
    Наверняка можно сделать так, чтобы скрипт работал быстрее, но старался
    оптимизировать по скорости и памяти.
"""


class Command(BaseCommand):

    help = 'Download, parse and save to database log-file.'

    def handle(self, *args, **options):
        fields = [f.name for f in Log._meta.get_fields()][1:]
        req_f = (0, 3, 4, 5, 7, 8, 9, 10)
        url = args[0]

        if url.endswith('.log'):
            print('Start downloading log file...')
            response = requests.get(url)
            data = response.content
            print('Log file has been downloaded...')

            filename = 'logs/' + datetime.now().strftime("%d.%m.%Y_%H%M%S") + '_access.log'
            with open(filename, 'wb') as f:
                f.write(data)
            print('Log file has been saved...')
            with open(filename) as f:
                parsed_list = [prepare_fields(req_f, parse(s)) for s in f if s.strip()]
            print('Logs have been prepared...')

            if len(fields) == len(req_f):
                Log.objects.bulk_create([Log(**dict(zip(fields, obj_data))) for obj_data in parsed_list])
            print('Logs have been saved into database.')
            print('Done.')
        else:
            print('No log-file in request. Try again.')

    def add_arguments(self, parser):
        parser.add_argument(
            nargs=1,
            type=str,
            dest='args',
        )


# Parse string
def parse(string_data):

    # delete last " symbol
    # Иногда в данных встречаются вторые двойные кавычки (например, в user-agent).
    # Чтобы было вообще без них по краям, лучше тогда использовать .strip().
    def strip_plus(s):
        # return s.strip('"')
        return s[:-1]

    list_data = string_data.strip().split(' "')
    list_data = [list_data[0]] + list(map(strip_plus, list_data[1:]))
    list_data[0] = list_data[0].replace('[', '').replace(']', '').split(maxsplit=3)
    list_data[1] = list_data[1].replace('"', '').split()
    return list_data[0] + list_data[1] + list_data[2:]


# Filter and prepare fields for DB
def prepare_fields(fields_num, data_list):
    data_list[3] = datetime.strptime(data_list[3], '%d/%b/%Y:%H:%M:%S %z')
    data_list[7] = int(data_list[7])
    if len(data_list) == 12:
        data_list[8] = int(data_list[8])
    else:
        data_list = data_list[:8] + [-1] + data_list[8:]
    return [data_list[i] for i in fields_num]

