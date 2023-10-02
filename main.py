from dotenv import load_dotenv
import telepot
import requests
import os

def main():
    load_dotenv()
    
    telegram_bot_api = os.getenv("TELEGRAM_BOT_API")
    devman_api = os.getenv("DEVMAN_API")
    
    bot = telepot.Bot(telegram_bot_api)
    
    devman_url = "https://dvmn.org/api/user_reviews/"
    devman_long_polling = "https://dvmn.org/api/long_polling/?timestamp=1555493856"
    
    headers = {
        "Authorization": f"Token {devman_api}"
    }
    timestamp = None
    
    def get_user_chat_id():
        try:
            chat_id = int(input("Введите ваш chat_id: "))
            return chat_id
        except ValueError:
            print("Некорректный chat_id. Пожалуйста, введите целое число.")
            return get_user_chat_id()
    
    telegram_id = get_user_chat_id()
    
    while True:
        try:
            url = devman_long_polling
            if timestamp:
                url += f"&timestamp={timestamp}"
            response = requests.get(url, headers=headers, timeout=5)
            response.raise_for_status()
            response = response.json()
            timestamp = response['last_attempt_timestamp']
    
            if response['status'] == 'found':
                lesson_title = response['new_attempts'][0]['lesson_title']
                is_negative = response['new_attempts'][0]['is_negative']
                lesson_url = f"https://dvmn.org{response['new_attempts'][0]['lesson_url']}"
    
                if is_negative:
                    message = f"Преподаватель проверил работу!\nУрок: {lesson_title}\nРабота не принята\nСсылка на урок: {lesson_url}"
                else:
                    message = f"Преподаватель проверил работу!\nУрок: {lesson_title}\nРабота принята\nСсылка на урок: {lesson_url}"
    
                bot.sendMessage(telegram_id, message)
    
        except requests.exceptions.ReadTimeout:
            print("Превышено время ожидания запроса.")
        except requests.exceptions.ConnectionError:
            print("Произошла ошибка при установлении соединения.")
            print("Ожидаем восстановление соединения...")
        except requests.exceptions.RequestException as e:
            print(f"Произошла ошибка при выполнении запроса: {e}")


if __name__ == '__main__':
    main()
