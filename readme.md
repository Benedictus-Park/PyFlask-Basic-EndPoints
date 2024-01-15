# PyFlask-Basic-Endpoints
## 개관
매번 개발하기 귀찮은 핵심 Endpoint를 구현하여 박아두기 위한 Repository.
기본적으로 Layered Architecture를 택하고 있음.

권한 구분이 필요한 서비스에 접근하려고 할 때 거쳐야 하는 인증 절차는
Decorator 패턴으로 정의해 두었음.
세부사항은 endpoints.py 참조

**[*, 개발 예정인 것들]**
- 로그인*
- 회원가입*
- 글 작성(텍스트 기반)*
---
## 본문
**[환경]**
- Python Flask
- [Python] SQLAlchemy
- [Python] bcrypt
- [Python] pyjwt
- [Optional] MySQL Version 8
## endpoints.py
Presentation Layer.
들어온 요청에서 데이터를 까서 Service Layer에 넘기고,
Service Layer의 Return을 Forwarding하는 것까지가 역할.
- def registration()
### services/
Service Layer.
실질적인 연산, 검증 등을 수행함.
### dao/
Persistence Layer.
데이터 접근 작업을 수행함.