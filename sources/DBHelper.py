import pandas as pd
import csv
from influxdb import DataFrameClient
import datetime
from influxdb import InfluxDBClient


host = 'keties.iptime.org'
port = 55586
user = 'honeyb'
passwd = '12345'
protocol = 'line'
dbname = 'HBNU_CMET ATOMm-4000'
measurement = '20221121_0047'


def data_load_pandas(file_path):
    df = pd.read_csv(file_path, sep=',')
    df['REG_TIME'] = df['REG_DATE'] + ' ' + df['REG_TIME']
    df['REG_TIME'] = pd.to_datetime(df['REG_TIME'], format='%Y-%m-%d %H:%M:%S')
    # 필요 없는 열 삭제
    df = df.drop(['REG_DATE', 'NICKNAME', 'SENSOR_TYPE', 'MIN_VALUE', 'MAX_VALUE'], axis =1)
    # 열 순서 재배치
    df = df.reindex(columns=['REG_TIME', 'NAME', 'VALUE'])
    # 데이터 길이가 긴 형식 => 넓은 형식 변환
    df = pd.pivot_table(df, index='REG_TIME', columns='NAME', values='VALUE', fill_value = 0)
    df = df.reset_index()
    # 'REG_TIME'을 데이터프레임 인덱스로 지정
    df.set_index('REG_TIME', inplace=True)
    df.to_csv('data/Processed_lincData.csv')
    print(df)

    return df

def data_insert(data):
    client = DataFrameClient(host, port, user, passwd, dbname)
    # check database list
    list_db = client.get_list_database()
    ret = next((item for item in list_db if item['name'] == dbname), None)
    if ret is None:
        client.create_database(dbname)
    # Write data to measurement of 'HBNU_CMET ATOMm-4000' database.
    client.write_points(data, measurement, protocol=protocol)


def data_load_csv(file_path):
    # 파일로 읽어드리기 => 첫행 출력할 땐 빠르다.
    f = open(file_path, 'r')
    csvreader = csv.reader(f)

    columns = next(csvreader)
    fist_value = next(csvreader)
    # measurement = fist_value[0]+fist_value[7]+fist_value[1]
    measurement = '220928_221121_' + fist_value[7]
    host = 'keties.iptime.org'
    port = 55586

    client = InfluxDBClient(host=host, port=port)
    dbname = '220928_221121_SLA_Link'

    print("Create database: " + dbname)
    client.drop_database(dbname)
    client.create_database(dbname)

    # create data
    data = []
    for line in csvreader:
        time_str = line[0] + ' ' + line[7]
        format_ = '%Y-%m-%d %H:%M:%S'
        timestamp = datetime.datetime.strptime(time_str, format_)
        _min = float(line[4])
        _max = float(line[5])
        _value = float(line[6])

        point = [
            {
                'measurement': measurement,
                'tags': {
                    'MachineName': line[1],
                    'ParamName': line[2],
                    'SensorType': line[3]
                },
                'fields': {
                    'Min': _min,
                    'Max': _max,
                    'Value': _value
                },
                'time': timestamp
            }
        ]
        print("Write points: {0}".format(point))
        client.write_points(point, database=dbname)