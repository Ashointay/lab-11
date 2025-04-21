import psycopg2
import csv


def connect():
    return psycopg2.connect(
        dbname="phonebook",
        user="postgres",
        password="Zhasminchik6",
        host="localhost",
        port="5432",
    )

def insert_from_csv(filename):
    conn = connect()
    cur = conn.cursor()
    try:
        with open(filename, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                cur.execute(
                    "INSERT INTO PhoneBook (first_name, phone) VALUES (%s, %s)",
                    (row["first_name"], row["phone"]),
                )
        conn.commit()
        print("CSV data inserted successfully.")
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
        cur.execute("CALL insert_or_update_user(%s, %s)", (name, phone))
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
        cur.execute("SELECT * FROM search_contacts(%s)", (pattern,))
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
        cur.execute("SELECT * FROM get_contacts_paginated(%s,%s)", (limit, offset))
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


def delete_data():
    conn = connect()
    cur = conn.cursor()
    try:
        name = input("Enter name to delete (or leave blank): ")
        phone = input("Enter phone to delete (or leave blank): ")
        cur.execute("CALL delete_user(%s, %s)", (
            name if name else None,
            phone if phone else None
        ))
        conn.commit()
        print("Data deleted successfully.")
    except Exception as e:
        print("Error:", e)
    finally:
        cur.close()
        conn.close()

def menu():
    while True:
        print("\nPhoneBook Menu:")
        print("1. Insert from CSV")
        print("2. Insert or update user")
        print("3. Search by name or pattern")
        print("4. Delete data by name or phone")
        print("5. Get paginated data")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            filename = input("Enter CSV filename (e.g. contacts.csv): ")
            insert_from_csv(filename)
        elif choice == "2":
            insert_or_update_user()
        elif choice == "3":
            search_by_pattern()
        elif choice == "4":
            delete_data()
        elif choice == "5":
            get_paginated_data()
        elif choice == "0":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    menu()
