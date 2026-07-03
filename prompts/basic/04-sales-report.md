# 04. 영업일지 구현

```text
Smart Sales CLI에 영업일지 기능을 추가해줘.

[작업 branch]
- ai/sales-report

[변경 허용 범위]
- sales_report_service.py
- app.py
- tests/test_sales_report_service.py

[완료 조건]
- 영업일지 등록
- 영업일지 목록 조회
- 영업일지 수정
- 등록된 고객사에 대해서만 영업일지 작성 가능
- 신규 영업일지는 DRAFT 상태로 저장
- 상태가 APPROVED인 영업일지는 수정 차단
- 관련 unittest 추가

[금지 사항]
- submit, approve, reject, withdraw 기능은 아직 구현하지 마.
- 기존 JSON 필드명을 변경하지 마.
- customer_service.py는 수정하지 마.
- 관련 없는 리팩터링을 하지 마.

먼저 현재 branch, 변경 계획, 생성하거나 수정할 파일, 추가할 테스트를 설명하고 승인을 기다려줘.
```
