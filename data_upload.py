import os
import django
import csv
import sys

# 일반 파이썬앱(스크립트)에서 django ORM을 사용하려면 다음의 설정 필요
# django 환경설정 파일 지정
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "doit_django_prj.settings")
# django settings 메모리 로딩 적용
django.setup()

# Foods 클래스와 연결된 테이블에 data를 업로딩 하기위해 import함
from food_sales.models import Foods

# csv 파일 위치 변수로 정의
CSV_PATH = './datas/food_sales.csv'

with open(CSV_PATH, 'r',  encoding='utf-8') as file:
  data_rows = csv.reader(file, skipinitialspace=True)
  # header(첫번째 줄) 제외
  next(data_rows, None)

  # 공백라인을 제거하기 위해서
  data_rows = list(data_rows)
  # print("전 ", data_rows)
  data_rows = list(filter(None, data_rows))
  print("후 ", data_rows)

  # DB 테이블에 한 레코드씩 입력하기
  for row in data_rows:
    # print(row[0])
    if row[0] != None or row[0] != '':
      # 무조건 upload, 중복 데이터 발생가능
      # Foods.objects.create(
      # cook_name = row[0],
      # count = row[1],
      # unit_price = row[2],
      # )

      # 중복회피, 업로딩
      # filter로 중복을 체크하고, 있다면 update/ 없다면 create해줌
      # 두가지 파라미터가 쓰임
      Foods.objects.update_or_create(
        # filter : 중복을 체크할 값
        cook_name = row[0],

        # cook_name : Foods 클래스의 속성 => 연결된 테이블의 cook_name 속성
        # cook_name과 하나의 menu_name 값과 비교함, 값이 있는지 없는지 체크하는 역할

        # 새로 create할 value : filter한 결과에 의해 중복값이 없을 때
        defaults={
            'cook_name' : row[0],
            'count' : row[1],
            'unit_price' : row[2],
        
        }
      )