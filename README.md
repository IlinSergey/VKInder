# Vkinder бот

Vkinder - бот для соцсети VK

## Установка

1. Клонируйте репозиторий с github
2. Создайте виртуальное окружение
3. Установите зависимости `pip install requirements.txt`
4. Создайте файл `config.py`
5. Впишите в `config.py` переменные:
```
vk_group_token = 'Токен сообщества VK'
vk_user_token = 'Токен пользователя VK'
db = 'Параметры для подключения к PostgreSQL (при использовании модуля data_base)'
```
6. Запустите бота командой `python main.py`

### Функционал бота

Бот автоматически считает параметры с вашей страницы и будет присылать фото и ссылку на подходящую страницу противоположного пола.
По умолчанию подбирает страницы 'в активном поиске', в городе пользователя бота.

Пару можно добавить в избранное и позже просматривать список избранных страниц.

1. `начать` или `привет` Начать работу с ботом
2. `помощь` выведет список моманд для бота
3. `параметры` изменить параметры поиска пары
4. `искать` искать пару