import argparse
import logging
import os
import requests
import telepot
import time
from dotenv import load_dotenv

def parse_args():
    parser = argparse.ArgumentParser(description="Telegram Bot")
    parser.add_argument("--chat_id", type=int, required=True, help="Ваш chat_id")
    return parser.parse_args()


def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        filename='bot.log'
    )

    load_dotenv()
    telegram_bot_api = os.getenv("TELEGRAM_BOT_API")
    devman_api = os.getenv("DEVMAN_API")

    if not (telegram_bot_api and devman_api):
        raise ValueError("Не удалось загрузить переменные окружения")

    bot = telepot.Bot(telegram_bot_api)
    args = parse_args()
    chat_id = args.chat_id

    devman_url = "https://dvmn.org/api/user_reviews/"
    headers = {
        "Authorization": f"Token {devman_api}"
    }
    timestamp = None

    while True:
        try:
            params = {}
            if timestamp:
                params["timestamp"] = timestamp

            response = requests.get(devman_url, headers=headers, params=params)
            response.raise_for_status()
            checking_tasks = response.json()
            status = checking_tasks.get('status')
            timestamp = checking_tasks.get('last_attempt_timestamp')

            if status == 'found':
                new_attempts = checking_tasks.get('new_attempts')
                if new_attempts and isinstance(new_attempts, list) and len(new_attempts) > 0:
                    lesson_title = new_attempts[0].get('lesson_title')
                    is_negative = new_attempts[0].get('is_negative')
                    lesson_url = f"https://dvmn.org{new_attempts[0].get('lesson_url')}"

                    if lesson_title and is_negative is not None and lesson_url:
                        if is_negative:
                            message = f"Преподаватель проверил работу!\nУрок: {lesson_title}\nРабота не принята\nСсылка на урок: {lesson_url}"
                        else:
                            message = f"Преподаватель проверил работу!\nУрок: {lesson_title}\nРабота принята\nСсылка на урок: {lesson_url}"

                        bot.sendMessage(chat_id, message)

        except requests.exceptions.ReadTimeout:
            logging.error("Превышено время ожидания запроса.")
        except requests.exceptions.ConnectionError:
            logging.error("Произошла ошибка при установлении соединения.")
            logging.info("Ожидаем восстановление соединения...")
            time.sleep(60)
        except requests.exceptions.RequestException as e:
            logging.error(f"Произошла ошибка при выполнении запроса: {e}")


if __name__ == '__main__':
    main()
