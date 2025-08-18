import duckdb

def main():
    conn = duckdb.connect('database.db')
    try:
        result = conn.execute("SELECT * FROM users").fetchall()
        print("Users in database:")
        for row in result:
            print(row)
    finally:
        conn.close()

if __name__ == "__main__":
    main()
