from sqlalchemy import create_engine, Column, Integer, String, UniqueConstraint, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Country(Base):
    __tablename__ = 'country'
    country_id = Column(Integer, primary_key=True)
    country = Column(String(50), nullable=False, unique=True)
    cities = relationship('City', back_populates='country')

class City(Base):
    __tablename__ = 'city'
    city_id = Column(Integer, primary_key=True)
    city = Column(String(50), nullable=False)
    country_id = Column(Integer, ForeignKey('country.country_id'))
    country = relationship('Country', back_populates='cities')

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    age = Column(Integer)
    email = Column(String(50), nullable=False, unique=True)

engine = create_engine('mysql+pymysql://root:Basededatos2023@localhost/sakila')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def crear_pais():
    nombre_pais = input('Introduce el nombre del país: ')
    pais = Country(country=nombre_pais)
    session.add(pais)
    session.commit()
    print(f'Se ha creado el país {pais.country}')

def listar_paises():
    paises = session.query(Country).all()
    for pais in paises:
        print(pais.country)

def eliminar_pais():
    nombre_pais = input('Introduce el nombre del país a eliminar: ')
    pais = session.query(Country).filter_by(country=nombre_pais).one()
    session.delete(pais)
    session.commit()
    print(f'Se ha eliminado el país {pais.country}')

def crear_ciudad():
    nombre_ciudad = input('Introduce el nombre de la ciudad: ')
    nombre_pais = input('Introduce el nombre del país al que pertenece: ')
    pais = session.query(Country).filter_by(country=nombre_pais).one()
    ciudad = City(city=nombre_ciudad, country=pais)
    session.add(ciudad)
    session.commit()
    print(f'Se ha creado la ciudad {ciudad.city} en el país {pais.country}')

def listar_ciudades():
    ciudades = session.query(City).all()
    for ciudad in ciudades:
        print(f'{ciudad.city} ({ciudad.country.country})')

def eliminar_ciudad():
    nombre_ciudad = input('Introduce el nombre de la ciudad a eliminar: ')
    ciudad = session.query(City).filter_by(city=nombre_ciudad).one()
    session.delete(ciudad)
    session.commit()
    print(f'Se ha eliminado la ciudad {ciudad.city} del país {ciudad.country.country}')

def crear_tabla_usuarios():
    class Usuario(Base):
        __tablename__ = 'usuarios'
        id = Column(Integer, primary_key=True, autoincrement=True)
        name = Column(String(50), nullable=False)
        age = Column(Integer)
        email = Column(String(50), nullable=False, unique=True)
        __table_args__ = (UniqueConstraint('email', name='unique_email'),)
    Base.metadata.create_all(engine)
    print('Se ha creado la tabla de usuarios')

def borrar_tabla_usuarios():
    Usuario.table.drop(engine)
    print('Se ha eliminado la tabla de ususarios')

def mostrar_estructura_tabla_usuarios():
    print(Usuario.table)


while True:
    print('Menú principal:')
    print('1. Crear país')
    print('2. Listar países')
    print('3. Eliminar país')
    print('4. Crear ciudad')
    print('5. Listar ciudades')
    print('6. Eliminar ciudad')
    print('7. Crear tabla usuarios')
    print('8. Borrar tabla usuarios')
    print('9. Mostrar estructura tabla usuarios')
    print('0. Salir')

    opcion = input('Seleccione una opción: ')

    if opcion == '1':
        crear_pais()
    elif opcion == '2':
        listar_paises()
    elif opcion == '3':
        eliminar_pais()
    elif opcion == '4':
        crear_ciudad()
    elif opcion == '5':
        listar_ciudades()
    elif opcion == '6':
        eliminar_ciudad()
    elif opcion == '7':
        crear_tabla_usuarios()
    elif opcion == '8':
        borrar_tabla_usuarios()
    elif opcion == '9':
        mostrar_estructura_tabla_usuarios()
    elif opcion == '0':
        break
    else:
        print('Opción inválida')
