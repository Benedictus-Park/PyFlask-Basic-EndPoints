# PyFlask-Basic-Endpoints
## 개관
매번 개발하기 귀찮은 핵심 Endpoint를 구현하여 박아두기 위한 Repository.
기본적으로 Layered Architecture를 택하고 있음.

권한 구분이 필요한 서비스에 접근하려고 할 때 거쳐야 하는 인증 절차는
Decorator 패턴으로 정의해 두었음.
세부사항은 endpoints.py 참조

- 유저 관리
    - 로그인
        - 유저 조회
    - 회원가입
        - 유저 생성
    - 탈퇴
    - 정보 변경
    - 권한 분리(관리자/일반 사용자)
        - 제재 기능
            - 블록
            - 탈퇴 처리
- 텍스트 기반 게시판
    - CRUD
    - 제재 기능
        - 게시물 삭제
- Log(기본 90일 유지)
---
## 본문
**[환경]**
- Python Flask
- [Python] SQLAlchemy
- [Optional] MySQL Version 8
- 기타 Python Package는 requirments.txt 참조