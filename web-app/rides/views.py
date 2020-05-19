from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from .models import Ride, Driver
from .forms import RideForm
from .forms import DriverForm
from django.db.models import Q

# Create your views here.
def home(request):
    return render(request, "home.html", {})

def rides(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')
    # for drivers
    entry = Driver.objects.filter(user=request.user.id)
    if entry.exists():
        print("It's a driver")
        return redirect("orders")

    obj = Ride.objects.filter(Q(user=request.user.id) | Q(sharer=request.user.id)).exclude(status="complete")
    drivers = Driver.objects.filter(user=request.user.id)
    context = {
        'objects' : obj,
        'drivers' : drivers
    }
    return render(request, "rides.html", context)

def create(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')
    form = RideForm(request.POST or None)
    context = {
        'form' : form
    }
    return render(request, "create.html", context)

def submit(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')
    data = request.POST.copy()
    data['user'] = str(request.user.id)
    print(data)
    form = RideForm(data or None)
    if form.is_valid():
        form.save()
        return redirect('rides')
    else:
        print("form invalid")

def edit(request, ride_id):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')
    global ride_form
    if request.POST:
        form = RideForm(request.POST)
        print(form)
        if form.is_valid():
            book = Ride.objects.get(pk=ride_id)
            ride_form = RideForm(request.POST, instance = book)
            ride_form.save() #cleaned indenting, but would not save unless I added at least 6 characters.
            return redirect('/rides/')
    else:
        ride = Ride.objects.get(pk=ride_id)
        ride_form = RideForm(instance=ride)

    return render(request, 'edit.html', {'ride_id': ride_id, 'form':ride_form })

def search(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')
    if request.POST:
        print(request.POST['destination'])
        obj = Ride.objects.filter(destination=request.POST['destination'], number=request.POST['number'], arrival=request.POST['arrival'], shared=True, status="open")
        context = {
            'objects': obj
        }
        return render(request, "result.html", context)
    else:
        return render(request, 'search.html', {})




# Create your views here.

def register(request):
    form = UserCreationForm
    context = {
        'form' : form
    }
    return render(request, "registration/register.html", context)

def signup(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        form.save()
    return redirect('/rides')

def driver(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')
    if request.POST:
        data = request.POST.copy()
        # data['user'] = str(request.user.id)
        print(data)
        form = DriverForm(data or None)
        if form.is_valid():
            form.save()
            return redirect('rides')
        else:
            print("form invalid")
    else:
        form = DriverForm(request.POST or None)
        context = {
            'user': request.user,
            'form': form
        }
        return render(request, "driver.html", context)

def update(request, user):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')
    global driver_form
    if request.POST:
        data = request.POST.copy()
        # data['user'] = str(request.user.id)
        form = DriverForm(data or None)
        print(form)
        if form.is_valid():
            book = Driver.objects.get(pk=user)
            driver_form = DriverForm(request.POST, instance = book)
            driver_form.save() #cleaned indenting, but would not save unless I added at least 6 characters.
            return redirect('/rides/')
    else:
        driver = Driver.objects.get(pk=user)
        driver_form = DriverForm(instance=driver)

    return render(request, 'update.html', {'user': user, 'form':driver_form })

def orders(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')
    # for drivers
    entry = Driver.objects.filter(user=request.user.id)
    if not entry.exists():
        print("It's a rider")
        return redirect("rides")

    obj = Ride.objects.filter(status="confirmed")
    drivers = Driver.objects.filter(user=request.user.id)
    context = {
        'objects' : obj,
        'drivers' : drivers
    }
    return render(request, "orders.html", context)

def confirm(request, ride_id):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')
    Ride.objects.filter(pk=ride_id).update(status='confirmed')
    Ride.objects.filter(pk=ride_id).update(driver=request.user.id)
    print(Ride.objects.get(pk=ride_id).email)
    send_mail('Your ride is confirmed!', 'Check out http://localhost:8000/', 'pcphd97@163.com',
              [Ride.objects.get(pk=ride_id).email], fail_silently=False)
    return redirect("orders")

def opens(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')
    # for drivers
    entry = Driver.objects.filter(user=request.user.id)
    if not entry.exists():
        print("It's a rider")
        return redirect("rides")

    obj = Ride.objects.filter(status="open")
    drivers = Driver.objects.filter(user=request.user.id)
    context = {
        'objects' : obj,
        'drivers' : drivers
    }
    return render(request, "opens.html", context)

def complete(request, ride_id):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')
    Ride.objects.filter(pk=ride_id).update(status='complete')
    return redirect("orders")

def detail(request, ride_id):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')
    ride = Ride.objects.get(pk=ride_id)
    driver = Driver.objects.get(user=ride.driver)
    return render(request, 'detail.html', {'ride': ride, 'driver':driver })

def join(request, ride_id):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')
    Ride.objects.filter(pk=ride_id).update(sharer=request.user.id)
    return redirect("rides")