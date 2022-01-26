import shelve
from SQLighter import SQLighter
from config import shelve_name, database_name

def count_rows():
    """
    Данный метод считает общее количество строк в базе данных и сохраняет в хранилище.

    """
    db = SQLighter(database_name)
    rowsnum = db.count_rows()
    with shelve.open(shelve_name) as storage:
        storage['rows_count'] = rowsnum


def get_rows_count():
    """
    Получает из хранилища количество строк в БД
    :return: (int) Число строк
    """
    with shelve.open(shelve_name) as storage:
        rowsnum = storage['rows_count']
    return rowsnum


def set_user_project(chat_id, estimated_answer):
    """
    Записываем юзера в участники проекта и запоминаем, что он должен ответить.
    :param chat_id: id юзера
    :param estimated_answer: тайм стэйты из БД ПМ (из БД)
    """
    with shelve.open(shelve_name) as storage:
        storage[str(chat_id)] = estimated_answer


def finish_user(chat_id):
    """
    Закрываем диалог с пользователем
    :param chat_id: id юзера
    """
    with shelve.open(shelve_name) as storage:
        del storage[str(chat_id)]


def get_answer_for_user(chat_id):
    """
    Получаем правильный ответ для текущего юзера.
    В случае, если человек просто ввёл какие-то символы, не выбрав временной отрезок возвращаем None
    :param chat_id: id юзера
    :return: (str) Отрезок времени / None
    """
    with shelve.open(shelve_name) as storage:
        try:
            answer = storage[str(chat_id)]
            return answer
        # Если человек не выбирает варианты, ничего не возвращаем
        except KeyError:
            return None


def generate_markup(time_1, time_2):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    all_answers = '{},{}'.format(time_1, time_2)
    list_items = []
    for item in all_answers.split(','):
        list_items.append(item)
    for item in list_items:
        markup.add(item)
    return markup
