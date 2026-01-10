# Django 백엔드 스터디 2회차 문제

**2025-08-05**  
**작성자: 김호중**

---

## 컴퓨터공학 – 서술형 (문제당 3점)

### 1. REST 아키텍처 스타일의 핵심 제약 조건(Uniform Interface 등)을 나열하고 각 제약이 주는 이점을 서술하시오. (중요)

> **REST의 6가지 핵심 제약 조건:**
>
> | 제약 조건 | 설명 | 이점 |
> |----------|------|------|
> | **Client-Server** | 클라이언트와 서버의 관심사 분리 | 독립적 진화 가능, 확장성 향상 |
> | **Stateless** | 각 요청은 독립적, 서버는 클라이언트 상태 저장 안 함 | 서버 확장 용이, 신뢰성 향상 |
> | **Cacheable** | 응답은 캐시 가능 여부 명시 | 네트워크 효율성, 응답 속도 향상 |
> | **Uniform Interface** | 일관된 인터페이스 (리소스 식별, 표현을 통한 조작, 자기 서술적 메시지, HATEOAS) | 단순성, 가시성, 독립적 진화 |
> | **Layered System** | 계층화된 시스템 아키텍처 | 보안, 로드밸런싱, 캐싱 계층 추가 용이 |
> | **Code on Demand** (선택) | 서버가 클라이언트에 실행 코드 전송 가능 | 클라이언트 기능 확장 |
>
> **Uniform Interface의 4가지 하위 제약:**
> - **리소스 식별**: URI로 리소스 고유 식별
> - **표현을 통한 조작**: JSON/XML 등 표현으로 리소스 조작
> - **자기 서술적 메시지**: 메시지만으로 처리 방법 이해 가능
> - **HATEOAS**: 응답에 다음 가능한 액션 링크 포함

---

### 2. B-tree 인덱스 내부 동작 원리와, 선택도(selectivity)가 낮을 때 인덱스가 오히려 성능을 저하시킬 수 있는 이유를 설명하시오. (중요)

> **B-tree 인덱스 동작 원리:**
> - 균형 트리 구조로, 루트→브랜치→리프 노드로 구성
> - 리프 노드에 실제 데이터 포인터(RowID) 저장
> - 검색 시간 복잡도: O(log N)
> - 범위 검색에 효율적 (리프 노드가 연결 리스트로 연결)
>
> ```
>           [50]              ← 루트
>          /    \
>     [20,30]  [70,80]        ← 브랜치
>     /  |  \    |   \
>   [...리프 노드들...]       ← 데이터 포인터
> ```
>
> **선택도(Selectivity)란?**
> - 선택도 = (고유 값 개수) / (전체 행 개수)
> - 높은 선택도: 고유 값이 많음 (예: 주민번호, 이메일)
> - 낮은 선택도: 중복 값이 많음 (예: 성별, 상태 코드)
>
> **낮은 선택도에서 성능 저하 이유:**
> 1. **Random I/O 증가**: 인덱스 → 테이블 왕복이 많아짐
> 2. **Full Table Scan이 더 효율적**: 연속 읽기가 랜덤 읽기보다 빠름
> 3. **인덱스 유지 비용**: INSERT/UPDATE 시 인덱스 갱신 오버헤드
>
> **예시:**
> ```sql
> -- 성별 컬럼 (선택도 낮음): 인덱스 비효율
> SELECT * FROM users WHERE gender = 'M';  -- 50% 행 반환
>
> -- 이메일 컬럼 (선택도 높음): 인덱스 효율적
> SELECT * FROM users WHERE email = 'user@example.com';  -- 1행 반환
> ```

---

### 3. 로드밸런싱 알고리즘 Round-Robin, Least-Connections, IP Hash 세 알고리즘의 특징과 사용 시 고려해야 할 점을 비교하시오.

> | 알고리즘 | 동작 방식 | 장점 | 단점 | 적합한 상황 |
> |----------|----------|------|------|-------------|
> | **Round-Robin** | 순서대로 순환 분배 | 구현 간단, 균등 분배 | 서버 성능 차이 무시 | 동일 스펙 서버, 균일한 요청 |
> | **Least-Connections** | 연결 수가 적은 서버 선택 | 동적 부하 반영 | 연결 추적 오버헤드 | 긴 연결 유지 서비스 (WebSocket) |
> | **IP Hash** | 클라이언트 IP 해시로 서버 결정 | 세션 지속성 보장 | 서버 추가/제거 시 재분배 | 세션 기반 애플리케이션 |
>
> **고려사항:**
>
> **Round-Robin:**
> - 서버 가중치(Weighted) 적용 고려
> - Health Check와 함께 사용 필수
> - Stateless 서비스에 적합
>
> **Least-Connections:**
> - 연결 카운트 실시간 추적 필요
> - 긴 유휴 연결 처리 정책 필요
> - 서버 성능 차이가 있을 때 유리
>
> **IP Hash:**
> - NAT 환경에서 동일 IP 집중 가능
> - Consistent Hashing으로 서버 변경 영향 최소화
> - 세션 클러스터링의 대안

---

### 4. Docker 컨테이너가 VM보다 경량화되는 원리를 네임스페이스·cgroups 관점에서 설명하고, 보안 격리 측면의 차이를 논하시오. (중요)

> **경량화 원리:**
>
> | 구분 | VM | Container |
> |------|-----|-----------|
> | **커널** | 각각 독립 커널 | 호스트 커널 공유 |
> | **부팅** | OS 부팅 필요 (분 단위) | 프로세스 시작 (초 단위) |
> | **메모리** | GB 단위 | MB 단위 |
> | **격리 수준** | 하드웨어 레벨 | 프로세스 레벨 |
>
> **Linux Namespace (격리):**
> - **PID**: 프로세스 ID 격리 (컨테이너 내 PID 1)
> - **NET**: 네트워크 스택 격리 (가상 인터페이스)
> - **MNT**: 파일시스템 마운트 격리
> - **UTS**: 호스트명/도메인명 격리
> - **IPC**: 프로세스 간 통신 격리
> - **USER**: 사용자/그룹 ID 격리
>
> **cgroups (자원 제한):**
> - CPU 사용량 제한 (cpu.shares, cpu.quota)
> - 메모리 제한 (memory.limit_in_bytes)
> - 디스크 I/O 제한 (blkio)
> - 네트워크 대역폭 제한
>
> **보안 격리 차이:**
>
> | 측면 | VM | Container |
> |------|-----|-----------|
> | **커널 취약점** | 독립 커널로 영향 제한 | 호스트 커널 공유로 위험 전파 가능 |
> | **탈출 공격** | 하이퍼바이저 탈출 어려움 | 커널 익스플로잇으로 호스트 접근 가능성 |
> | **권장 보안** | - | Seccomp, AppArmor, SELinux, rootless 컨테이너 |

---

### 5. TCP 3-way/4-way 핸드셰이크 과정을 설명하고, 대기 연결이 많은 서버에서 SYN flood를 완화하는 방법을 제시하시오.

> **3-way Handshake (연결 수립):**
> ```
> Client                Server
>   |---- SYN (seq=x) ---->|    1. 연결 요청
>   |<-- SYN-ACK (seq=y, ack=x+1) --|  2. 요청 수락
>   |---- ACK (ack=y+1) -->|    3. 연결 확립
> ```
>
> **4-way Handshake (연결 종료):**
> ```
> Client                Server
>   |---- FIN (seq=u) ---->|    1. 종료 요청
>   |<-- ACK (ack=u+1) ----|    2. 종료 요청 확인
>   |<-- FIN (seq=w) ------|    3. 서버도 종료 요청
>   |---- ACK (ack=w+1) -->|    4. 종료 확인
>   |   TIME_WAIT 상태     |
> ```
>
> **SYN Flood 공격:**
> - 공격자가 대량의 SYN 패킷을 위조 IP로 전송
> - 서버는 SYN-ACK 응답 후 ACK 대기 (Half-open 연결)
> - SYN 큐가 가득 차서 정상 연결 불가
>
> **완화 방법:**
>
> | 방법 | 설명 |
> |------|------|
> | **SYN Cookies** | SYN 큐 없이 seq 번호에 연결 정보 인코딩 |
> | **SYN 큐 확장** | `net.ipv4.tcp_max_syn_backlog` 증가 |
> | **타임아웃 단축** | Half-open 연결 타임아웃 감소 |
> | **방화벽/IDS** | 비정상 SYN 패턴 탐지 및 차단 |
> | **Rate Limiting** | IP당 SYN 요청 수 제한 |
> | **CDN/DDoS 방어** | Cloudflare 등 앞단에서 필터링 |

---

### 6. 페이징 vs 세그멘테이션에 대해서 설명하시오

> | 구분 | 페이징 (Paging) | 세그멘테이션 (Segmentation) |
> |------|-----------------|---------------------------|
> | **분할 단위** | 고정 크기 (페이지, 보통 4KB) | 가변 크기 (논리적 단위) |
> | **주소 변환** | 페이지 번호 + 오프셋 | 세그먼트 번호 + 오프셋 |
> | **외부 단편화** | 없음 | 발생 가능 |
> | **내부 단편화** | 발생 가능 (마지막 페이지) | 없음 |
> | **메모리 보호** | 페이지 단위 | 세그먼트 단위 (논리적 구분) |
>
> **페이징:**
> ```
> 가상 주소: [페이지 번호 | 오프셋]
>              ↓
> 페이지 테이블 → 물리 프레임 번호
>              ↓
> 물리 주소: [프레임 번호 | 오프셋]
> ```
> - 장점: 외부 단편화 없음, 구현 단순
> - 단점: 내부 단편화, 페이지 테이블 크기
>
> **세그멘테이션:**
> ```
> 가상 주소: [세그먼트 번호 | 오프셋]
>              ↓
> 세그먼트 테이블 → 베이스 주소 + 한계
>              ↓
> 물리 주소: 베이스 + 오프셋
> ```
> - 장점: 논리적 구조 반영 (코드/데이터/스택), 공유 용이
> - 단점: 외부 단편화, 복잡한 메모리 관리
>
> **현대 시스템:** 페이징 + 세그멘테이션 조합 (Segmented Paging)

---

### 7. 프로세스 vs 스레드 두 개념의 차이와 주소 공간/스택/파일 디스크립터 등 어떤 자원을 공유하는지 설명하시오. (중요)

> **프로세스 (Process):**
> - 실행 중인 프로그램의 인스턴스
> - 독립된 메모리 공간 (Code, Data, Heap, Stack)
> - OS로부터 자원 할당받는 단위
> - 프로세스 간 통신: IPC (파이프, 소켓, 공유 메모리 등)
>
> **스레드 (Thread):**
> - 프로세스 내 실행 흐름 단위
> - 같은 프로세스의 스레드들은 메모리 공유
> - 경량 프로세스 (Lightweight Process)
>
> **자원 공유 비교:**
>
> | 자원 | 프로세스 간 | 스레드 간 |
> |------|-------------|-----------|
> | **주소 공간** | 독립 (격리) | 공유 |
> | **코드 영역** | 독립 | 공유 |
> | **데이터/힙** | 독립 | 공유 |
> | **스택** | 독립 | 독립 (각자 스택) |
> | **파일 디스크립터** | 독립 | 공유 |
> | **PID** | 독립 | 동일 (TID는 다름) |
> | **전역 변수** | 독립 | 공유 |
> | **레지스터/PC** | 독립 | 독립 |
>
> ```
> 프로세스 A              프로세스 B
> ┌─────────────┐        ┌─────────────┐
> │  Code       │        │  Code       │
> │  Data/Heap  │        │  Data/Heap  │
> │ ┌─────┬─────┐│       │ ┌─────┬─────┐│
> │ │Stack│Stack││       │ │Stack│Stack││
> │ │ T1  │ T2  ││       │ │ T1  │ T2  ││
> │ └─────┴─────┘│       │ └─────┴─────┘│
> └─────────────┘        └─────────────┘
>      격리됨                  격리됨
> ```
>
> **장단점:**
> - 프로세스: 안정성 높음 (격리), 생성 비용 높음, 컨텍스트 스위칭 비용 높음
> - 스레드: 생성 비용 낮음, 통신 빠름, 동기화 필요 (Race Condition 주의)

---

## 컴퓨터공학 – 객관식, 단답형, O/X (문제당 2점)

### 1. Docker 컨테이너는 호스트 OS 커널을 공유한다. (O/X)

> **O**  
> 컨테이너는 VM과 달리 호스트 OS 커널을 공유하며, 네임스페이스와 cgroups로 격리한다.

---

### 2. Docker 이미지는 변경 불가능(immutable)하다. (O/X)

> **O**  
> Docker 이미지는 불변(immutable)이다. 컨테이너 실행 시 쓰기 가능한 레이어가 추가되며, 이미지 자체는 변경되지 않는다.

---

### 3. OS 커널 모드(Kernel Mode)는 사용자 모드(User Mode)보다 높은 권한을 가진다. (O/X)

> **O**  
> 커널 모드는 모든 하드웨어와 메모리에 접근 가능하며, 사용자 모드는 제한된 권한만 가진다.

---

### 4. NAT 게이트웨이(NAT Gateway)는 사설 IP를 공인 IP로 변환해 주는 역할만 수행하며, 트래픽 필터링 기능은 없다. (O/X)

> **O**  
> NAT 게이트웨이는 주소 변환(Network Address Translation)만 수행한다. 트래픽 필터링은 방화벽(Security Group, NACL 등)의 역할이다.

---

### 5. 마이크로서비스 아키텍처에서 API 게이트웨이(API Gateway)는 클라이언트 요청을 각 서비스로 라우팅할 뿐만 아니라, 인증·인가, 로깅, 속도 제한(rate limiting) 등의 기능도 제공한다. (O/X)

> **O**  
> API 게이트웨이는 라우팅 외에도 인증, 인가, 로깅, Rate Limiting, 요청/응답 변환, 캐싱 등 다양한 횡단 관심사를 처리한다.

---

### 6. TCP 3-way Handshake 순서 중 첫 번째 메시지는?

A. SYN  
B. SYN-ACK  
C. ACK  
D. FIN

> **정답: A. SYN**  
> 클라이언트가 서버에 연결 요청을 위해 SYN 플래그가 설정된 패킷을 먼저 전송한다.

---

### 7. B-Tree 인덱스의 특징으로 옳지 않은 것은?

A. 균형 트리 구조로 검색 시간이 로그(log) 스케일이다.  
B. 중복된 값이 많은 컬럼에 부적합하다.  
C. 대용량 범위 검색(range scan)에 효과적이다.  
D. 해시 연산을 기반으로 동작한다.

> **정답: D**  
> B-Tree는 트리 구조 기반이며, 해시 연산 기반은 Hash 인덱스이다. Hash 인덱스는 동등 비교(=)에만 효과적이고 범위 검색은 불가능하다.

---

### 8. Docker 컨테이너와 가상 머신의 가장 큰 차이점은?

A. 컨테이너는 하이퍼바이저를 사용한다.  
B. 컨테이너는 별도의 커널을 포함하지 않는다.  
C. 가상 머신은 호스트 커널을 공유한다.  
D. 가상 머신은 이미지 레이어를 사용하지 않는다.

> **정답: B**  
> 컨테이너는 호스트 커널을 공유하여 별도의 Guest OS/커널이 필요 없다. VM은 각각 독립된 커널을 가진다.

---

### 9. 4×4 미로에서 '1'은 이동 가능, '0'은 벽. (0,0)에서 (3,3)까지 최단 칸 수를 구하시오.

```
1 0 1 1
1 1 1 0
0 1 0 1
1 1 1 1
```

A. 7  
B. 8  
C. 9  
D. 10

> **정답: A. 7**
>
> **BFS로 최단 경로 탐색:**
> ```
> S 0 1 1     경로: (0,0)→(1,0)→(1,1)→(1,2)→(2,1)→(3,1)→(3,2)→(3,3)
> * * * 0     지나는 칸 수: 7칸 (시작점 포함)
> 0 * 0 1
> 1 * * E
> ```
> - 시작점(0,0)에서 끝점(3,3)까지 방문하는 칸의 개수는 7개

---

### 10. TCP의 흐름 제어(flow control) 메커니즘은?

A. 슬라이딩 윈도우(Sliding Window)  
B. 혼잡 제어(Congestion Control)  
C. 다중 경로 전송(Multipath Transmission)  
D. 체크섬(Checksum)

> **정답: A. 슬라이딩 윈도우(Sliding Window)**  
> 수신자가 윈도우 크기를 알려주어 송신자의 전송량을 조절한다. 혼잡 제어(B)는 네트워크 상태 기반, 체크섬(D)은 무결성 검증 용도이다.

---

## Django – 서술형 (문제당 3점)

### 1. 뷰 함수에서 request.GET과 request.POST 딕셔너리 객체가 각각 언제 사용되는지, 예시 상황을 들어 설명하시오. (중)

> **request.GET**
> - URL의 쿼리 스트링(Query String)으로 전달된 데이터를 담고 있는 딕셔너리 객체
> - HTTP GET 메서드뿐만 아니라 모든 요청에서 URL에 포함된 파라미터 접근 가능
> - 데이터가 URL에 노출되므로 민감하지 않은 정보에 사용
>
> **예시 상황:**
> ```python
> # URL: /search/?q=django&page=2
> def search(request):
>     keyword = request.GET.get('q', '')  # 'django'
>     page = request.GET.get('page', 1)   # '2'
>     # 검색 결과 반환
> ```
> - 검색어 전달, 페이지네이션, 정렬 옵션, 필터링 조건 등
>
> **request.POST**
> - HTTP POST 요청의 본문(body)에 담긴 폼 데이터를 담고 있는 딕셔너리 객체
> - 데이터가 URL에 노출되지 않아 민감한 정보 전송에 적합
> - CSRF 토큰 검증과 함께 사용
>
> **예시 상황:**
> ```python
> # 로그인 폼 제출
> def login(request):
>     if request.method == 'POST':
>         username = request.POST.get('username')
>         password = request.POST.get('password')
>         # 인증 처리
> ```
> - 로그인/회원가입, 게시글 작성, 파일 업로드 등 데이터 생성/수정 작업

---

### 2. AbstractBase vs multi-table inheritance vs proxy model 세 가지 모델 상속 방식의 차이·장단점을 설명하고, 실제 서비스에서 적합한 사용 사례를 각각 제시하시오 (중상)

> | 구분 | Abstract Base | Multi-table | Proxy |
> |------|---------------|-------------|-------|
> | **테이블 생성** | 부모 테이블 없음 | 부모·자식 각각 테이블 | 부모 테이블만 사용 |
> | **DB 조인** | 없음 | JOIN 발생 | 없음 |
> | **필드 추가** | 자식에서 상속 | 자식 테이블에 추가 | 불가 |
> | **부모 쿼리** | 불가 | 가능 | 가능 |
>
> **1. Abstract Base Class (추상 기본 클래스)**
> ```python
> class TimeStamped(models.Model):
>     created_at = models.DateTimeField(auto_now_add=True)
>     class Meta:
>         abstract = True
>
> class Article(TimeStamped):
>     title = models.CharField(max_length=200)
> ```
> - **장점**: 코드 재사용, JOIN 없이 성능 우수, 공통 필드 일관성
> - **단점**: 부모 타입으로 일괄 쿼리 불가
> - **사용 사례**: created_at, updated_at 같은 공통 타임스탬프 필드
>
> **2. Multi-table Inheritance (멀티 테이블 상속)**
> ```python
> class Content(models.Model):
>     title = models.CharField(max_length=200)
>
> class Video(Content):
>     duration = models.PositiveIntegerField()
> ```
> - **장점**: 부모 타입으로 모든 자식 쿼리 가능, 다형성 지원
> - **단점**: JOIN으로 성능 저하, 복잡한 스키마
> - **사용 사례**: CMS의 콘텐츠 타입 (Article, Video, Gallery 등)
>
> **3. Proxy Model (프록시 모델)**
> ```python
> class Order(models.Model):
>     status = models.CharField(max_length=20)
>
> class PaidOrder(Order):
>     class Meta:
>         proxy = True
>         ordering = ['-id']
> ```
> - **장점**: 메서드/매니저/정렬만 변경, 테이블 추가 없음
> - **단점**: 새 필드 추가 불가
> - **사용 사례**: 결제완료 주문만 필터링하는 매니저, 관리자용 정렬 변경

---

### 3. DRF에서 Model → Serializer → ViewSet → Router로 이어지는 데이터 흐름을 설명하고, ListCreateAPIView와 ModelViewSet 중 하나를 선택해 간단한 예시 코드와 함께 장단점을 논하시오. (중상)

> **데이터 흐름:**
> ```
> Model (DB 스키마) → Serializer (직렬화/역직렬화) → ViewSet (CRUD 로직) → Router (URL 자동 생성)
> ```
>
> | 단계 | 역할 |
> |------|------|
> | **Model** | 데이터베이스 테이블 정의, 필드와 관계 설정 |
> | **Serializer** | 모델 ↔ JSON 변환, 유효성 검사 |
> | **ViewSet** | HTTP 메서드에 따른 CRUD 액션 처리 |
> | **Router** | ViewSet을 기반으로 URL 패턴 자동 생성 |
>
> **ModelViewSet 예시 (선택):**
> ```python
> # models.py
> class Article(models.Model):
>     title = models.CharField(max_length=200)
>     content = models.TextField()
>
> # serializers.py
> class ArticleSerializer(serializers.ModelSerializer):
>     class Meta:
>         model = Article
>         fields = '__all__'
>
> # views.py
> class ArticleViewSet(viewsets.ModelViewSet):
>     queryset = Article.objects.all()
>     serializer_class = ArticleSerializer
>
> # urls.py
> router = DefaultRouter()
> router.register('articles', ArticleViewSet)
> urlpatterns = router.urls
> ```
>
> **ModelViewSet 장단점:**
> - **장점**: 최소 코드로 CRUD 전체 구현, Router와 결합해 URL 자동 생성
> - **단점**: 과도한 자동화로 세부 제어 어려움, 불필요한 액션 노출 가능
>
> **ListCreateAPIView와 비교:**
> - ListCreateAPIView는 목록 조회(GET)와 생성(POST)만 제공
> - 더 세밀한 제어가 필요하거나 특정 액션만 노출할 때 적합

---

### 4. 커스텀 미들웨어를 작성해 Content-Security-Policy 헤더를 삽입하는 과정을 설명하고, 미들웨어 체인에서의 위치 선정이 보안·성능에 미치는 영향을 논하시오. (중상)

> **CSP 미들웨어 구현:**
> ```python
> # middleware.py
> class CSPMiddleware:
>     def __init__(self, get_response):
>         self.get_response = get_response
>
>     def __call__(self, request):
>         response = self.get_response(request)
>         response['Content-Security-Policy'] = (
>             "default-src 'self'; "
>             "script-src 'self' 'unsafe-inline'; "
>             "style-src 'self' 'unsafe-inline';"
>         )
>         return response
> ```
>
> **settings.py 등록:**
> ```python
> MIDDLEWARE = [
>     'django.middleware.security.SecurityMiddleware',
>     'myapp.middleware.CSPMiddleware',  # 보안 미들웨어 직후
>     # ...
> ]
> ```
>
> **위치 선정의 영향:**
>
> | 위치 | 보안 영향 | 성능 영향 |
> |------|----------|----------|
> | **맨 앞** | 모든 응답에 헤더 적용 보장 | 불필요한 처리 가능 (에러 페이지 등) |
> | **SecurityMiddleware 직후** | 다른 보안 헤더와 함께 일관된 처리 | 권장 위치 |
> | **맨 뒤** | 다른 미들웨어가 응답 수정 가능 | 최소한의 처리 |
>
> **권장사항:**
> - SecurityMiddleware 직후에 배치하여 보안 헤더들을 일관되게 관리
> - 응답 수정 미들웨어보다 앞에 위치해야 헤더가 덮어쓰이지 않음
> - 정적 파일 서빙 미들웨어(WhiteNoise 등)보다 뒤에 두면 정적 파일에도 적용

---

### 5. 다음 코드를 보고 어떤 상속인지 추론하고 그 근거를 작성하시오. (추상, 멀티테이블, 프록시)

> **(1) 추상 기본 클래스 (Abstract Base Class)**
> ```python
> class TimeStamped(models.Model):
>     created_at = models.DateTimeField(auto_now_add=True)
>     class Meta:
>         abstract = True
>
> class Article(TimeStamped):
>     title = models.CharField(max_length=200)
> ```
> **근거:** `class Meta: abstract = True`가 명시되어 있음. TimeStamped 테이블은 생성되지 않고, Article 테이블에 created_at 필드가 포함됨.
>
> ---
>
> **(2) 멀티테이블 상속 (Multi-table Inheritance)**
> ```python
> class Content(models.Model):
>     title = models.CharField(max_length=200)
>
> class Video(Content):
>     duration = models.PositiveIntegerField()
> ```
> **근거:** abstract나 proxy 선언이 없는 일반 모델 상속. Content 테이블과 Video 테이블이 각각 생성되며, Video는 Content를 참조하는 OneToOneField(content_ptr)를 자동으로 가짐. 쿼리 시 JOIN 발생.
>
> ---
>
> **(3) 프록시 모델 (Proxy Model)**
> ```python
> class Order(models.Model):
>     status = models.CharField(max_length=20)
>
> class PaidOrder(Order):
>     class Meta:
>         proxy = True
>         ordering = ['-id']
> ```
> **근거:** `class Meta: proxy = True`가 명시되어 있음. 새 테이블이 생성되지 않고 Order 테이블을 그대로 사용. 기본 정렬 순서만 변경하거나 커스텀 매니저/메서드를 추가할 때 사용.

---

## 백엔드 – 논리적사고문제: 오픈뱅킹 계좌이체 이중지급 방지 설계

### 1. 이체 FSM을 설계하시오. (조건부 업데이트를 중심으로 서술)

> **상태 정의:**
> | 상태 | 설명 | 종단 여부 |
> |------|------|----------|
> | PENDING | 요청 접수, 장부에 보류 전표 기록 | X |
> | DISPATCHED | 은행 API 호출 완료, 응답 대기 | X |
> | SETTLED | 성공 확정, 실제 출금/입금 전표 | O |
> | FAILED | 거절/오류 확정, 보류 롤백 | O |
> | EXPIRED | 타임아웃 대기, 늦은 웹훅 수용 | X |
>
> **상태 전이 다이어그램:**
> ```
> PENDING → DISPATCHED → SETTLED
>              ↓            ↗
>           EXPIRED ────────
>              ↓
>           FAILED ← (DISPATCHED에서도 가능)
> ```
>
> **조건부 업데이트 규칙:**
> ```sql
> -- PENDING → DISPATCHED (은행 API 호출 시)
> UPDATE transfers SET status = 'DISPATCHED', external_ref = ?
> WHERE id = ? AND status = 'PENDING';
>
> -- DISPATCHED/EXPIRED → SETTLED (성공 웹훅 수신 시)
> UPDATE transfers SET status = 'SETTLED', settled_at = NOW()
> WHERE id = ? AND status IN ('DISPATCHED', 'EXPIRED');
>
> -- DISPATCHED/EXPIRED → FAILED (실패 웹훅 수신 시)
> UPDATE transfers SET status = 'FAILED', failed_at = NOW()
> WHERE id = ? AND status IN ('DISPATCHED', 'EXPIRED');
> ```
>
> **핵심 원칙:**
> - 상태는 앞으로만 진행 (역방향 전이 불가)
> - WHERE 절에 현재 상태 조건 포함 (비관적 잠금 대신 낙관적 동시성 제어)
> - affected_rows = 0이면 이미 다른 프로세스가 처리한 것으로 간주

---

### 2. 처리 흐름에 대해 자세히 설명하시오.

> **전체 처리 흐름:**
>
> **① 입구 단계 (Client → Server)**
> - 클라이언트가 `client_request_id` 생성 (UUID)
> - 서버는 이 값을 UNIQUE 제약으로 저장
> - 동일 요청 재전송 시 기존 레코드 반환 (멱등성 보장)
>
> **② 내부 기록 단계**
> - 트랜잭션 내에서 Transfer 레코드 생성 (status=PENDING)
> - 보류 전표 2줄 기록 (복식부기: 출금 보류 +, 보류 계정 -)
> - 아웃박스 테이블에 디스패치 작업 등록 (트랜잭셔널 아웃박스 패턴)
>
> **③ 외부 호출 단계 (Server → Bank)**
> - 워커가 아웃박스에서 작업 읽기
> - `external_ref` 생성: 결정적 해시(송금계좌+수취계좌+금액+날짜)
> - 은행 API 호출, status → DISPATCHED로 조건부 업데이트
> - 실패 시 지수 백오프로 재시도 (동일 external_ref 유지)
>
> **④ 응답/웹훅 처리 단계 (Bank → Server)**
> - 웹훅 수신 시 `event_id`로 중복 체크 (UNIQUE 제약)
> - 웹훅 먼저 저장 → 상태 조건부 업데이트
> - 성공: DISPATCHED/EXPIRED → SETTLED, 보류 → 실제 전표 전환
> - 실패: DISPATCHED/EXPIRED → FAILED, 보류 롤백 전표 기록
>
> **⑤ 타임아웃 처리**
> - 일정 시간 내 확정 없으면 DISPATCHED → EXPIRED
> - 사용자에게 "처리 중" 상태 표시
> - 늦은 웹훅이 오면 최종 상태로 전이

---

### 3. 다음 상황을 가정하였을 때 해결방안을 생각하고 서술하시오.

> **상황 1: 은행은 성공 처리했지만 네트워크 끊김으로 결과를 못 받음**
>
> | 문제 | 해결 방안 |
> |------|----------|
> | 응답 유실 | 동일 `external_ref`로 재시도 → 은행이 "이미 처리됨" 응답 |
> | 상태 불확실 | DISPATCHED 상태 유지, 타임아웃 후 EXPIRED로 전환 |
> | 이중 출금 위험 | 결정적 external_ref로 은행 측 멱등성 활용 |
>
> ```python
> # 재시도 로직
> try:
>     response = bank_api.transfer(external_ref=transfer.external_ref, ...)
> except Timeout:
>     # 상태는 DISPATCHED 유지, 재시도 스케줄링
>     schedule_retry(transfer.id, backoff=exponential)
> else:
>     if response.status == 'ALREADY_PROCESSED':
>         # 이미 성공한 것으로 처리
>         update_status_if(transfer.id, from=['DISPATCHED'], to='SETTLED')
> ```
>
> **추가 안전장치:**
> - 매일 대사(Reconciliation): 은행 거래목록과 우리 장부를 external_ref로 대조
> - 불일치 발견 시 알림 및 수동 검토
>
> ---
>
> **상황 2: 은행이 응답을 못 줬지만 웹훅이 뒤늦게 옴**
>
> | 문제 | 해결 방안 |
> |------|----------|
> | 응답 없이 웹훅만 수신 | 웹훅 event_id로 중복 체크 후 상태 전이 |
> | 순서 역전 | 조건부 업데이트로 안전하게 처리 |
> | EXPIRED 상태에서 웹훅 | EXPIRED도 비종단 상태로 설계하여 수용 |
>
> ```python
> # 웹훅 처리
> def handle_webhook(event_id, transfer_ref, status):
>     # 1. 웹훅 중복 체크 (event_id UNIQUE)
>     if WebhookEvent.objects.filter(event_id=event_id).exists():
>         return  # 이미 처리됨
>     
>     # 2. 웹훅 먼저 저장
>     WebhookEvent.objects.create(event_id=event_id, payload=...)
>     
>     # 3. 조건부 상태 업데이트
>     transfer = Transfer.objects.get(external_ref=transfer_ref)
>     if status == 'SUCCESS':
>         # DISPATCHED 또는 EXPIRED일 때만 SETTLED로
>         updated = Transfer.objects.filter(
>             id=transfer.id,
>             status__in=['DISPATCHED', 'EXPIRED']
>         ).update(status='SETTLED', settled_at=now())
>         
>         if updated:
>             finalize_ledger_entries(transfer)  # 보류 → 확정 전표
> ```
>
> **핵심 원칙:**
> - 웹훅 저장이 상태 변경보다 먼저 (원자성)
> - 종단 상태(SETTLED, FAILED)는 덮어쓰기 불가
> - 시간 순서가 아닌 현재 상태 값으로만 판단

---

## 백엔드 – 논리적사고문제: 외부 API 집계 게이트웨이 설계

### 1. 게이트웨이 FSM을 설계하시오.

> **1-1. 집계 요청 단위의 상태 정의 및 전이 규칙**
>
> | 상태 | 설명 |
> |------|------|
> | INIT | 요청 수신, 캐시 조회 전 |
> | FETCHING | 상류 API 병렬 호출 중 |
> | PARTIAL | 일부 상류 성공, 일부 실패/타임아웃 |
> | COMPLETE | 모든 상류 성공 |
> | SERVED | 응답 반환 완료 |
>
> ```
> INIT → (캐시 히트) → SERVED
>   ↓
> FETCHING → COMPLETE → SERVED
>         ↘ PARTIAL → SERVED
> ```
>
> **조건부 업데이트:**
> ```python
> # 모든 상류 완료 시에만 COMPLETE로 전이
> if all(upstream.status == 'SUCCESS' for upstream in upstreams):
>     request.status = 'COMPLETE'
> elif any(upstream.status in ['FAILED', 'TIMEOUT'] for upstream in upstreams):
>     request.status = 'PARTIAL'
> ```
>
> ---
>
> **1-2. 상류별 서브상태와 전체 응답 상태 매핑**
>
> | 서브상태 | 설명 |
> |---------|------|
> | INIT | 호출 전 |
> | IN_FLIGHT | 요청 전송됨, 응답 대기 |
> | SUCCESS | 2xx 응답 수신 |
> | FAILED | 4xx/5xx 또는 파싱 오류 |
> | STALE | 캐시된 오래된 데이터 사용 |
> | CB_OPEN | 회로차단기 열림, 호출 우회 |
>
> **매핑 규칙:**
> | FX | Weather | News | 전체 상태 | 응답 |
> |----|---------|------|----------|------|
> | SUCCESS | SUCCESS | SUCCESS | COMPLETE | 200 OK |
> | SUCCESS | SUCCESS | STALE | PARTIAL | 200 + partial 플래그 |
> | SUCCESS | CB_OPEN | FAILED | PARTIAL | 200 + 폴백 데이터 |
> | FAILED | FAILED | FAILED | - | 503 Service Unavailable |
>
> ---
>
> **1-3. 캐시 쓰기 시점/조건과 갱신 충돌 방지**
>
> **캐시 쓰기 조건:**
> - 상류가 SUCCESS일 때만 캐시 저장
> - STALE 응답(304)은 TTL만 갱신, 데이터는 유지
> - FAILED/CB_OPEN 시 캐시 쓰기 안 함
>
> **동시 요청 충돌 방지 (Singleflight 패턴):**
> ```python
> # 동일 캐시 키에 대해 하나의 요청만 상류 호출
> async def fetch_with_singleflight(cache_key, fetch_fn):
>     if cache_key in in_flight_requests:
>         return await in_flight_requests[cache_key]
>     
>     future = asyncio.create_task(fetch_fn())
>     in_flight_requests[cache_key] = future
>     try:
>         result = await future
>         cache.set(cache_key, result, ttl=300)
>         return result
>     finally:
>         del in_flight_requests[cache_key]
> ```
>
> ---
>
> **1-4. 회로차단기와 FSM 상호작용**
>
> | CB 상태 | FSM 동작 |
> |---------|----------|
> | CLOSED | 정상 호출, 실패 카운트 누적 |
> | OPEN | 호출 우회, 즉시 CB_OPEN 서브상태, 캐시 폴백 |
> | HALF_OPEN | 제한적 테스트 호출, 성공 시 CLOSED 전환 |
>
> ```python
> async def call_upstream(upstream_name, params):
>     cb = circuit_breakers[upstream_name]
>     
>     if cb.state == 'OPEN':
>         # 캐시 폴백 시도
>         cached = cache.get(make_key(upstream_name, params))
>         if cached:
>             return UpstreamResult(status='STALE', data=cached, from_cb=True)
>         return UpstreamResult(status='CB_OPEN', data=None)
>     
>     try:
>         result = await http_client.get(upstream_url, timeout=READ_TIMEOUT)
>         cb.record_success()
>         return UpstreamResult(status='SUCCESS', data=result)
>     except Exception as e:
>         cb.record_failure()
>         # 실패 시에도 stale 캐시 폴백
>         return fallback_to_cache(upstream_name, params)
> ```

---

### 2. 처리 흐름에 대해 자세히 설명하시오.

> **2-1. 전체 처리 단계**
>
> **① 파라미터 정규화 → 캐시 키 생성**
> ```python
> def normalize_params(params):
>     # 키 정렬, 소문자화, 기본값 대입
>     normalized = {k.lower(): v for k, v in sorted(params.items())}
>     normalized.setdefault('locale', 'en')
>     normalized.setdefault('lang', 'en')
>     return normalized
>
> def make_cache_key(endpoint, params, version='v1'):
>     normalized = normalize_params(params)
>     param_hash = hashlib.sha256(json.dumps(normalized).encode()).hexdigest()[:16]
>     return f"{version}:{endpoint}:{param_hash}"
> ```
>
> **② 캐시 조회**
> - 히트 시 즉시 반환 (신선 캐시)
> - 미스 시 상류 호출 진행
> - Stale 캐시는 폴백용으로 보관
>
> **③ 병렬 상류 호출**
> ```python
> async def fetch_all_upstreams(params):
>     tasks = [
>         fetch_upstream('fx', params, timeout=150, retries=2),
>         fetch_upstream('weather', params, timeout=150, retries=2),
>         fetch_upstream('news', params, timeout=150, retries=2),
>     ]
>     results = await asyncio.gather(*tasks, return_exceptions=True)
>     return results
> ```
>
> **④ ETag/If-None-Match 재검증**
> ```python
> async def fetch_with_etag(url, cached_etag):
>     headers = {'If-None-Match': cached_etag} if cached_etag else {}
>     response = await http_client.get(url, headers=headers)
>     
>     if response.status == 304:
>         # 캐시 TTL만 갱신
>         return CacheHit(refresh_ttl=True)
>     return response
> ```
>
> **⑤ 부분 실패 판단과 폴백 순서**
> - 1순위: 신선 캐시 (TTL 내)
> - 2순위: Stale 캐시 (TTL 초과, maxAge 내)
> - 3순위: 축약 응답/해당 필드 생략
>
> **⑥ 응답 조립**
> ```json
> {
>   "data": { "fx": {...}, "weather": {...}, "news": null },
>   "meta": {
>     "partial": true,
>     "sources": [
>       {"name": "fx", "status": "fresh", "age": 12},
>       {"name": "weather", "status": "fresh", "age": 5},
>       {"name": "news", "status": "stale", "age": 600}
>     ],
>     "trace_id": "abc123"
>   }
> }
> ```
>
> **⑦ 캐시 저장 및 로깅**
> - SUCCESS인 상류만 캐시 저장
> - 구조적 로깅: trace_id, 각 상류 응답시간, 상태, 폴백 여부
>
> ---
>
> **2-2. 시간 예산과 수치 설정**
>
> | 항목 | 값 | 근거 |
> |------|-----|------|
> | 전역 예산 | 600ms (p95) | 사용자 체감 한계 |
> | read_timeout | 150ms | 3개 상류 병렬 + 처리 오버헤드 고려 |
> | 재시도 최대 | 2회 | 150ms × 3 = 450ms < 600ms |
> | 재시도 백오프 | 지수 + 지터 (50~100ms) | 상류 부하 분산 |
> | CB 실패 임계 | 5회/10초 | 빠른 장애 감지 |
> | CB OPEN 유지 | 30초 | 상류 복구 대기 |
>
> ---
>
> **2-3. 레이트리밋 키 스코프와 초과 시 처리**
>
> | 레벨 | 키 스코프 | 이유 |
> |------|----------|------|
> | 클라이언트별 | API Key + IP | 악의적 클라이언트 격리 |
> | 상류별 | upstream:fx | 상류 API 계약 준수 |
> | 전역 | gateway:total | 전체 시스템 보호 |
>
> **초과 시 처리:**
> ```python
> if rate_limiter.is_exceeded(client_key):
>     # 1순위: 캐시 폴백
>     cached = cache.get(cache_key)
>     if cached:
>         return Response(cached, headers={'X-Rate-Limited': 'true'})
>     
>     # 2순위: 429 반환
>     return Response(status=429, headers={
>         'Retry-After': rate_limiter.retry_after(client_key)
>     })
> ```

---

### 3. 상황별 해결방안

> **상황 1: A, C 성공 / B 타임아웃 (stale 캐시 존재, 10분 경과)**
>
> **응답 본문 구성:**
> ```json
> {
>   "data": {
>     "fx": { /* A 신선 데이터 */ },
>     "weather": { /* B stale 데이터, 필드 완전 포함 */ },
>     "news": { /* C 신선 데이터 */ }
>   },
>   "meta": {
>     "partial": true,
>     "stale": true,
>     "sources": [
>       {"name": "fx", "status": "fresh", "age": 0, "cached": false},
>       {"name": "weather", "status": "stale", "age": 600, "cached": true, "reason": "timeout"},
>       {"name": "news", "status": "fresh", "age": 0, "cached": false}
>     ],
>     "trace_id": "xyz789"
>   }
> }
> ```
>
> **Stale-While-Revalidate 전략:**
> ```python
> # 응답 반환 후 백그라운드에서 B 재호출
> async def serve_with_swr(cache_key, stale_data):
>     # 즉시 stale 데이터 반환
>     response = make_response(stale_data, stale=True)
>     
>     # 백그라운드 재검증 (비동기)
>     asyncio.create_task(revalidate_upstream('weather', cache_key))
>     
>     return response
> ```
>
> **B 재호출 폭주 억제 (Singleflight):**
> ```python
> # 동일 키에 대해 하나의 재검증만 실행
> revalidation_locks = {}
>
> async def revalidate_upstream(name, cache_key):
>     if cache_key in revalidation_locks:
>         return  # 이미 재검증 중
>     
>     revalidation_locks[cache_key] = True
>     try:
>         result = await fetch_upstream(name, timeout=300)  # 여유 있는 타임아웃
>         if result.success:
>             cache.set(cache_key, result.data, ttl=300)
>     finally:
>         del revalidation_locks[cache_key]
> ```
>
> ---
>
> **상황 2: ETag 304 수신 + 캐시 키 정규화 미흡으로 중복 저장**
>
> **캐시 키 규칙 재정의:**
> ```python
> def make_normalized_cache_key(upstream, params, etag=None):
>     # 1. 버전 프리픽스
>     version = 'v2'
>     
>     # 2. 파라미터 정렬 + 소문자화
>     sorted_params = sorted(params.items())
>     normalized = {k.lower(): str(v).lower() for k, v in sorted_params}
>     
>     # 3. locale/lang 정규화
>     locale = normalized.get('locale', normalized.get('lang', 'en'))
>     normalized['locale'] = locale
>     normalized.pop('lang', None)  # lang은 locale로 통합
>     
>     # 4. 해시 생성
>     param_str = json.dumps(normalized, sort_keys=True)
>     param_hash = hashlib.sha256(param_str.encode()).hexdigest()[:16]
>     
>     # 5. ETag는 별도 메타데이터로 저장 (키에 포함 X)
>     return f"{version}:{upstream}:{param_hash}"
> ```
>
> **무효화/마이그레이션 절차:**
> ```python
> # 롤링 배포 중 호환성 (구·신 공존)
> def get_with_migration(params):
>     new_key = make_normalized_cache_key_v2(params)
>     old_key = make_cache_key_v1(params)
>     
>     # 신규 키 우선 조회
>     result = cache.get(new_key)
>     if result:
>         return result
>     
>     # 구 키 폴백 + 마이그레이션
>     result = cache.get(old_key)
>     if result:
>         cache.set(new_key, result)  # 신규 키로 복사
>         cache.delete(old_key)       # 구 키 삭제 (점진적)
>         return result
>     
>     return None
> ```
>
> **304 수신 시 TTL 갱신:**
> ```python
> if response.status == 304:
>     # 데이터는 유지, TTL만 리프레시
>     cache.touch(cache_key, ttl=300)
>     
>     # ETag 메타데이터 갱신
>     cache.set(f"{cache_key}:etag", response.headers['ETag'], ttl=300)
> ```
>
> **롤링 배포 호환성 전략:**
> 1. 신규 코드는 v2 키 생성, v1 키도 읽기 가능
> 2. 읽기 시 v1 → v2 자동 마이그레이션
> 3. 배포 완료 후 v1 키 TTL 만료로 자연 정리
> 4. 모니터링: v1 키 히트율 추적, 0%되면 v1 로직 제거
