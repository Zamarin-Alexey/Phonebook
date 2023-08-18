from math import ceil
import os
import json

# Имя файла для хранения данных
DATA_FILE = 'phonebook.json'


# Загрузка данных из файла
def load_phonebook() -> list[dict]:
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    return []


# Выгрузка данных в файл
def save_phonebook(phonebook: list[dict]) -> None:
    with open(DATA_FILE, 'w') as file:
        json.dump(phonebook, file)


# Постраничный вывод записей
def display_records(records: list[dict], page: int, per_page: int) -> None:
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    records_page = records[start_idx:end_idx]
    for record in records_page:
        print(f"ID: {record['record_id']}")
        print(f"\tФИО: {record['l_name']} {record['f_name']} {record.get('m_name', '')}")
        print(f"\tОрганизация: {record.get('org', 'Нет информации')}")
        print(f"\tРабочий телефон: {record.get('w_phone', 'Нет информации')}")
        print(f"\tЛичный телефон: {record.get('p_phone', 'Нет информации')}")
        print("=" * 40)


# Добавление новой записи
def add_record(phonebook: list[dict]) -> None:
    if not phonebook:
        record_id = 1
    else:
        record_id = phonebook[-1]['record_id'] + 1
    record = {
        'record_id': record_id,
        'l_name': input("Фамилия: "),
        'f_name': input("Имя: "),
        'm_name': input("Отчество: "),
        'org': input("Организация: "),
        'w_phone': input("Рабочий телефон: "),
        'p_phone': input("Личный телефон: ")
    }
    phonebook.append(record)
    save_phonebook(phonebook)
    print("Запись добавлена.")


# Бинарный поиск записи по id
def bin_search(phonebook: list[dict], record_id: int) -> int:
    l, r = 0, len(phonebook) - 1
    while l <= r:
        m = (l + r) // 2
        r_id = phonebook[m]['record_id']
        if r_id > record_id:
            r = m
        elif r_id < record_id:
            l = m + 1
        else:
            return m
    return -1


# Редактирование записей
def edit_record(phonebook: list[dict], record_id: int) -> None:
    idx = bin_search(phonebook, record_id)
    if idx != -1:
        record = phonebook[idx]
        print("Изменение записи:")
        record['l_name'] = (input(f"Фамилия ({record['l_name']}): "))
        record['f_name'] = input(f"Имя ({record['f_name']}): ")
        record['m_name'] = input(f"Отчество ({record.get('m_name', '')}): ")
        record['org'] = input(f"Организация ({record.get('org', '')}): ")
        record['w_phone'] = input(f"Рабочий телефон ({record.get('w_phone', '')}): ")
        record['p_phone'] = input(f"Личный телефон ({record.get('p_phone', '')}): ")
        save_phonebook(phonebook)
        print("Запись изменена.")
    else:
        print("Записи с таким ID не существует.")


# Поиск по записям
def search_records(phonebook: list[dict]) -> list[dict]:
    query = input("Введите текст для поиска: ").lower()
    results = []
    for record in phonebook:
        if any(query in value.lower() for value in record.values() if type(value) != int):
            results.append(record)
    return results


def main():
    phonebook = load_phonebook()

    while True:
        print("\n=== Телефонный справочник ===")
        print("1. Вывести записи")
        print("2. Добавить запись")
        print("3. Редактировать запись")
        print("4. Поиск записей")
        print("0. Выйти")
        choice = input("Выберите действие: ")

        if choice == '1':
            if not phonebook:
                print("\nЗаписей пока нет")
                continue

            page = 1                                    # Номер страницы
            per_page = 5                                # Количество записей на странице
            pages = ceil(len(phonebook) / per_page)     # Количество страниц
            display_records(phonebook, page, per_page)
            print(f"Страница {page} из {pages}\n")

            while True:
                print("---Доступные команды---")
                if page < pages:
                    print("1. Следующая страница")
                if page > 1:
                    print("2. Предыдущая страница")
                print("3. Переход на страницу по номеру")
                print("0. Выход в главное меню")

                disp_choice = input("Выберите действие: ")
                if disp_choice == '1' and page < pages:
                    page += 1
                elif disp_choice == '2' and page > 1:
                    page -= 1
                elif disp_choice == '3':
                    des_page = int(input("Введите номер страницы: "))
                    if des_page > pages:
                        print("\nСтраницы с таким номером не существует.\n")
                        continue
                    page = des_page
                elif disp_choice == '0':
                    break
                else:
                    print("Неверный выбор. Попробуйте снова.")
                    continue
                display_records(phonebook, page, per_page)
                print(f"Страница {page} из {pages}\n")

        elif choice == '2':
            add_record(phonebook)
        elif choice == '3':
            record_idx = int(input("Введите ID записи для редактирования: "))
            edit_record(phonebook, record_idx)
        elif choice == '4':
            results = search_records(phonebook)
            if results:
                print("Результаты поиска:")
                display_records(results, page=1, per_page=len(results))
            else:
                print("Ничего не найдено.")
        elif choice == '0':
            break
        else:
            print("Неверный выбор. Попробуйте снова.")


main()
