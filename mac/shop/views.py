from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .models import Product,Contact,Order,OrderUpdate
from math import ceil
from django.contrib.auth.models import User,auth
import json
from django.contrib import messages
# Create your views here.
def index(request):
    # products=Product.objects.all()

    allprods=[]
    catprods=Product.objects.values('category','id')
    # print(catprods)
    cats={item['category'] for item in catprods}
    for cat in cats:
        prod=Product.objects.filter(category=cat)
        n = len(prod)
        nslides = n // 4 + ceil(n / 4 - n // 4)
        allprods.append([prod,range(1,nslides),nslides])
    params={'allProds':allprods}
    # params={'nslides':nslides,'range':range(1,nslides),'product':products}
    return render(request,'shop/index.html',params)

def login(request):
    if(request.method=="POST"):
        username=request.POST['username']
        password=request.POST['password']
        print("-------------------")
        user=auth.authenticate(username=username,password=password)
        if(user is not None):
            auth.login(request,user)
            return HttpResponseRedirect("/home")
        else:
            messages.info(request,'Invalid Credentials')
            return HttpResponseRedirect("/")
    else:
        return render(request,'shop/login.html')

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')
def about(request):
    return render(request,'shop/about.html')

def contact(request):
    if request.method=='POST':
        name=request.POST.get('name',"")
        email=request.POST.get('email',"")
        phone=request.POST.get('phone',"")
        desc=request.POST.get('desc',"")
        contact=Contact(name=name,email=email,phone=phone,desc=desc)
        contact.save()
    return render(request,'shop/contact.html')

def tracker(request):
    if request.method=='POST':
        orderId=request.POST.get('orderId',"")
        email=request.POST.get('email',"")
        print(orderId,email)
        try:
            order=Order.objects.filter(order_id=orderId,email=email)
            if(len(order)>0):
                update=OrderUpdate.objects.filter(order_id=orderId)
                updates=[]
                for item in update:
                    updates.append({'text':item.update_desc,'time':item.timestamp})
                    response = json.dumps([updates,order[0].items_json],default=str)
                return HttpResponse(response)
            else:
                return HttpResponse("{}")
        except Exception :
            return HttpResponse("{}")
    return render(request,'shop/tracker.html')

def search(request,ll=None):
    allprods=[]
    # catprods=Product.objects.values('category','id')
    # print(catprods)
    prod_filter=Product.objects.raw(f"SELECT * FROM shop_Product WHERE product_name LIKE '%{ll}%'")
    # print(prod)
    cats={item.category for item in prod_filter}
    print(cats)
    for cat in cats:
        prod=[]
        for i in prod_filter:
            if(i.category==cat):
                prod.append(i)
        n = len(prod)
        print(prod)
        nslides = n // 4 + ceil(n / 4 - n // 4)
        allprods.append([prod,range(1,nslides),nslides])
    
    params={'allProds':allprods}
    # params={'nslides':nslides,'range':range(1,nslides),'product':products}
    return render(request,'shop/index.html',params)

def productview(request,myid):
    product=Product.objects.filter(id=myid)

    return render(request,'shop/prouctview.html',{'product':product[0]})

def checkout(request):
    if request.method=='POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        itemsjson=request.POST.get('itemsjson')
        address=request.POST.get('address1')+" "+request.POST.get('address2')
        city=request.POST.get('city')
        state=request.POST.get('state')
        zip_code=request.POST.get('zip_code')
        print('$$',itemsjson)
        order=Order(name=name,email=email,phone=phone,address=address,state=state,city=city,zip_code=zip_code,items_json=itemsjson)
        order.save()
        thank=True
        order_id=order.order_id
        update=OrderUpdate(order_id=order_id,update_desc="Your order has been placed successfully.")
        update.save()
        # print("id=",order_id)
        return render(request,'shop/checkout.html',{'thank':thank,'id':order_id})
    return render(request,'shop/checkout.html')


