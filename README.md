# 3DP_Data_Lincsolution_InfluxDB

![image](https://user-images.githubusercontent.com/87262811/214532433-106480a1-bb87-43b2-bfa9-78f08b46cf20.png)

## 위처럼 되어 있던 원본 데이터를 Pandas를 이용하여 불필요 데이터는 지우고 row값을 column의 인덱스로 변경하는 전처리작업 진행

### 모든 row에 같은 값이 들어가 있는 장비네임을 DB명으로 변경 ( DB명 : LINCSOLUTION_CMET_ATOMm-4000 )
### 불필요 데이터 삭제 ( MIN_VALUE, MAX_VALUE, SENSOR_TYPE )
#### Min,Max 값도 이미 정해져 있는 값이라 메타데이터로 정의해두면 데이터 크기를 감소시킬 수 있음
#### SENSOR_TYPE도 이미 이름에 나와 있고 TAG keys로 정의해 두고 사용하기에 크게 도움이 안되기에 삭제 후 데이터 크기를 감소하는 방향으로 진행

### pandas의 pivot_table()함수를 이용하여 전처리 하였음.

![image](https://user-images.githubusercontent.com/87262811/214532490-036b61c6-36fe-484e-b909-0360130870f9.png)


## 결과 : 데이터 크기 약 10배 정도 감소 하였고 DB Name과 Measurement 구조도 알아보기 편리해졌음.
![image](https://user-images.githubusercontent.com/87262811/214534024-28d1b91d-b26b-4240-8f20-10da5f9af43a.png)


## InfluxDB에 저장된 데이터를 Grafana로 시각화한 화면
![image](https://user-images.githubusercontent.com/87262811/214534321-95e3a29c-db3d-4001-a7e1-59cb0fa15b86.png)
