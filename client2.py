import psycopg2



if __name__ == '__main__':

    conn = psycopg2.connect(
        dbname="test_db",
        user="admin",
        password="admin",
        host="0.0.0.0",
        port="5435"
    )

    cur = conn.cursor()

    # cur.execute("""CREATE TABLE my_table2 (
    # name VARCHAR(100),
    # age INTEGER
    # );
    # """)
    
    # cur.execute("""INSERT INTO my_table2 (name, age)
    # VALUES (%s, %s)
    # """, ("antonydfgdffsdfsdfsdfsd", 234))
    cur.execute("""SELECT 1""")
    cur.execute("""SELECT * from my_table2""")

    #cur.execute("""SELECT * FROM table_doesnt_exist""")
    rows = cur.fetchall()
    for row in rows:
        print(row)

    cur.close()
    conn.close()

