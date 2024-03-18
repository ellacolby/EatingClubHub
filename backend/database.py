import os
import sys
import psycopg2
import dotenv

dotenv.load_dotenv()
DATABASE_URL = os.environ['DATABASE_URL']

#-----------------------------------------------------------------------

def main():

    if len(sys.argv) != 1:
        print('Usage: python ' + sys.argv[0], file=sys.stderr)
        sys.exit(1)

    try:
        with psycopg2.connect(DATABASE_URL) as connection:

            with connection.cursor() as cursor:

                #-------------------------------------------------------

                cursor.execute("DROP TABLE IF EXISTS books")
                cursor.execute("CREATE TABLE books "
                    + "(isbn TEXT, title TEXT, quantity INTEGER)")
                cursor.execute("INSERT INTO books "
                    + "(isbn, title, quantity) "
                    + "VALUES ('123',"
                    + "'The Practice of Programming',500)")
                cursor.execute("INSERT INTO books "
                    + "(isbn, title, quantity) "
                    + "VALUES ('234',"
                    + "'The C Programming Language',800)")
                cursor.execute("INSERT INTO books "
                    + "(isbn, title, quantity) "
                    + "VALUES ('345',"
                    + "'Algorithms in C',650)")

                #-------------------------------------------------------

                cursor.execute("DROP TABLE IF EXISTS authors")
                cursor.execute("CREATE TABLE authors "
                    + "(isbn TEXT, author TEXT)")
                cursor.execute("INSERT INTO authors (isbn, author) "
                    + "VALUES ('123','Kernighan')")
                cursor.execute("INSERT INTO authors (isbn, author) "
                    + "VALUES ('123','Pike')")
                cursor.execute("INSERT INTO authors (isbn, author) "
                    + "VALUES ('234','Kernighan')")
                cursor.execute("INSERT INTO authors (isbn, author) "
                    + "VALUES ('234','Ritchie')")
                cursor.execute("INSERT INTO authors (isbn, author) "
                    + "VALUES ('345','Sedgewick')")

                #-------------------------------------------------------

                cursor.execute("DROP TABLE IF EXISTS customers")
                cursor.execute("CREATE TABLE customers "
                    + "(custid TEXT, custname TEXT, street TEXT, "
                    + "zipcode TEXT)")
                cursor.execute("INSERT INTO customers "
                    + "(custid, custname, street, zipcode) VALUES "
                    + "('111','Princeton','114 Nassau St','08540')")
                cursor.execute("INSERT INTO customers "
                    + "(custid, custname, street, zipcode) VALUES "
                    + "('222','Harvard','1256 Mass Ave','02138')")
                cursor.execute("INSERT INTO customers "
                    + "(custid, custname, street, zipcode) VALUES "
                    + "('333','MIT','292 Main St','02142')")

                #-------------------------------------------------------

                cursor.execute("DROP TABLE IF EXISTS zipcodes")
                cursor.execute("CREATE TABLE zipcodes "
                    + "(zipcode TEXT, city TEXT, state TEXT)")
                cursor.execute("INSERT INTO zipcodes "
                    + "(zipcode, city, state) "
                    + "VALUES ('08540','Princeton', 'NJ')")
                cursor.execute("INSERT INTO zipcodes "
                    + "(zipcode, city, state) "
                    + "VALUES ('02138','Cambridge', 'MA')")
                cursor.execute("INSERT INTO zipcodes "
                    + "(zipcode, city, state) "
                    + "VALUES ('02142','Cambridge', 'MA')")

                #-------------------------------------------------------

                cursor.execute("DROP TABLE IF EXISTS orders")
                cursor.execute("CREATE TABLE orders "
                    + "(isbn TEXT, custid TEXT, quantity INTEGER)")
                cursor.execute("INSERT INTO orders (isbn, custid, "
                    + "quantity) "
                    + "VALUES ('123','222',20)")
                cursor.execute("INSERT INTO orders (isbn, custid, "
                    + "quantity) "
                    + "VALUES ('345','222',100)")
                cursor.execute("INSERT INTO orders (isbn, custid, "
                    + "quantity) "
                    + "VALUES ('123','111',30)")
                                
                #-------------------------------------------------------

    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)

#-----------------------------------------------------------------------

if __name__ == '__main__':
    main()
