
def show_main_menu():
    print("\n--- ГОЛОВНЕ МЕНЮ ---")
    print("1.  Показати дані (Show data)")
    print("2.  Додати дані (Add data)")
    print("3.  Редагувати дані (Update data)")
    print("4.  Видалити дані (Delete data)")
    print("5.  Згенерувати дані (Generate data)")
    print("6.  Вихід (Quit)")


def show_submenu(title, options):
    print(f"\n--- {title} ---")
    for i, option in enumerate(options, 1):
        print(f"{i}.  {option}")
    print("0.  <= Повернутись до головного меню")


def get_user_choice():
    return input("Ваш вибір: ").strip()


def show_message(message):
    print(f"\n*** {message} ***")


def show_list(rows, headers):
    if not rows:
        print("-> Немає даних для відображення.")
        return

    col_widths = [len(str(h)) for h in headers]
    for row in rows:
        for i, col in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(col)))

    header_line = " | ".join(f"{h:<{col_widths[i]}}" for i, h in enumerate(headers))
    print("\n" + header_line)
    print("-" * len(header_line))

    for row in rows:
        row_line = " | ".join(f"{str(col):<{col_widths[i]}}" for i, col in enumerate(row))
        print(row_line)


def get_id_input(prompt="ID"):
    return input(f"Введіть {prompt}: ").strip()


def get_generation_count():
    return input("Введіть кількість записів для генерації: ").strip()


def get_search_params():
    print("\n--- Комплексний пошук рейсів ---")
    min_weight = input("Введіть МІН вагу вантажу (напр., 5000): ").strip()
    max_weight = input("Введіть МАКС вагу вантажу (напр., 20000): ").strip()
    brand_pattern = input("Введіть шаблон марки авто (напр., 'Volv%' або '%'): ").strip()

    if not min_weight: min_weight = '0'
    if not max_weight: max_weight = '1000000'
    if not brand_pattern: brand_pattern = '%'

    return min_weight, max_weight, brand_pattern


def show_search_results(rows, duration_ms):
    headers = ["Trip ID", "Вантаж", "Вага", "Марка", "Номер", "Водій"]
    show_list(rows, headers)
    show_message(f"Час виконання запиту: {duration_ms:.2f} мс.")


def get_new_car_data():
    print("\n--- Додавання 'Car' ---")
    vin = input("VIN: ").strip()
    license_plate = input("Номерний знак: ").strip()
    brand = input("Марка: ").strip()
    load_capacity = input("Вантажопідйомність (кг): ").strip()
    return vin, license_plate, brand, load_capacity


def get_new_driver_data():
    print("\n--- Додавання 'Driver' ---")
    license_num = input("Номер посвідчення: ").strip()
    surname = input("Прізвище: ").strip()
    name = input("Ім'я: ").strip()
    category = input("Категорія: ").strip()
    return license_num, surname, name, category


def get_new_customer_data():
    print("\n--- Додавання 'Customer' ---")
    full_name = input("Повна назва компанії: ").strip()
    phone = input("Телефон: ").strip()
    email = input("Email: ").strip()
    address = input("Адреса: ").strip()
    return full_name, phone, email, address


def get_new_route_data():
    print("\n--- Додавання 'Route' ---")
    departure = input("Пункт відправлення: ").strip()
    destination = input("Пункт призначення: ").strip()
    distance = input("Відстань (км): ").strip()
    return departure, destination, distance


def get_new_service_data():
    print("\n--- Додавання 'Service' ---")
    car_id = input("ID Автомобіля (Car ID): ").strip()
    service_date = input("Дата обслуговування (YYYY-MM-DD): ").strip()
    description = input("Опис робіт: ").strip()
    cost = input("Вартість (напр., 3500.00): ").strip()
    return car_id, service_date, description, cost


def get_new_trip_data():
    print("\n--- Додавання 'Trip' ---")
    departure = input("Дата виїзду (YYYY-MM-DD): ").strip()
    arrival = input("Дата прибуття (YYYY-MM-DD): ").strip()
    return_d = input("Дата повернення (YYYY-MM-DD): ").strip()
    cargo_desc = input("Опис вантажу: ").strip()
    cargo_weight = input("Вага (кг): ").strip()
    car_id = input("ID Автомобіля (Car ID): ").strip()
    driver_id = input("ID Водія (Driver ID): ").strip()
    route_id = input("ID Маршруту (Route ID): ").strip()
    customer_id = input("ID Клієнта (Customer ID): ").strip()
    return departure, arrival, return_d, cargo_desc, cargo_weight, car_id, driver_id, route_id, customer_id


def get_update_car_data():
    print("\n--- Редагування 'Car' ---")
    car_id = input("ID автомобіля для оновлення: ").strip()
    brand = input(f"Нова Марка (enter, щоб пропустити): ").strip()
    load_capacity = input(f"Нова Вантажопідйомність (enter, щоб пропустити): ").strip()
    return car_id, brand, load_capacity


def get_update_driver_data():
    print("\n--- Редагування 'Driver' ---")
    driver_id = input("ID водія для оновлення: ").strip()
    surname = input(f"Нове Прізвище (enter, щоб пропустити): ").strip()
    name = input(f"Нове Ім'я (enter, щоб пропустити): ").strip()
    category = input(f"Нова Категорія (enter, щоб пропустити): ").strip()
    return driver_id, surname, name, category


def get_update_customer_data():
    print("\n--- Редагування 'Customer' ---")
    customer_id = input("ID клієнта для оновлення: ").strip()
    phone = input(f"Новий Телефон (enter, щоб пропустити): ").strip()
    email = input(f"Новий Email (enter, щоб пропустити): ").strip()
    return customer_id, phone, email


def get_update_route_data():
    print("\n--- Редагування 'Route' ---")
    route_id = input("ID маршруту для оновлення: ").strip()
    distance = input(f"Нова Відстань (км) (enter, щоб пропустити): ").strip()
    return route_id, distance


def get_update_service_data():
    print("\n--- Редагування 'Service' ---")
    service_id = input("ID обслуговування для оновлення: ").strip()
    description = input(f"Новий Опис (enter, щоб пропустити): ").strip()
    cost = input(f"Нова Вартість (enter, щоб пропустити): ").strip()
    return service_id, description, cost


def get_update_trip_data():
    print("\n--- Редагування 'Trip' ---")
    trip_id = input("ID рейсу для оновлення: ").strip()
    cargo_desc = input(f"Новий Опис вантажу (enter, щоб пропустити): ").strip()
    cargo_weight = input(f"Нова Вага (кг) (enter, щоб пропустити): ").strip()
    return trip_id, cargo_desc, cargo_weight