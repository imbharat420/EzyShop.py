from django.shortcuts import render

# Create your views here.
def checkout(request):
    return render(request, 'checkout/checkout.html')

def order(request):
    return render(request, 'checkout/order.html')
