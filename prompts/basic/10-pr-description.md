# 10. Pull Request 설명 작성

```text
현재 Git 변경 내용을 기준으로 Pull Request 설명 초안을 작성해줘.

[허용하는 읽기 전용 명령]
- git status --short
- git diff --stat main..HEAD
- git diff main..HEAD
- git log --oneline main..HEAD

[금지 사항]
- 파일과 Git 상태를 수정하지 마.
- git add, git commit, git push, git merge를 실행하지 마.

[포함 항목]
1. 변경 목적
2. 수정 파일
3. 핵심 변경 내용
4. 테스트 명령과 결과
5. 리뷰어가 확인할 부분
6. 남아 있는 제한 사항

PR 설명만 작성해줘.
```
