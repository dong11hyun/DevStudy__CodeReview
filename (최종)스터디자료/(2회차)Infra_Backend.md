# 백엔드 & 인프라 스터디 2회차 문제

**2025-10-03**  
**작성자: 김호중**

---

## 백엔드 – 논리적사고문제: 병렬프로그래밍

### 상황

당신은 전문 포토그래퍼와 이커머스 기업을 위한 B2B 클라우드 이미지 처리 플랫폼의 백엔드 엔지니어로 일하고 있습니다. 고객은 수백, 수천 장에 달하는 고해상도 RAW 이미지 파일(개당 50~100MB)을 업로드하고, 우리는 이 이미지들에 대해 다음과 같은 순차적인 처리 파이프라인을 실행하여 최종 결과물을 생성합니다.

**처리 파이프라인:**
1. **디코딩**: RAW 이미지 파일을 읽어 메모리 상의 비트맵 데이터로 변환
2. **리사이징**: 다양한 디바이스에 맞게 여러 해상도(4K, 1080p, 썸네일 등) 버전 생성
3. **필터 적용**: 가우시안 블러, 샤프닝 등 CPU 연산량이 매우 높은 커스텀 필터 적용
4. **워터마킹**: 고객사의 로고 이미지를 반투명하게 오버레이
5. **인코딩 및 저장**: 처리된 이미지를 JPEG, PNG 등 최종 포맷으로 변환하여 클라우드 스토리지에 저장

초기 버전의 처리기는 단일 스레드 Python 스크립트로 작성되었습니다. 이 스크립트는 32코어의 최신 CPU를 탑재한 서버에서 실행됨에도 불구하고, 단 하나의 CPU 코어만 사용하며 나머지 31개 코어는 유휴 상태로 남아있습니다. 이로 인해 수천 장의 이미지를 처리하는 배치 작업이 몇 시간씩 소요되어 고객의 불만이 증가하고 있습니다.

---

### 1. CPU-bound 워크로드에서 멀티프로세싱을 선택해야 하는 이유를 Python GIL과 연관지어 설명하시오.

> **Python GIL (Global Interpreter Lock):**
> - CPython 인터프리터가 한 번에 하나의 스레드만 Python 바이트코드를 실행하도록 강제하는 뮤텍스
> - 멀티스레딩을 해도 CPU-bound 작업은 실제로 병렬 실행되지 않음
>
> **멀티스레딩 vs 멀티프로세싱:**
>
> | 구분 | 멀티스레딩 | 멀티프로세싱 |
> |------|-----------|-------------|
> | **GIL 영향** | 받음 (CPU-bound 병렬화 불가) | 받지 않음 (프로세스별 독립 GIL) |
> | **메모리 사용량** | 낮음 (주소 공간 공유) | 높음 (프로세스별 독립 메모리) |
> | **컨텍스트 스위칭 비용** | 낮음 | 높음 |
> | **적합한 워크로드** | I/O-bound | CPU-bound |
>
> **이미지 처리는 CPU-bound 작업이므로:**
> ```python
> # 멀티스레딩 (GIL로 인해 병렬화 안됨)
> from concurrent.futures import ThreadPoolExecutor
> # 32개 스레드를 만들어도 1코어만 사용
>
> # 멀티프로세싱 (각 프로세스가 독립된 GIL 보유)
> from multiprocessing import Pool
> with Pool(32) as p:
>     p.map(process_image, image_list)
> # 32코어 모두 활용 가능
> ```
>
> **트레이드오프:**
> - 멀티프로세싱은 프로세스당 메모리 복사로 RAM 사용량 증가
> - 프로세스 생성/전환 비용이 스레드보다 높음
> - 그러나 CPU-bound에서는 이 오버헤드를 감수해도 32배 성능 향상이 가치 있음

---

### 2. 공유 카운터의 경쟁 상태(Race Condition) 문제와 해결 방안을 설명하시오.

> **경쟁 상태 발생 과정 (읽기-수정-쓰기 문제):**
>
> ```
> 시간  | 프로세스 A              | 프로세스 B              | total_processed
> -----|------------------------|------------------------|----------------
>  t1  | 읽기: total = 100      |                        | 100
>  t2  |                        | 읽기: total = 100      | 100
>  t3  | 수정: 100 + 1 = 101    |                        | 100
>  t4  |                        | 수정: 100 + 1 = 101    | 100
>  t5  | 쓰기: total = 101      |                        | 101
>  t6  |                        | 쓰기: total = 101      | 101  ← 102여야 함!
> ```
>
> **문제:** 2개의 이미지를 처리했지만 카운터는 1만 증가
>
> **해결 방안 - multiprocessing.Lock 사용:**
> ```python
> from multiprocessing import Process, Value, Lock
>
> def process_image(image_path, counter, lock):
>     # 이미지 처리 로직...
>     
>     # 임계 구역(Critical Section) - 원자적 연산 보장
>     with lock:
>         counter.value += 1
>
> if __name__ == '__main__':
>     counter = Value('i', 0)  # 공유 정수
>     lock = Lock()
>     
>     processes = []
>     for path in image_paths:
>         p = Process(target=process_image, args=(path, counter, lock))
>         processes.append(p)
>         p.start()
>     
>     for p in processes:
>         p.join()
>     
>     print(f"총 처리: {counter.value}")  # 정확한 값 보장
> ```
>
> **Lock의 원자성 보장:**
> - `with lock:`으로 임계 구역 진입 시 다른 프로세스는 대기
> - 읽기-수정-쓰기가 중단 없이 완료된 후에야 다른 프로세스 접근 허용

---

### 3. 거대한 데이터 전달의 IPC 병목 문제와 해결책을 설명하시오.

> **현재 방식의 문제점:**
> ```python
> # 문제: 100MB 비트맵을 각 워커에 전달
> with Pool(32) as p:
>     results = p.map(apply_filter, [bitmap1, bitmap2, ...])
>     # pickle 직렬화 → 파이프 전송 → 역직렬화
>     # 100MB × 1000장 = 100GB 복사 오버헤드!
> ```
>
> **직렬화/데이터 복사 오버헤드:**
> - pickle 직렬화: CPU 시간 소모
> - 프로세스 간 파이프 전송: 메모리 대역폭 병목
> - 역직렬화: 다시 CPU 시간 소모
> - 메모리 중복: 원본 + 직렬화된 데이터 + 워커의 복사본
>
> **해결책 - 파일 경로만 전달:**
> ```python
> def process_image_complete(file_path):
>     """워커가 독립적으로 전체 파이프라인 수행"""
>     # 1. 디코딩 (워커 내부에서 파일 읽기)
>     bitmap = decode_raw(file_path)
>     
>     # 2-4. 리사이징, 필터, 워터마크
>     processed = apply_pipeline(bitmap)
>     
>     # 5. 저장 (워커가 직접 S3 업로드)
>     output_path = upload_to_s3(processed)
>     
>     return {"input": file_path, "output": output_path, "status": "success"}
>
> with Pool(32) as p:
>     # 파일 경로 문자열만 전달 (수십 바이트)
>     results = p.map(process_image_complete, file_paths)
> ```
>
> **장점:**
> - IPC 데이터량: 100MB → 수십 바이트 (경로 문자열)
> - 워커 독립성: 각 워커가 자체적으로 파일 I/O 수행
> - 메모리 효율: 동시에 32개 이미지만 메모리에 로드

---

### 4. 암달의 법칙(Amdahl's Law) 관점에서 병렬화 한계를 분석하시오.

> **암달의 법칙:**
> ```
> 최대 속도 향상 = 1 / (S + P/N)
> 
> S = 순차 실행 부분 비율
> P = 병렬화 가능 부분 비율 (S + P = 1)
> N = 프로세서 개수
> ```
>
> **이미지 처리 파이프라인 분석:**
>
> | 작업 | 유형 | 이유 |
> |------|------|------|
> | 파일 목록 로드 | 순차 | 메인 프로세스에서 수행 |
> | 작업 분배 | 순차 | Pool.map() 내부 분배 로직 |
> | 개별 이미지 처리 | 병렬 | 이미지 간 의존성 없음 |
> | 결과 취합 | 순차 | 메인 프로세스에서 수집 |
> | 최종 보고서 생성 | 순차 | 모든 결과 필요 |
>
> **예시 계산:**
> ```
> 전체 작업 시간: 100초
> 순차 부분(S): 5초 → 5%
> 병렬 부분(P): 95초 → 95%
>
> N = 32 코어일 때:
> 최대 속도 향상 = 1 / (0.05 + 0.95/32)
>                = 1 / (0.05 + 0.0297)
>                = 1 / 0.0797
>                ≈ 12.5배
> ```
>
> **결론:**
> - 32코어를 사용해도 최대 12.5배 향상 (32배가 아님)
> - 순차 부분 5%가 병목이 되어 성능 상한 결정
> - 더 많은 코어를 추가해도 수확 체감 (N→∞이면 최대 20배)

---

### 5. 교착 상태(Deadlock) 발생 조건과 예방책을 설명하시오.

> **시나리오:**
> ```
> 프로세스 A: 필터 라이선스 획득 → 워터마크 라이선스 대기
> 프로세스 B: 워터마크 라이선스 획득 → 필터 라이선스 대기
> → 상호 대기로 인한 교착 상태!
> ```
>
> **교착 상태의 4가지 필요조건 (Coffman 조건):**
>
> | 조건 | 설명 | 현재 상황 |
> |------|------|----------|
> | **상호 배제** | 자원은 한 번에 하나의 프로세스만 사용 | 라이선스는 동시 사용 불가 |
> | **점유 대기** | 자원을 보유한 채 다른 자원 대기 | 필터 보유 + 워터마크 대기 |
> | **비선점** | 강제로 자원을 빼앗을 수 없음 | 라이선스 강제 회수 불가 |
> | **환형 대기** | 순환적으로 서로의 자원 대기 | A→B→A 순환 |
>
> **해결책 - 자원 획득 순서 강제 (환형 대기 방지):**
> ```python
> # 모든 프로세스가 동일한 순서로 자원 획득
> RESOURCE_ORDER = ['filter_license', 'watermark_license']
>
> def acquire_resources(needed_resources):
>     # 항상 정해진 순서로 정렬하여 획득
>     sorted_resources = sorted(needed_resources, 
>                               key=lambda x: RESOURCE_ORDER.index(x))
>     
>     acquired = []
>     for resource in sorted_resources:
>         locks[resource].acquire()
>         acquired.append(resource)
>     
>     return acquired
>
> # 사용
> resources = acquire_resources(['watermark_license', 'filter_license'])
> # 실제로는 filter → watermark 순서로 획득됨
> ```
>
> **왜 효과적인가:**
> - 환형 대기 조건 제거 (순환 구조 형성 불가능)
> - 모든 프로세스가 filter→watermark 순서를 따름
> - A가 filter를 보유하면 B는 filter를 먼저 기다림 (워터마크 선점 안 함)

---

## 인프라 심층 탐구: 단일 서버의 한계와 분산 시스템

### 상황

당신은 책 추천 및 독서 클럽 소셜 플랫폼 'BookNook'의 첫 인프라 개발자로 합류했습니다. 현재 전체 인프라는 클라우드의 **단일 가상 서버(EC2 t3.medium)** 한 대로 운영되고 있습니다.

**현재 구성:**
- Django 백엔드 (Gunicorn)
- PostgreSQL 데이터베이스
- Nginx 웹 서버
- DNS: booknook.com → 단일 서버 IP

유명 북튜버의 극찬 영상 이후 트래픽이 20배 폭증하며 서비스가 중단되었습니다.

---

### 1. V1 아키텍처의 단일 실패 지점(SPOF)을 분석하시오.

> **단일 실패 지점(Single Point of Failure) 분석:**
>
> ```
> 사용자 → DNS → [단일 서버] → 응답
>                    ↓
>          ┌─────────────────┐
>          │   EC2 Instance  │
>          │  ┌───────────┐  │
>          │  │   Nginx   │←─┼── SPOF #1: 웹서버
>          │  └─────┬─────┘  │
>          │        ↓        │
>          │  ┌───────────┐  │
>          │  │ Gunicorn  │←─┼── SPOF #2: 앱서버
>          │  └─────┬─────┘  │
>          │        ↓        │
>          │  ┌───────────┐  │
>          │  │PostgreSQL │←─┼── SPOF #3: 데이터베이스
>          │  └───────────┘  │
>          └─────────────────┘
>                    ↑
>             SPOF #4: EC2 인스턴스 자체
>             SPOF #5: 가용 영역 (AZ)
> ```
>
> **각 SPOF의 영향:**
>
> | SPOF | 장애 시 결과 |
> |------|-------------|
> | Nginx | 모든 HTTP 요청 처리 불가 |
> | Gunicorn | Django 앱 실행 불가 |
> | PostgreSQL | 모든 데이터 읽기/쓰기 불가 |
> | EC2 인스턴스 | 위 세 가지 모두 동시 중단 |
> | 가용 영역 | 데이터센터 전체 장애 시 복구 불가 |
>
> **결론:** 어느 하나라도 장애 발생 시 전체 서비스 중단

---

### 2. V2 아키텍처를 설계하고 트래픽 흐름을 설명하시오.

> **V2 아키텍처 설계:**
>
> ```
> 사용자
>    ↓
> [Route 53] ─── DNS 조회
>    ↓
> [Application Load Balancer] ─── 트래픽 분산
>    ↓               ↓
> ┌──────┐       ┌──────┐
> │ EC2  │       │ EC2  │ ←── Auto Scaling Group
> │ AZ-a │       │ AZ-b │     (최소 2, 최대 10)
> └──┬───┘       └──┬───┘
>    └───────┬──────┘
>            ↓
>    [RDS PostgreSQL]
>    (Multi-AZ 구성)
> ```
>
> **트래픽 흐름 단계별 설명:**
>
> | 단계 | 컴포넌트 | 역할 |
> |------|----------|------|
> | 1 | Route 53 | booknook.com → ALB DNS 이름으로 해석 |
> | 2 | Internet Gateway | VPC로 트래픽 진입 허용 |
> | 3 | ALB | 헬스체크 기반으로 건강한 인스턴스에 분산 |
> | 4 | EC2 (AZ-a 또는 AZ-b) | Django 앱 요청 처리 |
> | 5 | RDS (Multi-AZ) | 데이터 조회/저장, 자동 장애 조치 |
>
> **고가용성 확보:**
> - 다중 AZ 배포로 데이터센터 장애 대응
> - Auto Scaling으로 트래픽 변동 대응
> - ALB의 자동 장애 감지 및 우회

---

### 3. 다중 서버 환경에서 발생하는 상태 문제와 해결책을 제시하시오.

> **문제 1: 세션 정보 처리**
>
> ```
> 요청 1: 서버 A에서 로그인 → 세션 저장 (서버 A 메모리)
> 요청 2: 서버 B로 라우팅 → 세션 없음 → 로그인 풀림!
> ```
>
> **해결책: Redis 세션 스토어**
> ```python
> # settings.py
> SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
> SESSION_CACHE_ALIAS = 'default'
>
> CACHES = {
>     'default': {
>         'BACKEND': 'django_redis.cache.RedisCache',
>         'LOCATION': 'redis://elasticache-endpoint:6379/1',
>     }
> }
> ```
>
> ```
>        서버 A ──┐
>                 ├──→ [ElastiCache Redis] ←── 세션 중앙 저장
>        서버 B ──┘
> ```
>
> ---
>
> **문제 2: 프로필 이미지 파일 처리**
>
> ```
> 요청 1: 서버 A에서 이미지 업로드 → 서버 A 로컬 저장
> 요청 2: 서버 B에서 이미지 조회 → 파일 없음!
> ```
>
> **해결책: S3 중앙 스토리지**
> ```python
> # settings.py
> DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
> AWS_STORAGE_BUCKET_NAME = 'booknook-media'
> AWS_S3_REGION_NAME = 'ap-northeast-2'
> ```
>
> ```
>        서버 A ──┐
>                 ├──→ [S3 Bucket] ←── 파일 중앙 저장
>        서버 B ──┘
> ```
>
> **핵심 원칙:** 서버는 Stateless하게, 상태는 외부 서비스에 저장

---

### 4. 로드 밸런서의 헬스 체크와 자동 장애 복구를 설명하시오.

> **헬스 체크 동작 원리:**
>
> ```
> ALB ──GET /health──→ EC2-A (200 OK) ✓ 건강
>   ├──GET /health──→ EC2-B (200 OK) ✓ 건강
>   └──GET /health──→ EC2-C (503)     ✗ 비정상
> ```
>
> **헬스 체크 설정:**
> ```yaml
> HealthCheck:
>   Path: /health/
>   Protocol: HTTP
>   Port: 80
>   HealthyThreshold: 2      # 2번 연속 성공 → 건강
>   UnhealthyThreshold: 3    # 3번 연속 실패 → 비정상
>   Interval: 30             # 30초마다 체크
>   Timeout: 5               # 5초 내 응답 없으면 실패
> ```
>
> **자동 장애 복구 과정:**
>
> | 단계 | 시간 | 동작 |
> |------|------|------|
> | 1 | 0초 | EC2-C 장애 발생 |
> | 2 | 30초 | 첫 번째 헬스체크 실패 |
> | 3 | 60초 | 두 번째 헬스체크 실패 |
> | 4 | 90초 | 세 번째 헬스체크 실패 → EC2-C를 Target에서 제외 |
> | 5 | 90초~ | 모든 트래픽이 EC2-A, B로만 라우팅 |
> | 6 | 자동 | Auto Scaling이 새 인스턴스 시작 |
> | 7 | ~5분 | 새 인스턴스가 헬스체크 통과 후 트래픽 수신 |
>
> **고가용성 보장:** 사람의 개입 없이 자동으로 장애 감지 및 복구

---

### 5. 비기술직 CEO에게 인프라 투자의 필요성을 설명하시오.

> **비즈니스 관점 설득 논리:**
>
> **1. 다운타임의 기회비용**
> ```
> 지난 장애 시:
> - 다운타임: 6시간
> - 시간당 예상 매출: 100만원
> - 직접 손실: 600만원
> 
> 간접 손실:
> - 사용자 이탈 (재가입률 30% 감소 추정)
> - 앱스토어 별점 하락 (4.5→3.2)
> - SNS 부정 여론 확산
> ```
>
> **2. 투자 유치 영향**
> > "투자자는 기술적 리스크를 평가합니다. 단일 서버 아키텍처는 
> > Due Diligence 과정에서 심각한 레드플래그로 작용합니다."
>
> **3. 비용 대비 효과**
>
> | 항목 | V1 (현재) | V2 (제안) |
> |------|----------|----------|
> | 월 인프라 비용 | $50 | $300 |
> | 연간 추가 비용 | - | $3,000 |
> | 장애 시 손실 | $6,000+/회 | 거의 0 |
> | 확장 가능 트래픽 | 1x | 100x+ |
>
> **4. 성장 기회**
> > "다음 바이럴이 터졌을 때, 우리는 준비되어 있을 겁니다.
> > 지금의 투자는 미래 100배 성장을 위한 기반입니다."
>
> **핵심 메시지:** 
> "월 $250 추가 투자로 연간 수천만 원의 잠재적 손실을 예방하고,
> 투자 유치 및 사용자 신뢰를 확보할 수 있습니다."

---

## 인프라 심층 탐구: B2B SaaS 비동기 아키텍처

### 상황

당신은 B2B SaaS 스타트업의 인프라 개발자입니다. 핵심 서비스는 고객사 마케팅팀이 업로드한 대용량 원본 데이터를 기반으로 마케팅 성과 분석 리포트를 생성하는 웹 애플리케이션입니다.

**현재 문제점:**
- 리포트 생성에 5~10분 소요, 웹 서버가 동기적으로 처리
- 브라우저 타임아웃 발생
- Auto Scaling 축소 시 작업 중인 서버 종료로 작업 유실
- 생성된 리포트(1~2GB)가 웹 서버 로컬에 임시 저장
- EC2에 AWS 액세스 키 하드코딩으로 보안 위험

---

### 1. 웹 티어와 작업 티어를 분리하는 비동기 아키텍처를 설계하시오.

> **비동기 처리 아키텍처:**
>
> ```
> [사용자] ──POST /reports──→ [웹 서버]
>                                 │
>                    ┌────────────┴────────────┐
>                    ↓                         ↓
>              즉시 응답                   메시지 전송
>         202 Accepted                        │
>         {job_id: "abc123"}                  ↓
>                                        [SQS Queue]
>                                             │
>                                             ↓
>                                      [워커 인스턴스]
>                                      (별도 ASG)
>                                             │
>                                             ↓
>                                        리포트 생성
>                                        (5~10분)
>                                             │
>                                             ↓
>                                         [S3 저장]
> ```
>
> **처리 흐름:**
>
> | 단계 | 컴포넌트 | 동작 |
> |------|----------|------|
> | 1 | 웹 서버 | 요청 수신, job_id 생성, DB에 상태='대기중' 저장 |
> | 2 | 웹 서버 | SQS에 메시지 전송 (job_id, 파라미터) |
> | 3 | 웹 서버 | 즉시 202 Accepted 응답 반환 |
> | 4 | 워커 | SQS에서 메시지 수신, 상태='처리중' 업데이트 |
> | 5 | 워커 | 리포트 생성 (5~10분) |
> | 6 | 워커 | S3에 리포트 업로드, 상태='완료' 업데이트 |
> | 7 | 사용자 | GET /reports/{job_id}로 상태 폴링 |
>
> **장점:**
> - 웹 서버 응답성 유지 (밀리초 단위 응답)
> - 워커 독립 스케일링 (작업량에 따라)
> - 작업 유실 방지 (SQS 메시지 지속성)

---

### 2. S3와 Pre-Signed URL을 활용한 데이터 흐름과 상태 관리를 설명하시오.

> **데이터 흐름:**
>
> ```
> 워커 ──리포트(2GB)──→ S3 버킷 (비공개)
>                          │
>                          ↓
>              s3://reports/abc123.pdf
>                          │
> 사용자 ←──Pre-Signed URL──┘
>   ↓
> 직접 다운로드 (서버 경유 없음)
> ```
>
> **상태 관리 (DB 테이블):**
> ```sql
> CREATE TABLE report_jobs (
>     job_id UUID PRIMARY KEY,
>     status ENUM('pending', 'processing', 'completed', 'failed'),
>     created_at TIMESTAMP,
>     completed_at TIMESTAMP,
>     s3_key VARCHAR(255),
>     error_message TEXT
> );
> ```
>
> **사용자 상태 조회 API:**
> ```json
> GET /reports/abc123
> {
>     "job_id": "abc123",
>     "status": "completed",
>     "download_url": "https://s3...?X-Amz-Signature=...",
>     "expires_in": 3600
> }
> ```
>
> **Pre-Signed URL 동작 원리:**
> ```python
> import boto3
>
> s3_client = boto3.client('s3')
>
> # 1시간 동안 유효한 다운로드 URL 생성
> url = s3_client.generate_presigned_url(
>     'get_object',
>     Params={'Bucket': 'reports', 'Key': 'abc123.pdf'},
>     ExpiresIn=3600
> )
> # URL에 서명(Signature) 포함 → 유효 기간 내 인증 없이 접근 가능
> ```
>
> **장점:**
> - S3 버킷 비공개 유지 (보안)
> - 서버 대역폭 절약 (직접 S3에서 다운로드)
> - 시간 제한 접근 (만료 후 URL 무효)

---

### 3. IAM 역할(Role)을 사용한 안전한 권한 부여 방식을 설명하시오.

> **문제: 액세스 키 하드코딩**
> ```python
> # ❌ 절대 하면 안 되는 방식
> AWS_ACCESS_KEY_ID = 'AKIA...'
> AWS_SECRET_ACCESS_KEY = 'wJalrXUtnFE...'
> ```
> - 코드 저장소에 키 노출 위험
> - 키 유출 시 전체 AWS 계정 위험
> - 키 교체 시 모든 서버 재배포 필요
>
> **해결: IAM 역할(Role)**
>
> ```
> EC2 인스턴스 ──→ 인스턴스 메타데이터 서비스
>                   │
>                   ↓
>         임시 자격 증명 자동 발급
>         (Access Key + Secret + Session Token)
>                   │
>                   ↓ 자동 주입
>             boto3 SDK가 자동으로 사용
> ```
>
> **설정:**
> ```json
> // IAM Role 정책 (최소 권한 원칙)
> {
>     "Version": "2012-10-17",
>     "Statement": [
>         {
>             "Effect": "Allow",
>             "Action": ["s3:PutObject", "s3:GetObject"],
>             "Resource": "arn:aws:s3:::reports/*"
>         },
>         {
>             "Effect": "Allow",
>             "Action": ["sqs:ReceiveMessage", "sqs:DeleteMessage"],
>             "Resource": "arn:aws:sqs:*:*:report-queue"
>         }
>     ]
> }
> ```
>
> **왜 더 안전한가:**
>
> | 측면 | 액세스 키 | IAM 역할 |
> |------|----------|----------|
> | **자격 증명 교체** | 수동 (위험) | 자동 (매 시간) |
> | **유출 위험** | 코드/설정에 존재 | 인스턴스 외부 노출 없음 |
> | **최소 권한** | 사용자에게 과도한 권한 부여 경향 | 역할별 세밀한 권한 설정 |
> | **감사** | 어떤 인스턴스가 사용했는지 추적 어려움 | CloudTrail에서 인스턴스별 추적 |

---

### 4. SQS 기반 오토 스케일링과 서버리스(Fargate) 전략을 비교하시오.

> **전략 1: SQS 대기열 길이 기반 Auto Scaling**
>
> ```
> CloudWatch Alarm: ApproximateNumberOfMessages > 100
>                            ↓
>                    Auto Scaling 트리거
>                            ↓
>                    워커 인스턴스 추가
> ```
>
> ```yaml
> ScalingPolicy:
>   TargetTrackingConfiguration:
>     TargetValue: 10  # 인스턴스당 10개 메시지
>     CustomizedMetricSpecification:
>       MetricName: ApproximateNumberOfMessages
>       Namespace: AWS/SQS
> ```
>
> **전략 2: AWS Fargate (서버리스 컨테이너)**
>
> ```
> SQS ──→ Lambda (트리거) ──→ Fargate Task 시작
>                                  │
>                                  ↓
>                            컨테이너에서 처리
>                                  │
>                                  ↓
>                            완료 후 자동 종료
> ```
>
> **비교:**
>
> | 측면 | EC2 + ASG | Fargate |
> |------|-----------|---------|
> | **관리 오버헤드** | 높음 (AMI, 패치 등) | 낮음 (컨테이너만 관리) |
> | **비용 모델** | 인스턴스 시간 단위 | 요청/실행 시간 단위 |
> | **유휴 비용** | 최소 인스턴스 유지 비용 | 0 (실행 시만 과금) |
> | **콜드 스타트** | 수 분 (인스턴스 시작) | 수십 초 (컨테이너 시작) |
> | **장시간 작업** | 적합 | 적합 (Lambda는 15분 제한) |
>
> **추천:**
> - **월말 집중, 평소 거의 없음** → Fargate (유휴 비용 0)
> - **지속적 워크로드** → EC2 ASG (예약 인스턴스 할인)
> - **하이브리드** → 기본 EC2 + 피크 시 Fargate 버스팅

---

### 5. SQS Visibility Timeout과 Dead Letter Queue를 활용한 장애 복구를 설명하시오.

> **Visibility Timeout 동작:**
>
> ```
> 시간   SQS 대기열              워커 A
>  0초   [메시지] ─────────→ 수신 (처리 시작)
>        [보이지 않음]          │
>        Visibility Timeout     │
>        = 15분                  │ 리포트 생성 중...
>                                │
>  7분   [보이지 않음]          │
>                                │
> 10분   [보이지 않음]          ✗ 워커 A 비정상 종료!
>                                
> 15분   [메시지 다시 보임] ───→ 워커 B가 수신 (재처리)
> ```
>
> **설정:**
> ```python
> sqs.set_queue_attributes(
>     QueueUrl=queue_url,
>     Attributes={
>         'VisibilityTimeout': '900',  # 15분
>     }
> )
> ```
>
> **Dead Letter Queue (DLQ):**
>
> ```
> 메인 큐 ──실패 1회──→ 재시도
>          ──실패 2회──→ 재시도
>          ──실패 3회──→ DLQ로 이동
>                         │
>                         ↓
>                    [Dead Letter Queue]
>                    - 수동 검토
>                    - 알림 발송
>                    - 원인 분석
> ```
>
> ```json
> {
>     "RedrivePolicy": {
>         "deadLetterTargetArn": "arn:aws:sqs:*:*:report-dlq",
>         "maxReceiveCount": 3
>     }
> }
> ```
>
> **장애 복구 시나리오:**
>
> | 상황 | 동작 |
> |------|------|
> | 워커 충돌 | Visibility Timeout 후 다른 워커가 재처리 |
> | 반복 실패 | 3회 후 DLQ로 이동, 알림 발생 |
> | 일시적 오류 | 자동 재시도로 복구 |
> | 영구적 오류 | DLQ에서 분석 후 수동 처리 |
>
> **핵심:** 시스템이 "실패를 견딜 수 있도록" 설계됨

---

## 인프라 심층 탐구: AWS VPC 네트워크 설계

### 상황

당신은 민감한 개인 금융 정보를 다루는 FinTech 서비스 'SecureWallet'의 인프라 설계자입니다.

**아키텍처 요구사항:**
- 3-Tier 아키텍처 (웹/앱/DB)
- 앱 서버와 DB는 인터넷 직접 접근 불가
- 앱 서버는 외부 금융 API 호출 필요
- 고가용성 (단일 데이터센터 장애 대응)

---

### 1. VPC와 서브넷 구조를 설계하시오.

> **VPC CIDR 설계:**
> ```
> VPC: 10.0.0.0/16 (65,536 IP)
> ```
>
> **서브넷 구조 (2개 AZ):**
>
> | 서브넷 | CIDR | AZ | 용도 | 티어 |
> |--------|------|-----|------|------|
> | public-a | 10.0.1.0/24 | AZ-a | ALB, NAT GW | 웹 |
> | public-b | 10.0.2.0/24 | AZ-b | ALB, NAT GW | 웹 |
> | private-app-a | 10.0.11.0/24 | AZ-a | Django/Spring | 앱 |
> | private-app-b | 10.0.12.0/24 | AZ-b | Django/Spring | 앱 |
> | private-db-a | 10.0.21.0/24 | AZ-a | PostgreSQL | DB |
> | private-db-b | 10.0.22.0/24 | AZ-b | PostgreSQL | DB |
>
> **아키텍처 다이어그램:**
> ```
>                    ┌─── AZ-a ───┐    ┌─── AZ-b ───┐
>                    │            │    │            │
> Internet ──→ IGW ──┼→ public-a  │    │  public-b  │
>                    │  (ALB,NAT) │    │ (ALB,NAT)  │
>                    │     ↓      │    │     ↓      │
>                    │ private-   │    │ private-   │
>                    │   app-a    │    │   app-b    │
>                    │     ↓      │    │     ↓      │
>                    │ private-   │    │ private-   │
>                    │   db-a     │    │   db-b     │
>                    └────────────┘    └────────────┘
> ```
>
> **다중 AZ 이유:**
> - 단일 AZ 장애 시에도 서비스 지속
> - ALB가 건강한 AZ로 자동 라우팅
> - RDS Multi-AZ로 자동 페일오버

---

### 2. 사용자 요청이 애플리케이션 서버까지 도달하는 경로를 설명하시오.

> **패킷 여정 추적:**
>
> ```
> 1. 사용자 브라우저: securewallet.com 입력
>           ↓
> 2. [Route 53]
>    - DNS 해석: securewallet.com → ALB DNS
>    - 응답: alb-123.ap-northeast-2.elb.amazonaws.com
>           ↓
> 3. [Internet Gateway]
>    - VPC 진입 지점
>    - 공인 IP ↔ 사설 IP 변환
>           ↓
> 4. [라우팅 테이블 - Public Subnet]
>    - 0.0.0.0/0 → igw-xxx (인터넷)
>    - 10.0.0.0/16 → local (VPC 내부)
>           ↓
> 5. [Network ACL - Public Subnet]
>    - Stateless 방화벽
>    - 인바운드 443 허용
>           ↓
> 6. [Application Load Balancer]
>    - 헬스체크 기반 타겟 선택
>    - 앱 서버로 전달 (80번 포트)
>           ↓
> 7. [라우팅 테이블 - Private App Subnet]
>    - 10.0.0.0/16 → local
>           ↓
> 8. [보안 그룹 - App Server]
>    - 인바운드: ALB 보안 그룹에서 80 허용
>           ↓
> 9. [EC2 - Django/Spring]
>    - 요청 처리
> ```
>
> **각 컴포넌트 역할:**
>
> | 컴포넌트 | 역할 |
> |----------|------|
> | Route 53 | 도메인 → IP 변환 |
> | IGW | VPC ↔ 인터넷 연결 |
> | 라우팅 테이블 | 패킷 경로 결정 |
> | NACL | 서브넷 레벨 방화벽 |
> | ALB | 로드 분산, SSL 종료 |
> | 보안 그룹 | 인스턴스 레벨 방화벽 |

---

### 3. 프라이빗 서브넷에서 외부 인터넷 통신을 위한 NAT Gateway 설정을 설명하시오.

> **문제:**
> - 프라이빗 서브넷 → 인터넷 직접 불가
> - 하지만 외부 금융 API 호출 필요
>
> **해결: NAT Gateway**
>
> ```
> 프라이빗 서브넷 EC2
>         │
>         ↓ (10.0.11.5 → 외부 API)
> 라우팅 테이블: 0.0.0.0/0 → nat-gw
>         │
>         ↓
> [NAT Gateway] (퍼블릭 서브넷에 위치)
>    - 사설 IP → 공인 IP 변환
>    - 52.78.xxx.xxx로 변환
>         │
>         ↓
> [Internet Gateway] → 외부 API
> ```
>
> **라우팅 테이블 설정:**
>
> | 대상 | 타겟 | 서브넷 |
> |------|------|--------|
> | 10.0.0.0/16 | local | 공통 |
> | 0.0.0.0/0 | igw-xxx | 퍼블릭 |
> | 0.0.0.0/0 | nat-xxx | 프라이빗 |
>
> **NAT Gateway 배치:**
> ```
> ┌─── AZ-a ───────────────────────┐
> │  public-a                      │
> │    └─ NAT-GW-a (EIP 할당)      │
> │                                │
> │  private-app-a                 │
> │    └─ 라우팅: 0.0.0.0/0 → NAT-a│
> └────────────────────────────────┘
> 
> ┌─── AZ-b ───────────────────────┐
> │  public-b                      │
> │    └─ NAT-GW-b (EIP 할당)      │
> │                                │
> │  private-app-b                 │
> │    └─ 라우팅: 0.0.0.0/0 → NAT-b│
> └────────────────────────────────┘
> ```
>
> **특징:**
> - 아웃바운드(Egress) 전용 (외부 → 내부 직접 접근 불가)
> - AZ별 NAT GW로 고가용성 확보

---

### 4. 보안 그룹과 네트워크 ACL을 활용한 심층 방어 전략을 설계하시오.

> **보안 그룹 vs NACL 비교:**
>
> | 구분 | 보안 그룹 | NACL |
> |------|----------|------|
> | **상태** | Stateful | Stateless |
> | **적용 범위** | 인스턴스 (ENI) | 서브넷 |
> | **규칙 유형** | 허용만 | 허용/거부 |
> | **평가 순서** | 모든 규칙 | 번호 순서 |
> | **반환 트래픽** | 자동 허용 | 명시적 규칙 필요 |
>
> **보안 그룹 설계:**
>
> ```
> # SG-ALB (Application Load Balancer)
> Inbound:
>   - 443 from 0.0.0.0/0  (HTTPS)
> Outbound:
>   - 80 to SG-App
>
> # SG-App (애플리케이션 서버)
> Inbound:
>   - 80 from SG-ALB  ← "오직 ALB로부터만 허용"
> Outbound:
>   - 5432 to SG-DB
>   - 443 to 0.0.0.0/0 (외부 API)
>
> # SG-DB (데이터베이스)
> Inbound:
>   - 5432 from SG-App  ← "오직 앱 서버로부터만 허용"
> Outbound:
>   - (없음)
> ```
>
> **NACL 설계 (서브넷 레벨 광범위 규칙):**
>
> ```
> # NACL-Private-App
> Inbound:
>   100: ALLOW TCP 80 from 10.0.1.0/24 (public-a)
>   110: ALLOW TCP 80 from 10.0.2.0/24 (public-b)
>   200: DENY  TCP 22 from 0.0.0.0/0   ← "SSH 전면 차단"
>   *  : DENY  ALL
>
> Outbound:
>   100: ALLOW TCP 5432 to 10.0.21.0/24 (db-a)
>   110: ALLOW TCP 5432 to 10.0.22.0/24 (db-b)
>   200: ALLOW TCP 443 to 0.0.0.0/0   (외부 API)
>   300: ALLOW TCP 1024-65535 to 0.0.0.0/0 (응답)
>   *  : DENY  ALL
> ```
>
> **심층 방어:** NACL이 1차 방어, SG가 2차 방어로 다중 보안 계층

---

### 5. VPC 엔드포인트를 활용한 비용 절감과 보안 강화 방안을 제시하시오.

> **문제: NAT Gateway 비용 폭증**
>
> ```
> 앱 서버 ──로그──→ NAT GW ──→ Internet ──→ S3
>                    │
>              데이터 전송 비용!
>              (GB당 $0.045 + 처리 비용)
> ```
>
> **해결: VPC 엔드포인트**
>
> | 유형 | Gateway Endpoint | Interface Endpoint |
> |------|------------------|-------------------|
> | **지원 서비스** | S3, DynamoDB | 대부분의 AWS 서비스 |
> | **비용** | 무료 | 시간당 + 데이터 처리 |
> | **구현** | 라우팅 테이블 변경 | ENI (프라이빗 IP) |
> | **보안** | 정책 기반 | 보안 그룹 적용 |
>
> **Gateway Endpoint (S3):**
>
> ```
> 앱 서버 ──→ [Gateway Endpoint] ──→ S3
>             (라우팅 테이블 경유)
>             NAT GW 우회!
> ```
>
> ```yaml
> # 라우팅 테이블 자동 추가
> Destination: pl-xxx (S3 prefix list)
> Target: vpce-xxx (Gateway Endpoint)
> ```
>
> **Interface Endpoint (SSM):**
>
> ```
> 앱 서버 ──→ [ENI: 10.0.11.100] ──→ SSM
>             (프라이빗 서브넷 내 ENI)
>             인터넷 경유 없음!
> ```
>
> **비용 절감 효과:**
>
> | 항목 | NAT GW 경유 | VPC Endpoint |
> |------|------------|--------------|
> | S3 1TB 전송 | $45 + 처리비용 | $0 |
> | SSM 통신 | 데이터 비용 | $0.01/시간 |
>
> **보안 강화:**
> - 트래픽이 AWS 내부망만 통과 (인터넷 미경유)
> - S3 버킷 정책으로 VPC 엔드포인트 접근만 허용 가능
> ```json
> {
>     "Condition": {
>         "StringEquals": {
>             "aws:sourceVpce": "vpce-xxx"
>         }
>     }
> }
> ```