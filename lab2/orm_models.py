from sqlalchemy import Column, Integer, String, Date, ForeignKey, Numeric, Float
from sqlalchemy.orm import relationship
from database import Base


class Car(Base):
    __tablename__ = 'car'

    car_id = Column(Integer, primary_key=True, index=True)
    vin = Column(String(17), unique=True, nullable=False)
    license_plate = Column(String(20), unique=True, nullable=False)
    brand = Column(String(50), nullable=False)
    load_capacity = Column(Integer, nullable=False)

    # Зв'язки для ORM (дозволяє звертатися як car.trips)
    trips = relationship("Trip", back_populates="car")
    services = relationship("Service", back_populates="car")


class Driver(Base):
    __tablename__ = 'driver'

    driver_id = Column(Integer, primary_key=True, index=True)
    license_number = Column(String(20), unique=True, nullable=False)
    surname = Column(String(50), nullable=False)
    name = Column(String(50), nullable=False)
    license_category = Column(String(5), nullable=False)

    trips = relationship("Trip", back_populates="driver")


class Customer(Base):
    __tablename__ = 'customer'

    customer_id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    address = Column(String(200), nullable=False)

    trips = relationship("Trip", back_populates="customer")


class Route(Base):
    __tablename__ = 'route'

    route_id = Column(Integer, primary_key=True, index=True)
    departure_point = Column(String(100), nullable=False)
    destination_point = Column(String(100), nullable=False)
    distance_km = Column(Integer, nullable=False)

    trips = relationship("Trip", back_populates="route")


class Trip(Base):
    __tablename__ = 'trip'

    trip_id = Column(Integer, primary_key=True, index=True)
    departure_date = Column(Date, nullable=False)
    arrival_date = Column(Date, nullable=False)
    return_date = Column(Date)
    cargo_description = Column(String(200))
    cargo_weight = Column(Integer, nullable=False)

    car_id = Column(Integer, ForeignKey('car.car_id'), nullable=False)
    driver_id = Column(Integer, ForeignKey('driver.driver_id'), nullable=False)
    route_id = Column(Integer, ForeignKey('route.route_id'), nullable=False)
    customer_id = Column(Integer, ForeignKey('customer.customer_id'), nullable=False)

    car = relationship("Car", back_populates="trips")
    driver = relationship("Driver", back_populates="trips")
    route = relationship("Route", back_populates="trips")
    customer = relationship("Customer", back_populates="trips")


class Service(Base):
    __tablename__ = 'service'

    service_id = Column(Integer, primary_key=True, index=True)
    car_id = Column(Integer, ForeignKey('car.car_id'), nullable=False)
    service_date = Column(Date, nullable=False)
    description = Column(String(200), nullable=False)
    cost = Column(Numeric(10, 2), nullable=False)

    car = relationship("Car", back_populates="services")