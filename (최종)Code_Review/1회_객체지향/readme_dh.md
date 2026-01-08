# 2026_01_08
## 객체지향 프로그래밍의 4대 속성
1. 캡슐화 
2. 상속성
3. 다형성
4. 추상화

```python
# 데이터
    def __init__(self, name, breed):
        self.name = name
        self.breed = breed
# 메서드
    def bark(self):
        return f"{self.name}가 멍멍 짖습니다!"
```
> 데이터와 메서드를 하나로 묶었다. ==> 캡슐화

`__init__` : 생성자 또는 초기화 메서드
```
Dog("바둑이", "진돗개") 
    ↓
1. Python이 메모리에 빈 Dog 객체 생성
2. __init__(self, "바둑이", "진돗개") 자동 호출
3. self.name = "바둑이" 저장
4. self.breed = "진돗개" 저장
5. 완성된 객체 반환 → dog1에 할당
```

`self`란 무엇이고 왜 존재하는가?
- 나 자신(현재인스턴스)를 가리키는 참조 변

```python
#다중상속
class Dog(Animal, Pet) 

=> Animal 과 Pet 둘다에서 상속받은 Dog
```
```python
class Cat(Animal):
    def __init__(self, name, color):
        # self.name = name  <-- 이렇게 중복해서 쓰지 말고
        super().__init__(name) # 부모의 __init__을 호출하여 name 세팅 위임
        self.color = color     # 자식만의 고유 속성 초기화
```

```python
#강제 차단보다는 "건드리지 말라"는 신호를 보내는 것
# 아래와 같은 문법으로 변경가능함.
print(account._BankAccount__balance)
account._BankAccount__balance = -10000
```
