import datetime

import psycopg
from psycopg import errors
from config import DB_PARAMS
import time
import uuid
import random

class Model:
    def __init__(self):
        try:
            self.conn = psycopg.connect(**DB_PARAMS)
            self.conn.autocommit = False
        except Exception as e:
            self.conn = None
            print(f"Помилка підключення до БД: {e}")

    def close_connection(self):
        if self.conn:
            self.conn.close()

    def _execute_query(self, query, params=None, fetch=False):
        if not self.conn:
            return None, "Помилка: Немає з'єднання з БД."

        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query, params)

                if fetch:
                    result = cursor.fetchall()
                    self.conn.commit()
                    return result, "Запит успішно виконано."
                else:
                    rowcount = cursor.rowcount
                    self.conn.commit()
                    return rowcount, "Запит успішно виконано."

        except errors.ForeignKeyViolation as e:
            self.conn.rollback()
            return None, f"Помилка цілісності (ForeignKeyViolation): {e}"
        except Exception as e:
            self.conn.rollback()
            return None, f"Помилка при виконанні запиту: {e}"

    def get_all_data(self, table_name):
        if not table_name.replace('_', '').isalnum():
            return None, "Помилка: Неприпустима назва таблиці."

        query = f"SELECT * FROM {table_name} LIMIT 100"
        return self._execute_query(query, fetch=True)

    def add_car(self, vin, license_plate, brand, load_capacity):
        query = "INSERT INTO car (vin, license_plate, brand, load_capacity) VALUES (%s, %s, %s, %s)"
        try:
            load_capacity_int = int(load_capacity)
        except ValueError:
            return "Помилка: 'Вантажопідйомність' має бути числом.", False
        params = (vin, license_plate, brand, load_capacity_int)
        rowcount, message = self._execute_query(query, params)
        if rowcount is not None:
            return f"Успішно додано {rowcount} автомобіль.", True
        return message, False

    def add_driver(self, license_number, surname, name, license_category):
        query = "INSERT INTO driver (license_number, surname, name, license_category) VALUES (%s, %s, %s, %s)"
        params = (license_number, surname, name, license_category)
        rowcount, message = self._execute_query(query, params)
        if rowcount is not None:
            return f"Успішно додано {rowcount} водія.", True
        return message, False

    def add_customer(self, full_name, phone, email, address):
        query = "INSERT INTO customer (full_name, phone, email, address) VALUES (%s, %s, %s, %s)"
        params = (full_name, phone, email, address)
        rowcount, message = self._execute_query(query, params)
        if rowcount is not None:
            return f"Успішно додано {rowcount} клієнта.", True
        return message, False

    def add_route(self, departure, destination, distance):
        query = "INSERT INTO route (departure_point, destination_point, distance_km) VALUES (%s, %s, %s)"
        try:
            params = (departure, destination, int(distance))
        except ValueError:
            return "Помилка: 'Відстань' має бути числом.", False
        rowcount, message = self._execute_query(query, params)
        if rowcount is not None:
            return f"Успішно додано {rowcount} маршрут.", True
        return message, False

    def add_service(self, car_id, service_date, description, cost):
        query = "INSERT INTO service (car_id, service_date, description, cost) VALUES (%s, %s, %s, %s)"
        try:
            params = (int(car_id), service_date, description, float(cost))
        except ValueError:
            return "Помилка: ID має бути числом, а вартість - числом (напр., 3500.00).", False
        rowcount, message = self._execute_query(query, params)
        if rowcount is not None:
            return f"Успішно додано {rowcount} запис про обслуговування.", True
        return message, False

    def add_trip(self, departure, arrival, return_d, cargo_desc, cargo_weight, car_id, driver_id, route_id,
                 customer_id):
        query = "INSERT INTO trip (departure_date, arrival_date, return_date, cargo_description, cargo_weight, car_id, driver_id, route_id, customer_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        try:
            params = (departure, arrival, return_d, cargo_desc, int(cargo_weight), int(car_id), int(driver_id),
                      int(route_id), int(customer_id))
        except ValueError:
            return "Помилка: ID та вага мають бути числами."
        rowcount, message = self._execute_query(query, params)
        if rowcount is None:
            return message
        return f"Успішно додано {rowcount} рейс."

    def _update_record(self, table_name, id_field, record_id, fields_to_update, values):
        if not record_id.isdigit():
            return "Помилка: ID має бути числом."

        updates = []
        params = []

        for i, value in enumerate(values):
            if value:
                field_name = fields_to_update[i]
                updates.append(f"{field_name} = %s")
                params.append(value)

        if not updates:
            return "Немає даних для оновлення."

        params.append(int(record_id))
        query = f"UPDATE {table_name} SET {', '.join(updates)} WHERE {id_field} = %s"

        rowcount, message = self._execute_query(query, params)

        if rowcount == 0:
            return f"Запис з ID {record_id} не знайдено."
        elif rowcount is not None:
            return f"Запис (ID: {record_id}) успішно оновлено."
        else:
            return message

    def update_car(self, car_id, brand, load_capacity):
        fields = ["brand", "load_capacity"]
        values = [brand, load_capacity]
        try:
            if load_capacity: values[1] = int(load_capacity)
        except ValueError:
            return "Помилка: Вантажопідйомність має бути числом."
        return self._update_record("car", "car_id", car_id, fields, values)

    def update_driver(self, driver_id, surname, name, category):
        fields = ["surname", "name", "license_category"]
        values = [surname, name, category]
        return self._update_record("driver", "driver_id", driver_id, fields, values)

    def update_customer(self, customer_id, phone, email):
        fields = ["phone", "email"]
        values = [phone, email]
        return self._update_record("customer", "customer_id", customer_id, fields, values)

    def update_route(self, route_id, distance):
        fields = ["distance_km"]
        values = [distance]
        try:
            if distance: values[0] = int(distance)
        except ValueError:
            return "Помилка: Відстань має бути числом."
        return self._update_record("route", "route_id", route_id, fields, values)

    def update_service(self, service_id, description, cost):
        fields = ["description", "cost"]
        values = [description, cost]
        try:
            if cost: values[1] = float(cost)
        except ValueError:
            return "Помилка: Вартість має бути числом."
        return self._update_record("service", "service_id", service_id, fields, values)

    def update_trip(self, trip_id, cargo_desc, cargo_weight):
        fields = ["cargo_description", "cargo_weight"]
        values = [cargo_desc, cargo_weight]
        try:
            if cargo_weight: values[1] = int(cargo_weight)
        except ValueError:
            return "Помилка: Вага має бути числом."
        return self._update_record("trip", "trip_id", trip_id, fields, values)

    def delete_data_dynamic(self, table_name, field, value):
        if not table_name.replace('_', '').isalnum() or not field.replace('_', '').isalnum():
            return "Помилка: Неприпустима назва таблиці або поля."

        query = f"DELETE FROM {table_name} WHERE {field} = %s"

        try:
            param = int(value)
        except ValueError:
            param = str(value)

        rowcount, message = self._execute_query(query, (param,))

        if rowcount is None:
            if "ForeignKeyViolation" in message:
                return f"ПОМИЛКА: update або delete в таблиці \"{table_name}\" порушує обмеження зовнішнього ключа."
            return message
        elif rowcount == 0:
            return f"0 rows affected. (Запис з {field} = {value} не знайдено)."
        else:
            return f"Deleted successfully! {rowcount} рядків видалено."


    def _generate_data(self, query, count):
        rowcount, message = self._execute_query(query, (count,))
        if rowcount is None:
            return message
        return f"Успішно згенеровано {rowcount} записів."



    def generate_cars(self, count):

            if not self.conn:
                return "Помилка: Немає з'єднання з БД."

            generated_data = []
            brands = ['Volvo', 'MAN', 'Scania', 'Mercedes', 'DAF']

            print(f"Генерація {count} записів в Python...")
            for _ in range(count):
                raw_uuid = uuid.uuid4()
                vin = str(raw_uuid).replace('-', '').upper()[:17]

                plate = (
                        random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') +
                        random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') +
                        f"{random.randint(0, 9999):04d}" +
                        random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') +
                        random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
                )

                brand = random.choice(brands)
                load_capacity = random.randint(10000, 25000)

                generated_data.append((vin, plate, brand, load_capacity))

            query = """
                    INSERT INTO car (vin, license_plate, brand, load_capacity)
                    VALUES (%s, %s, %s, %s)
                    """

            print(f"Вставка {len(generated_data)} записів у БД...")
            try:
                with self.conn.cursor() as cursor:
                    cursor.executemany(query, generated_data)
                    inserted_count = cursor.rowcount
                    self.conn.commit()
                    if inserted_count < count:
                        return f"УВАГА: Змогли додати лише {inserted_count} унікальних записів з {count} запитаних (через дублікати VIN)."
                    else:
                        return f"Успішно згенеровано та додано {inserted_count} унікальних записів."

            except Exception as e:
                self.conn.rollback()
                return f"Помилка при пакетній вставці: {e}"

    def generate_drivers(self, count):
        query = """
                INSERT INTO driver (license_number, surname, name, license_category)
                SELECT 'DR' || trunc(100000 + random() * 900000)::text, \
                       (ARRAY ['Іваненко', 'Петренко', 'Сидоренко', 'Ковальчук', 'Шевченко'])[trunc(random() * 5) + 1], \
                       (ARRAY ['Петро', 'Олександр', 'Михайло', 'Іван', 'Сергій'])[trunc(random() * 5) + 1], \
                       (ARRAY ['B', 'C', 'CE'])[trunc(random() * 3) + 1]
                FROM generate_series(1, %s) \
                """
        return self._generate_data(query, count)

    def generate_routes(self, count):
        query = """
                INSERT INTO route (departure_point, destination_point, distance_km)
                SELECT (ARRAY ['Київ', 'Львів', 'Одеса', 'Харків', 'Дніпро'])[trunc(random() * 5) + 1], \
                       (ARRAY ['Варшава', 'Берлін', 'Прага', 'Відень', 'Краків'])[trunc(random() * 5) + 1], \
                       trunc(300 + random() * 1200)::int
                FROM generate_series(1, %s) \
                """
        return self._generate_data(query, count)

    def generate_customers(self, count):
        query = """
                INSERT INTO customer (full_name, phone, email, address)
                SELECT 'ТОВ ' || chr(trunc(65 + random() * 25)::int) || chr(trunc(65 + random() * 25)::int) || \
                       chr(trunc(65 + random() * 25)::int), \
                       '+380' || trunc(100000000 + random() * 900000000)::text, \
                       LEFT(MD5(random()::text), 10) || '@gmail.com', \
                       'м. Київ, вул. ' || (ARRAY ['Хрещатик', 'Сумська', 'Дерибасівська'])[trunc(random() * 3) + 1] || \
                       ', ' || trunc(1 + random() * 100)::text
                FROM generate_series(1, %s) \
                """
        return self._generate_data(query, count)


    def generate_trips(self, count):

            if not self.conn:
                return "Помилка: Немає з'єднання з БД."

            print("Отримання списків існуючих ID...")
            car_ids = self._get_existing_ids("car", "car_id")
            driver_ids = self._get_existing_ids("driver", "driver_id")
            route_ids = self._get_existing_ids("route", "route_id")
            customer_ids = self._get_existing_ids("customer", "customer_id")

            if not all([car_ids, driver_ids, route_ids, customer_ids]):
                return ("Помилка: Неможливо згенерувати 'trip'. "
                        "Одна або декілька батьківських таблиць порожні.")

            generated_data = []
            cargo_options = ['Будматеріали', 'Металопрокат', 'Продукти', 'Техніка', 'Хімікати']
            print(f"Генерація {count} записів 'trip' в Python...")
            for _ in range(count):
                departure_date = datetime.date.today() - datetime.timedelta(days=random.randint(0, 30))
                arrival_date = departure_date + datetime.timedelta(days=random.randint(1, 10))
                return_date = arrival_date + datetime.timedelta(days=random.randint(0, 5))
                cargo_desc = random.choice(cargo_options)
                cargo_weight = random.randint(50, 249) * 100

                car_id = random.choice(car_ids)
                driver_id = random.choice(driver_ids)
                route_id = random.choice(route_ids)
                customer_id = random.choice(customer_ids)

                generated_data.append((
                    departure_date, arrival_date, return_date, cargo_desc, cargo_weight,
                    car_id, driver_id, route_id, customer_id
                ))

            query = """
                    INSERT INTO trip (departure_date, arrival_date, return_date, cargo_description, cargo_weight,
                                      car_id, driver_id, route_id, customer_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """

            print(f"Вставка {len(generated_data)} записів у БД...")
            try:
                with self.conn.cursor() as cursor:
                    cursor.executemany(query, generated_data)
                    inserted_count = cursor.rowcount
                    self.conn.commit()
                    return f"Успішно згенеровано та додано {inserted_count} записів 'trip'."

            except Exception as e:
                self.conn.rollback()
                return f"Помилка при пакетній вставці 'trip': {e}"

    def generate_service(self, count):
        query = """
                INSERT INTO service (car_id, service_date, description, cost)
                SELECT (SELECT car_id FROM car ORDER BY random() LIMIT 1), \
                       CURRENT_DATE - (random() * 90)::int, \
                       (ARRAY ['Планове ТО', 'Ремонт двигуна', 'Заміна шин', 'Ремонт гальм'])[trunc(random() * 4) + 1], \
                       trunc(1000 + random() * 15000)::numeric(10, 2)
                FROM generate_series(1, %s) \
                """
        return self._generate_data(query, count)


    def search_trips_complex(self, min_weight, max_weight, brand_pattern):

        query = """
                SELECT t.trip_id, \
                       t.cargo_description, \
                       t.cargo_weight, \
                       c.brand, \
                       c.license_plate, \
                       d.name || ' ' || d.surname AS driver_full_name
                FROM trip AS t \
                         JOIN \
                     car AS c ON t.car_id = c.car_id \
                         JOIN \
                     driver AS d ON t.driver_id = d.driver_id
                WHERE t.cargo_weight BETWEEN %s AND %s
                  AND c.brand ILIKE %s; \
                """

        if not self.conn:
            return None, 0, "Помилка: Немає з'єднання з БД."

        try:
            with self.conn.cursor() as cursor:
                start_time = time.time()
                cursor.execute(query, (min_weight, max_weight, brand_pattern))
                end_time = time.time()
                duration_ms = (end_time - start_time) * 1000

                result = cursor.fetchall()
                self.conn.commit()
                return result, duration_ms, "Пошук успішний."

        except Exception as e:
            self.conn.rollback()
            return None, 0, f"Помилка пошуку: {e}"

    def _get_existing_ids(self, table_name, id_column):
        ids = []
        if not self.conn:
            return ids
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(f"SELECT {id_column} FROM {table_name}")
                ids = [row[0] for row in cursor.fetchall()]
        except Exception as e:
            print(f"Помилка отримання ID для {table_name}: {e}")
        return ids