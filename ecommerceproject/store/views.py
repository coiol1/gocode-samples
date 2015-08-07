from django.shortcuts import render, HttpResponse, redirect
from django.db.models import Q, Sum
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from models import Order, Product, OrderProduct

# Create your views here.
def index(request):
    if not request.user.is_authenticated():
        return redirect('/users/no_user/')
    json = request.GET.get('json')
    if json == 'true':
        jsondata = serializers.serialize('json', Product.objects.all())
        return HttpResponse(jsondata, content_type='application/json')
    
    products = Product.objects.all()
    qparams = ''

    filtering = request.GET.get('filter')
    if filtering:
        qparams += '&filter=' + filtering
        if filtering == 'low':
            products = products.filter(price__lte = 9999)
        if filtering == 'medium':
            products = products.filter(price__gte = 10000, price__lte = 1000000)
        if filtering == 'high':
            products = products.filter(price__gte = 1000001)
        products = sorted(products, key = lambda x: x.price)
    
    search = request.GET.get('search')
    if search:
        qparams += '&search=' + search
        products = products.filter(Q(name__icontains = search) | Q(description__icontains = search))
        products = sorted(products, key = lambda x: x.name) #if search, sort alphabetically
    
    sortby = request.GET.get('sortby')
    if sortby:
        qparams += '&sortby=' + sortby
        if sortby == 'price_asc':
            products = sorted(products, key = lambda x: x.price)
        elif sortby == 'price_desc':
            products = sorted(products, key = lambda x: x.price, reverse = True)
        elif sortby == 'alpha':
            products = sorted(products, key = lambda x: x.name)
    
    #products is now the properly sorted list of objects
    paginator = Paginator(products, 5)
    page = request.GET.get('page')
    try:
        product_page = paginator.page(page)
    except PageNotAnInteger:
        product_page = paginator.page(1)
    except EmptyPage:
        product_page = paginator.page(paginator.num_pages)
    
    return render(request, 'store/index.html', {'products': product_page, 'num_items': len(products), 'qparams': qparams})

def cart(request):
    if not request.user.is_authenticated():
        return redirect('/users/no_user/')
    remove = request.POST.get('remove')
    if remove:
        OrderProduct.objects.get(pk = remove).delete()
    update_id = request.POST.get('update_id')
    if update_id:
        update_op = OrderProduct.objects.get(pk = update_id)
        update_op.quantity = request.POST['update_quantity']
        update_op.save()
    try:
        current_order = Order.objects.get(status = 1, username = request.user.username)
    except:
        current_order = Order.objects.create(status = 1, username = request.user.username)
    product_id = request.POST.get('add_product')
    if product_id:
        try:
            current_op = OrderProduct.objects.get(order = current_order, product_id = product_id)
            current_op.quantity += int(request.POST['add_quantity'])
            current_op.save()
        except:
            new_op = OrderProduct.objects.create(order = current_order, product = Product.objects.get(pk = product_id), quantity = request.POST['add_quantity'])
    cart_contents = []
    subtotal = 0
    for op in OrderProduct.objects.all():
        if op.order == current_order:
            cart_contents.append(op)
            subtotal += op.product.price * op.quantity
    return render(request, 'store/cart.html', {'cart_contents': cart_contents, 'subtotal': '{:,.2f}'.format(subtotal / 100.0)})

def checkout(request):
    if not request.user.is_authenticated():
        return redirect('/users/no_user/')
    try:
        current_order = Order.objects.get(status = 1, username = request.user.username)
        current_order.status = 2
        current_order.save()
    except:
        pass
    return render(request, 'store/checkout.html', {})

def admin(request):
    orders = Order.objects.all()
    products = Product.objects.all()
    orderproducts = OrderProduct.objects.all()
    return render(request, 'store/admin.html', {'orders': orders, 'products': products, 'orderproducts': orderproducts})

def closeup(request, item_id):
    if not request.user.is_authenticated():
        return redirect('/users/no_user/')
    chosen_product = Product.objects.get(pk = item_id)
    return render(request, 'store/closeup.html', {'product': chosen_product})