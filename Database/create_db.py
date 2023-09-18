import sqlite3
from faker import Faker

fake = Faker()


def create_tables(conn):
    cursor = conn.cursor()

    # Clients table
    cursor.execute('''
    CREATE TABLE clients (
        client_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        phone_number TEXT,
        address TEXT
    )
    ''')

    # Employees table
    cursor.execute('''
    CREATE TABLE employees (
        employee_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        position TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        hire_date TEXT
    )
    ''')

    # Products table
    cursor.execute('''
    CREATE TABLE products (
        product_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        description TEXT,
        price REAL NOT NULL,
        stock_quantity INTEGER
    )
    ''')

    # Orders table
    cursor.execute('''
    CREATE TABLE orders (
        order_id INTEGER PRIMARY KEY,
        client_id INTEGER,
        date_ordered TEXT,
        total_price REAL,
        FOREIGN KEY (client_id) REFERENCES clients(client_id)
    )
    ''')

    # Sales table
    cursor.execute('''
    CREATE TABLE sales (
        sale_id INTEGER PRIMARY KEY,
        order_id INTEGER,
        product_id INTEGER,
        quantity_sold INTEGER,
        sale_price REAL,
        FOREIGN KEY (order_id) REFERENCES orders(order_id),
        FOREIGN KEY (product_id) REFERENCES products(product_id)
    )
    ''')

    # Shipments table
    cursor.execute('''
    CREATE TABLE shipments (
        shipment_id INTEGER PRIMARY KEY,
        order_id INTEGER,
        employee_id INTEGER,
        shipment_date TEXT,
        shipment_status TEXT,
        FOREIGN KEY (order_id) REFERENCES orders(order_id),
        FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
    )
    ''')

    conn.commit()
    print("Tables created successfully!")


def insert_fake_data(conn):
    cursor = conn.cursor()

    # Inserting fake data into clients table
    for _ in range(50):
        cursor.execute('''
        INSERT INTO clients (name, email, phone_number, address)
        VALUES (?, ?, ?, ?)
        ''', (fake.name(), fake.email(), fake.phone_number(), fake.address()))

    # Inserting fake data into employees table
    for _ in range(50):
        cursor.execute('''
        INSERT INTO employees (name, position, email, hire_date)
        VALUES (?, ?, ?, ?)
        ''', (fake.name(), fake.job(), fake.email(), fake.date_this_decade()))

    # Inserting fake data into products table
    for _ in range(50):
        cursor.execute('''
        INSERT INTO products (name, description, price, stock_quantity)
        VALUES (?, ?, ?, ?)
        ''', (fake.bs(), fake.sentence(), fake.random_int(10, 1000), fake.random_int(1, 100)))

    # Inserting fake data into orders, sales, shipments
    for _ in range(50):
        cursor.execute('''
        INSERT INTO orders (client_id, date_ordered, total_price)
        VALUES (?, ?, ?)
        ''', (fake.random_int(1, 50), fake.date_this_year(), fake.random_int(10, 1000)))

        cursor.execute('''
        INSERT INTO sales (order_id, product_id, quantity_sold, sale_price)
        VALUES (?, ?, ?, ?)
        ''', (fake.random_int(1, 50), fake.random_int(1, 50), fake.random_int(1, 5), fake.random_int(10, 1000)))

        cursor.execute('''
        INSERT INTO shipments (order_id, employee_id, shipment_date, shipment_status)
        VALUES (?, ?, ?, ?)
        ''', (fake.random_int(1, 50), fake.random_int(1, 50), fake.date_this_year(), fake.random_element(elements=('Shipped', 'Pending', 'Delivered'))))

    conn.commit()
    print("Fake data inserted successfully!")


def main():
    conn = sqlite3.connect('ecommerce.db')
    create_tables(conn)
    insert_fake_data(conn)
    conn.close()


if __name__ == '__main__':
    main()
