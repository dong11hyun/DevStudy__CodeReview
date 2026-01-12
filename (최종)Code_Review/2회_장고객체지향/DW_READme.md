# 2회차 코드리뷰 - Django 객체지향 프로그래밍

> 2026.01.12 / DH & DW

---

## 주요 학습 내용

| 섹션 | 파일 | 핵심 |
|------|------|------|
| DecimalField | oop1.py | 모델 필드의 숫자 자릿수 제한 |
| HttpResponse | oop2.py | HTTP 응답 객체와 파라미터 |
| Form Widget | oop2.py | 폼 필드의 HTML 렌더링 방식 |
| Form Validation | oop2.py | cleaned_data, ValidationError |
| Middleware | oop4.py | `__call__` 매직 메서드, 함수 객체 |

---

## 1. DecimalField (oop1.py)

```python
class Product(models.Model):  # ← models.Model 상속

price = models.DecimalField(max_digits=10, decimal_places=2)
```

### 핵심 개념

> models.Model 상속	Django가 제공하는 ORM 기능 자동 획득

> 상속으로 얻는 것  save(), delete(), objects.all() 등


| 파라미터 | 설명 | 결과 |
|----------|------|------|
| `max_digits=10` | 전체 숫자 최대 자릿수 | 정수 + 소수 합쳐서 10자리 |
| `decimal_places=2` | 소수점 이하 자릿수 | 소수점 2자리 |

### 저장 가능한 값 범위
```
정수 부분: max_digits - decimal_places = 10 - 2 = 8자리
최대값: 99,999,999.99
```

---

## 2. HttpResponse (oop2.py)

```python
return HttpResponse("Hello, World!")
```

### 핵심 개념

| 파라미터 | 설명 | 예시 |
|----------|------|------|
| `content` | 응답 본문 (문자열, 바이트) | `"Hello, World!"` |
| `content_type` | MIME 타입 | `"text/html"`, `"application/json"` |
| `status` | HTTP 상태 코드 | `200`, `404`, `500` |
| `reason` | 상태 코드 설명 | `"OK"`, `"Not Found"` |
| `charset` | 문자 인코딩 | `"utf-8"` |

### 상속 예시
```python
class GoodbyeResponse(HttpResponse):
    def __init__(self, *args, **kwargs):
        super().__init__("Goodbye!", *args, **kwargs)

return GoodbyeResponse()  # → "Goodbye!" 출력
```

view 라는 클래스안에 정의된 함수
 "get",
        "post",
        "put",
        "patch",
        "delete",
        "head",
        "options",
        "trace",

---

## 3. Form Widget (oop3.py)

```python
content = forms.CharField(widget=forms.Textarea)
```

### 핵심 개념

| 개념 | 설명 |
|------|------|
| Widget | 폼 필드가 HTML로 어떻게 표현될지 결정 |
| `forms.Textarea` | `<textarea>` 태그로 렌더링 |

### Widget 종류

| Widget | HTML 결과 | 용도 |
|--------|----------|------|
| `TextInput` | `<input type="text">` | 짧은 텍스트 (기본값) |
| `Textarea` | `<textarea>` | 긴 텍스트 |
| `PasswordInput` | `<input type="password">` | 비밀번호 |
| `Select` | `<select>` | 드롭다운 |

---

## 4. Form Validation (oop3.py)

### cleaned_data

```python
data = self.cleaned_data['message']
```

| 요소 | 설명 |
|------|------|
| `cleaned_data` | 유효성 검사 통과 후 Django가 자동 생성하는 딕셔너리 |
| `['message']` | 폼에서 정의한 필드 이름으로 접근 |

### 데이터 흐름
```
request.POST['age']         → "25" (문자열, 원본)
form.cleaned_data['age']    → 25   (정수, 검증+변환됨)
```

> ⚠️ `is_valid()` 호출 후에만 `cleaned_data` 사용 가능

### ValidationError

```python
raise forms.ValidationError("스팸 메시지는 허용되지 않습니다.")
```

| 키워드 | 역할 |
|--------|------|
| `raise` | 예외를 발생시키는 Python 키워드 |
| `ValidationError` | 유효성 검사 실패를 알리는 Django 예외 |

---

## 5. Middleware와 `__call__` (oop4.py)

```python
class MyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response
```

### 핵심 개념

| 개념 | 설명 |
|------|------|
| `__init__` | 객체 **생성 시** 실행 (생성자) |
| `__call__` | 객체를 **함수처럼 호출** 가능하게 함 |
| `self.get_response` | 함수를 저장한 변수 |
| `self.get_response(request)` | 저장된 함수를 호출 |

### `__call__` 예시
```python
class Greeting:
    def __call__(self, name):
        return f"Hello, {name}!"

greet = Greeting()
greet("철수")  # → "Hello, 철수!" (객체를 함수처럼 호출)
```

### 미들웨어 실행 흐름
```
middleware = MyMiddleware(next_handler)  # __init__ 실행
middleware(request)                       # __call__ 실행
```

> 💡 Python에서 함수는 일급 객체! 변수에 저장하고 나중에 호출 가능

---

## 한눈에 보기

```
oop1.py  → DecimalField, max_digits, decimal_places
oop2.py  → HttpResponse, 
oop3.py  → Widget, cleaned_data, ValidationError
oop4.py  → __call__, 미들웨어, 함수 객체
```