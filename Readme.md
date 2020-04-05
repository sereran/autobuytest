## 환경
```
$ python -V 
3.7.7
```

## 의존성 설치
크롬 driver : https://chromedriver.storage.googleapis.com/index.html?path=80.0.3987.106/
<br>
각 버전에 맞게 설치 필요
<br><br>
잠자기 방지 활성화 (어댑터 연결 시에만) 
```
sudo pmset -c disablesleep 1
```
잠자기 방지 활성 해제 (어댑터 연결 시에만)
```
sudo pmset -c disablesleep 0
```
```
$ pip install --upgrade pip
$ python -m pip install selenium
$ python -m pip install bs4
```

## 실행
- 쿠팡 계정
```
$ python autobuy_coupang.py '${id}' '${pw}'
```
- 신세계몰 카카오톡 로그인 연동된 카카오 계정
```
$ python autobuy_emart.py '${id}' '${pw}'
```
- emart - 신세계몰 계정
```
$ python autobuy_ssg.py '${id}' '${pw}'
```