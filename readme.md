# PyFlask-Basic-Endpoints
### 개관
매번 개발하기 귀찮은 핵심 Endpoint를 구현하여 박아두기 위한 Repository.
기본적으로, Layered Architecture를 택하고 있음.

**[*, 개발 예정인 것들]**
- 로그인*
- 회원가입*
- 글 작성(텍스트 기반)*
## 본문
**[환경]**
- Python Flask
- MySQL Version > 7
- [Python] SQLAlchemy
- [Python] bcrypt
- [Python] pyjwt
### endpoints.py
Presentation Layer.
들어온 요청에서 데이터를 까서 Service Layer에 넘기고,
Service Layer의 Return을 Forwarding하는 것까지가 역할.
### services/
Service Layer.
실질적인 연산, 검증 등을 수행함.
### dao/
Persistence Layer.
데이터 접근 작업을 수행함.