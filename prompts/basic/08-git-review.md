# 08. Git 변경 검토 요청

```text
현재 Git 변경 상태를 검토해줘.

[허용하는 읽기 전용 명령]
- git branch --show-current
- git status --short
- git diff --stat
- git diff
- git diff --staged

[금지 사항]
- 파일을 생성하거나 수정하지 마.
- git add, git commit, git push를 실행하지 마.
- branch를 생성, 삭제, 전환하지 마.
- git restore, git reset, git clean을 실행하지 마.

[검토 항목]
1. 현재 branch가 ai/* 작업 branch인지 확인
2. 요청하지 않은 파일 변경 여부
3. untracked 파일 포함 여부
4. JSON 스키마 변경 여부
5. 기존 기능 훼손 가능성
6. 불필요한 리팩터링 여부
7. 보안 정보 포함 가능성
8. 권장 commit 단위

코드는 수정하지 말고 위험 요소와 권장 조치만 정리해줘.
```
