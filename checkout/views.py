from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

# Create your views here.
@login_required(login_url='login')
def checkout(request):
    return render(request, 'checkout/checkout.html')

def order(request):
    return render(request, 'checkout/order.html')


def place_order(request):
    return HttpResponse('Place Order')
