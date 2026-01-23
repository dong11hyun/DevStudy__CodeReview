## models.py

class Product
uuid >> int이고 autoincrement PK설정가능

DecimalField >> decimal_places=2 소숫점 2번째까지 표현

> PositiveIntegerField : 0 또는 양의 정수만 저장

> on_delete= CASCADE 와 PROTECT 차이

```
CASCADE	부모 삭제 시 자식도 함께 삭제	주문 삭제 → 주문항목도 삭제
PROTECT	자식이 있으면 부모 삭제 불가 (에러 발생)	카테고리에 상품 있으면 카테고리 삭제 방지
SET_NULL	부모 삭제 시 자식의 FK를 NULL로 설정	작성자 탈퇴해도 게시글 유지
SET_DEFAULT	부모 삭제 시 기본값으로 설정

(결제 기록, 로그 등)는 PROTECT나 SET_NULL을 사용하여 실수로 삭제되는 것을 방지
```

unique 유일성, 최소성
Pk 와 구분

유일성 (Uniqueness)
"테이블의 모든 행(row)을 유일하게 식별할 수 있어야 한다"
ex) 이름 (동명이인 가능)
    NULL 허용
최소성	불필요한 속성 없음
ex) 학번 

`order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")`


```
class Message(models.Model):
    sender = models.ForeignKey(User, related_name="sent_messages")
    receiver = models.ForeignKey(User, related_name="received_messages")
# 사용
user.sent_messages.all()      # 보낸 메시지들
user.received_messages.all()  # 받은 메시지들
```

```
class Order(models.Model):
    # 주문
    pass
class OrderItem(models.Model):
    # 주문 항목 (자식)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
```

방향	코드	설명
정방향	order_item.order	주문항목 → 주문 (ForeignKey 따라감)
역방향	order.items.all()	주문 → 주문항목들 (related_name 사용)

> related_name 없으면 둘 다 user.message_set이 되어 충돌 에러 발생!

## model_idem.py


PositiveSmallIntegerField(),  JSONField() , DateTimeField(auto_now_add=True)

auto_now_add=True	생성 시점에 자동으로 현재 시간 저장	❌ 수정 불가
auto_now=True	저장할 때마다 현재 시간으로 업데이트	❌ 수정 불가
default=timezone.now	생성 시 기본값, 수동 수정 가능	✅ 수정 가능

JSONField(): 왜쓰냐? 컬럼 구조를 미리 못 정하거나 자주 바뀌는 데이터"를 저장할 때 JSONField


## serializer.py


> many=True (리스트 처리)

> many=False (기본)	단일 객체 {...}
> many=True	리스트 [{...}, {...}]

>  Serializer는 **"JSON ↔ Python 변환 + 데이터 검증


```
# ❌ Serializer 없이 직접 구현
import json
def create_order(request):
    # 1. JSON 파싱 (수동)
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    
    # 2. 검증 (수동) - 매우 번거로움
    if 'items' not in data:
        return JsonResponse({"error": "items required"}, status=400)
    
    if not isinstance(data['items'], list):
        return JsonResponse({"error": "items must be list"}, status=400)
    
    for item in data['items']:
        if 'sku' not in item:
            return JsonResponse({"error": "sku required"}, status=400)
        if 'quantity' not in item:
            return JsonResponse({"error": "quantity required"}, status=400)
        if not isinstance(item['quantity'], int) or item['quantity'] < 1:
            return JsonResponse({"error": "quantity must be >= 1"}, status=400)
    
    # 3. 비즈니스 로직...
```
```
#  Serializer 사용
def create_order(request):
    serializer = OrderCreateIn(data=request.data)
    serializer.is_valid(raise_exception=True)  # 한 줄로 끝!
    
    items = serializer.validated_data['items']
    # 비즈니스 로직...
```


## view.py  (bad)

문제점 

0. def create_order(request): get 이든 post든 뭘 넣어도 돌아감

1. serializer 없이 직접 구현. json 로드시켜서 일일이 검증

2. fat-view 문제

11번째의 for it in items: 를 통한 계산 처리는 
wallet 이나 다른 재고 및 가격(total) 앱에서 처리하는것이 좋음

db 저장인 .save() 도 다른 앱에서 계산처리 후 
정합성 및 원자성 따진 다음 저장하는것이 좋음

notify_webhook(order.id):
현 코드에서 주문 완료 후 외부 시스템(결제, 배송, 알림 서비스 등)에 HTTP 요청을 보냄


Webhook(웹훅) : 이벤트가 발생하면 자동으로 HTTP 요청을 보내는 알림 시스템


## view.py  (good)

