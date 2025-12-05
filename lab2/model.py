import time
import random
import datetime
import uuid
import sqlalchemy
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from database import SessionLocal, engine, Base
from orm_models import Car, Driver, Customer, Route, Trip, Service

Base.metadata.create_all(bind=engine)


class Model:
    def __init__(self):
        self.db = SessionLocal()

    def close_connection(self):
        self.db.close()

    def _get_model_class(self, table_name):
        mapping = {
            'car': Car,
            'driver': Driver,
            'customer': Customer,
            'route': Route,
            'trip': Trip,
            'service': Service
        }
        return mapping.get(table_name.lower())

    def get_all_data(self, table_name):
        model_class = self._get_model_class(table_name)
        if not model_class:
            return None, "Помилка: Неприпустима назва таблиці."

        try:
            records = self.db.query(model_class).limit(100).all()

            result = []
            columns = [c.name for c in model_class.__table__.columns]
            for r in records:
                row = tuple(getattr(r, col) for col in columns)
                result.append(row)
            return result, "Запит успішно виконано."
        except SQLAlchemyError as e:
            return None, f"Помилка отримання даних: {e}"

    def add_car(self, vin, license_plate, brand, load_capacity):
        try:
            car = Car(
                vin=vin,
                license_plate=license_plate,
                brand=brand,
                load_capacity=int(load_capacity)
            )
            self.db.add(car)
            self.db.commit()
            return f"Успішно додано автомобіль (ID: {car.car_id}).", True
        except ValueError:
            return "Помилка: Вантажопідйомність має бути числом.", False
        except IntegrityError:
            self.db.rollback()
            return "Помилка: VIN або номер вже існують.", False
        except Exception as e:
            self.db.rollback()
            return f"Помилка: {e}", False

    def add_driver(self, license_number, surname, name, license_category):
        try:
            driver = Driver(
                license_number=license_number,
                surname=surname,
                name=name,
                license_category=license_category
            )
            self.db.add(driver)
            self.db.commit()
            return f"Успішно додано водія (ID: {driver.driver_id}).", True
        except IntegrityError:
            self.db.rollback()
            return "Помилка: Водій з таким номером вже існує.", False
        except Exception as e:
            self.db.rollback()
            return f"Помилка: {e}", False

    def add_customer(self, full_name, phone, email, address):
        try:
            customer = Customer(
                full_name=full_name,
                phone=phone,
                email=email,
                address=address
            )
            self.db.add(customer)
            self.db.commit()
            return "Успішно додано клієнта.", True
        except IntegrityError:
            self.db.rollback()
            return "Помилка: Email вже зайнятий.", False
        except Exception as e:
            self.db.rollback()
            return f"Помилка: {e}", False

    def add_route(self, departure, destination, distance):
        try:
            route = Route(
                departure_point=departure,
                destination_point=destination,
                distance_km=int(distance)
            )
            self.db.add(route)
            self.db.commit()
            return "Успішно додано маршрут.", True
        except ValueError:
            return "Помилка: Відстань має бути числом.", False
        except Exception as e:
            self.db.rollback()
            return f"Помилка: {e}", False

    def add_service(self, car_id, service_date, description, cost):
        try:
            service = Service(
                car_id=int(car_id),
                service_date=service_date,
                description=description,
                cost=float(cost)
            )
            self.db.add(service)
            self.db.commit()
            return "Успішно додано запис про сервіс.", True
        except IntegrityError:
            self.db.rollback()
            return "Помилка: Автомобіль з таким ID не існує.", False
        except ValueError:
            return "Помилка типів даних.", False
        except Exception as e:
            self.db.rollback()
            return f"Помилка: {e}", False

    def add_trip(self, departure, arrival, return_d, cargo_desc, cargo_weight, car_id, driver_id, route_id,
                 customer_id):
        try:
            trip = Trip(
                departure_date=departure,
                arrival_date=arrival,
                return_date=return_d if return_d else None,
                cargo_description=cargo_desc,
                cargo_weight=int(cargo_weight),
                car_id=int(car_id),
                driver_id=int(driver_id),
                route_id=int(route_id),
                customer_id=int(customer_id)
            )
            self.db.add(trip)
            self.db.commit()
            return "Успішно додано рейс.", True
        except ValueError:
            return "Помилка: Введіть коректні числові дані.", False
        except IntegrityError as e:
            self.db.rollback()
            return f"Помилка цілісності (перевірте ID): {e}", False
        except Exception as e:
            self.db.rollback()
            return f"Помилка: {e}", False

    def _update_record(self, model_class, record_id, fields, values):
        try:
            record = self.db.query(model_class).get(record_id)
            if not record:
                return f"Запис з ID {record_id} не знайдено."

            updated = False
            for field, value in zip(fields, values):
                if value:
                    setattr(record, field, value)
                    updated = True

            if updated:
                self.db.commit()
                return f"Запис (ID: {record_id}) оновлено."
            return "Немає даних для оновлення."
        except Exception as e:
            self.db.rollback()
            return f"Помилка оновлення: {e}"

    def update_car(self, car_id, brand, load_capacity):
        try:
            lc = int(load_capacity) if load_capacity else None
            return self._update_record(Car, int(car_id), ["brand", "load_capacity"], [brand, lc])
        except ValueError:
            return "Помилка числа."

    def update_driver(self, driver_id, surname, name, category):
        return self._update_record(Driver, int(driver_id), ["surname", "name", "license_category"],
                                   [surname, name, category])

    def update_customer(self, customer_id, phone, email):
        return self._update_record(Customer, int(customer_id), ["phone", "email"], [phone, email])

    def update_route(self, route_id, distance):
        try:
            d = int(distance) if distance else None
            return self._update_record(Route, int(route_id), ["distance_km"], [d])
        except ValueError:
            return "Помилка числа."

    def update_service(self, service_id, description, cost):
        try:
            c = float(cost) if cost else None
            return self._update_record(Service, int(service_id), ["description", "cost"], [description, c])
        except ValueError:
            return "Помилка числа."

    def update_trip(self, trip_id, cargo_desc, cargo_weight):
        try:
            w = int(cargo_weight) if cargo_weight else None
            return self._update_record(Trip, int(trip_id), ["cargo_description", "cargo_weight"], [cargo_desc, w])
        except ValueError:
            return "Помилка числа."

    def delete_data_dynamic(self, table_name, field, value):
        model_class = self._get_model_class(table_name)
        if not model_class:
            return "Невірна таблиця."

        try:
            filter_value = int(value)
        except ValueError:
            filter_value = value

        try:
            objs = self.db.query(model_class).filter(getattr(model_class, field) == filter_value).all()

            if not objs:
                return f"0 rows affected (Запис {field}={value} не знайдено)."

            count = len(objs)
            for obj in objs:
                self.db.delete(obj)

            self.db.commit()
            return f"Deleted successfully! {count} рядків видалено."
        except IntegrityError:
            self.db.rollback()
            return "ПОМИЛКА: Видалення неможливе через зв'язки (Foreign Key)."
        except Exception as e:
            self.db.rollback()
            return f"Помилка: {e}"

    def generate_cars(self, count):
        brands = ['Volvo', 'MAN', 'Scania', 'Mercedes', 'DAF']
        cars_to_add = []

        print(f"Генерація {count} автомобілів в Python...")
        try:
            for _ in range(count):
                vin = uuid.uuid4().hex[:17].upper()
                p1 = "".join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=2))
                p2 = f"{random.randint(0, 9999):04d}"
                p3 = "".join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=2))
                license_plate = f"{p1}{p2}{p3}"

                cars_to_add.append(Car(
                    vin=vin,
                    license_plate=license_plate,
                    brand=random.choice(brands),
                    load_capacity=random.randint(10000, 25000)
                ))

            self.db.bulk_save_objects(cars_to_add)
            self.db.commit()
            return f"Успішно згенеровано {count} авто."
        except Exception as e:
            self.db.rollback()
            return f"Помилка генерації: {e}"

    def generate_drivers(self, count):
        surnames = ['Іваненко', 'Петренко', 'Сидоренко', 'Ковальчук', 'Шевченко', 'Щербатюк', 'Ямпольський', 'Підлубний', 'Клокун']
        names = ['Петро', 'Олександр', 'Михайло', 'Іван', 'Сергій', 'Євген', 'Дмитро', 'Роман', 'Владислав', 'Всеволод']
        categories = ['B', 'C', 'CE']
        drivers_to_add = []

        try:
            for _ in range(count):
                drivers_to_add.append(Driver(
                    license_number=f"DR{random.randint(100000, 999999)}",
                    surname=random.choice(surnames),
                    name=random.choice(names),
                    license_category=random.choice(categories)
                ))

            self.db.bulk_save_objects(drivers_to_add)
            self.db.commit()
            return f"Успішно згенеровано {count} водіїв."
        except Exception as e:
            self.db.rollback()
            return f"Помилка генерації: {e}"

    def generate_routes(self, count):
        deps = ['Київ', 'Львів', 'Одеса', 'Харків', 'Дніпро']
        dests = ['Варшава', 'Берлін', 'Прага', 'Відень', 'Краків']
        routes_to_add = []

        try:
            for _ in range(count):
                routes_to_add.append(Route(
                    departure_point=random.choice(deps),
                    destination_point=random.choice(dests),
                    distance_km=random.randint(300, 1500)
                ))
            self.db.bulk_save_objects(routes_to_add)
            self.db.commit()
            return f"Успішно згенеровано {count} маршрутів."
        except Exception as e:
            self.db.rollback()
            return f"Помилка: {e}"

    def generate_customers(self, count):
        streets = ['Хрещатик', 'Сумська', 'Дерибасівська', 'Європейська', 'Машинобудівників', 'Київська']
        customers_to_add = []

        try:
            for _ in range(count):
                suffix = "".join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=3))
                customers_to_add.append(Customer(
                    full_name=f"ТОВ {suffix}",
                    phone=f"+380{random.randint(100000000, 999999999)}",
                    email=f"{uuid.uuid4().hex[:10]}@gmail.com",
                    address=f"м. Київ, вул. {random.choice(streets)}, {random.randint(1, 100)}"
                ))
            self.db.bulk_save_objects(customers_to_add)
            self.db.commit()
            return f"Успішно згенеровано {count} клієнтів."
        except Exception as e:
            self.db.rollback()
            return f"Помилка: {e}"

    def generate_trips(self, count):

        try:
            car_ids = [r[0] for r in self.db.query(Car.car_id).all()]
            driver_ids = [r[0] for r in self.db.query(Driver.driver_id).all()]
            route_ids = [r[0] for r in self.db.query(Route.route_id).all()]
            customer_ids = [r[0] for r in self.db.query(Customer.customer_id).all()]

            if not all([car_ids, driver_ids, route_ids, customer_ids]):
                return "Помилка: Батьківські таблиці порожні. Спочатку згенеруйте їх."

            trips_to_add = []
            cargos = ['Будматеріали', 'Металопрокат', 'Продукти', 'Техніка', 'Хімікати', 'Лікарські препарати', 'Нафтопродукти']

            print(f"Генерація {count} рейсів...")
            for _ in range(count):
                dep_date = datetime.date.today() - datetime.timedelta(days=random.randint(0, 30))
                arr_date = dep_date + datetime.timedelta(days=random.randint(1, 6))
                ret_date = arr_date + datetime.timedelta(days=random.randint(1, 5))

                trips_to_add.append(Trip(
                    departure_date=dep_date,
                    arrival_date=arr_date,
                    return_date=ret_date,
                    cargo_description=random.choice(cargos),
                    cargo_weight=random.randint(50, 250) * 100,
                    car_id=random.choice(car_ids),
                    driver_id=random.choice(driver_ids),
                    route_id=random.choice(route_ids),
                    customer_id=random.choice(customer_ids)
                ))

            self.db.bulk_save_objects(trips_to_add)
            self.db.commit()
            return f"Успішно згенеровано {count} рейсів."
        except Exception as e:
            self.db.rollback()
            return f"Помилка генерації рейсів: {e}"

    def generate_service(self, count):
        try:
            car_ids = [r[0] for r in self.db.query(Car.car_id).all()]
            if not car_ids: return "Немає авто."

            desc_opts = ['Планове ТО', 'Ремонт двигуна', 'Заміна шин', 'Ремонт гальм', 'Ремонт КПП']
            services_to_add = []

            for _ in range(count):
                services_to_add.append(Service(
                    car_id=random.choice(car_ids),
                    service_date=datetime.date.today() - datetime.timedelta(days=random.randint(0, 90)),
                    description=random.choice(desc_opts),
                    cost=round(random.uniform(1000, 15000), 2)
                ))

            self.db.bulk_save_objects(services_to_add)
            self.db.commit()
            return f"Успішно згенеровано {count} сервісних записів."
        except Exception as e:
            self.db.rollback()
            return f"Помилка: {e}"

    def search_trips_complex(self, min_weight, max_weight, brand_pattern):
        try:
            start_time = time.time()

            results = self.db.query(
                Trip.trip_id,
                Trip.cargo_description,
                Trip.cargo_weight,
                Car.brand,
                Car.license_plate,
                (Driver.name + " " + Driver.surname).label("driver_full_name")
            ).join(Trip.car).join(Trip.driver) \
                .filter(Trip.cargo_weight.between(min_weight, max_weight)) \
                .filter(Car.brand.ilike(brand_pattern)) \
                .all()

            end_time = time.time()
            duration_ms = (end_time - start_time) * 1000

            return results, duration_ms, "Пошук успішний."
        except Exception as e:
            return None, 0, f"Помилка пошуку: {e}"