from model import Model
import view


def run():
    model = Model()

    if model.conn is None:
        view.show_message("Не вдалося підключитися до БД. Робота програми неможлива.")
        return

    while True:
        view.show_main_menu()
        choice = view.get_user_choice()

        if choice == '1':
            run_show_data_menu(model)
        elif choice == '2':
            run_add_data_menu(model)
        elif choice == '3':
            run_update_data_menu(model)
        elif choice == '4':
            run_delete_menu(model)
        elif choice == '5':
            run_generate_data_menu(model)
        elif choice == '6':
            model.close_connection()
            view.show_message("До побачення!")
            break
        else:
            view.show_message("Невірний вибір. Спробуйте ще раз.")


def run_show_data_menu(model):
    options = ["Показати 'Car'", "Показати 'Driver'", "Показати 'Route'",
               "Показати 'Customer'", "Показати 'Trip'", "Показати 'Service'",
               "Комплексний пошук рейсів"]

    while True:
        view.show_submenu("Меню Перегляду Даних (Show data)", options)
        choice = view.get_user_choice()

        if choice == '1':
            rows, msg = model.get_all_data("car")
            if rows: view.show_list(rows, ["car_id", "vin", "license_plate", "brand", "load_capacity"])
            view.show_message(msg)
        elif choice == '2':
            rows, msg = model.get_all_data("driver")
            if rows: view.show_list(rows, ["driver_id", "license_number", "surname", "name", "license_category"])
            view.show_message(msg)
        elif choice == '3':
            rows, msg = model.get_all_data("route")
            if rows: view.show_list(rows, ["route_id", "departure_point", "destination_point", "distance_km"])
            view.show_message(msg)
        elif choice == '4':
            rows, msg = model.get_all_data("customer")
            if rows: view.show_list(rows, ["customer_id", "full_name", "phone", "email", "address"])
            view.show_message(msg)
        elif choice == '5':
            rows, msg = model.get_all_data("trip")
            if rows: view.show_list(rows,["trip_id", "departure_date", "arrival_date", "return_date", "cargo_description",
                                     "cargo_weight", "car_id", "driver_id", "route_id", "customer_id"])
            view.show_message(msg)
        elif choice == '6':
            rows, msg = model.get_all_data("service")
            if rows: view.show_list(rows, ["service_id", "car_id", "service_date", "description", "cost"])
            view.show_message(msg)
        elif choice == '7':
            handle_complex_search(model)
        elif choice == '0':
            break
        else:
            view.show_message("Невірний вибір.")


def handle_complex_search(model):
    try:
        min_w, max_w, pattern = view.get_search_params()
        min_w_int, max_w_int = int(min_w), int(max_w)
        rows, duration, message = model.search_trips_complex(min_w_int, max_w_int, pattern)
        if rows is not None:
            view.show_search_results(rows, duration)
        view.show_message(message)
    except ValueError:
        view.show_message("Помилка: Вага має бути числом.")


def run_add_data_menu(model):
    options = ["Додати 'Car'", "Додати 'Driver'", "Додати 'Customer'",
               "Додати 'Route'", "Додати 'Service'",
               "Додати 'Trip'"]

    while True:
        view.show_submenu("Меню Додавання Даних (Add data)", options)
        choice = view.get_user_choice()
        try:
            if choice == '1':
                data = view.get_new_car_data()
                msg, success = model.add_car(*data)
                view.show_message(msg)
            elif choice == '2':
                data = view.get_new_driver_data()
                msg, success = model.add_driver(*data)
                view.show_message(msg)
            elif choice == '3':
                data = view.get_new_customer_data()
                msg, success = model.add_customer(*data)
                view.show_message(msg)
            elif choice == '4':
                data = view.get_new_route_data()
                msg, success = model.add_route(*data)
                view.show_message(msg)
            elif choice == '5':
                data = view.get_new_service_data()
                msg, success = model.add_service(*data)
                view.show_message(msg)
            elif choice == '6':
                data = view.get_new_trip_data()
                msg = model.add_trip(*data)
                view.show_message(msg)
            elif choice == '0':
                break
            else:
                view.show_message("Невірний вибір.")
        except Exception as e:
            view.show_message(f"Помилка вводу: {e}")


def run_update_data_menu(model):
    options = ["Редагувати 'Car'", "Редагувати 'Driver'", "Редагувати 'Customer'",
               "Редагувати 'Route'", "Редагувати 'Service'", "Редагувати 'Trip'"]

    while True:
        view.show_submenu("Меню Редагування Даних (Update data)", options)
        choice = view.get_user_choice()
        try:
            if choice == '1':
                data = view.get_update_car_data()
                msg = model.update_car(*data)
                view.show_message(msg)
            elif choice == '2':
                data = view.get_update_driver_data()
                msg = model.update_driver(*data)
                view.show_message(msg)
            elif choice == '3':
                data = view.get_update_customer_data()
                msg = model.update_customer(*data)
                view.show_message(msg)
            elif choice == '4':
                data = view.get_update_route_data()
                msg = model.update_route(*data)
                view.show_message(msg)
            elif choice == '5':
                data = view.get_update_service_data()
                msg = model.update_service(*data)
                view.show_message(msg)
            elif choice == '6':
                data = view.get_update_trip_data()
                msg = model.update_trip(*data)
                view.show_message(msg)
            elif choice == '0':
                break
            else:
                view.show_message("Невірний вибір.")
        except Exception as e:
            view.show_message(f"Помилка вводу: {e}")


def run_delete_menu(model):
    options = ["Видалити 'Car'", "Видалити 'Driver'", "Видалити 'Customer'",
               "Видалити 'Route'", "Видалити 'Service'",
               "Видалити 'Trip'"]

    while True:
        view.show_submenu("Меню Видалення Даних (Delete data)", options)
        choice = view.get_user_choice()

        table_name = None
        id_field = None

        if choice == '1':
            table_name, id_field = 'car', 'car_id'
        elif choice == '2':
            table_name, id_field = 'driver', 'driver_id'
        elif choice == '3':
            table_name, id_field = 'customer', 'customer_id'
        elif choice == '4':
            table_name, id_field = 'route', 'route_id'
        elif choice == '5':
            table_name, id_field = 'service', 'service_id'
        elif choice == '6':
            table_name, id_field = 'trip', 'trip_id'
        elif choice == '0':
            break
        else:
            view.show_message("Невірний вибір.")
            continue

        try:
            value = view.get_id_input(f"ID запису з '{table_name}' для видалення")
            message = model.delete_data_dynamic(table_name, id_field, value)
            view.show_message(message)
        except Exception as e:
            view.show_message(f"Помилка: {e}")


def run_generate_data_menu(model):
    options = ["Згенерувати 'Car'", "Згенерувати 'Driver'", "Згенерувати 'Route'",
               "Згенерувати 'Customer'", "Згенерувати 'Trip' (з FK)", "Згенерувати 'Service' (з FK)"]

    while True:
        view.show_submenu("Меню Генерації Даних (Generate data)", options)
        choice = view.get_user_choice()

        try:
            if choice == '0':
                break

            count_str = view.get_generation_count()
            count = int(count_str)
            if count <= 0: raise ValueError("Кількість > 0")

            if choice == '1':
                view.show_message(model.generate_cars(count))
            elif choice == '2':
                view.show_message(model.generate_drivers(count))
            elif choice == '3':
                view.show_message(model.generate_routes(count))
            elif choice == '4':
                view.show_message(model.generate_customers(count))
            elif choice == '5':
                view.show_message(model.generate_trips(count))
            elif choice == '6':
                view.show_message(model.generate_service(count))
            else:
                view.show_message("Невірний вибір.")

        except ValueError as e:
            view.show_message(f"Помилка: Кількість має бути додатнім числом. {e}")
        except Exception as e:
            view.show_message(f"Неочікувана помилка: {e}")