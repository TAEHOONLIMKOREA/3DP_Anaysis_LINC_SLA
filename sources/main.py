import csv
import pandas as pd
import datetime
from influxdb import InfluxDBClient


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # 판다스로 읽기
    # df = pd.read_csv('data/20221121_djtp_sensordata.csv')
    # print(df)
    # row_1 = df.iloc[0]
    # print(row_1[0] + 'T' + row_1[7] + 'Z')

    # 파일로 읽어드리기 => 첫행 출력할 땐 빠르다.
    f = open('data/20221121_djtp_sensordata.csv', 'r')
    csvreader = csv.reader(f)

    columns = next(csvreader)
    fist_value = next(csvreader)
    # measurement = fist_value[0]+fist_value[7]+fist_value[1]
    measurement = fist_value[1]


    client = InfluxDBClient(host="localhost", port=8086)
    dbname = 'lincsolution'

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













