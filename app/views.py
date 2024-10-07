from django.db.models import Count
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.views import View
import razorpay
from . models import Cart, Product, Customer, Payment, OrderPlaced, Wishlist
from django.contrib.auth.decorators import login_required
from . forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.conf import settings
from django.utils.decorators import method_decorator

@login_required
def home(request):
	totalitem = total_item(request)
	wishlist = total_wish(request)
	return render(request, "app/home.html", locals())


@login_required
def about(request):
	totalitem = total_item(request)
	wishlist = total_wish(request)
	return render(request, "app/about.html",locals())


@login_required
def contact(request):
	totalitem = total_item(request)
	wishlist = total_wish(request)
	return render(request, "app/contact.html", locals())


@login_required
def logout_user(request):
	logout(request)
	messages.success(request, "Logged out successfully.")
	return redirect('login')


@method_decorator(login_required, name='dispatch')
class CategoryView(View):
	def get(self, request, val):
		totalitem = total_item(request)
		wishlist = total_wish(request)
		products = Product.objects.filter(category=val)
		title = Product.objects.filter(category=val).values('title')
		return render(request, "app/category.html", locals())
	

@method_decorator(login_required, name='dispatch')
class CategoryTitleView(View):
	def get(self, request, val):
		totalitem = total_item(request)
		wishlist = total_wish(request)
		products = Product.objects.filter(title=val)
		title = Product.objects.filter(category=products[0].category).values('title')
		return render(request, "app/category.html", locals())
	

@method_decorator(login_required, name='dispatch')
class ProductDetailView(View):
	def get(self, request, pk):
		product = Product.objects.get(pk=pk)
		wishitem = Wishlist.objects.filter(Q(product=product) & Q(user=request.user))
		totalitem = total_item(request)
		wishlist = total_wish(request)
		return render(request, "app/productdetail.html", locals())


class CustomerRegistrationView(View):
	def get(self, request):
		form = CustomerRegistrationForm()
		return render(request, "app/customerregistration.html", {'form': form})
	
	def post(self, request):
		form = CustomerRegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, "Registration is successful.")
			form = CustomerRegistrationForm()
		else:
			messages.warning(request, "Invalid input, try again.")
		return render(request, "app/customerregistration.html", {'form': form})
	

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
	def get(self, request):
		totalitem = total_item(request)
		wishlist = total_wish(request)
		cart = Cart.objects.filter(user=request.user)
		form = CustomerProfileForm()
		return render(request, "app/profile.html", locals())
	
	def post(self, request):
		form = CustomerProfileForm(request.POST)
		if form.is_valid():
			user = request.user
			name = form.cleaned_data['name']
			mobile = form.cleaned_data['mobile']
			city = form.cleaned_data['city']
			zipcode = form.cleaned_data['zipcode']
			messages.success(request, "Profile saved successfully.")
			profile = Customer(user=user, name=name, mobile=mobile, city=city, zipcode=zipcode)
			profile.save()
		else:
			messages.warning(request, "Invalid input, try again.")
		return render(request, "app/profile.html", locals())
	

@login_required
def address(request):
	totalitem = total_item(request)
	wishlist = total_wish(request)
	address = Customer.objects.filter(user=request.user)
	return render(request, "app/address.html", locals())


@method_decorator(login_required, name='dispatch')
class UpdateAddress(View):
	def get(self, request, pk):
		totalitem = total_item(request)
		wishlist = total_wish(request)
		customer = Customer.objects.get(pk=pk)
		form = CustomerProfileForm(instance=customer)
		return render(request, "app/profile.html", locals())
	
	def post(self, request, pk):
		form = CustomerProfileForm(request.POST)
		if form.is_valid():
			cust = Customer.objects.get(pk=pk)
			cust.name = form.cleaned_data['name']
			cust.mobile = form.cleaned_data['mobile']
			cust.city = form.cleaned_data['city']
			cust.zipcode = form.cleaned_data['zipcode']
			messages.success(request, "Profile saved successfully.")
			cust.save()
		else:
			messages.warning(request, "Invalid input, try again.")
		return redirect('address')


@login_required
def add_to_cart(request):
	user = request.user
	totalitem = total_item(request)
	wishlist = total_wish(request)
	product_id = request.GET.get('prod_id')
	product = Product.objects.get(id=product_id)
	Cart(user=user, product=product).save()
	return redirect('/showcart')


@login_required
def show_cart(request):
	user = request.user
	totalitem = total_item(request)
	wishlist = total_wish(request)
	cart = Cart.objects.filter(user=user)
	amount = 0
	for p in cart:
		value = p.quantity * p.product.discounted_price
		amount += value
	totalamount = amount + 50
	return render(request, "app/addtocart.html", locals())


@method_decorator(login_required, name='dispatch')
class CheckoutView(View):
	def get(self, request):
		user = request.user
		totalitem = total_item(request)
		wishlist = total_wish(request)
		address = Customer.objects.filter(user=user)
		cart = Cart.objects.filter(user=user)
		famount = 0
		for p in cart:
			famount += (p.quantity * p.product.discounted_price)
		totalamount = famount + 50
		razoramount = int(totalamount * 100)
		client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
		data = { "amount": razoramount, "currency": "INR", "receipt": "order_rcptid_12"}
		payment_response = client.order.create(data=data)
		print (payment_response)

		order_id = payment_response['id']
		order_status = payment_response['status']
		if order_status == 'created':
			payment = Payment (
			user = user,
			amount = totalamount,
			razorpay_order_id = order_id,
			razorpay_payment_status = order_status
			)
			payment.save()
		return render(request, "app/checkout.html", locals())


@login_required
def payment_done(request):
	order_id=request.GET.get('order_id')
	payment_id=request.GET.get('payment_id')
	cust_id=request.GET.get('cust_id')
	# print("payment_doneoid= ", order_id," pid = ", payment_id," cid = ",cust_id)
	user=request.user
	#return redirect("orders")
	customer=Customer.objects.get(id=cust_id)
	#To update payment status and payment id
	payment = Payment.objects.get(razorpay_order_id=order_id)
	payment.paid = True
	payment.razorpay_payment_id= payment_id
	payment.save()
	#To save order details
	cart = Cart.objects.filter(user=user)
	for c in cart:
		OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity, payment=payment).save()
		c.delete()
	return redirect("orders")


@login_required
def orders(request):
	totalitem = total_item(request)
	wishlist = total_wish(request)
	order_placed = OrderPlaced.objects.filter(user=request.user)
	return render(request, "app/orders.html", locals())


def plus_cart(request):
	if request.method == 'GET':
		prod_id = request.GET['prod_id']
		c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
		c.quantity += 1
		c.save()
		user = request.user
		cart = Cart.objects.filter(user=user)
		amount = 0
		for p in cart:
			amount += (p.quantity * p.product.discounted_price)
		totalamount = amount + 50
		
		data={
			"quantity": c.quantity,
			"amount": amount,
			"totalamount": totalamount
		}
		return JsonResponse(data)
	

def minus_cart(request):
	if request.method == 'GET':
		prod_id = request.GET['prod_id']
		c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
		c.quantity -= 1
		c.save()
		user = request.user
		cart = Cart.objects.filter(user=user)
		amount = 0
		for p in cart:
			value = p.quantity * p.product.discounted_price
			amount += value
		totalamount = amount + 50
		
		data={
			"quantity": c.quantity,
			"amount": amount,
			"totalamount": totalamount
		}
		return JsonResponse(data)
	

def remove_cart(request):
	if request.method == 'GET':
		prod_id = request.GET['prod_id']
		c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
		c.delete()
		user = request.user
		cart = Cart.objects.filter(user=user)
		amount = 0
		for p in cart:
			value = p.quantity * p.product.discounted_price
			amount += value
		totalamount = amount + 50
		
		data={
			"amount": amount,
			"totalamount": totalamount
		}
		return JsonResponse(data)


def	total_item(request):
	totalitem = 0
	if request.user.is_authenticated:
		totalitem = len(Cart.objects.filter(user=request.user))
	return totalitem

def	total_wish(request):
	wishitem = 0
	if request.user.is_authenticated:
		wishitem = len(Wishlist.objects.filter(user=request.user))
	return wishitem


def plus_wishlist(request):
	if request.method == 'GET':
		prod_id=request.GET['prod_id']
		product=Product.objects.get(id=prod_id)
		user = request.user
		Wishlist(user=user, product=product).save()
		data={
		'message': 'Wishlist Added Successfully',
		}
		return JsonResponse(data)


def minus_wishlist(request):
	if request.method == 'GET':
		prod_id=request.GET['prod_id']
		product=Product.objects.get(id=prod_id)
		user = request.user
		Wishlist.objects.filter(user=user, product=product).delete()
		data={
		'message': 'Wishlist Remove Successfully',
		}
		return JsonResponse(data)
	

def wishlist(request):
	totalitem = total_item(request)
	wishlist = total_wish(request)
	product = Wishlist.objects.filter(user=request.user)
	return render(request, "app/wishlist.html", locals())



def search(request):
	query = request.GET['search']
	totalitem = total_item(request)
	wishlist = total_wish(request)
	product = Product.objects.filter(Q(title__icontains=query))
	return render(request, "app/search.html", locals())

#5:36:20