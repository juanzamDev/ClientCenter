import os
import traceback
import sys
import psycopg2
import uuid

sys.path.append(os.path.join(os.path.dirname(os.path.abspath("__file__")), "solucion-victoria"))
import config
import random

# Se definen los parámetros de conexión a la BD con base en el ambiente (Dev/Prod)
def init_db():
    try:
        if 'DBNAME_DEV' not in os.environ:
            database=config.ProductionConfig.DBNAME
            user=config.ProductionConfig.DBUSER
            password=config.ProductionConfig.DBPASS
            host=config.ProductionConfig.DBHOST
            port=config.ProductionConfig.DBPORT
        else:
            database=config.DevelopmentConfig.DBNAME
            user=config.DevelopmentConfig.DBUSER
            password=config.DevelopmentConfig.DBPASS
            host=config.DevelopmentConfig.DBHOST
            port=config.DevelopmentConfig.DBPORT

        conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
        cur = conn.cursor()

        # Se borran las tablas usuario, conversacion y agente
        cur.execute("DROP TABLE IF EXISTS Clientes CASCADE;")
        cur.execute("DROP TABLE IF EXISTS Transacciones CASCADE;")
        cur.execute("DROP TABLE IF EXISTS Saldos CASCADE;")
        cur.execute("DROP TABLE IF EXISTS Informacion_Adicional CASCADE;")

        cur.execute("CREATE TABLE Clientes (id INT PRIMARY KEY ,"
                    "nombre varchar (100) NOT NULL,"
                    "correo varchar (100) NOT NULL,"
                    "direccion varchar (100) NOT NULL,"
                    "telefono varchar (100) NOT NULL,"
                    "fecha date DEFAULT CURRENT_TIMESTAMP);")

        cur.execute("CREATE TABLE Transacciones (id uuid PRIMARY KEY,"
                    "cliente_id INT NOT NULL,"
                    "tipo_transaccion varchar (50),"
                    "monto varchar (100) NOT NULL,"
                    "fecha date DEFAULT CURRENT_TIMESTAMP,"
                    "FOREIGN KEY (cliente_id) REFERENCES Clientes(id));")

        cur.execute("CREATE TABLE Saldos (id uuid PRIMARY KEY,"
                    "cliente_id INT,"
                    "tipo_cuenta VARCHAR(100),"
                    "saldo DECIMAL(10, 2),"
                    "fecha_actualizacion TIMESTAMP,"
                    "FOREIGN KEY (cliente_id) REFERENCES Clientes(id));")

        cur.execute("CREATE TABLE Informacion_Adicional ("
                "id uuid PRIMARY KEY,"
                "cliente_id INT,"
                "categoria VARCHAR(50),"
                "detalle TEXT,"
                "FOREIGN KEY (cliente_id) REFERENCES Clientes(id));")
        
        # Insertar datos en la tabla Clientes
        cur.execute("INSERT INTO Clientes (id, nombre, correo, direccion, telefono, fecha) VALUES "
            "(1007677635, 'Juan', 'juan.zambrano@gamil.com', 'Calle 123, Calle 3 - Garzon', '1234567890', CURRENT_TIMESTAMP),"
            "(55059733, 'María', 'maria.gonzalez@example.com', 'Av. Principal, Calle 3 - Neiva', '0987654321', CURRENT_TIMESTAMP),"
            "(12189436, 'Pedro', 'pedro.diaz@example.com', 'Carrera 456, Carrera 1 Cali', '9876543210', CURRENT_TIMESTAMP),"
            "(1007677652, 'Laura', 'laura.lopez@example.com', 'Calle Principal, Calle 10 Bogotá', '5678901234', CURRENT_TIMESTAMP),"
            "(134029340, 'Carlos', 'carlos.martinez@example.com', 'Av. Central, Calle 1 Medellin', '2345678901', CURRENT_TIMESTAMP),"
            "(123456789, 'Ana', 'ana.rodriguez@example.com', 'Calle 456, Calle 2 - Barranquilla', '3456789012', CURRENT_TIMESTAMP),"
            "(987654321, 'Luis', 'luis.gomez@example.com', 'Av. Norte, Calle 5 - Cartagena', '4567890123', CURRENT_TIMESTAMP),"
            "(567890123, 'Sofía', 'sofia.hernandez@example.com', 'Carrera 789, Carrera 2 - Pereira', '5678901234', CURRENT_TIMESTAMP),"
            "(234567890, 'Miguel', 'miguel.perez@example.com', 'Calle Sur, Calle 4 - Bucaramanga', '6789012345', CURRENT_TIMESTAMP),"
            "(345678901, 'Isabella', 'isabella.lopez@example.com', 'Av. Oeste, Calle 6 - Santa Marta', '7890123456', CURRENT_TIMESTAMP);")

        # Insertar datos en la tabla Transacciones
        cur.execute("INSERT INTO Transacciones (id, cliente_id, tipo_transaccion, monto, fecha) VALUES "
            f"('{str(uuid.uuid4())}', 1007677635, 'Depósito', 1000.00, CURRENT_TIMESTAMP),"
            f"('{str(uuid.uuid4())}', 55059733, 'Retiro', -500.00, CURRENT_TIMESTAMP),"
            f"('{str(uuid.uuid4())}', 12189436, 'Depósito', 1500.00, CURRENT_TIMESTAMP),"
            f"('{str(uuid.uuid4())}', 1007677652, 'Transferencia', -200.00, CURRENT_TIMESTAMP),"
            f"('{str(uuid.uuid4())}', 134029340, 'Depósito', 800.00, CURRENT_TIMESTAMP),"
            f"('{str(uuid.uuid4())}', 123456789, 'Retiro', -300.00, CURRENT_TIMESTAMP),"
            f"('{str(uuid.uuid4())}', 987654321, 'Depósito', 500.00, CURRENT_TIMESTAMP),"
            f"('{str(uuid.uuid4())}', 567890123, 'Transferencia', -100.00, CURRENT_TIMESTAMP),"
            f"('{str(uuid.uuid4())}', 234567890, 'Depósito', 1200.00, CURRENT_TIMESTAMP),"
            f"('{str(uuid.uuid4())}', 345678901, 'Retiro', -700.00, CURRENT_TIMESTAMP);")

        # Insertar datos en la tabla Saldos
        cur.execute("INSERT INTO Saldos (id, cliente_id, tipo_cuenta, saldo, fecha_actualizacion) VALUES "
            f"('{str(uuid.uuid4())}', 1007677635, 'Ahorros', 2000.00, CURRENT_TIMESTAMP),"
            f"('{str(uuid.uuid4())}', 55059733, 'Corriente', 3000.00, CURRENT_TIMESTAMP),"
            f"('{str(uuid.uuid4())}', 12189436, 'Ahorros', 2500.00, CURRENT_TIMESTAMP),"
            f"('{str(uuid.uuid4())}', 1007677652, 'Corriente', 1200.00, CURRENT_TIMESTAMP),"
            f"('{str(uuid.uuid4())}', 134029340, 'Ahorros', 500.00, CURRENT_TIMESTAMP),"
            f"('{str(uuid.uuid4())}', 123456789, 'Corriente', 4000.00, CURRENT_TIMESTAMP),"
            f"('{str(uuid.uuid4())}', 987654321, 'Ahorros', 1500.00, CURRENT_TIMESTAMP),"
            f"('{str(uuid.uuid4())}', 567890123, 'Corriente', 6000.00, CURRENT_TIMESTAMP),"
            f"('{str(uuid.uuid4())}', 234567890, 'Ahorros', 3500.00, CURRENT_TIMESTAMP),"
            f"('{str(uuid.uuid4())}', 345678901, 'Corriente', 8000.00, CURRENT_TIMESTAMP);")

        # Insertar datos en la tabla Informacion_Adicional (opcional)
        cur.execute("INSERT INTO Informacion_Adicional (id, cliente_id, categoria, detalle) VALUES "
            f"('{str(uuid.uuid4())}', 1007677635, 'Notas', 'Cliente con buena historia crediticia.'),"
            f"('{str(uuid.uuid4())}', 55059733, 'Notas', 'Cliente nuevo en el banco.'),"
            f"('{str(uuid.uuid4())}', 12189436, 'Notas', 'Cliente frecuente en el banco.'),"
            f"('{str(uuid.uuid4())}', 1007677652, 'Notas', 'Cliente con varios productos en el banco.'),"
            f"('{str(uuid.uuid4())}', 134029340, 'Notas', 'Cliente con saldo negativo en su cuenta.'),"
            f"('{str(uuid.uuid4())}', 123456789, 'Notas', 'Cliente con transacciones sospechosas.'),"
            f"('{str(uuid.uuid4())}', 987654321, 'Notas', 'Cliente con historial de pagos a tiempo.'),"
            f"('{str(uuid.uuid4())}', 567890123, 'Notas', 'Cliente con alta rotación de fondos.'),"
            f"('{str(uuid.uuid4())}', 234567890, 'Notas', 'Cliente con préstamo vigente.'),"
            f"('{str(uuid.uuid4())}', 345678901, 'Notas', 'Cliente con cuenta inactiva.');")
        
        conn.commit()
        cur.close()
        conn.close()
    
    except:
        print(traceback.format_exc())
        print("No hemos podido crear la BD. Intenta de nuevo")

if __name__ == "__main__":
    init_db()
