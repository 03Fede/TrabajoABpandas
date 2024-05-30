
class LibretaDireccionesPandasDB:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        self.connection = self.engine.connect()
        self.crear_tabla()  # Crear la tabla al iniciar
    
    def crear_tabla(self):
        # Crear la tabla contactos si no existe
        create_table_query = text("""
        CREATE TABLE IF NOT EXISTS contactos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            Nombre VARCHAR(255),
            Apellido VARCHAR(255),
            Telefono VARCHAR(255) UNIQUE,
            Direccion VARCHAR(255),
            Empleo VARCHAR(255),
            usuario_id INT
        );
        """)
        self.connection.execute(create_table_query)
    
    def agregar_contacto(self, nombre, apellido, telefono, direccion, empleo, usuario_id):
        df = pd.DataFrame({
            "Nombre": [nombre], 
            "Apellido": [apellido], 
            "Telefono": [telefono], 
            "Direccion": [direccion], 
            "Empleo": [empleo],
            "usuario_id": [usuario_id]
        })
        try:
            df.to_sql("contactos", self.engine, if_exists='append', index=False)
            print("Contacto agregado con éxito.")
        except IntegrityError as e:
            print(f"Error: No se pudo agregar el contacto. El número de teléfono '{telefono}' ya existe.")
    
    def buscar_contacto(self, criterio):
        query = text("SELECT * FROM contactos WHERE Nombre LIKE :criterio OR Apellido LIKE :criterio")
        parametros = {'criterio': f'%{criterio}%'}
        resultados = pd.read_sql(query, self.connection, params=parametros)
        return resultados
    
    def listar_contactos(self):
        query = text("SELECT id, Nombre, Apellido, Telefono FROM contactos")
        resultados = pd.read_sql(query, self.connection)
        return resultados
    
    def eliminar_contacto(self, id_contacto):
        delete_query = text("DELETE FROM contactos WHERE id = :id_contacto")
        parametros = {'id_contacto': id_contacto}
        try:
            result = self.connection.execute(delete_query, parametros)
            print(f"Se eliminó correctamente el contacto con el ID {id_contacto}.")
        except IntegrityError as e:
            print(f"Error: No se pudo eliminar el contacto. El ID {id_contacto} no existe.")

# Función para mostrar el menú
def mostrar_menu():
    print("1. Agregar contacto")
    print("2. Buscar contacto")
    print("3. Listar contactos")
    print("4. Eliminar contacto")
    print("5. Salir")

# URL de la base de datos
db_url = 'mysql+pymysql://root:toor@localhost/libreta_direcciones'
libreta_pandas_db = LibretaDireccionesPandasDB(db_url)

while True:
    mostrar_menu()
    opcion = input("Seleccione una opción: ")
    
    if opcion == '1':
        # Opción para agregar un contacto
        nombre = input("Ingrese el nombre del contacto: ")
        apellido = input("Ingrese el apellido del contacto: ")
        telefono = input("Ingrese el número de teléfono del contacto: ")
        direccion = input("Ingrese la dirección del contacto: ")
        empleo = input("Ingrese el empleo del contacto: ")
        usuario_id = int(input("Ingrese el ID del usuario: "))
        
        libreta_pandas_db.agregar_contacto(nombre, apellido, telefono, direccion, empleo, usuario_id)
    elif opcion == '2':
        # Opción para buscar un contacto
        criterio = input("Ingrese el criterio de búsqueda (nombre o apellido): ")
        resultados = libreta_pandas_db.buscar_contacto(criterio)
        print(resultados)
    elif opcion == '3':
        # Opción para listar todos los contactos
        contactos = libreta_pandas_db.listar_contactos()
        print(contactos)
    elif opcion == '4':
        # Opción para eliminar un contacto
        id_contacto = input("Ingrese el ID del contacto que desea eliminar: ")
        libreta_pandas_db.eliminar_contacto(id_contacto)
    elif opcion == '5':
        # Opción para salir del programa
        print("¡Hasta luego!")
        break
    else:
        print("Opción no válida. Por favor, seleccione una opción válida.")
