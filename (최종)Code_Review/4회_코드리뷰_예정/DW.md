## models.py

**아웃박스 패턴(Transactional Outbox Pattern)**은 **"데이터베이스에 데이터를 저장하는 것"**과 "외부 시스템(메시지 큐 등)으로 이벤트를 발행하는 것" 사이의 **데이터 정합성(Consistency)**을 보장하기 위해 사용하는 패턴입니다.

`transaction.on_commit`: 편지를 우체통에 넣는 작업(DB 트랜잭션)이 완전히 끝난 뒤에 우체부(Dispatch 함수)를 부르는 역할을 합니다.


>"DB 저장과 메시지 발송을 '동시에' 성공시키기 위해, 메시지도 일단 DB에 저장한 뒤, 나중에 꺼내 보내는 전략" 입니다.


---

## tx_basic.py

transaction.atomic()을 중첩해서 쓰면 **"거대한 트랜잭션 안에 안전한 체크포인트(Savepoint)를 만드는 것"**과 같습니다

def create_order
"동시에 여러 명이 주문하면 재고가 마이너스가 되지 않을까?"
👉 해결: select_for_update()로 해당 상품 행을 잠그고(Lock) 시작하는구나! (동시성 제어)

def charge_and_log
"장부 기록하다가 에러가 나면, 결체 처리된 것까지 다 취소해버려야 하나?"
👉 해결: with transaction.atomic():으로 내부만 감싸서, 실패해도 기록만 취소하고 결제 상태는 유지하는구나! (부분 롤백)


F 객체

더 확실한 원자성(Atomicity): 잠금이 혹시라도 풀리거나 실수로 누락되더라도, DB 레벨에서 stock = stock - 1 연산을 하므로 최소한 **"누군가의 업데이트를 덮어써서 숫자가 튀는 일"**은 절대 발생하지 않습니다.
성능(Performance): 값을 Python으로 가져왔다가 다시 보내는 왕복 과정(Round-trip) 없이 DB 안에서 바로 연산하므로 빠릅니다.

F() 객체의 단점 (Trade-off)

1. **메모리 값 불일치 (State Inconsistency)**
   - `F()`로 DB를 업데이트해도, 현재 내 손에 들고 있는 Python 객체(`p`)의 값은 바뀌지 않습니다.
   - **해결책**: `p.refresh_from_db()`를 호출해서 DB 값을 다시 가져와야 합니다.
```
p.stock = F('stock') - 1
p.save() 
# 1. 은행에 전화해서 1 깎으라고 함. (DB: 9로 변경됨)
# 2. 하지만 내 앱(p)은 아직 모름. 
print(p.stock) 
# -> 10 (아까 처음 가져왔던 그 숫자 그대로)
# -> 여기서 "어? 왜 안 깎였지?" 하고 당황할 수 있음.
p.refresh_from_db() 
# 3. 앱 새로고침! (DB에서 다시 숫자를 읽어옴)
print(p.stock) 
# -> 9 (이제야 DB랑 똑같아짐)
```

2. **save() 메서드 우회 (Validation Bypass)**
   - `update()` 메서드와 함께 `F()`를 쓰면 `model.save()`가 호출되지 않습니다.
   - 따라서 `save()` 메서드 안에 넣어둔 **커스텀 데이터 검증 로직이나 시그널(Signal)이 실행되지 않습니다.**

3. **복잡한 로직 구현의 한계**
   - "재고가 0보다 작아지면 에러를 내라" 같은 조건문은 `F()`만으로는 어렵습니다. (DB 제약조건 `CheckConstraint`를 따로 걸어야 함)
   - Python 코드 레벨에서 즉각적으로 "지금 값이 몇이지?"를 보고 분기 처리를 할 수 없습니다.

> 요약: 
>save() 는 **"내 손에 있는 걸 저장"**하는 것이고, 
>update()는 **"DB에게 시키는 원격 명령"**입니다. 그래서 update()는 F() 객체(수식)와 찰떡궁합인 것입니다.



이 코드는 내부 블록이 성공했다 하더라도, 즉시 실행되지 않습니다.

on_commit 훅은 가장 바깥쪽 트랜잭션(Root Transaction)이 완전히 커밋된 직후에 실행됩니다.
만약 charge_and_log가 True를 반환했지만, 이 함수를 호출한 상위 코드에서 나중에 에러가 발생해 전체 롤백이 된다면?
emit_paid는 실행되지 않습니다. (데이터 일관성 보장)


이중 중첩된 atomic 은 내부 atomic 에서 .save() 되고, 외부 atomic 에서 실패하면 어떻게 되나?

> 내부 atomic의 성공은 "진짜 저장(Commit)"이 아니라, "일단 보류(Pending)" 상태로 바깥 트랜잭션에 합쳐지는 것이기 때문입니다.


>비유: 문서 작성
>외부 atomic 시작: "보고서 작성"이라는 큰 작업을 시작합니다.
>내부 atomic 성공: 보고서 중간에 "1장은 완벽해!"라고 생각하고 저장 버튼을 >눌렀습니다. (하지만 파일 닫기는 안 함)
>외부 atomic 실패: 갑자기 컴퓨터 전원이 꺼졌습니다. (에러 발생)
>결과: "1장은 완벽해!"라고 생각했던 부분까지 모두 날아갑니다.


수동!!

1. `transaction.savepoint()`
"여기서 세이브 한번 하자 (깃발 꽂기)"

현재 트랜잭션 상태를 기억하는 **임시 저장 지점(Savepoint)**을 생성합니다.
반환값 (sid): 생성된 세이브포인트의 고유 ID(문자열)를 반환합니다. 나중에 이 지점을 찾기 위한 '티켓'입니다.
DB에는 실제 커밋이 일어나지 않았습니다. 그냥 마킹만 한 것입니다.

2. `transaction.savepoint_rollback(sid)`
"망했다, 아까 세이브한 곳으로 불러오기! (로드)"

지정한 sid 이후에 발생한 모든 DB 변경 사항을 취소하고, 그 지점의 상태로 되돌립니다.
try-except 블록에서 에러가 났을 때, 전체를 취소하는 게 아니라 이 부분만 없었던 일로 만들 때 사용합니다.

3. `transaction.savepoint_commit(sid)`
"여기까진 클리어! 세이브 파일 지우고 계속 진행해."

주의: 진짜 DB에 '저장(Commit)'하는 것이 아닙니다!
**"이 세이브포인트는 이제 필요 없다(Release)"**는 뜻입니다.
"여기까지 작업은 성공했으니, 굳이 돌아올 일이 없다. 아까 꽂은 깃발(메모리 자원)을 뽑아버려라"는 의미입니다.
변경된 데이터는 아직 '보류' 상태로 트랜잭션 안에 남아 있습니다. 바깥쪽 atomic이 최종적으로 끝날 때 DB에 들어갑니다.


---

## tx_concurrency.py

> nowait 잠금: 이미 잠겨 있으면 즉시 실패
기본 동작: 보통 select_for_update()를 하면, 누군가 먼저 자원을 쓰고 있을 때 끝날 때까지 하염없이 기다립니다(Blocking).
nowait=True: **"지금 당장 못 쓰면 에러 뱉어!"**라고 DB에 요청합니다.

> 데드락 예방: 항상 같은 순서로 자원 잠그기
교착 상태
  sorted([p1_id, p2_id]): **"누가 오든 무조건 번호 작은 상품부터 집어라"**라는 규칙을 만듭니다.

> skip_locked=True (배치 선점)

skip_locked=True: **"이미 잠겨 있으면 건너뛰고 다음 걸로 넘어가!"**

---

## tx_on_commit.py

`lambda: schedule_outbox_dispatch()`

> 인자가 하나도 필요 없는 함수를 만들 때는 lambda: 뒤에 바로 실행할 코드를 적습니다.

(order: Order) : 파이썬의 Type Hint(타입 힌트) 문법입니다.

의미: "이 함수를 호출할 때,
order 라는 변수에는 Order 클래스의 인스턴스(객체)가 들어오는 것이 올바르다"고 명시하는 것

---

## tx_retry.py 🔺🔺🔺🔺

**학습 포인트**:
  - 데드락(Deadlock)이나 직렬화 실패(Serialization Failure)와 같은 "일시적 DB 에러" 식별
  - `functools.wraps`와 데코레이터를 이용한 **재시도(Retry) 로직** 구현
  - 지수 백오프(Exponential Backoff) 전략 적용


### 1. 일시적 오류 (Transient Errors)와 식별
python
PG_RETRY_ERRCODES = {'40001', '40P01'} # 40001: Serialization Failure, 40P01: Deadlock Detected
개념: DB 시스템에서 데이터 정합성을 지키기 위해 **"지금은 처리할 수 없으니 나중에 다시 시도해라"**라며 의도적으로 발생시키는 에러입니다.
Deadlock (데드락): 두 트랜잭션이 서로 상대방이 잡고 있는 자원을 기다리며 무한 대기에 빠진 상황. DB는 이를 감지하고 하나를 강제 종료시킵니다.
Serialization Failure (직렬화 실패): 트랜잭션 격리 수준(Isolation Level)이 높을 때(예: Serializable), 동시 실행된 트랜잭션들의 결과가 순차 실행 결과와 다를 수 있다고 판단되면 발생시킵니다.
is_retryable 함수: 모든 에러를 재시도하면 안 됩니다(예: 문법 에러, 데이터 제약조건 위반 등은 재시도해도 똑같이 실패함). 오직 "다시 하면 성공할 가능성이 있는" 에러만 골라내는 필터 역할을 합니다.

### 2. 데코레이터 패턴과 @wraps
python
def retry_on_tx_failure(...):
    def deco(fn):
        @wraps(fn)  # <--- 여기!
        def wrapper(*args, **kwargs):
            ...
데코레이터: 함수(safe_increment_counter)의 코드를 직접 수정하지 않고도 "재시도 기능"을 덧입힐 수 있게 해주는 파이썬의 디자인 패턴입니다.
@wraps(fn): 데코레이터를 쓰면 원래 함수(fn)의 이름(__name__)이나 설명(__doc__)이 wrapper 함수 것으로 덮어씌워져 버립니다. wraps는 원래 함수의 메타데이터를 복사해서 유지해주는 "매너 있는" 데코레이터를 만들 때 필수적입니다.
### 3. 지수 백오프 (Exponential Backoff)
python
time.sleep(backoff * attempt)
개념: 재시도할 때 기다리는 시간을 점점 늘리는 전략입니다.
이유: 데드락이나 경합 상황에서 즉시(0초 뒤) 다시 시도하면, 또다시 똑같은 타이밍에 충돌할 확률이 높습니다. 잠깐 쉬어줌으로써 다른 트랜잭션이 먼저 지나가게 비켜주는 것입니다. (예: 0.1초 -> 0.2초 -> 0.3초...)

### 4. 데코레이터 순서의 중요성 (매우 중요)
python
@retry_on_tx_failure(...)  # 1. 재시도 로직이 바깥쪽
@transaction.atomic        # 2. 트랜잭션이 안쪽
def safe_increment_counter(...):
이 순서는 절대적입니다.

작동 순서:
retry_on_tx_failure가 시작됨 (Loop 진입).
transaction.atomic이 새로운 트랜잭션을 엽니다.
safe_increment_counter 본문 실행.
만약 데드락 발생 -> DB가 에러를 뱉음 -> 트랜잭션 롤백됨.
에러가 retry_on_tx_failure로 올라감 -> except에서 잡아서 sleep 후 다시 Loop.
다시 transaction.atomic 실행 (깨끗한 새 트랜잭션 시작!)
반대로 쓴다면?: 트랜잭션 안에서 에러를 잡아서 재시도하려고 해도, 이미 그 트랜잭션은 "오염된(Aborted/Poisoned)" 상태라 재사용이 불가능합니다. (Postgres에서는 current transaction is aborted 에러 발생)

### 5. 멱등성 (Idempotency) 전제
python
"""idempotent 구간에만 적용할 것!"""
개념: 연산을 여러 번 수행해도 결과가 달라지지 않는 성질...이라기보단, 여기서는 **"실패했다면 아무런 부작용(Side Effect) 없이 처음부터 다시 실행해도 안전한가?"**를 의미합니다.
주의: 만약 함수 내부에서 "이메일 발송(외부 API 호출)"을 하고 나서 DB 업데이트를 하다가 데드락이 났다면?
재시도 로직이 돌면서 이메일이 2번, 3번 발송될 수 있습니다.
따라서 이 패턴은 순수하게 DB 작업만 있거나, 부작용이 없는 코드에만 감싸야 합니다.

### 요약

이 코드는 **"동시성 이슈로 실패할 수 있는 DB 작업을(1), 안전하게 새 트랜잭션으로 감싸서(4), 점점 대기 시간을 늘려가며(3), 자동으로 다시 시도(2)하게 해주는 도구"**입니다. 단, **부작용이 없는 코드(5)**에만 써야 합니다.

