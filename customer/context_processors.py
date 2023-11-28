from owner.models import Carts
def show_cart_count(request):
    # cart_count=Carts.objects.filter(user=request.user,status="incart").count()
    # return {'cart_count':cart_count}
    cart_count = 0  # Default count if user is not authenticated
    if request.user.is_authenticated:
        cart_count = Carts.objects.filter(user=request.user, status="incart").count()
    return {'cart_count': cart_count}