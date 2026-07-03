# 03. 고객사 검색 구현

```text
Smart Sales CLI에 고객사 검색 기능을 추가해줘.

[작업 branch]
- ai/customer-search

[변경 허용 범위]
- customer_service.py
- app.py
- tests/test_customer_service.py

[완료 조건]
- 고객사명, 담당자명, 이메일에 검색어가 포함되면 조회
- 검색은 대소문자를 구분하지 않음
- 빈 문자열과 공백만 입력한 검색어는 빈 목록 반환
- 기존 고객사 CRUD 기능 유지
- 관련 unittest 추가

[금지 사항]
- 기존 JSON 필드명을 변경하지 마.
- 검색 기능과 관련 없는 리팩터링을 하지 마.

먼저 현재 branch, 변경 계획, 수정 대상 함수, 추가할 테스트를 설명하고 승인을 기다려줘.
```
