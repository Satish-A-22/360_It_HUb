# views.py
from django.shortcuts import render,redirect

from It_Services.models import UserData,Service

from It_Services.forms import UserDataForm,ServiceForm

def first(request):
    return redirect("https://satish-a-22.github.io/Satish_A_Portfolio/")


def submit_form(request):
    local=False
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        check = request.POST.get('check', 'off')  # 'check' is the name attribute in your HTML form
        tick = check == 'on'
        # request.session['local']=False
        # print(request.session.get('local'))
        # lock=False
        
        # Check if the email already exists
        if UserData.objects.filter(email=email).exists():
            if UserData.objects.filter(password=password).exists():
                local=False
                request.session['lock'] = True
                print(request.session.get('lock'))
            # return render(request, 'item.html', {'error_message': 'Account with this email already exists'})
                return service_list(request)
            else:
                return render(request, 'home.html', {'error_message': 'Account and Password not matching'})
                

        # Check if the checkbox is not checked
        if not tick:
            return render(request, 'home.html', {'error_message': 'Please check the box to proceed'})

        # Save the new user data
        store = UserData(email=email, password=password, check_me_out=tick)
        
        store.save()
        # request.session['lock'] = True
        # Redirect to the email page or home page after successful save
        
        email = request.POST.get('email')
            # Check if the email exists in the UserData model
            # user = UserData.objects.filter(email=email).first()
            
                # Generate a 4-digit OTP
                 # Redirect to OTP verification page
        otp = random.randint(1000, 9999)
                # Store the OTP in the user's session
        request.session['otp'] = otp
        request.session['email'] = email
                
                # Send the OTP via email
        send_mail(
            'Your OTP Code',
            f'Your OTP code is {otp}.',
            'from@example.com',
            [email],
            fail_silently=False,
        )
        return redirect('otp') # Redirect to home.html if email not found
    return render(request, 'home.html')

        
        
    #     return redirect('otp') 
    # # Replace 'email_page' with your actual URL name for the success page

    # # Handle GET requests or when the form is not submitted
    # return render(request, 'home.html')

from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
import random
# from django.contrib.auth import views as auth_views
 
from django.shortcuts import render, get_object_or_404

def email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        # Check if the email exists in the UserData model
        user = UserData.objects.filter(email=email).first()
        if user:
            # Generate a 4-digit OTP
            otp = random.randint(1000, 9999)
            # Store the OTP in the user's session
            request.session['otp'] = otp
            request.session['email'] = email
            
            # Send the OTP via email
            send_mail(
                'Your OTP Code',
                f'Your OTP code is {otp}.',
                'from@example.com',
                [email],
                fail_silently=False,
            )
            return redirect('otp')  # Redirect to OTP verification page
        else:
            return redirect('home')  # Redirect to home.html if email not found
    return render(request, 'email.html')

def otp(request):
    if request.method == 'POST':
        otp1 = request.POST.get('otp1')
        otp2 = request.POST.get('otp2')
        otp3 = request.POST.get('otp3')
        otp4 = request.POST.get('otp4')
        entered_otp = f"{otp1}{otp2}{otp3}{otp4}"
        session_otp = str(request.session.get('otp'))

        if entered_otp == session_otp:
            # return redirect('items')  # Redirect to itemform.html if OTP is correct
            request.session['lock'] = True
            return service_list(request)
        else:
            messages.error(request, 'OTP does not match')
            return redirect('otp')  # Reload OTP page with error message

    return render(request, 'otp.html')
lock=False
def service_list(request):
    print(request.session.get('lock'))
    if request.session.get('lock')==True:
        services = Service.objects.all()  # Fetch all services from the database
        request.session['lock']=True
        return render(request, 'item.html', {'services': services})
    else:
        return render(request,'home.html')
   
def submit_service(request):
    print(request.session.get('lock'))
    if request.session.get('lock')==True:
        if request.method == 'POST':
            form = ServiceForm(request.POST, request.FILES)
            if form.is_valid():
                # Save the form data to the database
                form.save()
                return service_list(request) # Redirect to the home page or any other page after successful submission
        else:
            form = ServiceForm()
        return render(request, 'itemform.html', {'form': form})
    else:
        return render(request,'home.html')

def service_detail(request, pk):
    service = get_object_or_404(Service, pk=pk)
    return render(request, 'service_detail.html', {'service': service})

def update_service(request, pk):
    service = get_object_or_404(Service, pk=pk)
    form = ServiceForm(request.POST or None, instance=service)
    if form.is_valid():
        form.save()
        # return redirect('service_detail', pk=service.pk)
        return service_list(request)
        
    return render(request, 'update_service.html', {'form': form, 'service': service})


def delete_service(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        service.delete()
        return redirect('service_list')
    return render(request, 'delete_service.html', {'service': service})


from django.shortcuts import render, get_object_or_404, redirect
from .models import Service, Subscription
from django.http import JsonResponse
import razorpay

def subscription_page(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    return render(request, 'subscription.html', {'service': service})



def subscription_view(request, pk):
    service = get_object_or_404(Service, pk=pk)
    # net_price = service.service_price + (service.service_price * service.service_tax / 100)
    price=service.service_price
    tax= service.service_tax

    if request.method == 'POST':
        action = request.POST.get('action')
        address = request.POST.get('address')
        # check= request.POST.get('check','off')
        
        if action == 'subscribe':
            # Handle subscription logic
            Subscription.objects.create(
                service=service,
                address=address,
                payment_status='pending'
            )
            return redirect('subscription_page', pk=pk)

        elif action == 'paynow':
            
            razorpay_order_id = request.POST.get('razorpay_order_id')
            razorpay_payment_id = request.POST.get('razorpay_payment_id')
            razorpay_signature = request.POST.get('razorpay_signature')
            request.session['pay_id']=razorpay_payment_id
            
            # Here, you should verify the payment using Razorpay's client library
            # Assuming payment verification is done and successful

            Subscription.objects.create(
                service=service,
                address=address,
                razorpay_order_id=razorpay_order_id,
                razorpay_payment_id=razorpay_payment_id,
                razorpay_signature=razorpay_signature,
                payment_status='completed'
            )
            return redirect('success')  # Redirect to a success page after payment

    return render(request, 'subscription_page.html', {'service': service, 'price': price,'tax':tax})

def create_subscription(request):
    if request.method == 'POST':
        service_id = request.POST['service_id']
        address = request.POST['address']
        razorpay_order_id = request.POST['razorpay_order_id']
        razorpay_payment_id = request.POST['razorpay_payment_id']
        razorpay_signature = request.POST['razorpay_signature']
        
        subscription = Subscription(
            service_id=service_id,
            address=address,
            razorpay_order_id=razorpay_order_id,
            razorpay_payment_id=razorpay_payment_id,
            razorpay_signature=razorpay_signature,
            payment_status='completed'  # Assuming payment is successful
        )
        subscription.save()
        return redirect('success')  # Redirect to a success page or any other page
    return redirect('home')  # Redirect to home if the request is not POST

def razorpay_callback(request):
    if request.method == 'POST':
        data = request.POST
        razorpay_order_id = data.get('razorpay_order_id')
        razorpay_payment_id = data.get('razorpay_payment_id')
        razorpay_signature = data.get('razorpay_signature')
        
        subscription = Subscription.objects.filter(
            razorpay_order_id=razorpay_order_id,
            razorpay_payment_id=razorpay_payment_id,
            razorpay_signature=razorpay_signature
        ).first()
        
        if subscription:
            subscription.payment_status = 'completed'
            subscription.save()
            return JsonResponse({'status': 'success'})
    
    return JsonResponse({'status': 'failure'})

def log(request):
    del request.session['lock']
    del request.session['pay_id']
    return submit_form(request)
    
def success(request):
    id=request.session.get('pay_id')
    return render(request,'success_page.html',{'pay_id':id})