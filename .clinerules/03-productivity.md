# 추가 과정 생산성 규칙

## 적용 시점
- 이 규칙은 3시간 추가 과정에서 사용한다.
- 기본 과정의 `01-workflow.md`, `02-quality.md` 규칙을 함께 유지한다.

## 1. Plan 우선
- 구현 전에 완료 조건과 테스트 케이스 초안을 먼저 제시한다.
- 작업 범위가 크면 함수 단위나 파일 단위로 더 작게 나눈다.
- 한 task에서 수정할 파일이 4개를 초과하거나 서로 다른 기능이 함께 포함되면 작업을 더 작게 분리한다.

## 2. Task 분리
- 기능 하나가 끝나면 새 task에서 다음 기능을 시작한다.
- 새 task를 시작하기 전에 현재 상태와 다음 작업을 Markdown 인수인계 메모로 요약한다.

### Task 인수인계 메모 형식
```markdown
# Task 인수인계 메모

## 완료한 기능
- 

## 생성하거나 수정한 파일
- 

## 테스트 명령과 결과
- 

## 남아 있는 문제
- 

## 다음 task에서 수행할 작업
- 

## 유지해야 할 JSON 필드와 상태값
- 
```

## 3. 안전한 자동화
- 읽기, 검색, 테스트처럼 반복적이고 되돌리기 쉬운 작업만 선택적으로 자동 승인할 수 있다.
- 파일 대량 수정, 패키지 설치, 삭제, Git 상태 변경은 자동 승인하지 않는다.

### 선택적 Auto Approve 가능 예시
- 파일 읽기
- 코드 검색
- `git status`
- `git status --short`
- `git diff`
- `git diff --stat`
- `git branch --show-current`
- `python -m unittest discover -s tests -v`

### Auto Approve 금지 예시
- `git add`
- `git commit`
- `git push`
- `git pull`
- `git merge`
- `git reset`
- `git restore`
- `git clean`
- `pip install`
- 파일 삭제
- 대량 파일 수정

## 4. 품질 유지
- 빠르게 작업하더라도 전체 unittest와 Git diff 검토를 생략하지 않는다.
- 품질 점검은 넓게 수행하되 수정은 한 번에 하나의 문제만 처리한다.
- Auto Approve를 사용하더라도 commit 전에는 반드시 사람이 `git diff --staged`를 확인한다.
