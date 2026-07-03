# 16. 종합 미니 실습: 고객사 CSV 내보내기

```text
Smart Sales CLI에 고객사 목록 CSV 내보내기 기능을 추가해줘.

[작업 branch]
- ai/customer-csv-export

[변경 허용 범위]
- customer_export_service.py
- app.py
- tests/test_customer_export_service.py

[완료 조건]
- Python 표준 라이브러리 csv 모듈 사용
- 고객사 목록을 exports/customers.csv 파일로 저장
- exports 폴더가 없으면 생성
- 고객 데이터가 없을 때도 헤더가 포함된 CSV 생성
- 기존 고객사 관리 기능 유지
- 관련 unittest 추가

[금지 사항]
- 외부 패키지를 설치하지 마.
- 기존 JSON 필드명을 변경하지 마.
- customer_service.py는 수정하지 마.
- 관련 없는 리팩터링을 하지 마.

먼저 현재 branch, 변경 계획, CSV 컬럼, 테스트 항목을 설명하고 승인을 기다려줘.
```
