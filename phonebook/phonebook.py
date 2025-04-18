import psycopg2
import csv

def connect():
    return psycopg2.connect(
        dbname="phonebook",
        user="postgres",
        password="Zhasminchik6",
        host="localhost",
        port="5432"
    )

def insert_from_csv(filename):
    conn = connect()
    cur = conn.cursor()
    try:
        with open(filename, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                cur.execute("INSERT INTO PhoneBook (first_name, phone) VALUES (%s, %s)",
                            (row['first_name'], row['phone']))
        conn.commit()
        print("CSV data inserted successfully.")
    except Exception as e:
        print("Error:", e)
    finally:
        cur.close()
        conn.close()

def insert_manual():
    name = input("Enter name: ")
    phone = input("Enter phone: ")
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO PhoneBook (first_name, phone) VALUES (%s, %s)", (name, phone))
        conn.commit()
        print("Data inserted successfully.")
    except Exception as e:
        print("Error:", e)
    finally:
        cur.close()
        conn.close()

def search_by_pattern():
    pattern = input("Enter name or part of name/phone to search: ")
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM PhoneBook WHERE first_name ILIKE %s OR phone ILIKE %s", 
                    ('%' + pattern + '%', '%' + pattern + '%'))
        rows = cur.fetchall()
        if rows:
            for row in rows:
                print(row)
        else:
            print("No records found.")
    except Exception as e:
        print("Error:", e)
    finally:
        cur.close()
        conn.close()

def get_paginated_data():
    limit = int(input("Enter limit (number of records per page): "))
    offset = int(input("Enter offset (start record): "))
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM PhoneBook ORDER BY id LIMIT %s OFFSET %s", (limit, offset))
        rows = cur.fetchall()
        if rows:
            for row in rows:
                print(row)
        else:
            print("No records found.")
    except Exception as e:
        print("Error:", e)
    finally:
        cur.close()
        conn.close()

def insert_or_update_user():
    name = input("Enter name: ")
    phone = input("Enter phone: ")
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute("SELECT 1 FROM PhoneBook WHERE first_name = %s", (name,))
        if cur.fetchone():
            cur.execute("UPDATE PhoneBook SET phone = %s WHERE first_name = %s", (phone, name))
            print("User updated successfully.")
        else:
            cur.execute("INSERT INTO PhoneBook (first_name, phone) VALUES (%s, %s)", (name, phone))
            print("User added successfully.")
        conn.commit()
    except Exception as e:
        print("Error:", e)
    finally:
        cur.close()
        conn.close()

def bulk_insert_users():
    names = input("Enter names (comma separated): ").split(',')
    phones = input("Enter phones (comma separated): ").split(',')
    
    if len(names) != len(phones):
        print("Names and phones count mismatch.")
        return
    
    incorrect_entries = []
    conn = connect()
    cur = conn.cursor()
    try:
        for i in range(len(names)):
            if phones[i].isdigit() and 6 <= len(phones[i]) <= 15:  
                cur.execute("INSERT INTO PhoneBook (first_name, phone) VALUES (%s, %s)", (names[i], phones[i]))
            else:
                incorrect_entries.append(f"{names[i]} ({phones[i]})")
        
        conn.commit()
        if incorrect_entries:
            print(f"Incorrect entries: {', '.join(incorrect_entries)}")
        else:
            print("All users inserted successfully.")
    except Exception as e:
        print("Error:", e)
    finally:
        cur.close()
        conn.close()

def delete_data():
    choice = input("Delete by (1) name or (2) phone? ")
    conn = connect()
    cur = conn.cursor()
    try:
        if choice == '1':
            name = input("Enter name: ")
            cur.execute("DELETE FROM PhoneBook WHERE first_name = %s", (name,))
        elif choice == '2':
            phone = input("Enter phone: ")
            cur.execute("DELETE FROM PhoneBook WHERE phone = %s", (phone,))
        else:
            print("Invalid choice.")
            return
        conn.commit()
        if cur.rowcount > 0:
            print("Data deleted successfully.")
        else:
            print("No matching record found.")
    except Exception as e:
        print("Error:", e)
    finally:
        cur.close()
        conn.close()

def menu():
    while True:
        print("\nPhoneBook Menu:")
        print("1. Insert from CSV")
        print("2. Insert manually")
        print("3. Search by name or pattern")
        print("4. Delete data by name or phone")
        print("5. Get paginated data")
        print("6. Insert or update user")
        print("7. Bulk insert users")
        print("0. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            filename = input("Enter CSV filename (e.g. contacts.csv): ")
            insert_from_csv(filename)
        elif choice == '2':
            insert_manual()

        elif choice == '3':
            search_by_pattern()
        elif choice == '4':
            delete_data()
        elif choice == '5':
            get_paginated_data()
        elif choice == '6':
            insert_or_update_user()
        elif choice == '7':
            bulk_insert_users()
        elif choice == '0':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    menu()
