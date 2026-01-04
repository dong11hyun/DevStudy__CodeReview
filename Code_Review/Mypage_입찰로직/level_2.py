from django.db import transaction  # 추가 필요
@login_required
def charge_wallet(request):
    if request.method == 'POST':
        amount = int(request.POST.get('amount', 0))
        if amount > 0:
            # ⭐ [트랜잭션 시작] 여기서부터는 한 몸이다!
            with transaction.atomic():
                wallet = Wallet.objects.select_for_update().get(user=request.user) # 락(Lock)도 걸어주는 게 정석
                
                wallet.balance += amount
                wallet.save()
                
                Transaction.objects.create(...)
            # ⭐ [트랜잭션 끝] 둘 다 성공했으니 DB에 진짜 반영!
            
            messages.success(...)
    return redirect('mypage')