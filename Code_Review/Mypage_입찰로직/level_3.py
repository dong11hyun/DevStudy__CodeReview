from django.db.models import F          # [추가] DB 레벨 연산을 위한 모듈
from django.db import transaction       # [추가] 트랜잭션 관리를 위한 모듈

# 재화 충전 (간이 버전) _ 144_181_codeline
@login_required
@transaction.atomic
def charge_wallet(request):
    if request.method == 'POST':
        try:
            amount = int(request.POST.get('amount', 0))
            # [수정] 유효성 검사 강화: 잘못된 금액이 들어오면 에러를 강제로 발생시킴
            if amount <= 0:
                raise ValueError("금액은 0보다 커야 합니다.")

            # [수정] select_for_update() 추가: 
            # 데이터를 가져올 때 해당 행(Row)에 잠금(Lock)을 걸어 다른 요청이 동시에 수정하지 못하게 막음
            wallet = Wallet.objects.select_for_update().get(user=request.user)
            
            # [수정] F객체 사용: 
            # 파이썬 메모리가 아닌, DB가 직접 현재 값에서 더하기를 수행하도록 지시 (동시성 문제 2차 방어)
            wallet.balance = F('balance') + amount 
            wallet.save()
            
            # [추가] DB 값 갱신: 
            # F객체로 연산한 후에는 파이썬 변수(wallet.balance)가 실제 숫자를 모르므로, DB에서 다시 값을 불러옴
            wallet.refresh_from_db()

            Transaction.objects.create(
                wallet=wallet,
                amount=amount,
                transaction_type='DEPOSIT',
                description='마이페이지에서 충전'
            )
            messages.success(request, f"{amount}원이 충전되었습니다!")

        except ValueError: # [추가] 값 에러(문자 입력, 음수 입력 등) 처리
            messages.error(request, "잘못된 금액입니다.")
        except Wallet.DoesNotExist: # [추가] 지갑이 없는 경우 처리
            messages.error(request, "지갑이 없습니다.")

    return redirect('mypage')