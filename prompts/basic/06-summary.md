# 06. 고객 활동 요약 구현

```text
Smart Sales CLI에 고객사별 영업활동 요약 기능을 추가해줘.

[작업 branch]
- ai/summary

[변경 허용 범위]
- summary_service.py
- app.py
- tests/test_summary_service.py

[완료 조건]
- 고객사별 전체 영업일지 수 출력
- 상태별 영업일지 개수 출력
- 최근 활동일은 activity_date 기준으로 계산
- 영업일지가 없는 고객사도 조회 가능
- 영업일지가 없는 경우 최근 활동일은 "-"로 출력
- 관련 unittest 추가

[금지 사항]
- 기존 JSON 필드명을 변경하지 마.
- 기존 고객사 관리, 검색, 영업일지, 결재 기능을 변경하지 마.
- 요약 결과 저장을 위한 새로운 JSON 파일을 만들지 마.

먼저 현재 branch, 변경 계획, 요약 계산 방식, 추가할 테스트를 설명하고 승인을 기다려줘.
```
