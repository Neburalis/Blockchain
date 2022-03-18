import hashlib  # Импрортируем библиотеку

text = input()  # Строка
# byte_text = text.encode()  # Переводим в байты

# hash_text_sha256 = hashlib.sha256(byte_text).hexdigest()  # Можно или так
hash_text_sha256 = hashlib.sha256(text.encode()).hexdigest()  # или так, но данный вариант используется чаще

hash_text_sha384 = hashlib.sha384(text.encode()).hexdigest()  # также воспользуемся другими алгоритмами хеширования

hash_text_sha512 = hashlib.sha512(text.encode()).hexdigest()

hash_text_sha1 = hashlib.sha1(text.encode()).hexdigest()

print(f'sha1: {hash_text_sha1} \nsha256: {hash_text_sha256} \nsha384: {hash_text_sha384} \nsha512: {hash_text_sha512}')
