# 🐍 Django 객체지향 심층 분석 (oop1.py ~ oop4.py)

이 문서는 4개의 예제 파일을 통해 **Django가 객체지향 프로그래밍(OOP)의 원칙**을 어떻게 구현하고 있는지 상세히 분석합니다. 단순한 코드 설명을 넘어, **설계 철학(Design Philosophy)**, **실제 동작 방식(Under the hood)**, 그리고 **현업에서 적용해야 할 Best Practice**를 포함합니다.

---

## 1️⃣ `oop1.py`: Model과 비즈니스 로직의 응집 (Encapsulation)

### 📄 코드 다시보기
```python
class Product(models.Model):  
    name = models.CharField(...)
    price = models.DecimalField(...)

    def apply_discount(self, percent):  
        self.price *= (1 - percent/100)
        return self.price
```

### 💡 핵심 OOP 개념: "데이터와 행위를 하나로"
객체지향의 제1원칙은 **캡슐화(Encapsulation)** 입니다. 데이터(속성)를 가지고 있는 객체가 그 데이터를 조작하는 방법(메서드)도 함께 가지고 있어야 한다는 원칙입니다.

*   **Active Record 패턴**: Django 모델은 데이터베이스 테이블의 행(Row)을 객체로 매핑하는 Active Record 패턴을 따릅니다. 객체 스스로가 데이터 저장(`save`), 삭제(`delete`), 로직 처리(`apply_discount`)의 책임을 가집니다.
*   **응집도(Coherence) 증가**: 할인 로직이 뷰(View)나 유틸리티 파일에 흩어져 있지 않고, 가격(`price`) 데이터가 있는 모델 클래스 내부에 위치합니다. 이로 인해 관련된 코드가 한곳에 모여 유지보수가 쉬워집니다. (`Fat Model, Skinny View` 지향)

### ⚙️ 실제 사용 시나리오 (How it works)
개발자가 이 모델을 실제 `shell`이나 `views.py`에서 사용할 때의 흐름입니다.

```python
# 1. 인스턴스 생성 (아직 DB 반영 안 됨)
apple = Product(name="사과", price=10000)

# 2. 메서드 호출 (객체 내부 상태 변경)
# 뷰에서는 구체적인 계산 식을 몰라도 됨. "할인해라"라는 메시지만 던짐.
new_price = apple.apply_discount(10)  

# 3. 영속화 (DB 저장)
# apply_discount는 메모리상의 값만 바꾸므로, 반드시 save() 호출 필요
apple.save() 
```

### 🧐 Review Point (심화)
1.  **책임의 범위**: 단순히 값을 바꾸는 것 외에, 할인 내역을 로그로 남겨야 한다면? 모델 메서드 안에서 로깅까지 처리하면 모델이 너무 무거워집니다. 이럴 땐 Service Layer 도입을 고려해야 합니다.
2.  **불변성(Immutability)**: 함수형 프로그래밍 스타일을 선호한다면, 원본 `self.price`를 바꾸지 않고 할인된 가격만 리턴하는 `get_discounted_price` 방식이 사이드 이펙트(Side Effect)를 줄일 수 있어 더 안전할 수 있습니다.

---

## 2️⃣ `oop2.py`: CBV를 통한 다형성과 상속 (Polymorphism)

### 📄 코드 다시보기
```python
class HelloView(View):
    def get(self, request): ...

class GoodbyeView(HelloView):  
    def get(self, request): ...
```

### 💡 핵심 OOP 개념: "상속과 오버라이딩"
*   **템플릿 메서드 패턴 (Template Method Pattern)**: Django `View` 클래스는 요청 처리의 전체 흐름(뼈대)을 이미 `dispatch()` 메서드 안에 정의해 두었습니다. 개발자는 그 흐름 중 특정 단계인 `get()`, `post()` 만 **오버라이딩(재정의)** 하면 됩니다.
*   **리스코프 치환 원칙 (LSP)**: 자식 클래스(`GoodbyeView`)는 부모 클래스(`HelloView`)가 들어갈 자리에 대체되어도 논리적으로 문제가 없어야 합니다.

### ⚙️ 실제 사용 시나리오 (How it works)
`urls.py`에 등록될 때와 요청이 들어올 때의 동작입니다.

```python
# urls.py
urlpatterns = [
    path('hello/', HelloView.as_view()),
    path('bye/', GoodbyeView.as_view()),
]
```
1.  **진입점**: 요청이 오면 `as_view()`가 뷰 클래스의 인스턴스를 생성하고 `dispatch()`를 호출합니다.
2.  **다형성**: `dispatch()`는 HTTP 메서드(GET, POST 등)를 확인하고, 해당 이름과 일치하는 메서드(`get`, `post`)를 동적으로 찾아 호출합니다.
    *   `HelloView` 인스턴스라면 → 자신의 `get()` 실행 (Hello World)
    *   `GoodbyeView` 인스턴스라면 → 오버라이딩된 `get()` 실행 (Goodbye)

### 🧐 Review Point (심화)
1.  **잘못된 상속 (Anti-pattern)**: `GoodbyeView`가 `HelloView`를 상속받은 것은 **"구현 상속"**의 나쁜 예입니다. '작별인사'가 '인사'의 기능을 재사용하지 않는데 상속받았습니다. 이 경우 두 클래스는 형제 관계가 되어야 맞습니다.
    *   **Bad**: `class GoodbyeView(HelloView):` (부모의 get을 덮어써버림)
    *   **Good**: `class GoodbyeView(View):` 또는 `class GoodbyeView(BaseMsgView):`

---

## 3️⃣ `oop3.py`: Form Validation과 할리우드 원칙 (Hooks)

### 📄 코드 다시보기
```python
class ContactForm(forms.Form):
    ...
    def clean_message(self): ...
```

### 💡 핵심 OOP 개념: "제어의 역전(IoC)과 훅(Hook)"
**"Don't call us, we'll call you." (할리우드 원칙)**
Django 프레임워크(`forms.Form`)가 검증의 주도권을 가지고 있으며, 필요할 때 개발자가 정의한 메서드(`clean_message`)를 찾아내서 호출합니다.

### ❓ `form.is_valid()`는 언제 쓰이는가?
`oop3.py` 파일은 **붕어빵 틀(Form 클래스)** 만 정의한 것입니다. 실제로 이 틀을 사용해서 유효성 검사를 시작하는 곳은 **View(views.py)** 입니다. `is_valid()`가 바로 **"검증 기계 작동 버튼"** 입니다.

```python
# views.py (가상의 뷰 파일)
from django.shortcuts import render, HttpResponse
from .oop3 import ContactForm

def contact_view(request):
    # 1. GET 요청: 빈 폼 보여주기
    if request.method == 'GET':
        form = ContactForm()
        return render(request, 'contact.html', {'form': form})

    # 2. POST 요청: 데이터 처리
    elif request.method == 'POST':
        # 사용자 입력 데이터로 폼 인스턴스 생성 (Data Binding)
        form = ContactForm(request.POST) 
        
        # 🟢 여기가 시작점입니다! 🟢
        # 이 버튼을 누르는 순간 위 다이어그램의 검증 로직이 촤르륵 돌아갑니다.
        if form.is_valid():  
            # 검증 통과 (clean_message 등 모두 통과)
            print(form.cleaned_data['message']) # 정제된 데이터 사용
            return HttpResponse("성공!")
        else:
            # 검증 실패 (clean_message에서 에러 발생 등)
            # 에러 메시지가 담긴 form을 다시 템플릿으로 보냄
            return render(request, 'contact.html', {'form': form})
```

### 🎨 시각적 흐름도 (Visual Flow)

```
      [ Django 프레임워크 (System) ]                  [ 내가 쓴 코드 (User) ]
      
             form.is_valid()  ◀─────── views.py에서 호출하는 순간 시작!
                   │
                   ▼
             _clean_fields() ◀────────── (1. 폼 안의 필드들을 하나씩 순회)
                   │
    ┌──────────────┴──────────────┐
    │  현재 체크 중인 필드: "message" │
    └──────────────┬──────────────┘
                   │
                   ▼
    "clean_message" 라는 이름의         (2. Reflection: 이름으로 메서드 찾기)
      함수가 정의되어 있는가?
                   │
          ┌────────┴────────┐
          │  네, 있습니다!   │ ───────────────────────┐
          └────────┬────────┘                        │
                   │                                 │ (3. Hook Call: 역호출)
                   │                        ▼────────┴────────▼
                   │                        def clean_message(self):
                   │                            # 사용자가 작성한 검증 로직
                   │                            if "spam" in data:
                   │                                error!
                   │ <─────────────────────     return data
                   │      (4. 반환)
                   ▼
      cleaned_data['message'] 에 저장
```

### ⚙️ 실제 동작 원리 (How it works under the hood)
Django의 폼 검증 시스템은 **Reflection(리플렉션)** 기법을 사용합니다. 이는 실행 중에 객체의 내부 구조(메서드 이름 등)를 들여다보고 조작하는 기술입니다.

1.  `_clean_fields` 메서드는 폼에 선언된 모든 필드(`name`, `email`, `message`)를 루프 돕니다.
2.  각 필드 이름 앞에 `clean_` 접두사를 붙여 봅니다. (`clean_message`)
3.  `hasattr(self, 'clean_message')`를 통해 해당 이름의 메서드가 실제 존재하는지 확인합니다.
4.  존재한다면 `getattr(self, 'clean_message')()`로 해당 메서드를 가져와 실행시킵니다.

### 🧐 Review Point (심화)
1.  **관심사의 분리**: 뷰(View)는 복잡한 검증 로직을 알 필요가 없습니다. 뷰는 단지 `is_valid()` 결과에 따라 성공/실패 페이지만 보여주면 됩니다. **"검증은 폼의 책임"** 이라는 원칙이 철저히 지켜졌습니다.
2.  **확장성(Extensibility)**: 새로운 필드 `phone`을 추가하고 검증하고 싶다면, `clean_phone` 메서드만 추가하면 됩니다. `full_clean` 같은 핵심 로직을 건드릴 필요가 없습니다. (Open-Closed Principle)

---

## 4️⃣ `oop4.py`: Middleware와 데코레이터 패턴 (Callable Object)

### 📄 코드 다시보기
```python
class SimpleMiddleware:
    def __init__(self, get_response): ...
    def __call__(self, request): ...
```

### 💡 핵심 OOP 개념: "객체를 함수처럼 다루기"
*   **데코레이터 패턴 (Decorator Pattern)**: 미들웨어는 '러시아 인형(마트료시카)'과 같습니다. 실제 뷰 함수를 미들웨어 객체가 감싸고(Wrap), 그 미들웨어를 또 다른 미들웨어가 감쌉니다. 기능을 덧붙이면서도 핵심 로직(뷰)은 건드리지 않습니다.
*   **Callable Interface**: 파이썬의 덕 타이핑(Duck Typing)을 활용합니다. "함수냐 객체냐"는 중요하지 않습니다. "호출 가능(`__call__`)한가?"가 중요합니다.

### ⚙️ 실제 사용 시나리오 (How it works)
Django 서버가 시작될 때(`__init__`)와 요청이 들어올 때(`__call__`)가 명확히 나뉩니다.

```python
# 1. 서버 초기화 시점 (단 1번 실행)
# 체인 형성: Middleware( View_Function )
middleware_instance = SimpleMiddleware(actual_view_func)

# 2. 요청 들어올 때 (매번 실행)
# Django 코어는 이 객체를 함수처럼 호출합니다.
response = middleware_instance(request) 

# 내부 동작:
# - [전처리] print("요청 시작")
# - self.get_response(request) -> 실제 뷰 실행
# - [후처리] print("응답 완료")
# - return response
```

### 🧐 Review Point (심화)
1.  **상태 관리 주의**: 미들웨어는 **싱글톤(Singleton)** 처럼 동작합니다(프로세스당 1개). 따라서 `__init__`에서 만든 인스턴스 변수는 모든 요청이 공유합니다.
    *   **위험**: `self.user_id = request.user.id` (다른 사람의 요청과 섞일 수 있음 😱)
    *   **안전**: 로컬 변수 사용 `user_id = request.user.id`

---

## 📝 종합 요약: Django스러운 코드란?

코드 리뷰 시 다음 질문을 던져보세요.

1.  **데이터 처리 로직이 뷰(View)에 노출되어 있는가?**
    *   👉 `oop1.py` 처럼 모델 메서드로 숨기세요 (Encapsulation).
2.  **조건문(if-else)으로 로직을 분기하고 있는가?**
    *   👉 `oop2.py` 처럼 클래스 상속과 오버라이딩으로 해결 가능한지 보세요 (Polymorphism).
3.  **검증 로직이 중복되거나 복잡한가?**
    *   👉 `oop3.py` 처럼 Form 내부 훅으로 위임하세요 (Separation of Concerns).
4.  **여러 뷰에 공통적으로 적용해야 할 횡단 관심사(로깅, 인증)인가?**
    *   👉 `oop4.py` 처럼 미들웨어(데코레이터)로 해결하세요 (AOP).
