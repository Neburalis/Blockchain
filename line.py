import hashlib as hl
import json
from glob import glob
from time import time as t

complexity = 2  # Сложность генерации (сколько нулей должно быть в начале хеша)
fp = 'blocks//'  # Относительный путь до папки с блоками
blocks_name = 'block'  # Название блока (можно изменить но тогда нужно удалить всё содержимое папки)
len_of_line = 10  # Длина цепочки которая "дописывается" в конец данной
save_old_blocks = True  # Сохранить уже созданную цепочку, (При первом запуске должно быть False)
# если False то новые блоки будут записыватся "Поверх" а старые безвозвратно удалятся


def sort_glob(fp):  # Функция для правильного упорядочивания путей к файлам блоков
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


def read_blocks(name, fp):  # Считываем цепочку уже созданных блоков
    fp = str(fp) + str(name) + '*' + '.json'
    files = sort_glob(fp)
    blocks = []
    for file_name in files:
        with open(file_name, 'r', encoding='UTF8') as file:
            blocks.append(json.load(file))
    return blocks


def write_block(block, fp):  # Записываем один блок
    fp = str(fp) + str(block['name']) + '.json'
    with open(fp, 'w', encoding='UTF8') as file:
        json.dump(block, file, indent=4)


def generate_block(number, last_one, mercls_tree):  # Генерируем новый блок
    global complexity, blocks_name
    if last_one is None:
        hash_last_one = None
    else:
        hash_last_one = last_one["hash"]
    name = blocks_name
    block_name = name + str(number)
    block = {
        "time": t(),
        "number": number,
        "name": block_name,
        "nonce": 0,
        "hash_last_one": hash_last_one,
        'transactions_mercls_tree': mercls_tree,
        "complexity": complexity
    }
    hash = hl.sha256(str(block).encode()).hexdigest()
    while hash[0:complexity] != '0' * complexity:
        block['nonce'] += 1
        hash = hl.sha256(str(block).encode()).hexdigest()
    block['hash'] = hash
    # print(json.dumps(block, indent=4))
    return block


# t1 = t()
#
# if save_old_blocks:  # Проверяем нужноли считывать старые блоки
#     blocks = (read_blocks('block', fp))
# else:
#     blocks = [generate_block(0, None, None)]
#
# for i in range(len(blocks), len(blocks) + len_of_line):
#     blocks.append(generate_block(i, blocks[-1], None))
#
# for i in blocks:
#     write_block(i, fp)
#
# t2 = t()
# print(f'Выполнение программы заняло {t2-t1} секунд')
