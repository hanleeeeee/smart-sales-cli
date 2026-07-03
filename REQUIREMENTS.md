# Smart Sales CLI 요구사항

직접 코딩하지 않고 VS Code의 Cline에 단계별 프롬프트를 입력하여 완성하는 교육용 프로젝트입니다.

## 기술 제약
- Python 3.10 이상
- 외부 프레임워크 없이 Python 표준 라이브러리만 사용
- JSON 파일 저장 방식
- CLI 메뉴 방식
- 기능별 모듈 분리
- unittest 기반 자동 테스트

## 최종 기능
1. 고객사 등록, 목록, 상세 조회, 검색, 수정, 삭제
2. 영업일지 등록, 목록, 수정
3. 영업일지 상신, 승인, 반려, 회수
4. 고객사별 활동 요약
5. 입력값 검증 및 오류 메시지
6. unittest 회귀 테스트

## 추가 과정 기능
7. 고객사 목록 CSV 내보내기

## 데이터 구조

### customers.json
```json
[
  {
    "customer_id": "C001",
    "customer_name": "예시 고객사",
    "manager_name": "홍길동",
    "email": "hong@example.com"
  }
]
```

### sales_reports.json
```json
[
  {
    "report_id": "R001",
    "customer_id": "C001",
    "activity_date": "2026-06-09",
    "content": "제품 소개 미팅",
    "status": "DRAFT"
  }
]
```

## 상태 전이 규칙

| 현재 상태 | action | 변경 상태 |
|---|---|---|
| `DRAFT` | submit | `SUBMITTED` |
| `SUBMITTED` | approve | `APPROVED` |
| `SUBMITTED` | reject | `REJECTED` |
| `SUBMITTED` | withdraw | `DRAFT` |
| 그 외 | - | 차단 |

## 작업 원칙
- 한 번에 한 단계만 구현
- Cline이 계획을 먼저 제시한 뒤 승인 후 수정
- 각 단계가 끝나면 직접 실행 및 테스트
- git status와 git diff로 변경 범위 확인
- 정상 동작할 때만 commit
