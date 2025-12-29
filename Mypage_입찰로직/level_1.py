@login_required
def charge_wallet(request):
    if request.method == 'POST':
        amount = int(request.POST.get('amount', 0))
        if amount > 0:
            wallet = Wallet.objects.get(user=request.user)
            wallet.balance += amount
            wallet.save()
            
            # 충전 기록 남기기
            Transaction.objects.create(
                wallet=wallet,
                amount=amount,
                transaction_type='DEPOSIT',
                description='마이페이지에서 충전'
            )
            messages.success(request, f"{amount}원이 충전되었습니다! 💵")
    return redirect('mypage')
