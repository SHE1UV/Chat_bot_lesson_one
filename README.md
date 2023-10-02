# Уведомления о проверке работ с помощью Telegram

### Описание проекта

Этот скрипт отправляет уведомления в Telegram о проверке работ на Devman.

### Как установить

Убедитесь, что Python3 установлен на вашем компьютере. Если нет, установите его с [официального сайта](https://www.python.org/).

Установите необходимые библиотеки, запустив команду:

```
pip install -r requirements.txt
```

### Как запустить проект

Запустите скрипт можно с помощью команды:

```
python main.py --chat_id YOUR_CHAT_ID
```

Где `YOUR_CHAT_ID` - это идентификатор вашего чата в Telegram.

### Функциональность

Скрипт будет периодически проверять наличие новых уведомлений о проверке работ на Devman. В случае обнаружения нового уведомления, он отправит соответствующее сообщение в ваш Telegram.

### Переменные окружения

Для корректной работы скрипта, убедитесь, что в файле `.env` указаны корректные значения:

```
TELEGRAM_BOT_API=ваш_токен_бота
DEVMAN_API=токен_devman
```

Чтобы узнать `DEVMAN_API`, вы можете перейти по данной [ссылке.](https://dvmn.org/api/docs/) 

### Логирование

Скрипт ведет лог в файл `bot.log`, в котором записываются все события и ошибки, происходящие в процессе его работы.

### Цель проекта

Данный проект был разработан в образовательных целях в рамках онлайн-курса для веб-разработчиков на платформе [dvmn.org](https://dvmn.org/).
