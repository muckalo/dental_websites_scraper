import psycopg2

from app.config.config import DB_PARAMS


""" PSQL """
params = DB_PARAMS


def create_tables(commands):
    """ CREATE DB IF NOT EXISTS """
    create_db()

    """ create tables in the PostgreSQL database"""
    conn = None
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        if isinstance(commands, str):
            # create only one table
            cur.execute(commands)
        elif isinstance(commands, tuple):
            # create table one by one
            for command in commands:
                cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        pass
    finally:
        if conn is not None:
            conn.close()


def create_db():
    db_name = params["database"]
    del params["database"]
    conn = None
    try:
        conn = psycopg2.connect(**params)
        conn.autocommit = True
        cur = conn.cursor()

        sql_check_db = """SELECT datname FROM pg_catalog.pg_database WHERE datname = '{}'""".format(db_name)
        cur.execute(sql_check_db)

        db_exists = cur.fetchone()
        if not db_exists:
            cur.execute('CREATE DATABASE {};'.format(db_name))
        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        pass
    finally:
        if conn is not None:
            conn.close()
    params["database"] = db_name


def update_data_into_psql(table_name, data, where_col, where_val):
    try:
        columns = ["{}".format(i) for i in data.keys()]
        values = ["{}".format(i) if isinstance(i, psycopg2.Binary) else "'{}'".format(i) for i in data.values()]
        update_sql = ', '.join('{} = {}'.format(c, v) for c, v in zip(columns, values))
        sql = """UPDATE public.{} SET {} WHERE {} = '{}';""".format(table_name, update_sql, where_col, where_val)
        row = query_data_from_psql(sql, row_count=True)
        return row
    except Exception as e:
        return None


def insert_data_into_psql(table_name, data, return_field_name=None):
    try:
        columns = ', '.join(["{}".format(i) for i in data.keys()])
        values = ', '.join(["{}".format(i) if isinstance(i, psycopg2.Binary) else "'{}'".format(i) for i in data.values()])
        if return_field_name:
            sql = """INSERT INTO {} ({}) VALUES ({}) RETURNING {};""".format(table_name, columns, values, return_field_name)
        else:
            sql = """INSERT INTO {} ({}) VALUES ({});""".format(table_name, columns, values)
        row = query_data_from_psql(sql, fetch_one=True)
        return row
    except Exception as e:
        return None


def insert_all_data_at_once_into_psql(data, table_name, one_col=False):
    try:
        columns = ', '.join(["{}".format(i) for i in data[0].keys()])
        t3 = ', '.join([
            str(tuple(['{}'.format(i.replace("'", '"')) if "'" in i else '{}'.format(i) for i in data[i_data].values()]))
            for i_data in range(len(data))
        ])
        if one_col:
            t3 = t3.replace("',", "'")
        sql = """INSERT INTO {table_name} ({columns}) VALUES {values}""".format(
            table_name=table_name, columns=columns, values=t3
        )
        insert_status = query_data_from_psql(sql, row_count=True)
        return insert_status
    except Exception as e:
        return None


def query_data_from_psql(sql, fetch_one=False, fetch_all=False, row_count=False):
    conn = None
    rows = None
    try:
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the sql statement
        cur.execute(sql)

        if fetch_one:
            rows = cur.fetchone()
        elif fetch_all:
            rows = cur.fetchall()
        elif row_count:
            rows = cur.rowcount
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        pass
    finally:
        if conn is not None:
            conn.close()
    return rows


def check_does_date_exist(table_name):
    # SELECT id,value,card FROM my_table ORDER BY id DESC LIMIT 1;
    sql = """SELECT * FROM {table_name} ORDER BY jobs_date DESC LIMIT 1;""".format(table_name=table_name)
    # print('sql: {}'.format(sql))
    try:
        query_result = query_data_from_psql(sql, fetch_all=True)
        # print('query_result: {}'.format(query_result))
        query_result_formatted = [
            {
                'jobs_date': query_result[i][0],
                'started': query_result[i][1],
                'finished': query_result[i][2],
                'last_restart': query_result[i][3]
            }
            for i in range(len(query_result))
        ]
        return query_result_formatted[0]
    except Exception as e:
        print('Exception(prepare_data_for_queue): {}'.format(e))
        return None
