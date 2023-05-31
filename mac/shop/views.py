from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Electric, Contact, Order, OrderReport, Cart, Api
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import json
import random
from django.template.loader import get_template
from xhtml2pdf import pisa
import requests
from geopy.geocoders import Nominatim
from django.contrib import messages


def pdf(request, order_id):
    order = Order.objects.filter(order_unique_id=order_id)
    sum = 0
    for i in order:
        sum += i.amount

    item = order[0].items_json
    data = json.loads(item)
    template_path = 'shop/pdf.html'
    context = {'data': data, 'order': order, 'sum': sum}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = ' filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def history(request):
    user_id = request.session.get('id')
    order = Order.objects.filter(user_id=user_id)
    api_table = Api.objects.all()

    if len(api_table) == 0:
        api_response = requests.get('https://jsonplaceholder.typicode.com/users')
        api_data = api_response.json()
        for i in api_data:
            api_id = i['id']
            name = i['name']
            email = i['email']
            street = i['address']['street']
            suite = i['address']['suite']
            city = i['address']['city']
            zipcode = i['address']['zipcode']
            lat = i['address']['geo']['lat']
            lng = i['address']['geo']['lng']
            phone = i['phone']
            website = i['website']
            company_name = i['company']['name']
            catchpharse = i['company']['catchPhrase']
            bs = i['company']['bs']
            api = Api(api_id=api_id, name=name, email=email, street=street, suite=suite, city=city, zipcode=zipcode,
                      lat=lat, lng=lng, phone=phone, website=website, company_name=company_name,
                      catchpharse=catchpharse,
                      bs=bs)
            api.save()
            api_table = Api.objects.all()

    if request.method == 'POST':
        city_id = request.POST.get('id', '')
        lat = request.POST.get('lat', '')
        lng = request.POST.get('lng', '')
        full_address = Api.objects.filter(api_id=city_id)
        geolocator = Nominatim(user_agent="geoapiExercises")

        Latitude = lat
        Longitude = lng

        location = geolocator.reverse(Latitude + "," + Longitude)

        for i in full_address:
            address = i.street + i.suite + i.city + i.zipcode
        return HttpResponse(location)

    return render(request, 'shop/history.html', {'order': order, 'api_table': api_table})


def invoice(request, order_id):
    order = Order.objects.filter(order_unique_id=order_id)
    item = order[0].items_json
    data = json.loads(item)
    return render(request, 'shop/invoice.html', {'data': data, 'order': order, 'id': order_id})


def handle_login(request):
    if request.method == 'POST':
        firstname = request.POST.get('name', '')
        password = request.POST.get('password', '')
        user = authenticate(username=firstname, password=password)

        if user is not None:
            myid = user.id
            request.session['id'] = myid
            login(request, user)
            messages.success(request, 'successfully loggedin...'+ str(request.user))
            return redirect('/shop/index/')
        else:
            messages.error(request, 'PLEASE TRY AGAIN WITH CORRECT USERNAME OR PASSWORD ')
            return redirect('/shop/index/')
    return render(request, 'shop/login.html')


def handle_logout(request):
    logout(request)
    return redirect('/shop/index')


def create_user(request):
    if request.method == 'POST':
        firstname = request.POST.get('firstname', '')
        lastname = request.POST.get('lastname', '')
        Email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        repeat_password = request.POST.get('repeatpassword', '')
        myuser = User.objects.create_user(firstname, Email, password)
        myuser.first_name = firstname
        myuser.last_name = lastname
        myuser.save()
        return redirect('/shop/')
    return render(request, 'shop/create_user.html')


def index(request):
    user = request.user
    if User.objects.filter(username=user.username).exists():
        user_id = request.session.get('id')
        cart = Cart.objects.values('name', 'qty').filter(user_id=user_id)
        item_num = 0
        for i in cart:
            item_num += i['qty']
    else:
        user_id = 0
        cart = Cart.objects.values('name', 'qty').filter(user_id=user_id)
        item_num = 0
        for i in cart:
            item_num += i['qty']


    ele_product = Electric.objects.filter(category="Electric")
    fashion_products = Electric.objects.filter(category="Fashion")
    list = Cart.objects.all()
    products_list = {'ele_pr': ele_product, 'fashion_pr': fashion_products, 'list': list,
                     'id_': user_id, 'cart': cart, 'item_num': item_num}
    return render(request, 'shop/index.html', products_list)


def about(request):
    return render(request, 'shop/about.html')


def contact(request):
    if request.method == "POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
        thank = True
        subject = "Vist to MY SHOPPING"
        message = "thank you  for take out some time for us. "
        send_mail(subject, message, settings.EMAIL_HOST_USER, [email], fail_silently=False)
        return render(request, 'shop/contact.html', {'thank': thank})
    return render(request, 'shop/contact.html')


def tracker(request):
    if request.method == "POST":
        order_unique_id = request.POST.get('orderid', '')
        email = request.POST.get('email', '')

        try:
            order = Order.objects.filter(order_unique_id=order_unique_id, email=email)
            if len(order) > 0:
                update = OrderReport.objects.filter(order_id=order_unique_id)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps({"status": "success", "updates": updates, "items_json": order[0].items_json},
                                          default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status": "noitem"}')
        except Exception as e:
            return HttpResponse('{"status": "error"}')

    return render(request, 'shop/tracker.html')


def cart(request):
    user_id = request.session.get('id')
    list = Cart.objects.values('name', 'qty', 'price').filter(user_id=user_id)
    total = 0
    total_item = 0
    item_num = 0
    for i in list:
        y = i['qty']
        total_item += y
        x = i['price']
        total += x
        item_num += i['qty']
    return render(request, 'shop/cart.html',
                  {'list': list, 'total': total, 'total_item': total_item, 'item_num': item_num})


def cart_delete(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id', '')
        Cart.objects.filter(user_id=user_id).delete()
    return HttpResponse()


def minus_db(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        id = request.POST.get('user_id', '')
        Cart.objects.filter(user_id=id, name=name).delete()
    return HttpResponse()


def cart_table(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        qty = request.POST.get('qty', '')
        price = request.POST.get('price', '')
        user_id = request.POST.get('user_id', '')
        product_id = request.POST.get('product_id', '')
        total = int(price) * int(qty)

    if Cart.objects.filter(name=name, user_id=user_id):
        Cart.objects.filter(name=name).update(qty=qty, price=total)

    else:
        cart_db = Cart(name=name, qty=qty, price=total, user_id=user_id, product_id=product_id)
        cart_db.save()

    return HttpResponse(request)


def products(request, myid):
    ele_products = Electric.objects.filter(id=myid)
    return render(request, 'shop/prod_view.html', {'product': ele_products[0]})


def checkout(request):
    user_id = request.session.get('id')
    list = Cart.objects.values().filter(user_id=user_id)
    total = 0
    for i in list:
        x = i['price']
        total += x
    if request.method == "POST":
        itemsJson = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        amount = request.POST.get('amount', '')
        address = request.POST.get('address1', '') + "" + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        order_unique_id = key_genarate()
        user_id = user_id
        order = Order(order_unique_id=order_unique_id, name=name, email=email, phone=phone, address=address, city=city,
                      state=state, zip_code=zip_code, user_id=user_id,
                      items_json=itemsJson, amount=amount)
        order.save()

        update = OrderReport(order_id=order.order_unique_id, update_desc='order has been placed', user_id=user_id)
        update.save()
        thank = True
        id = order.order_unique_id
        subject = "Successfully purchase items"
        message = "thank you  for purchase items from us your total amount is " + amount + " Your order will be reach at you as soon as possible. Your Order Id is." + id
        send_mail(subject, message, settings.EMAIL_HOST_USER, [email], fail_silently=False)
        return render(request, 'shop/checkout.html', {'thank': thank, 'id': id})
    return render(request, 'shop/checkout.html', {'list': list, 'total': total})


def key_genarate():
    number = '0123456789'
    alpha = 'abcdefghijklmnopqrstuvwxyz'
    id = ''
    for i in range(0, 10, 2):
        id += random.choice(number)
        id += random.choice(alpha)
    return id


def search(request):
    queary = request.GET['queary']
    if len(queary) > 78:
        allprod = Electric.objects.none()
    else:
        allprodstitle = Electric.objects.filter(product_name__contains=queary)
        allprodscategory = Electric.objects.filter(category__contains=queary)
        allprod = allprodstitle.union(allprodscategory)
    user_id = request.session.get('id')
    cart = Cart.objects.values('name', 'qty').filter(user_id=user_id)
    item_num = 0
    for i in cart:
        item_num += i['qty']
    list = Cart.objects.all()

    params = {'allprod': allprod, 'queary': queary, 'list': list,
              'id_': user_id, 'cart': cart, 'item_num': item_num}
    return render(request, 'shop/search.html', params)
