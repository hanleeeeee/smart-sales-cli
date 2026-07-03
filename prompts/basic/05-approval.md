# 05. 결재 흐름 구현

```text
Smart Sales CLI에 영업일지 결재 흐름을 추가해줘.

[작업 branch]
- ai/approval

[변경 허용 범위]
- approval_service.py
- app.py
- tests/test_approval_service.py

[구조 원칙]
- approval_service.py는 영업일지 상태 전이 규칙을 담당해줘.
- 데이터 읽기와 저장은 기존 storage.py의 공개 함수를 재사용해줘.
- app.py에는 메뉴 연결만 추가해줘.
- sales_report_service.py 수정이 필요하면 먼저 이유를 설명하고 추가 승인을 기다려줘.

[상태 전이 규칙]
- DRAFT 상태에서 submit 실행 → SUBMITTED
- SUBMITTED 상태에서 approve 실행 → APPROVED
- SUBMITTED 상태에서 reject 실행 → REJECTED
- SUBMITTED 상태에서 withdraw 실행 → DRAFT
- 그 외 상태 전이는 모두 차단
- APPROVED 상태의 영업일지는 수정 불가

[완료 조건]
- 허용되지 않은 상태 전이는 오류 메시지를 출력
- 기존 영업일지 등록, 조회, 수정 기능 유지
- 정상 전이와 잘못된 전이를 검증하는 unittest 추가

[금지 사항]
- 기존 JSON 필드명을 변경하지 마.
- 새로운 상태값을 임의로 추가하지 마.
- 상태 전이와 관련 없는 리팩터링을 하지 마.

먼저 현재 branch, 변경 계획, 상태 전이 구현 방식, 추가할 테스트를 설명하고 승인을 기다려줘.
```
