import DBHelper



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    dir_path = 'data/20221121_djtp_sensordata.csv'
    # csv data load as using python
    data = DBHelper.data_load_pandas(dir_path)
    # Insert Data to InfluxDB
    DBHelper.data_insert(data)













