from database_connection import getDatabaseConnection


def main():
    cursor = getDatabaseConnection()

    # create companies table
    cursor.execute("""
        CREATE TABLE COMPANY(
            id SERIAL PRIMARY KEY NOT NULL,
            registration_code INT NOT NULL,
            name VARCHAR(100) NOT NULL,
            total_capital INT NOT NULL,
            date_established DATE NOT NULL
            )
        """)

    # create persons table
    cursor.execute("""
        CREATE TABLE PERSON(
            id SERIAL PRIMARY KEY NOT NULL,
            identification_number BIGINT NOT NULL,
            name VARCHAR(100) NOT NULL,
            lastname VARCHAR(100) NOT NULL
            )
        """)
    
    # create shares table
    cursor.execute("""
        CREATE TABLE SHARE(
            id SERIAL PRIMARY KEY NOT NULL,
            company_id INT NOT NULL,
            person_id INT NOT NULL,
            share_size INT NOT NULL,
            is_founder BOOLEAN NOT NULL
            )
        """)
    cursor.close()
    
    return
if __name__ == '__main__':
    main()
