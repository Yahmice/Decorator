import os
import datetime
from functools import wraps

def formatdata(format_datetime = "%Y/%m/%d"):
    def logger(old_function):
        @wraps(old_function)
        def new_function(*args, **kwargs):
            start = datetime.datetime.now()

            result = old_function(*args, **kwargs)
            
            start = start.strftime(format_datetime)
            
            with open('main.log', 'a') as file:
                file.writelines(
                f'Сейчас будет вызвана функция {old_function.__name__}, с аргументами {args} и {kwargs}. '
                f'Начало работы {start} '
                f'Возвращаемое значение: {old_function(*args, **kwargs)}'
            )
                
            return result
        
        return new_function
    
    return logger


def test_1():

    path = 'main.log'
    if os.path.exists(path):
        os.remove(path)

    @formatdata(format_datetime="%Y:%m:%d")
    def hello_world():
        return 'Hello World'

    @formatdata(format_datetime="%Y:%m:%d")
    def summator(a, b=0):
        return a + b

    @formatdata(format_datetime="%Y:%m:%d")
    def div(a, b):
        return a / b

    assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
    result = summator(2, 2)
    assert isinstance(result, int), 'Должно вернуться целое число'
    assert result == 4, '2 + 2 = 4'
    result = div(6, 2)
    assert result == 3, '6 / 2 = 3'
    
    assert os.path.exists(path), 'файл main.log должен существовать'

    summator(4.3, b=2.2)
    summator(a=0, b=0)

    with open(path) as log_file:
        log_file_content = log_file.read()

    assert 'summator' in log_file_content, 'должно записаться имя функции'
    for item in (4.3, 2.2, 6.5):
        assert str(item) in log_file_content, f'{item} должен быть записан в файл'


if __name__ == '__main__':
    test_1()

