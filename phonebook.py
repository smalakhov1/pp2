import psycopg2
import csv
from config import load_config



#creating a table

def create_table():
    sql="""
        CREATE TABLE IF NOT EXISTS phonebook (
            id         SERIAL PRIMARY KEY,
            first_name VARCHAR(50) NOT NULL,
            phone      VARCHAR(20) UNIQUE NOT NULL
        )
    """
    # SERIAL PRIMARY KEY -> gives uniqe id to every row(ascending from 1 to n of rows)
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor()as cur:
                cur.execute(sql) # cursor executing our sql requst
            conn.commit() # saving changes
            print('Phonebook table is created')
    except (Exception, psycopg2.DatabaseError) as error:
        print(f'Error create_table: {error}')



#inserting from csv

def insert_from_csv(filename = 'contacts.csv'):
    contacts = []
    with open(filename, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            contacts.append((row['first_name'], row['phone']))

        # opening and reading csv file, then with csv.DictReader converting every csv row into list of tuples

        sql = """INSERT INTO phonebook(first_name, phone)
         VALUES(%s, %s)
         ON CONFLICT DO NOTHING"""
        
        # %s is a plaseholder for varibles. we can write this sql requsts with f"string{}" but it will cause sql injection problem(content of the varables will affect the requst itself)

        try:
            config = load_config()
            with psycopg2.connect(**config) as conn:
                with conn.cursor() as cur:
                    cur.executemany(sql, contacts) #executemany -> applying same sql requst for each tuple in the list
                conn.commit()
                print(f"Imported {len(contacts)} contacts from {filename}")
        except(Exception, psycopg2.DatabaseError) as error:
            print(f"Error insert_from_csv: {error}")

#inserting from input

def insert_from_console():
    first_name = input('Name: ').strip() # getting name and number for new contact
    phone = input('Number: ').strip()

    sql = """INSERT INTO phonebook (first_name, phone)
             VALUES (%s, %s) RETURNING id"""
    contact_id = None # we already have id(SERIAL PRIMARY KEY)
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (first_name, phone))  # passing data as a tuple, psycopg2 substitutes first_name for the first %s and phone number for the second %s.
                row = cur.fetchone() # method that taking ine row from the requests result
                if row:
                    contact_id = row[0] # id of inserted row
            conn.commit()
            print(f"Added contact with id= {contact_id}: {first_name} {phone}")
    
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error insert_from_console: {error}")
    finally:
        return contact_id
    
#search

def search_contacts():
    query = input("Enter a name or the beginning of a phone number: ").strip()

    sql = """SELECT * FROM phonebook
            WHERE first_name ILIKE %s OR phone LIKE %s""" # ILIKE will find rows name regarding the register(Алибек, АЛИБЕК, алибек and so on)
    
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (f"%{query}%", f"{query}%"))
                rows = cur.fetchall() # fetchall() — fetches all found rows. Returns a list of tuples:

                if rows:
                    print(f"\nFound {len(rows)}: ")
                    for row in rows:
                        print(f" {row[0]}. {row[1]}] - {row[2]}")  
                        # id first_name phone
                else:
                    print("Nothing found")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error search_contacts: {error}")


#updating

def update_contact():
    name = input('Enter contact name to update: ').strip()
    print('What to update?')
    print('  1. Phone')
    print('  2. Name')
    choice = input('Choose: ').strip()

    if choice == '1':
        new_value = input('New phone: ').strip()
        sql = "UPDATE phonebook SET phone = %s WHERE first_name = %s"
    elif choice == '2':
        new_value = input('New name: ').strip()
        sql = "UPDATE phonebook SET first_name = %s WHERE first_name = %s"
    else:
        print('Invalid choice')
        return

    updated_count = 0
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (new_value, name))
                updated_count = cur.rowcount
            conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(f'Error: {error}')
    finally:
        if updated_count == 0:
            print('Contact not found')
        else:
            print(f'Updated: {updated_count} row(s)')
        return updated_count
    

# deleting

def delete_contact():
    print('Delete by:')
    print('1. Name')
    print('2. Number')
    choice = input('Choice: ').strip()

    if choice == '1':
        value = input('Enter name: ').strip()
        sql = "DELETE FROM phonebook WHERE first_name = %s"
    elif choice == '2':
        value = input('Enter number: ').strip()
        sql = "DELETE FROM phonebook WHERE phone = %s"
    else:
        print('Incorrect input')
        return

    deleted_count = 0
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (value,))  # (value,) - tuple with one element
                deleted_count = cur.rowcount
            conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(f'Error delete_contact: {error}')
    finally:
        if deleted_count == 0:
            print('Contact not found')
        else:
            print(f'Deleted: {deleted_count} contacts')
        return deleted_count
    
#MAIN MENU

def main():
    create_table()

    while True:
        print('\n========= PhoneBook =========')
        print('1. Import from CSV')
        print('2. Add contact')
        print('3. Search contacts')
        print('4. Update contact')
        print('5. Delete contact')
        print('0. Exit')
        print('==============================')

        choice = input('Choose action: ').strip()

        if   choice == '1': insert_from_csv()
        elif choice == '2': insert_from_console()
        elif choice == '3': search_contacts()
        elif choice == '4': update_contact()
        elif choice == '5': delete_contact()
        elif choice == '0':
            print('bye')
            break
        else:
            print('Invalid choice, try again')

if __name__ == '__main__':
    main()