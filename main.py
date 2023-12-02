import graphql


def format_graphql_query(query: str) -> str:
    try:
        # Парсим запрос с использованием библиотеки graphql-core-next
        parsed_query = graphql.parse(query)
        # Форматируем запрос и возвращаем отформатированный текст
        formatted_query = graphql.print_ast(parsed_query)
        return formatted_query
    except graphql.GraphQLError as e:
        # Если есть ошибки в запросе, бросаем исключение
        raise Exception(f'Ошибка форматирования GraphQL-запроса: {str(e)}')


# Ввод GraphQL-запроса из консоли
user_query = input("Введите ваш GraphQL-запрос:\n")

formatted_query = format_graphql_query(user_query)
print(f'\nОтформатированный запрос:\n{formatted_query}')
