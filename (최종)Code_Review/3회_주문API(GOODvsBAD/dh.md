# 3회차 주문 API (GOOD vs BAD) 코드 리뷰

## 📁 파일 구조 개요

| 파일 | 역할 |
|------|------|
| `model.py` | 핵심 도메인 모델 (Product, Order, OrderItem) |
| `model_idem.py` | 멱등성(Idempotency) 키 모델 |
| `serializers.py` | 입력 데이터 유효성 검증 |
| `services.py` | 비즈니스 로직 (✅ GOOD 패턴) |
| `view_bad.py` | ❌ 안티패턴 예시 |
| `view_good.py` | ✅ 모범 사례 예시 |

---

## 📌 model.py 상세 분석

### 1. `unique=True` 의미

```python
sku = models.CharField(max_length=50, unique=True)
```

| 속성 | 설명 |
|------|------|
| **유일성** | ✅ 보장 - DB 레벨 UNIQUE 제약조건 |
| **최소성** | ❌ 해당 없음 (복합키 개념) |
| **Primary Key** | ❌ 아님 - 별도 `id` 필드가 PK |

**unique vs primary_key 비교:**

| 항목 | `unique=True` | `primary_key=True` |
|------|--------------|-------------------|
| NULL 허용 | 가능 (null=True 필요) | 불가 |
| 여러 개 가능 | ✅ | ❌ 테이블당 1개 |
| 자동 인덱스 | ✅ | ✅ |

> 💡 `sku`는 **비즈니스 식별자**, 내부적으로 `id`가 PK 역할

---

### 2. DecimalField 역할

```python
price = models.DecimalField(max_digits=12, decimal_places=2)
```

**✅ 금액 계산에는 반드시 Decimal 사용**

```python
# ❌ float 문제점
>>> 0.1 + 0.2
0.30000000000000004

# ✅ Decimal은 정확
>>> Decimal("0.1") + Decimal("0.2")
Decimal('0.3')
```

| 파라미터 | 의미 |
|----------|------|
| `max_digits=12` | 전체 자릿수 (최대 9999999999.99) |
| `decimal_places=2` | 소수점 자릿수 |

---

### 3. UUID 기능 및 `editable=False`

```python
id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
```

**UUID란?** 128비트 고유 식별자 (예: `550e8400-e29b-41d4-a716-446655440000`)

| 항목 | 설명 |
|------|------|
| `primary_key=True` | 이 필드가 PK (자동 id 생성 안됨) |
| `default=uuid.uuid4` | 생성 시 자동 UUID 할당 |
| `editable=False` | Admin/Form에서 수정 불가 |

**UUID vs AutoField 비교:**

| 항목 | UUID | AutoField (1,2,3...) |
|------|------|---------------------|
| 예측 가능성 | ❌ 불가 | ✅ 쉽게 예측 |
| 보안 | ✅ URL 노출 안전 | ❌ `/orders/102/` → 103 시도 가능 |
| 분산 시스템 | ✅ 충돌 없이 생성 | ❌ DB 의존 필요 |
| 인덱스 성능 | ⚠️ 약간 느림 | ✅ 빠름 |

---

### 4. 문자열 ForeignKey (Lazy Reference)

```python
user = models.ForeignKey("users.User", on_delete=models.PROTECT)
```

**✅ 사용 가능** - 지연 참조(Lazy Reference) 문법

| 방식 | 문법 | 용도 |
|------|------|------|
| 직접 참조 | `ForeignKey(User, ...)` | import된 모델 |
| 문자열 참조 | `ForeignKey("app.Model", ...)` | **순환 import 방지** |

> ⚠️ 실무에서는 `settings.AUTH_USER_MODEL` 사용 권장

---

### 5. `on_delete=models.PROTECT`

**PROTECT: 참조된 객체의 삭제를 차단** → `ProtectedError` 발생

| on_delete 옵션 | 동작 |
|----------------|------|
| **PROTECT** | ❌ 삭제 차단 |
| CASCADE | 함께 삭제 (위험!) |
| SET_NULL | NULL로 변경 |
| SET_DEFAULT | 기본값으로 변경 |

**왜 PROTECT?**
- 주문 기록 **영구 보존** 필요 (회계/법적)
- 유저 탈퇴해도 주문 이력 유지
- 실수 삭제 방지

---

### 6. 기타 핵심 포인트

#### `related_name` - 역참조 이름
```python
order = models.ForeignKey(Order, related_name="items")
# order.items.all() 로 접근 가능
```

#### `PositiveIntegerField`
```python
stock = models.PositiveIntegerField(default=0)
```
- DB 레벨 음수 입력 방지 (재고/수량용)

#### `auto_now_add=True`
```python
created_at = models.DateTimeField(auto_now_add=True)
```
- 최초 생성 시 자동 시간 저장, 이후 변경 불가

---

## 📌 model_idem.py - 멱등성 키

```python
class IdempotencyKey(models.Model):
    key = models.CharField(max_length=128, unique=True)
    request_hash = models.CharField(max_length=64)
    status_code = models.PositiveSmallIntegerField()
    response_body = models.JSONField()
```

**역할:** 중복 요청 방지 (같은 키로 재요청 시 이전 응답 반환)

> 💡 결제 API 필수 패턴 - 네트워크 오류로 인한 중복 결제 방지

---

## 📌 serializers.py - 입력 검증

```python
class OrderCreateIn(serializers.Serializer):
    items = OrderItemIn(many=True)
    
    def validate_items(self, items):
        if not items:
            raise serializers.ValidationError("At least one item is required.")
```

- View에서 직접 검증하지 않고 **Serializer에 위임**

---

## 📌 services.py - 비즈니스 로직 (GOOD ✅)

```python
@transaction.atomic
def create_order(*, user, items: list[dict]) -> Order:
    by_sku = {p.sku: p for p in Product.objects.select_for_update().filter(sku__in=skus)}
    Product.objects.filter(pk=p.pk).update(stock=F("stock") - q)
    OrderItem.objects.bulk_create(bulk_items)
    transaction.on_commit(lambda: publish_order_created(order.id))
```

| 패턴 | 설명 |
|------|------|
| `@transaction.atomic` | 전체가 원자적 실행 |
| `select_for_update()` | 행 수준 락 (Race Condition 방지) |
| `F("stock") - q` | Atomic Update (동시성 안전) |
| `bulk_create()` | 한 번의 쿼리로 여러 INSERT |
| `on_commit()` | 커밋 성공 후에만 이벤트 발행 |

---

## 📌 view_bad.py vs view_good.py 비교

| 주제 | ❌ BAD | ✅ GOOD |
|------|--------|---------|
| JSON 파싱 | `json.loads()` 수동 | DRF `request.data` |
| 유효성 검증 | 없음 | Serializer 사용 |
| 금액 계산 | `float` 사용 | `Decimal` 사용 |
| DB 조회 | 루프 내 개별 조회 (N+1) | 일괄 조회 `filter(sku__in=skus)` |
| 동시성 | `stock -= q` (Race 취약) | `F("stock") - q` (Atomic) |
| 트랜잭션 | 없음 | `@transaction.atomic` |
| INSERT | 루프 내 `create()` | `bulk_create()` |
| 이벤트 발행 | 커밋 전 발행 | `on_commit()` |
| HTTP 상태코드 | 200 | 201 CREATED |
| 인증 | 없음 | `@permission_classes` |
| 멱등성 | 없음 | `IdempotencyKey` |

---

## ❌ view_bad.py 문제점 상세

| 라인 | 문제 | 결과 |
|------|------|------|
| 6 | `json.loads()` 수동 파싱 | 예외 처리 없음, 500 에러 |
| 7 | 유효성 검증 없음 | 잘못된 데이터 통과 |
| 10 | `float` 사용 | 금액 정밀도 손실 |
| 12 | 루프 내 `get()` | N+1 Query |
| 14~16 | 중간 에러 시 롤백 없음 | 데이터 불일치 |
| 15~16 | `stock -= q; save()` | Race Condition |
| 26 | 커밋 전 이벤트 발행 | 실패해도 이벤트 발행됨 |

---

## ✅ view_good.py 멱등성 처리 흐름

1. 요청 수신
2. `Idempotency-Key` 헤더 확인
3. 있으면 → DB에서 키 조회 (`select_for_update`)
4. 이미 처리됨? → 캐시된 응답 반환
5. 처리 안됨? → 주문 생성 → 응답 캐싱 → 반환

---

## 📋 핵심 요약

| 개념 | 핵심 |
|------|------|
| `unique=True` | 유일성 O, PK 아님 |
| `DecimalField` | 금액 정밀 계산 (float 대신) |
| `UUID` | 예측 불가 PK, 보안에 유리 |
| `editable=False` | Admin/Form 수정 불가 |
| 문자열 FK | 순환 import 방지용 Lazy Reference |
| `PROTECT` | 참조된 객체 삭제 차단 |
| 멱등성 | 중복 요청에 동일 응답 보장 |
| `select_for_update` | 행 잠금으로 동시성 제어 |
| `F()` 표현식 | Atomic Update |
| `on_commit()` | 커밋 성공 후 이벤트 발행 |
