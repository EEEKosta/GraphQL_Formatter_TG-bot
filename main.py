import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, CallbackContext
import graphql

# Установите ваш токен Telegram бота
TOKEN = 'YOUR_TOKEN'

# Включаем логирование для получения информации о возможных ошибках
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def start(update: Update) -> None:
    update.message.reply_text(
        'Привет! Я бот GraphQL Formatter. Просто отправь мне GraphQL-запрос, и я форматирую его для тебя.')


def format_graphql(update: Update) -> None:
    try:
        # Получаем текст сообщения с GraphQL-запросом от пользователя
        user_query = update.message.text
        # Парсим и форматируем GraphQL-запрос
        formatted_query = graphql_format(user_query)
        # Отправляем отформатированный запрос обратно пользователю
        update.message.reply_text(f'Вот отформатированный запрос:\n{formatted_query}')
    except Exception as e:
        # В случае ошибки отправляем пользователю сообщение об ошибке
        update.message.reply_text(f'Произошла ошибка: {str(e)}')


def graphql_format(query: str) -> str:
    try:
        # Парсим запрос с использованием библиотеки graphql-core-next
        parsed_query = graphql.parse(query)
        # Форматируем запрос
        formatted_query = graphql.print_ast(parsed_query)
        return formatted_query
    except graphql.GraphQLError as e:
        # Если есть ошибки в запросе, бросаем исключение
        raise Exception(f'Ошибка форматирования GraphQL-запроса: {str(e)}')


def main() -> None:
    # Инициализируем бота с использованием токена
    updater = Updater(TOKEN)

    # Получаем диспетчер бота
    dp = updater.dispatcher

    # Добавляем обработчик команды /start
    dp.add_handler(CommandHandler("start", start))

    # Добавляем обработчик для текстовых сообщений, содержащих GraphQL-запросы
    dp.add_handler(MessageHandler(filters.text & ~filters.command, format_graphql))

    # Запускаем бота
    updater.start_polling()

    # Оставляем бота в режиме работы до принудительного завершения
    updater.idle()


if __name__ == '__main__':
    main()
