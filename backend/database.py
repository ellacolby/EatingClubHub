import os
import sys
import psycopg2
import dotenv

dotenv.load_dotenv()
DATABASE_URL = os.environ['DATABASE_URL']

def execute(statements, params=[]):
    try:
        with psycopg2.connect(DATABASE_URL) as connection:
            with connection.cursor() as cursor:
                for statement in statements:
                    cursor.execute(statement, params)
                if cursor.rowcount > 1:
                    table = cursor.fetchall()
                    return table
            
    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)

def get_announcements():
    return execute(["SELECT * from announcements"])

def create_announcement(title=None, description=None, image=None):
    execute([
        f"""
            INSERT INTO announcements (title, description, image)
            VALUES ('{title}', '{description}', '{image}')
        """
    ])

def get_clubs():
    return execute(["SELECT * from clubs"])

def create_club(name=None, description=None, image=None, coffee_chat_link=None):
    execute([
        f"""
            INSERT INTO clubs (name, description, image, coffee_chat_link)
            VALUES ('{name}', '{description}', '{image}', '{coffee_chat_link}')
        """
    ])

def get_events():
    return execute(["SELECT * from events"])

def create_event(name=None, location=None, description=None, start_time=None, end_time=None):
    execute([
        f"""
            INSERT INTO events (name, location, description, start_time, end_time)
            VALUES ('{name}', '{location}', '{description}', '{start_time}', '{end_time}')
        """
    ])

def get_users():
    return execute(["SELECT * from users"])

def create_user(name=None, netid=None, profile_pic=None):
    execute([
        f"""
            INSERT INTO events (name, location, description, start_time, end_time)
            VALUES ('{name}', '{netid}', '{profile_pic}')
        """
    ])

def main():
    if len(sys.argv) != 1:
        print('Usage: python ' + sys.argv[0], file=sys.stderr)
        sys.exit(1)

    try:
        with psycopg2.connect(DATABASE_URL) as connection:

            with connection.cursor() as cursor:
                clubs = get_clubs()
                for club in clubs:
                    print(club)

                #-------------------------------------------------------


                # cursor.execute("DROP TABLE IF EXISTS clubs")
                # cursor.execute("CREATE TABLE clubs "
                #     + "(club_id SERIAL PRIMARY KEY, name TEXT, description TEXT, "
                #     + "image TEXT, coffe_chat_link TEXT)")
                # cursor.execute("INSERT INTO clubs (name, description) "
                #     + "VALUES ('Cottage', 'BEST CLUB IN DA STREET')")

                #-------------------------------------------------------

                # cursor.execute("DROP TABLE IF EXISTS users")
                # cursor.execute("CREATE TABLE users "
                #     + "(user_id SERIAL PRIMARY KEY, name TEXT, netid TEXT, profile_pic TEXT,"
                #     + " favorite_clubs INTEGER[],"
                #     + " events INTEGER[],"
                #     + " FOREIGN KEY (favorite_clubs) REFERENCES clubs(id),"
                #     + " FOREIGN KEY (events) REFERENCES events(id))")
                # cursor.execute("INSERT INTO authors (isbn, author) "
                #     + "VALUES ('123','Kernighan')")
                # cursor.execute("INSERT INTO authors (isbn, author) "
                #     + "VALUES ('123','Pike')")
                # cursor.execute("INSERT INTO authors (isbn, author) "
                #     + "VALUES ('234','Kernighan')")
                # cursor.execute("INSERT INTO authors (isbn, author) "
                #     + "VALUES ('234','Ritchie')")
                # cursor.execute("INSERT INTO authors (isbn, author) "
                #     + "VALUES ('345','Sedgewick')")

                #-------------------------------------------------------
                # cursor.execute("ALTER TABLE clubs RENAME COLUMN coffe_chat_link to coffee_chat_link")

                # cursor.execute("DROP TABLE IF EXISTS events")
                # cursor.execute("CREATE TABLE events "
                #     + "(event_id SERIAL PRIMARY KEY, name TEXT, location TEXT, description TEXT, "
                #     + "start_time TEXT, end_time TEXT)")
                # cursor.execute("INSERT INTO customers "
                #     + "(custid, custname, street, zipcode) VALUES "
                #     + "('111','Princeton','114 Nassau St','08540')")
                # cursor.execute("INSERT INTO customers "
                #     + "(custid, custname, street, zipcode) VALUES "
                #     + "('222','Harvard','1256 Mass Ave','02138')")
                # cursor.execute("INSERT INTO customers "
                #     + "(custid, custname, street, zipcode) VALUES "
                #     + "('333','MIT','292 Main St','02142')")

                #-------------------------------------------------------


                # cursor.execute("DROP TABLE IF EXISTS announcements")
                # cursor.execute("CREATE TABLE announcements "
                #     + "(announcement_id SERIAL PRIMARY KEY, title TEXT, description TEXT, image TEXT)")
                # cursor.execute("INSERT INTO zipcodes "
                #     + "(zipcode, city, state) "
                #     + "VALUES ('08540','Princeton', 'NJ')")
                # cursor.execute("INSERT INTO zipcodes "
                #     + "(zipcode, city, state) "
                #     + "VALUES ('02138','Cambridge', 'MA')")
                # cursor.execute("INSERT INTO zipcodes "
                #     + "(zipcode, city, state) "
                #     + "VALUES ('02142','Cambridge', 'MA')")

                #-------------------------------------------------------

    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)

#-----------------------------------------------------------------------

if __name__ == '__main__':
    main()
