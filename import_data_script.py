from psycopg2.errors import UniqueViolation
from psycopg2.extensions import connection as _connection
from psycopg2.extras import execute_batch
import pandas as pd
from data_classes import Departments
from datetime import datetime
from context_manager import conn_context_pg, sb_settings


DAY = {
    'Пн.': 1,
    'Вт.': 2,
    'Ср.': 3,
    'Чт.': 4,
    'Пт.': 5,
    'Сб.': 6,
    'Вск.': 7,
}

def load_data_to_postgre(pg_conn: _connection, data: list) -> None:
    try:
        pg_curs = pg_conn.cursor()
        departments_data = []
        schedule_data = []
        for row in data:
            temp_row_departments = {'id': row.id,
                                    'name': row.name,
                                    'code': row.code,
                                    'type_dep': row.type_dep,
                                    'address': row.address,
                                    'coordinates': row.coordinates,
                                    }
            days = row.days.split(',')
            times = row.times.split(' ')
            if days[0] != '-' and times[0] != 'X':
                if len(times)/len(days) == 2:
                    modified = datetime.now().date()
                    j = 0
                    for i in range(0, len(days)):
                        temp_row_schedule = {
                                'department_id': row.id,
                                'day': DAY[days[i]],
                                'start_work':
                                (int(times[j][0:2])*60)+int(times[j][3:5]),
                                'finish_work':
                                (int(times[j+1][0:2])*60)+int(times[j+1][3:5]),
                                'start_break': None,
                                'finish_break': None,
                                'modified': modified,
                        }
                        j += 2
                else:
                    j = 0
                    for day in days:
                        if '(' in times[j+1]:
                            temp_row_schedule = {
                                'department_id': row.id,
                                'day': DAY[day],
                                'start_work':
                                (int(times[j][0:2])*60)+int(times[j][3:5]),
                                'finish_work':
                                (int(times[j+1][0:2])*60)+int(times[j+1][3:5]),
                                'start_break':
                                ((int(times[j+1][6:8])*60) +
                                 int(times[j+1][9:11])),
                                'finish_break':
                                (int(times[j+2][0:2])*60)+int(times[j+2][3:5]),
                                'modified': modified,
                                }
                            j+3
                        else:
                            temp_row_schedule = {
                                    'department_id': row.id,
                                    'day': DAY[day],
                                    'start_work':
                                    (int(times[j][0:2])*60)+int(times[j][3:5]),
                                    'finish_work':
                                    ((int(times[j+1][0:2])*60) +
                                     int(times[j+1][3:4])),
                                    'start_break': None,
                                    'finish_break': None,
                                    'modified': modified,
                            }
                            j += 2
                schedule_data.append(temp_row_schedule)
            departments_data.append(temp_row_departments)
        departments_querry = '''INSERT INTO content.departments
        (id, name, code, type_dep, address, coordinates)
        VALUES (%(id)s, %(name)s, %(code)s, %(type_dep)s, %(address)s,
        %(coordinates)s)'''
        schedule_querry = '''INSERT INTO content.schedule (department_id, day,
        start_work, finish_work, start_break, finish_break, modified)
        VALUES (%(department_id)s, %(day)s, %(start_work)s, %(finish_work)s,
        %(start_break)s, %(finish_break)s, %(modified)s)'''
        execute_batch(pg_curs, departments_querry, departments_data)
        execute_batch(pg_curs, schedule_querry, schedule_data)
    except UniqueViolation:
        pg_conn.rollback()
    else:
        pg_conn.commit()


def main():
    data = pd.read_excel(
        '01122020.xls', sheet_name='Данные', skiprows=7, usecols='B,D:F,I,M:N')
    data.columns = [
        'code', 'name', 'type_dep', 'address', 'coordinates', 'days', 'times']
    data_from_xls = data[0:735]
    data_to_db = []
    for row in data_from_xls.itertuples():
        data_to_db.append(Departments(*list(row)))
    with conn_context_pg(sb_settings) as pg_conn:
        load_data_to_postgre(pg_conn, data_to_db)


if __name__ == '__main__':
    main()
