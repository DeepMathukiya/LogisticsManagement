import streamlit as st
import pandas as pd
import mysql.connector

def connect_to_database():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="logisticsmanagement"
    )

conn = connect_to_database()
c = conn.cursor() 
def create_tables():
    c.execute('''
              CREATE TABLE IF NOT EXISTS Person(
                    person_id INTEGER PRIMARY KEY AUTO_INCREMENT,
                    name VARCHAR(255)
                   
                    )'''
              )
    c.execute('''CREATE TABLE IF NOT EXISTS PersonContact(
                    person_id INTEGER ,
                    contact_info varchar(10),
                    PRIMARY KEY (person_id, contact_info),
                    FOREIGN KEY (person_id) REFERENCES Person(person_id)
                    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS Customer(
                    customer_id INTEGER PRIMARY KEY AUTO_INCREMENT,
                    person_id INTEGER,
                    address VARCHAR(255),
                    foreign key (person_id) references Person(person_id)
                    )''')
    
    c.execute(
'''CREATE TABLE IF NOT EXISTS Warehouses (
                    warehouse_id INTEGER PRIMARY KEY AUTO_INCREMENT,
                    name VARCHAR(255) NOT NULL,
                    location VARCHAR(255),
                    capacity INT
                    )''')
    
    c.execute('''
              CREATE TABLE IF NOT EXISTS Employees (
                    employee_id INTEGER PRIMARY KEY AUTO_INCREMENT,
                    person_id INTEGER,
                    position VARCHAR(255),
                    department VARCHAR(255),
                    foreign key (person_id) references Person(person_id)
                    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS Vehicles (
                    vehicle_id INTEGER PRIMARY KEY AUTO_INCREMENT,
                    type VARCHAR(255),
                    capacity INT,
                    status VARCHAR(255)
                    )''')
    
    c.execute('''
              CREATE TABLE IF NOT EXISTS Shipments (
                    shipment_id INTEGER PRIMARY KEY AUTO_INCREMENT,
                    sender_id INT,
                    receiver_id INT,
                    origin_warehouse_id INT,
                    destination_warehouse_id INT,
                    departure_time DATETIME,
                    arrival_time DATETIME,
                    status VARCHAR(255),
                    FOREIGN KEY (sender_id) REFERENCES Customer(customer_id),
                    FOREIGN KEY (receiver_id) REFERENCES Customer(customer_id),
                    FOREIGN KEY (origin_warehouse_id) REFERENCES Warehouses(warehouse_id),
                    FOREIGN KEY (destination_warehouse_id) REFERENCES Warehouses(warehouse_id)
                    )''')
    
    c.execute('''
              CREATE TABLE IF NOT EXISTS Routes (
                    route_id INTEGER PRIMARY KEY AUTO_INCREMENT,
                    origin_location VARCHAR(255),
                    destination_location VARCHAR(255),
                    distance FLOAT,
                    duration INT
                    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS Orders (
                    order_id INTEGER PRIMARY KEY AUTO_INCREMENT,
                    customer_id INT,
                    shipment_id INT,
                    order_date DATE,
                    delivery_date DATE,
                    status VARCHAR(255),
                    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id),
                    FOREIGN KEY (shipment_id) REFERENCES Shipments(shipment_id)
                    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS Inventory (
                    inventory_id INTEGER PRIMARY KEY AUTO_INCREMENT,
                    warehouse_id INT,
                    quantity INT,
                    FOREIGN KEY (warehouse_id) REFERENCES Warehouses(warehouse_id)
                    )''')    
    c.execute('''CREATE TABLE IF NOT EXISTS VehicleAssign (
                    route_id INT,
                    vehicle_id INT,
                    shipment_id INT,
                    PRIMARY KEY (route_id, vehicle_id,shipment_id),
                    FOREIGN KEY (route_id) REFERENCES Routes(route_id),
                    FOREIGN KEY (vehicle_id) REFERENCES Vehicles(vehicle_id),
                    FOREIGN KEY (shipment_id) REFERENCES Shipments(shipment_id)
                    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS Employees_Shipments (
                    employee_id INT,
                    shipment_id INT,
                    role VARCHAR(255),
                    PRIMARY KEY (employee_id, shipment_id),
                    FOREIGN KEY (employee_id) REFERENCES Employees(employee_id),
                    FOREIGN KEY (shipment_id) REFERENCES Shipments(shipment_id)
                    )''')
    conn.commit()
    print('Tables created successfully')

def insert_data(table_name, *args):
    if table_name == "Person":
        c.execute('''INSERT INTO Person (person_id,name) VALUES (%s,%s)''', args)
    if table_name == "PersonContact":
        c.execute('''INSERT INTO PersonContact (person_id, contact_info) VALUES (%s, %s)''', args)    
    if table_name == "Customer":
        c.execute('''INSERT INTO Customer (customer_id,person_id, address) VALUES (%s,%s, %s)''', args)
    elif table_name == "Warehouses":
        c.execute('''INSERT INTO Warehouses (warehouse_id,name, location, capacity) VALUES (%s,%s, %s, %s)''', args)
    elif table_name == "Employees":
        c.execute('''INSERT INTO Employees (employee_id, person_id , position, department) VALUES (%s,%s, %s, %s)''', args)
    elif table_name == "Vehicles":
        c.execute('''INSERT INTO Vehicles (vehicle_id,type, capacity, status) VALUES (%s,%s, %s, %s)''', args)
    elif table_name == "Shipments":
        c.execute('''INSERT INTO Shipments (shipment_id,sender_id, receiver_id, origin_warehouse_id, destination_warehouse_id, departure_time, arrival_time, status) VALUES (%s,%s, %s, %s, %s, %s, %s, %s)''', args)
    elif table_name == "Routes":
        c.execute('''INSERT INTO Routes (route_id,origin_location, destination_location, distance, duration) VALUES (%s,%s, %s, %s, %s)''', args)
    elif table_name == "Orders":
        c.execute('''INSERT INTO Orders (order_id,customer_id, shipment_id, order_date, delivery_date, status) VALUES (%s,%s, %s, %s, %s, %s)''', args)
    elif table_name == "Inventory":
        c.execute('''INSERT INTO Inventory (inventory_id,warehouse_id, quantity) VALUES (%s,%s,%s)''', args)
    elif table_name == "VehicleAssign":
        c.execute('''INSERT INTO Routes_Vehicles (route_id, vehicle_id,shipment_id) VALUES (%s, %s, %s)''', args)
    elif table_name == "Employees_Shipments":
        c.execute('''INSERT INTO Employees_Shipments (employee_id, shipment_id, role) VALUES (%s, %s, %s)''', args)
    conn.commit()

# def delete_data(table_name, primary_key):
#     c.execute(f'''DELETE FROM {table_name} WHERE {table_name}_id = %s''', (primary_key,))
#     conn.commit()
def delete_data(table_name, primary_key):
    if(table_name == "VehicleAssign"):
        c.execute(f'''DELETE FROM {table_name} WHERE route_id = %s and vehicle_id = %s and shipment_id = %s''', (primary_key[0],primary_key[1],primary_key[2]))
    elif(table_name == "Employees_Shipments"):
        c.execute(f'''DELETE FROM {table_name} WHERE employee_id = %s and shipment_id = %s''', (primary_key[0],primary_key[1]))
    elif(table_name=="Orders"):
        c.execute(f'''DELETE FROM {table_name} WHERE order_id = %s''', (primary_key[0],))
    elif(table_name=="Inventory"):
        c.execute(f'''DELETE FROM {table_name} WHERE inventory_id = %s''', (primary_key[0],)) 
    conn.commit()


def update_data(table_name, primary_key, *args):
    placeholders = ', '.join(['%s'] * len(args))
    if table_name == "Person":
        c.execute(f'''UPDATE {table_name} SET person_id = %s, name = %s WHERE person_id = %s''', args + (primary_key[0],))
    if table_name == "PersonContact":
        c.execute(f'''UPDATE {table_name} SET person_id = %s , contact_info = %s WHERE person_id = %s and contact_info = %s''', args + (primary_key[0],primary_key[1],))    
    if table_name == "Customer":
        c.execute(f'''UPDATE {table_name} SET customer_id = %s, person_id=%s, address = %s WHERE customer_id = %s''', args + (primary_key[0],))
    elif table_name == "Warehouses":
        c.execute(f'''UPDATE {table_name} SET warehouse_id = %s,name = %s, location = %s, capacity = %s WHERE warehouse_id = %s''', args + (primary_key[0],))
    elif table_name == "Employees":
        c.execute(f'''UPDATE {table_name} SET employee_id = %s , person_id=%s, position = %s, department = %s, WHERE employee_id = %s''', args + (primary_key[0],))
    elif table_name == "Vehicles":
        c.execute(f'''UPDATE {table_name} SET vehicle_id = %s, type = %s, capacity = %s, status = %s WHERE vehicle_id = %s''', args + (primary_key[0],))
    elif table_name == "Shipments":
        c.execute(f'''UPDATE {table_name} SET shipment_id = %s , sender_id = %s, receiver_id = %s, origin_warehouse_id = %s, destination_warehouse_id = %s, departure_time = %s, arrival_time = %s, status = %s WHERE shipment_id = %s''', args + (primary_key[0],))
    elif table_name == "Routes":
        c.execute(f'''UPDATE {table_name} SET route_id = %s ,origin_location = %s, destination_location = %s, distance = %s, duration = %s WHERE route_id = %s''', args + (primary_key[0],))
    elif table_name == "Orders":
        c.execute(f'''UPDATE {table_name} SET order_id = %s ,customer_id = %s, shipment_id = %s, order_date = %s, delivery_date = %s, status = %s WHERE order_id = %s''', args + (primary_key[0],))
    elif table_name == "Inventory":
        c.execute(f'''UPDATE {table_name} SET inventory_id = %s, warehouse_id = %s, quantity = %s WHERE inventory_id = %s''', args + (primary_key[0],))
    elif table_name == "VehicleAssign":
        c.execute(f'''UPDATE {table_name} SET route_id= %s , vehicle_id = %s,  shipment_id = %s WHERE route_id = %s and vehicle_id= %s and shipment_id= %s''', args + (primary_key[0],primary_key[1],primary_key[2]))
    elif table_name == "Employees_Shipments":
        c.execute(f'''UPDATE {table_name} SET employee_id= %s ,shipment_id = %s, role = %s WHERE employee_id = %s and shipment_id = %s ''', args + (primary_key[0], primary_key[1]))
    conn.commit()

def view_data(table_name):
    c.execute(f'''SELECT * FROM {table_name}''')
    data = c.fetchall()
    return data

def main():
    st.set_page_config(page_title="Logs System", page_icon="img.svg", layout="wide", initial_sidebar_state="auto")

    st.title("Logistics Management System")
    create_tables()

    menu = ["Insert Data", "Delete Data", "Update Data", "View Data"]
    choice = st.sidebar.selectbox("Select Option", menu)

    if choice == "Insert Data":
        st.subheader("Insert Data")
        table_name = st.selectbox("Select Table", ["Person","PersonContact","Customer", "Warehouses", "Employees", "Vehicles", "Shipments", "Routes", "Orders", "Inventory", "VehicleAssign", "Employees_Shipments"])
        if table_name:
            c.execute(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table_name}'")
            columns = [col[0] for col in c.fetchall()]
            args = [st.text_input(columns[i], key=str(i)) for i in range(len(columns))]
        if st.button("Insert"):
            insert_data(table_name, *args)
            st.success(f"{table_name} Data Inserted Successfully!")

    elif choice == "Delete Data":
        st.subheader("Delete Data")
        table_name = st.selectbox("Select Table", ["Orders", "Inventory","VehicleAssign", "Employees_Shipments"])
        # primary_key = st.text_input(f"Enter {table_name}_id to delete")
        c.execute(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE WHERE TABLE_NAME = '{table_name}' AND CONSTRAINT_NAME = 'PRIMARY'")        
        columns1 = [col[0] for col in c.fetchall()]
        primary_key = [st.text_input(columns1[i], key=str(i)) for i in range(len(columns1))]
        
        if primary_key and st.button("Delete"):
            delete_data(table_name, primary_key)
            st.success(f"{table_name} Data Deleted Successfully!")

    elif choice == "Update Data":
        st.subheader("Update Data")
        table_name = st.selectbox("Select Table", ["Person","PersonContact","Customer", "Warehouses", "Employees", "Vehicles", "Shipments", "Routes", "Orders", "Inventory", "VehicleAssign", "Employees_Shipments"])
        c.execute(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE WHERE TABLE_NAME = '{table_name}' AND CONSTRAINT_NAME = 'PRIMARY'")        
        columns1 = [col[0] for col in c.fetchall()]
        primary_key = [st.text_input(columns1[i], key=str(i)) for i in range(len(columns1))]
        # primary_key = st.text_input(f"Enter {table_name.lower()}_id to update")
        if primary_key:
            st.subheader("Fill Updated Data")
            c.execute(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table_name}'")
            columns = [col[0] for col in c.fetchall()]
            cols = st.columns(len(columns)) 
            args = [st.text_input(columns[i]) for i in range(len(columns))]
            if st.button("Update"):
                # update_data(table_name, primary_key, *args)
                update_data(table_name, primary_key, *args)
                st.success(f"{table_name} Data Updated Successfully!")
    # elif choice == "Update Data":
    #     st.subheader("Update Data")
    #     table_name = st.selectbox("Select Table", ["Customer", "Warehouses", "Employees", "Vehicles", "Shipments", "Routes", "Orders", "Inventory", "Products", "Routes_Vehicles", "Employees_Shipments"])
    #     primary_key = st.text_input(f"Enter {table_name.lower()}_id to update")
    
    #     if primary_key:
    #         c.execute(f"PRAGMA table_info({table_name})")
    #         columns = [col[1] for col in c.fetchall()]
    #         cols = st.columns(len(columns))
    #         args = [cols[i].text_input(columns[i], key=str(i)) for i in range(len(columns))]

    #         if st.button("Update"):
    #             update_data(table_name, primary_key, *args)
    #             st.success(f"{table_name} Data Updated Successfully!")




    elif choice == "View Data":
        st.subheader("View Data")
        table_name = st.selectbox("Select Table", ["Person","PersonContact","Customer", "Warehouses", "Employees", "Vehicles", "Shipments", "Routes","Orders", "Inventory","VehicleAssign", "Employees_Shipments"])
        if table_name:
            data = view_data(table_name)
            df = pd.DataFrame(data, columns=[col[0] for col in c.description])
            st.dataframe(df)

if __name__ == "__main__":
    main()