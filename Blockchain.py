from os import mkdir  # подключаем наши модули и вспомогательные библиотеки
import transaktion as tr
import mercls_tree as mt
import hashlib as hl
import line as bg
from glob import glob
from time import time


def complexity_read(fp):  # считывает "сложность" хеширования блока
    with open(fp+'complexity', 'r') as file:
        complexity = file.read()
    try:
        complexity = int(complexity)
    except ValueError:
        complexity = 'False'
    return complexity


def complexity_save(complexity):  # записывает "сложность" хеширования блока
    global fp
    with open(fp+'complexity', 'w') as file:
        file.write(str(complexity))


def sort_glob(fp):  # Функция для  упорядочивания в порядке возрастания путей к файлам блоков
    easy_glob = glob(fp)
    out = []
    num = 0
    while len(easy_glob) > 0:
        for i, el in enumerate(easy_glob):
            if el[16:-5] == str(num):
                out.append(easy_glob.pop(i))
                num += 1
                break
    return out


fp = 'block_data//'  # Путь до папки с данными блоков
tr.get_key('')  # Получаем ключики
try:
    bg.complexity = int(complexity_read(fp))  # считываем сложность
except ValueError:   # если не получилось
    pass
except FileNotFoundError:
    pass
files = sort_glob(fp + 'block*.json')  # Все пути к блокам
print(files)
if len(glob(fp + 'block*.json')) > 0:  # Проверям есть ли данные блоков
    if bg.save_old_blocks:  # Если нужно сохранять старые блоки, то считываем цепочку.
        print('Считываю цепочку уже созданных блоков')
        blocks = bg.read_blocks('block', fp)
    else:  # Иначе генерируеми нулевой "пустой" блок
        blocks = [bg.generate_block(0, None, None)]
        bg.write_block(blocks[-1], fp)
else:  # Иначе генерируеми нулевой "пустой" блок
    blocks = [bg.generate_block(0, None, None)]
    bg.write_block(blocks[-1], fp)

run = True
while run:  # Основной цикл программы
    print('='*12, end='\n\n')  # Просто разделитель
    block_number = blocks[-1]["number"] + 1  # Номер текущего блока
    print(f'Сбор данных для блока {block_number}')
    count = int(input('Введите количество транзакций '))
    if count > 0:  # Собераем данные для транзакции
        fp_transactions = fp + 'user_transactions' + str(block_number) + '//'
        for i in range(1, count + 1):
            print(f'--------------------------\nГенирация транзакции {i}')
            user = {
                'address': input('Введите свой адрес (транслитом) '),
                'post_code': int(input('Введите свой индекс (цифрами) '))
            }
            weight = input('Введите вес посылки в кг (цифрами) ') + 'kg'
            group = int(input('Введите группу посылки (цифрами) '))
            sender = {
                "name": input('Введите ФИО отправителя (транслитом) '),
                "address": input('Введите адрес отправителя (транслитом) '),
                "post_code": input('Введите индекс отправителя (цифрами) ')
            }
            recipient = {
                "name": input('Введите ФИО получателя (транслитом) '),
                "address": input('Введите адрес получателя (транслитом) '),
                "post_code": input('Введите индекс получателя (цифрами) ')
            }
            print('Создание транзакции..')
            user_transactoin = tr.generate_transaction(
                user=user,
                weight=weight,
                group=group,
                sender=sender,
                recipient=recipient,
                number=i
            )
            del user, weight, group, sender, recipient  # удаляем переменные которые уже не требуются
            print('Транзакция созданна успешно.')
            print('Создание электронной подписи транзакции..')
            transaction_signature = tr.sign_transaction(user_transactoin)  # Подписывает транзакцию
            print('Электронная подпись транзакции созданна успешно.')
            print('Проверка электронной подписи транзакции..')
            tr.verify(user_transactoin, transaction_signature)  # Проверяем подпись
            print('Проверка пройдена успешно.')
            print('Запись транзакции в файл..')
            try:
                mkdir(fp_transactions)  # Пытаемся создать папку (нельзя записывать в папку, если её не существует)
            except FileExistsError:  # Если она уже существует то ничего не делаем
                pass
            tr.write_transaction(user_transactoin, transaction_signature, fp_transactions)  # записываем в файл
            print('Транзакция записанна в файл успешно.')

        print('--------------------------\nПерехожу к следующему этапу')  # Считывание и проверка транзакций
        print('Считывание транзакций из файла..')
        transactions = mt.read_transactions(fp_transactions)
        print('Считывание транзакций из файла произошло успешно')
        for i, transaction in enumerate(transactions):
            number = transaction[0]['additional']['number']
            print(f"--------------------------\nПровека подписи транзакции {number}")
            mt.verify(transaction=transaction[0], signature=transaction[1])
            print('Подпись верна')
            transaction[0]['signature'] = transaction[1]
            transactions[i] = transaction[0]
        del transaction

        print('Генерирую дерево меркла для транзакций')  # Создаем дерево хеший (нужно для проверки)
        transactions_hashs = []
        for i, transaction in enumerate(transactions):
            transactions_hashs.append(hl.sha256(str(transaction).encode()).hexdigest())
        mercl_tree = mt.mercles_tree(transactions_hashs)
    else:
        mercl_tree = None

    print('Перехожу к генерации блока..')  # Создаем блок
    print('Это может занаять до нескольких минут')
    t1 = time()
    blocks.append(bg.generate_block(block_number, blocks[-1], mercl_tree))
    t2 = time()
    if t2-t1 < 2:  # Проверяем, если создался слишком быстро, то усложняем создание
        bg.complexity += 1
        complexity_save(bg.complexity)
        # print(bg.complexity)
    elif t2-t1 > 15:  # Проверяем, если создался слишком медленно, то упрощаем создание
        bg.complexity -= 1
        complexity_save(bg.complexity)
        # print(bg.complexity)
    print('Блок сгенерирован успешно.')
    print('Запись блока в файл..')
    bg.write_block(blocks[-1], fp)  # Сохраняем созданный блок
    print('блок записан в файл успешно.')

    del count
    print('-'*10)
    verefy = True
    while verefy:  # Спрашиваем продолжать или нет
        tmp = input('Вы желаете продолжить? (Y/N)')
        if tmp.lower() == 'y':
            verefy = False
        elif tmp.lower() == 'n':
            run = False
            verefy = False
        else:
            print('\nВаша команда не распознана')

    del verefy, tmp

print('До свидания, будем рады видеть вас снова.')
