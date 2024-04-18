
def get_url_from_base_urls(connect, data):
    with connect.cursor() as cursor:
        cursor.execute(
            f"""SELECT *
                FROM urls
                WHERE name = '{data}'"""
        )
        return cursor.fetchone()


def get_id_url_from_base_urls(connect, data):
    with connect.cursor() as cursor:
        cursor.execute(
            f"""SELECT id
                FROM urls
                WHERE name = '{data}'"""
        )
        return cursor.fetchone()

def get_data_url_from_base_by_id(connect, id):
    with connect.cursor() as cursor:
        cursor.execute(
            f"""SELECT *
                FROM urls
                WHERE id = '{id}'"""
        )
        return cursor.fetchone()


def write_data_to_base_urls(connect, data):
    with connect.cursor() as cursor:
        if not get_url_from_base_urls(connect, data):
            cursor.execute(
                "INSERT INTO urls (name) VALUES (%s)",
                [data]
            )
            connect.commit()
        return get_id_url_from_base_urls(connect, data)



def get_all_urls_from_base_ulrs(connect):
    with connect.cursor() as cursor:
        cursor.execute("""SELECT *
                          FROM urls
                          ORDER BY id DESC""")
        return cursor.fetchall()