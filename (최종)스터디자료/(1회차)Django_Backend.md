# Django 백엔드 스터디 1회차 문제

**2025-08-02**  
**작성자: 김호중**

---

## 컴퓨터공학 – 서술형 (문제당 3점)

### 1. TCP와 UDP에 대해서 설명하시오

> **TCP (Transmission Control Protocol)**
> - 연결 지향적 프로토콜로, 데이터 전송 전 3-way handshake를 통해 연결을 설정
> - 신뢰성 보장: 순서 보장, 재전송, 흐름 제어, 혼잡 제어 제공
> - 속도는 UDP보다 느리지만 데이터 무결성이 중요한 경우 사용 (HTTP, FTP, 이메일 등)
>
> **UDP (User Datagram Protocol)**
> - 비연결 지향적 프로토콜로, 연결 설정 없이 데이터를 전송
> - 신뢰성 미보장: 순서 보장 없음, 재전송 없음
> - 빠른 속도가 필요하고 일부 데이터 손실이 허용되는 경우 사용 (스트리밍, 게임, DNS 등)

---

### 2. 객체지향이 무엇인지 설명하시오

> **객체지향 프로그래밍(OOP, Object-Oriented Programming)** 은 프로그램을 객체(Object)들의 집합으로 모델링하는 프로그래밍 
>
> **4대 특성:**
> 1. **캡슐화(Encapsulation)**: 데이터와 메서드를 하나로 묶고, 외부로부터 내부 구현을 숨김
> 2. **상속(Inheritance)**: 기존 클래스의 속성과 메서드를 새 클래스가 물려받음
> 3. **다형성(Polymorphism)**: 같은 인터페이스로 다양한 타입의 객체를 다룰 수 있음
> 4. **추상화(Abstraction)**: 복잡한 시스템에서 핵심 개념만 추출하여 모델링
>
> **장점:** 코드 재사용성, 유지보수성, 확장성 향상

---

### 3. 데이터베이스 index에 대해서 설명하시오

> **인덱스(Index)** 는 데이터베이스 테이블의 검색 속도를 높이기 위한 자료구조이다.
>
> **특징:**
> - 책의 목차처럼 특정 컬럼 값의 위치를 빠르게 찾을 수 있게 해줌
> - 주로 B-Tree, B+Tree, Hash 등의 자료구조 사용
> - SELECT 쿼리의 WHERE, ORDER BY, JOIN 성능 향상
>
> **장점:** 조회 속도 향상
>
> **단점:** 
> - 추가 저장 공간 필요
> - INSERT, UPDATE, DELETE 시 인덱스도 갱신해야 하므로 쓰기 성능 저하
> - 카디널리티가 낮은 컬럼에는 효과가 적음

---

### 4. POST, GET, PUT, DELETE, PATCH가 무엇인지 설명하시오

> **HTTP 메서드**로, RESTful API에서 CRUD 작업에 대응된다:
>
> | 메서드 | 설명 | CRUD | 멱등성 |
> |--------|------|------|--------|
> | **GET** | 리소스 조회 (데이터 요청) | Read | O |
> | **POST** | 리소스 생성 (데이터 전송) | Create | X |
> | **PUT** | 리소스 전체 수정 (대체) | Update | O |
> | **PATCH** | 리소스 부분 수정 | Update | X |
> | **DELETE** | 리소스 삭제 | Delete | O |
>
> - **멱등성**: 같은 요청을 여러 번 해도 결과가 동일한 성질
> - GET, PUT, DELETE는 멱등성을 가짐

---

### 5. 쿠키와 세션에 대해서 설명하시오

> **쿠키(Cookie)**
> - 클라이언트(브라우저)에 저장되는 작은 데이터 조각
> - Key-Value 형태로 저장, 만료 시간 설정 가능
> - 모든 요청에 자동으로 서버에 전송됨
> - 보안에 취약 (클라이언트에서 조작 가능)
>
> **세션(Session)**
> - 서버에 저장되는 사용자 상태 정보
> - 세션 ID만 쿠키로 클라이언트에 전달
> - 보안성이 높음 (데이터가 서버에 있음)
> - 서버 메모리/스토리지 사용, 확장성 고려 필요
>
> **비교:** 세션은 보안성이 높지만 서버 리소스를 사용하고, 쿠키는 클라이언트에 부담을 주지만 보안에 취약

---

### 6. OSI 7 Layer에 대해서 설명하시오

> **OSI 7계층**은 네트워크 통신을 7개의 계층으로 표준화한 모델이다:
>
> | 계층 | 이름 | 역할 | 프로토콜/장비 예시 |
> |------|------|------|-------------------|
> | 7 | **응용 계층** | 사용자 인터페이스, 애플리케이션 서비스 | HTTP, FTP, SMTP |
> | 6 | **표현 계층** | 데이터 형식 변환, 암호화, 압축 | JPEG, SSL/TLS |
> | 5 | **세션 계층** | 세션 설정/유지/종료 관리 | NetBIOS, RPC |
> | 4 | **전송 계층** | 종단간 신뢰성 있는 데이터 전송 | TCP, UDP |
> | 3 | **네트워크 계층** | 라우팅, 논리적 주소 지정 | IP, 라우터 |
> | 2 | **데이터링크 계층** | 물리적 주소 지정, 프레임 전송 | MAC, 스위치 |
> | 1 | **물리 계층** | 비트 단위 전송, 전기적 신호 | 케이블, 허브 |

---

### 7. 3-way handshake에 대해서 설명하시오

> **3-way handshake**는 TCP 연결을 설정하는 과정이다:
>
> 1. **SYN**: 클라이언트 → 서버로 연결 요청 (SYN 플래그, 시퀀스 번호 전송)
> 2. **SYN-ACK**: 서버 → 클라이언트로 연결 수락 응답 (SYN + ACK 플래그)
> 3. **ACK**: 클라이언트 → 서버로 확인 응답 (ACK 플래그)
>
> ```
> Client          Server
>   |---- SYN ---->|
>   |<-- SYN+ACK --|
>   |---- ACK ---->|
>   |   연결 성립   |
> ```
>
> 이 과정을 통해 양측이 데이터를 주고받을 준비가 되었음을 확인하고, 신뢰성 있는 연결을 수립한다.

---

### 8. Stack과 Queue에 대해 설명하시오

> **Stack (스택)**
> - **LIFO (Last In First Out)**: 마지막에 들어온 것이 먼저 나감
> - 주요 연산: push(삽입), pop(제거), peek(조회)
> - 활용: 함수 호출 스택, 뒤로가기, 괄호 검사, DFS
>
> **Queue (큐)**
> - **FIFO (First In First Out)**: 먼저 들어온 것이 먼저 나감
> - 주요 연산: enqueue(삽입), dequeue(제거)
> - 활용: 작업 대기열, 프린터 큐, BFS, 메시지 큐
>
> ```
> Stack: [1, 2, 3] → push(4) → [1, 2, 3, 4] → pop() → [1, 2, 3] (4 반환)
> Queue: [1, 2, 3] → enqueue(4) → [1, 2, 3, 4] → dequeue() → [2, 3, 4] (1 반환)
> ```

---

### 9. Python 리스트와 튜플의 차이점에 대해 설명하시오

> | 구분 | 리스트 (List) | 튜플 (Tuple) |
> |------|---------------|--------------|
> | **가변성** | 가변(Mutable) - 수정 가능 | 불변(Immutable) - 수정 불가 |
> | **문법** | `[1, 2, 3]` | `(1, 2, 3)` |
> | **메모리** | 더 많은 메모리 사용 | 더 적은 메모리 사용 |
> | **속도** | 상대적으로 느림 | 상대적으로 빠름 |
> | **해시** | 해시 불가 (dict 키 X) | 해시 가능 (dict 키 O) |
> | **용도** | 변경이 필요한 데이터 | 변경되면 안 되는 데이터 |
>
> ```python
> my_list = [1, 2, 3]
> my_list[0] = 10  # 가능
>
> my_tuple = (1, 2, 3)
> my_tuple[0] = 10  # TypeError 발생
> ```

---

### 10. Python에서 `__init__()`에 대해 객체지향프로그래밍과 연관지어 설명하시오

> **`__init__()`**은 Python 클래스의 **생성자(Constructor)** 메서드이다.
>
> - 객체가 생성될 때 자동으로 호출되어 인스턴스 변수를 초기화
> - 첫 번째 매개변수는 항상 `self` (생성되는 인스턴스 자신을 참조)
> - 객체의 초기 상태를 설정하는 역할
>
> ```python
> class Person:
>     def __init__(self, name, age):
>         self.name = name  # 인스턴스 변수 초기화
>         self.age = age
>
> # 객체 생성 시 __init__() 자동 호출
> person = Person("홍길동", 25)
> ```
>
> **OOP와의 연관:**
> - **캡슐화**: 객체 생성 시 필요한 데이터를 내부에 저장
> - **추상화**: 복잡한 초기화 로직을 생성자에서 처리
> - 객체의 상태를 일관되게 초기화하여 안정적인 객체 생성 보장

---

## 컴퓨터공학 – 객관식, 단답형, O/X (문제당 2점)

### 1. HTTP 200은 "요청 성공"을 의미한다. (O/X)

> **O**  
> HTTP 200 OK는 요청이 성공적으로 처리되었음을 나타내는 상태 코드이다.

---

### 2. TCP 연결 성립은 3-way handshake, 종료는 보통 4-way handshake로 이뤄진다. (O/X)

> **O**  
> 연결 수립은 SYN → SYN-ACK → ACK (3-way), 종료는 FIN → ACK → FIN → ACK (4-way)

---

### 3. 데이터베이스에 인덱스를 추가하면 모든 SELECT 쿼리가 반드시 더 빨라진다. (O/X)

> **X**  
> 인덱스가 사용되지 않는 쿼리(예: 인덱스 컬럼을 조건으로 사용하지 않는 경우, LIKE '%문자열', 함수 적용 등)에서는 효과가 없거나 오히려 느려질 수 있다. 또한 카디널리티가 낮은 컬럼에서는 Full Scan이 더 효율적일 수 있다.

---

### 4. TCP는 순서/재전송 보장을 제공하고, UDP는 연결 설정 없이 보낸다. (O/X)

> **O**  
> TCP는 신뢰성(순서 보장, 재전송)을 제공하고, UDP는 비연결형으로 빠르게 전송한다.

---

### 5. 데이터베이스에서 Primary Key는 NULL을 허용한다. (O/X)

> **X**  
> Primary Key는 NULL을 허용하지 않는다. 유일성(Unique)과 NOT NULL 제약 조건을 모두 만족해야 한다.

---

### 6. 현재 작업 중인 디렉터리 경로를 출력하는 리눅스 명령어는?

A. ls  
B. pwd  
C. cd ..  
D. whoami

> **정답: B. pwd**  
> pwd (Print Working Directory)는 현재 작업 디렉터리의 절대 경로를 출력한다.

---

### 7. 좀비(zombie) 프로세스를 가장 잘 설명한 것은?

A. CPU를 과점하는 무한 루프 프로세스  
B. 종료됐지만 부모가 wait()로 수거하지 않아 테이블 엔트리만 남은 상태  
C. 메모리에만 있고 프로세스 테이블에 없는 상태  
D. 커널 스레드

> **정답: B**  
> 좀비 프로세스는 자식 프로세스가 종료되었지만 부모 프로세스가 wait() 시스템 콜로 종료 상태를 수거하지 않아 프로세스 테이블에 엔트리만 남아있는 상태이다.

---

### 8. Docker에서 이미지(Image)와 컨테이너(Container)의 관계 설명으로 가장 맞는 것은?

A. 이미지는 실행 중인 프로그램이고, 컨테이너는 템플릿이다.  
B. 이미지는 불변 템플릿, 컨테이너는 그 이미지를 실행한 인스턴스이다.  
C. 이미지는 네트워크 설정, 컨테이너는 저장소만 가진다.  
D. 이미지는 로그, 컨테이너는 설정 파일이다.

> **정답: B**  
> 이미지는 읽기 전용의 불변 템플릿이고, 컨테이너는 이미지를 기반으로 실행된 인스턴스이다. 클래스와 객체의 관계와 유사하다.

---

### 9. 다음 의사코드의 시간 복잡도는?

```python
for i in range(n):
    for j in range(i, n):
        count += 1
```

A. O(n)  
B. O(n log n)  
C. O(n²)  
D. O(n³)

> **정답: C. O(n²)**  
> 내부 루프 실행 횟수: n + (n-1) + (n-2) + ... + 1 = n(n+1)/2 ≈ O(n²)

---

### 10. Airflow에서 DAG를 가장 정확히 설명한 것은?

A. 실행 중인 컨테이너  
B. 작업과 의존관계로 이루어진 유향 비순환 그래프  
C. 파이썬 가상환경  
D. 외부 데이터베이스 연결

> **정답: B**  
> DAG (Directed Acyclic Graph)는 작업(Task)들과 그 의존 관계를 정의한 유향 비순환 그래프로, 워크플로우를 표현한다.

---

## Django – 객관식, 단답형, O/X (문제당 2점)

### 1. Django는 MTV(Model–Template–View) 패턴을 따른다. (O/X)

> **O**  
> Django는 MTV 패턴을 사용한다. Model(데이터), Template(화면), View(로직)

---

### 2. Django의 View는 요청을 받아 로직을 수행하고 HttpResponse를 반환한다. (O/X)

> **O**  
> View는 요청(Request)을 받아 비즈니스 로직을 처리하고 HttpResponse 객체를 반환한다.

---

### 3. path()는 정규식 기반 URL 매칭 함수다. (O/X)

> **X**  
> `path()`는 단순 문자열 패턴 매칭을 사용한다. 정규식 기반은 `re_path()`이다.

---

### 4. 모델을 수정한 뒤에는 makemigrations 후 migrate를 해야 한다. (O/X)

> **O**  
> `makemigrations`로 마이그레이션 파일을 생성하고, `migrate`로 데이터베이스에 적용한다.

---

### 5. QuerySet은 지연 평가된다. (O/X)

> **O**  
> QuerySet은 Lazy Evaluation으로, 실제로 데이터가 필요할 때(iteration, slicing, len() 등)까지 DB 쿼리를 실행하지 않는다.

---

### 6. 미들웨어는 순서가 중요하다. (O/X)

> **O**  
> 미들웨어는 `MIDDLEWARE` 설정의 순서대로 요청 시 위→아래, 응답 시 아래→위 순으로 실행된다.

---

### 7. Django는 ASGI를 통해 비동기(Async) 뷰를 지원한다. (O/X)

> **O**  
> Django 3.0부터 ASGI를 지원하며, 3.1부터 비동기 뷰를 공식 지원한다.

---

### 8. 기본 키를 명시하지 않으면 Django가 자동으로 기본 키 필드를 만든다. (O/X)

> **O**  
> 모델에 Primary Key를 지정하지 않으면 Django가 자동으로 `id` 필드(AutoField/BigAutoField)를 생성한다.

---

### 9. 모델 필드를 수정했다. 올바른 명령 실행 순서는?

A. migrate → makemigrations  
B. runserver → migrate  
C. makemigrations → migrate  
D. collectstatic → migrate

> **정답: C. makemigrations → migrate**  
> 모델 변경 → makemigrations (마이그레이션 파일 생성) → migrate (DB에 적용)

---

### 10. 로그인한 사용자만 접근하도록 함수형 뷰를 보호하는 가장 쉬운 방법은?

A. @csrf_exempt  
B. @login_required  
C. @permission_required('auth.view_user')  
D. @require_POST

> **정답: B. @login_required**  
> `@login_required` 데코레이터는 로그인하지 않은 사용자를 로그인 페이지로 리다이렉트한다.

---

## Django - 서술형 (문제당 3점)

### 1. Django의 요청–응답 라이프사이클을 처음부터 끝까지 단계별로 서술하시오. (하)

> **Django 요청-응답 라이프사이클:**
>
> 1. **클라이언트 요청**: 브라우저가 HTTP 요청을 서버로 전송
> 2. **WSGI/ASGI 서버**: 요청을 받아 Django 애플리케이션에 전달
> 3. **미들웨어 (요청 단계)**: `process_request()`, `process_view()` 순서로 실행
> 4. **URL 라우팅**: `urls.py`에서 URL 패턴 매칭하여 적절한 View 결정
> 5. **View 실행**: 비즈니스 로직 수행, 모델과 상호작용
> 6. **Template 렌더링** (선택): 템플릿 엔진이 HTML 생성
> 7. **HttpResponse 생성**: View가 응답 객체 반환
> 8. **미들웨어 (응답 단계)**: `process_response()` 역순으로 실행
> 9. **WSGI/ASGI 서버**: 응답을 클라이언트에게 전송
>
> ```
> Client → WSGI → Middleware(요청) → URL Router → View → Template
>                                                      ↓
> Client ← WSGI ← Middleware(응답) ← ← ← ← HttpResponse
> ```

---

### 2. URL 해석 전후에 미들웨어가 어떻게 동작하는지, 어떤 훅들이 관여하는지 명확히 설명하시오. (중)

> **미들웨어 훅과 실행 순서:**
>
> | 훅 | 실행 시점 | 설명 |
> |----|----------|------|
> | `process_request(request)` | URL 해석 전 | 모든 요청에 대해 실행, 응답 반환 시 이후 단계 스킵 |
> | `process_view(request, view_func, view_args, view_kwargs)` | URL 해석 후, View 호출 전 | View 함수와 인자 정보 접근 가능 |
> | `process_template_response(request, response)` | View 반환 후 | TemplateResponse인 경우에만 호출 |
> | `process_response(request, response)` | 응답 반환 전 | 모든 응답에 대해 실행 |
> | `process_exception(request, exception)` | View에서 예외 발생 시 | 예외 처리 및 대체 응답 생성 |
>
> **실행 흐름:**
> ```
> 요청 → MW1.process_request → MW2.process_request → URL해석
>      → MW1.process_view → MW2.process_view → View실행
>      → MW2.process_response → MW1.process_response → 응답
> ```
> (요청은 위→아래, 응답은 아래→위 순서)

---

### 3. MTV vs MVC를 비교하여 Django의 Model–Template–View가 전통적 MVC의 각 구성요소와 어떻게 매핑되는지 근거와 함께 서술하시오. (하)

> **MVC vs MTV 매핑:**
>
> | MVC | MTV (Django) | 역할 |
> |-----|--------------|------|
> | **Model** | **Model** | 데이터 구조 정의, DB와의 상호작용, 비즈니스 로직 |
> | **View** | **Template** | 사용자에게 보여지는 UI, 데이터 표현 방식 |
> | **Controller** | **View** | 요청 처리, 로직 수행, Model과 Template 연결 |
>
> **근거:**
> - Django의 **View**는 요청을 받아 로직을 처리하고 응답을 반환하므로 MVC의 Controller 역할
> - Django의 **Template**은 HTML을 렌더링하여 화면을 구성하므로 MVC의 View 역할
> - Django에서는 **URL Dispatcher**도 Controller의 일부 역할(라우팅)을 담당
>
> Django가 MTV라 명명한 이유는 View라는 용어가 "무엇을 보여줄지"를 결정하는 로직이라는 관점에서 붙여진 것

---

### 4. URL 라우팅에서 path()와 re_path()의 차이를 설명하시오 (하)

> **path() vs re_path():**
>
> | 구분 | path() | re_path() |
> |------|--------|-----------|
> | **패턴 방식** | 단순 문자열 + 타입 컨버터 | 정규 표현식 |
> | **가독성** | 높음 | 낮음 |
> | **유연성** | 제한적 | 매우 유연 |
> | **사용 예** | `path('user/<int:id>/')` | `re_path(r'^user/(?P<id>[0-9]+)/$')` |
>
> **path() 타입 컨버터:**
> - `<int:pk>`: 정수
> - `<str:name>`: 문자열 (기본값)
> - `<slug:title>`: 슬러그
> - `<uuid:id>`: UUID
> - `<path:file_path>`: 경로 (슬래시 포함)
>
> **권장사항:** 가능하면 `path()` 사용, 복잡한 패턴이 필요할 때만 `re_path()` 사용

---

### 5. N+1 문제를 재현·진단·개선하는 절차를 서술하시오. (중)

> **N+1 문제란?**
> 1개의 쿼리로 N개 객체를 가져온 후, 각 객체의 관계 데이터를 가져오기 위해 N번의 추가 쿼리가 발생하는 문제
>
> **재현:**
> ```python
> # N+1 발생 코드
> posts = Post.objects.all()  # 1번 쿼리
> for post in posts:
>     print(post.author.name)  # N번 쿼리 (각 post마다 author 조회)
> ```
>
> **진단:**
> - Django Debug Toolbar 사용
> - `connection.queries` 로그 확인
> - `django.db.backends` 로거 활성화
>
> **개선:**
> ```python
> # select_related (ForeignKey, OneToOne - JOIN 사용)
> posts = Post.objects.select_related('author').all()
>
> # prefetch_related (ManyToMany, 역참조 - 별도 쿼리 후 Python에서 조합)
> posts = Post.objects.prefetch_related('tags').all()
> ```
>
> - `select_related`: SQL JOIN으로 한 번에 가져옴 (1:1, N:1 관계)
> - `prefetch_related`: 별도 쿼리 후 Python에서 매핑 (M:N, 역참조)

---

### 6. values(), values_list(), only(), defer()가 메모리 사용량과 전송량에 미치는 영향을 비교 설명하시오. (하)

> | 메서드 | 반환 타입 | 특징 | 메모리/전송량 |
> |--------|----------|------|---------------|
> | `values()` | 딕셔너리 리스트 | 지정 필드만 딕셔너리로 반환 | 최소 (필요한 컬럼만) |
> | `values_list()` | 튜플 리스트 | 지정 필드만 튜플로 반환 | 최소 (딕셔너리보다 경량) |
> | `only()` | 모델 인스턴스 | 지정 필드만 즉시 로드, 나머지는 지연 로드 | 중간 (접근 시 추가 쿼리 가능) |
> | `defer()` | 모델 인스턴스 | 지정 필드를 지연 로드 | 중간 (접근 시 추가 쿼리 가능) |
>
> ```python
> # values() - 딕셔너리 반환
> User.objects.values('id', 'name')  # [{'id': 1, 'name': 'Kim'}, ...]
>
> # values_list() - 튜플 반환
> User.objects.values_list('id', 'name')  # [(1, 'Kim'), ...]
> User.objects.values_list('name', flat=True)  # ['Kim', 'Lee', ...]
>
> # only() - 모델 인스턴스, 지정 필드만 로드
> User.objects.only('name')  # 다른 필드 접근 시 추가 쿼리
>
> # defer() - 모델 인스턴스, 지정 필드 제외하고 로드
> User.objects.defer('bio')  # bio 필드 접근 시 추가 쿼리
> ```
>
> **선택 기준:** 모델 메서드가 필요하면 only/defer, 단순 데이터만 필요하면 values/values_list

---

### 7. 쿼리셋의 지연 평가(lazy)와 캐시 동작을 설명하고, 슬라이싱이 DB에 미치는 영향과 주의점을 서술하시오. (중)

> **지연 평가 (Lazy Evaluation):**
> - QuerySet은 생성 시점에 DB 쿼리를 실행하지 않음
> - 실제 데이터가 필요한 시점(평가 시점)에 쿼리 실행
>
> **평가가 발생하는 경우:**
> - Iteration (for문)
> - 슬라이싱 (step 사용 시)
> - len(), list(), bool()
> - repr(), print()
>
> **캐시 동작:**
> ```python
> qs = User.objects.all()
> for user in qs:  # 쿼리 실행 + 결과 캐시
>     print(user.name)
> for user in qs:  # 캐시된 결과 사용 (쿼리 없음)
>     print(user.email)
> ```
>
> **슬라이싱의 영향:**
> ```python
> # LIMIT, OFFSET으로 변환 - 쿼리 실행 안 함 (새 QuerySet 반환)
> users = User.objects.all()[:10]  # LIMIT 10
>
> # step 사용 시 즉시 평가 (리스트 반환)
> users = User.objects.all()[::2]  # 전체 조회 후 Python에서 슬라이싱
> ```
>
> **주의점:**
> - 슬라이싱 후 filter() 불가 (이미 평가된 QuerySet)
> - 큰 offset은 성능 저하 (DB가 앞부분을 건너뛰어야 함)
> - 매번 새로운 QuerySet을 평가하면 캐시 미사용으로 비효율

---

### 8. XSS/클릭재킹/호스트 헤더 공격에 대한 Django 기본 방어와 추가적으로 설정해야 할 보안 헤더를 서술하시오. (중상)

> **XSS (Cross-Site Scripting):**
> - **기본 방어**: 템플릿 자동 이스케이프 (`{{ variable }}` → HTML 이스케이프)
> - **추가 설정**:
>   - `Content-Security-Policy` 헤더 설정
>   - `|safe` 필터 사용 최소화
>   - `mark_safe()` 신중하게 사용
>
> **클릭재킹 (Clickjacking):**
> - **기본 방어**: `XFrameOptionsMiddleware` (기본 활성화)
> - **추가 설정**:
>   ```python
>   X_FRAME_OPTIONS = 'DENY'  # 또는 'SAMEORIGIN'
>   ```
>
> **호스트 헤더 공격:**
> - **기본 방어**: `ALLOWED_HOSTS` 설정 필수
>   ```python
>   ALLOWED_HOSTS = ['example.com', 'www.example.com']
>   ```
>
> **추가 보안 헤더 (settings.py):**
> ```python
> # HTTPS 강제
> SECURE_SSL_REDIRECT = True
> SECURE_HSTS_SECONDS = 31536000
> SECURE_HSTS_INCLUDE_SUBDOMAINS = True
> SECURE_HSTS_PRELOAD = True
>
> # 쿠키 보안
> SESSION_COOKIE_SECURE = True
> CSRF_COOKIE_SECURE = True
> SESSION_COOKIE_HTTPONLY = True
>
> # 기타
> SECURE_CONTENT_TYPE_NOSNIFF = True
> SECURE_BROWSER_XSS_FILTER = True  # deprecated, CSP 권장
> ```

---

### 9. manage.py, \_\_init\_\_.py, settings.py, urls.py, wsgi.py 각 파일이 어떤 역할을 하는지 설명하시오

> | 파일 | 역할 |
> |------|------|
> | **manage.py** | Django 프로젝트 관리를 위한 커맨드라인 유틸리티. runserver, migrate, makemigrations, shell 등의 명령어 실행 진입점 |
> | **\_\_init\_\_.py** | 해당 디렉터리를 Python 패키지로 인식하게 함. 보통 비어있거나 패키지 초기화 코드 포함 |
> | **settings.py** | 프로젝트 설정 파일. DB 설정, 미들웨어, 앱 목록, 템플릿 설정, 보안 설정, 정적 파일 경로 등 모든 구성 정보 포함 |
> | **urls.py** | URL 라우팅 설정. URL 패턴과 View를 매핑. 프로젝트 루트 urls.py에서 각 앱의 urls.py를 include |
> | **wsgi.py** | WSGI(Web Server Gateway Interface) 호환 서버와의 진입점. 배포 시 Gunicorn, uWSGI 등이 이 파일을 통해 Django 앱 실행 |
>
> ```
> myproject/
> ├── manage.py          # 프로젝트 관리 CLI
> └── myproject/
>     ├── __init__.py    # 패키지 선언
>     ├── settings.py    # 설정
>     ├── urls.py        # URL 라우팅
>     ├── wsgi.py        # WSGI 진입점
>     └── asgi.py        # ASGI 진입점 (비동기)
> ```

---

### 10. Session, Token, JWT/OAuth2를 비교 평가하시오. (중상)

> | 구분 | Session | Token (Simple) | JWT | OAuth2 |
> |------|---------|----------------|-----|--------|
> | **저장 위치** | 서버 (메모리/DB/Redis) | 서버 DB | 클라이언트 | 클라이언트 |
> | **상태** | Stateful | Stateful | Stateless | Stateless |
> | **확장성** | 낮음 (서버 간 세션 공유 필요) | 중간 | 높음 | 높음 |
> | **보안** | 높음 (서버 저장) | 중간 | 중간 (탈취 시 위험) | 높음 (범위 제한) |
>
> **Session 기반:**
> - 장점: 서버에서 완전한 제어, 즉시 무효화 가능
> - 단점: 서버 메모리 사용, 분산 환경에서 세션 공유 필요
>
> **Token (Simple Token):**
> - 장점: 구현 간단
> - 단점: DB 조회 필요, 무효화 시 DB 업데이트 필요
>
> **JWT (JSON Web Token):**
> - 장점: Stateless, 서버 부담 적음, 마이크로서비스에 적합
> - 단점: 토큰 크기가 큼, 만료 전 강제 무효화 어려움, 탈취 시 위험
> - 구조: Header.Payload.Signature
>
> **OAuth2:**
> - 장점: 권한 위임, 제3자 인증, 범위(scope) 기반 접근 제어
> - 단점: 구현 복잡, 추가 인프라 필요
> - 용도: 소셜 로그인, API 접근 권한 위임
>
> **선택 기준:**
> - 단순 웹앱: Session
> - SPA/모바일 앱: JWT
> - 마이크로서비스: JWT + Redis (블랙리스트)
> - 제3자 인증/API: OAuth2
