from sqlalchemy import create_engine, Column, Integer, String, UniqueConstraint, ForeignKey, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, declarative_base, joinedload

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
    __table_args__ = (UniqueConstraint('email', name='unique_email'),)

engine = create_engine('mysql+pymysql://root:Basededatos2023@localhost/sakila')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def crear_pais():
    nombre_pais = input('Introduce el nombre del país: ')
    pais = session.query(Country).filter_by(country=nombre_pais).first()
    if pais:
        print(f'Ya existe un país con el nombre {nombre_pais}')
        return
    nuevo_pais = Country(country=nombre_pais)
    session.add(nuevo_pais)
    session.commit()
    print(f'Se ha creado el país {nuevo_pais.country}')

def listar_paises():
    paises = session.query(Country).all()
    for pais in paises:
        print(pais.country)

def eliminar_pais():
    nombre_pais = input('Introduce el nombre del país a eliminar: ')
    pais = session.query(Country).filter_by(country=nombre_pais).one_or_none()
    if pais is None:
        print(f'El país {nombre_pais} no se encuentra en la base de datos')
        return
    ciudades = session.query(City).filter_by(country_id=pais.country_id).all()

    print(f'Está a punto de eliminar el país {pais.country} y todas las siguientes ciudades relacionadas:')
    for ciudad in ciudades:
        print(ciudad.city)
    confirmacion = input('¿Está seguro que desea eliminar el país y todas sus ciudades relacionadas? (s/n): ')
    if confirmacion.lower() == 's':
        for ciudad in ciudades:
            session.delete(ciudad)
        session.delete(pais)
        session.commit()
        print(f'Se ha eliminado el país {pais.country} y todas sus ciudades relacionadas.')
    else:
        print('Operación cancelada')

def crear_ciudad():
    nombre_ciudad = input('Introduce el nombre de la ciudad: ')
    nombre_pais = input('Introduce el nombre del país al que pertenece: ')
    pais = session.query(Country).filter_by(country=nombre_pais).one()

    ciudad_existente = session.query(City).filter_by(city=nombre_ciudad, country_id=pais.country_id).first()
    if ciudad_existente:
        print(f'Ya existe una ciudad llamada {nombre_ciudad} en el país {nombre_pais}')
        return

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
    nombre_pais = input('Introduce el nombre del país al que pertenece la ciudad: ')
    ciudad = session.query(City).join(Country).filter(City.city == nombre_ciudad, Country.country == nombre_pais).one_or_none()
    if ciudad is None:
        print(f'La ciudad {nombre_ciudad} no se encuentra en la base de datos')
        return
    nombre_pais = ciudad.country.country
    confirmacion = input(f'¿Estás seguro que deseas eliminar la ciudad {ciudad.city} en el país {nombre_pais}? (s/n): ')
    if confirmacion.lower() == 's':
        session.delete(ciudad)
        session.commit()
        print(f'Se ha eliminado la ciudad {ciudad.city} del país {nombre_pais}')
    else:
        print('Operación cancelada')

def crear_tabla_usuarios():
    if not inspect(engine).has_table('user'):
        Base.metadata.create_all(engine)
        print('Se ha creado la tabla de usuarios')
    else:
        print('La tabla de usuarios ya existe')

def borrar_tabla_usuarios():
    inspector = inspect(engine)
    if not inspector.has_table('user'):
        print('La tabla de usuarios no existe')
    else:
        Base.metadata.tables["user"].drop(bind=engine, checkfirst=True)
        print('Se ha eliminado la tabla de usuarios')

def mostrar_estructura_tabla_usuarios():
    inspector = inspect(engine)
    if inspector.has_table('user'):
        insp = inspect(User)
        columns = insp.columns
        print("Estructura de la tabla 'User':")
        for column in columns:
            print(f"{column.name}: {column.type}")
    else:
        print("La tabla no existe en la base de datos")


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
