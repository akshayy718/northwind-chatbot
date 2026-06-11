import sqlite3

def create_northwind_database():
    # Create/connect to database
    conn = sqlite3.connect('northwind.db')
    cursor = conn.cursor()
    
    # Create Customers table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Customers (
        CustomerID TEXT PRIMARY KEY,
        CompanyName TEXT,
        ContactName TEXT,
        City TEXT,
        Country TEXT,
        Phone TEXT
    )
    ''')
    
    # Create Products table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products (
        ProductID INTEGER PRIMARY KEY,
        ProductName TEXT,
        Category TEXT,
        UnitPrice REAL,
        UnitsInStock INTEGER
    )
    ''')
    
    # Create Orders table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Orders (
        OrderID INTEGER PRIMARY KEY,
        CustomerID TEXT,
        OrderDate TEXT,
        ShipCity TEXT,
        ShipCountry TEXT,
        FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
    )
    ''')
    
    # Insert sample customers
    customers = [
        ('ALFKI', 'Alfreds Futterkiste', 'Maria Anders', 'Berlin', 'Germany', '030-0074321'),
        ('ANATR', 'Ana Trujillo Emparedados', 'Ana Trujillo', 'Mexico D.F.', 'Mexico', '(5) 555-4729'),
        ('ANTON', 'Antonio Moreno Taquería', 'Antonio Moreno', 'Mexico D.F.', 'Mexico', '(5) 555-3932'),
        ('AROUT', 'Around the Horn', 'Thomas Hardy', 'London', 'UK', '(171) 555-7788'),
        ('BERGS', 'Berglunds snabbköp', 'Christina Berglund', 'Luleå', 'Sweden', '0921-12 34 65'),
        ('BLAUS', 'Blauer See Delikatessen', 'Hanna Moos', 'Mannheim', 'Germany', '0621-08460'),
        ('BLONP', 'Blondesddsl père et fils', 'Frédérique Citeaux', 'Strasbourg', 'France', '88.60.15.31'),
        ('BOLID', 'Bólido Comidas preparadas', 'Martín Sommer', 'Madrid', 'Spain', '(91) 555 22 82'),
        ('BONAP', 'Bon app', 'Laurence Lebihan', 'Marseille', 'France', '91.24.45.40'),
        ('BOTTM', 'Bottom-Dollar Markets', 'Elizabeth Lincoln', 'Tsawassen', 'Canada', '(604) 555-4729')
    ]
    
    cursor.executemany('INSERT OR IGNORE INTO Customers VALUES (?,?,?,?,?,?)', customers)
    
    # Insert sample products
    products = [
        (1, 'Chai', 'Beverages', 18.00, 39),
        (2, 'Chang', 'Beverages', 19.00, 17),
        (3, 'Aniseed Syrup', 'Condiments', 10.00, 13),
        (4, 'Chef Anton Cajun Seasoning', 'Condiments', 22.00, 53),
        (5, 'Grandma Boysenberry Spread', 'Condiments', 25.00, 120),
        (6, 'Northwoods Cranberry Sauce', 'Condiments', 40.00, 6),
        (7, 'Mishi Kobe Niku', 'Meat/Poultry', 97.00, 29),
        (8, 'Ikura', 'Seafood', 31.00, 31),
        (9, 'Queso Cabrales', 'Dairy Products', 21.00, 22),
        (10, 'Tofu', 'Produce', 23.25, 35)
    ]
    
    cursor.executemany('INSERT OR IGNORE INTO Products VALUES (?,?,?,?,?)', products)
    
    # Insert sample orders
    orders = [
        (10248, 'ALFKI', '2024-07-04', 'Berlin', 'Germany'),
        (10249, 'ANATR', '2024-07-05', 'Mexico D.F.', 'Mexico'),
        (10250, 'AROUT', '2024-07-08', 'London', 'UK'),
        (10251, 'BERGS', '2024-07-08', 'Luleå', 'Sweden'),
        (10252, 'BLAUS', '2024-07-09', 'Mannheim', 'Germany')
    ]
    
    cursor.executemany('INSERT OR IGNORE INTO Orders VALUES (?,?,?,?,?)', orders)
    
    conn.commit()
    conn.close()
    print("✅ Northwind database created successfully!")
    print("📊 Database file: northwind.db")

if __name__ == "__main__":
    create_northwind_database()