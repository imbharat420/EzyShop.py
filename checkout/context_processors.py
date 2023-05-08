# Total Order price 
from .models import Order

def total_order_price(request):
    total = 0
    if request.user.is_authenticated:
        order = Order.objects.filter(user=request.user, is_ordered=True)
        if order.exists():
            for item in list(order):
                total += item.order_total
    return dict(total_order_price=total) 