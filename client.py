import psycopg2



if __name__ == '__main__':

    conn = psycopg2.connect(
        dbname="test_db",
        user="admin",
        password="admin",
        host="0.0.0.0",
        port="5432"
    )

    cur = conn.cursor()

    cur.execute("SELECT 1")
    #cur.execute("SELECT * from sdgdg")

    cur.execute("""DO $$
    BEGIN
    RAISE EXCEPTION 'Print the message of exception %', now();
    END $$;
    """)
    rows = cur.fetchall()
    for row in rows:
        print(row)

    cur.close()
    conn.close()