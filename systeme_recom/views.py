from _curses import flash

from django.contrib.auth.models import User
from django.contrib.sessions.backends import db
from django.core.mail import send_mail, BadHeaderError
from django.core.paginator import Paginator
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect


from .inscription import NewUserForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes

from .formContact import ContactForm
from .forms import CultureForm
import turicreate as tc
from .models import Culture, UserProfile
from django.http import JsonResponse
from django.core import serializers

# Create your views here.
# if form.is_valid():
#     form.save()
#     return HttpResponse(' submitted successfully ')


def index(request):
    cultures = Culture.objects.all()
    data = {'cultures': cultures}
    return render(request,'index.html',data)


def culture(request):
    cultures = Culture.objects.all()
    data = {'cultures': cultures}
    return render(request, 'culture.html', data)


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("index")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request, template_name="register.html", context={"register_form": form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, "You are now logged in as {username}.")
                return redirect("index")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="login.html", context={"login_form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("index")

def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "password_reset_email"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ("/password_reset/done/")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="password_reset.html", context={"password_reset_form":password_reset_form})


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = "Contact"
        body = {
            'first_name': form.cleaned_data['first_name'],
            'last_name': form.cleaned_data['last_name'],
            'email': form.cleaned_data['email_address'],
            'message': form.cleaned_data['message'],
        }
        message = "\n".join(body.values())

        try:
            send_mail(subject, message, 'admin@example.com', ['admin@example.com'])
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        return redirect("index")
    form = ContactForm()
    return render(request,'contact.html',{'form': form})


def apropos(request):
    return render(request, 'apropos.html')


def mil(request):
    cultures = Culture.objects.all()
    data = {'cultures': cultures}
    return render(request, 'mil.html', data)


def riz(request):
    cultures = Culture.objects.all()
    data = {'cultures': cultures}
    return render(request, 'riz.html', data)


def arachide(request):
    cultures = Culture.objects.all()
    data = {'cultures': cultures}
    return render(request, 'arachide.html', data)


def mais(request):
    cultures = Culture.objects.all()
    data = {'cultures': cultures}
    return render(request, 'mais.html', data)


def sorgho(request):
    cultures = Culture.objects.all()
    data = {'cultures': cultures}
    return render(request, 'sorgho.html', data)


def tomate(request):
    cultures = Culture.objects.all()
    data = {'cultures': cultures}
    return render(request, 'tomate.html', data)


def niebe(request):
    cultures = Culture.objects.all()
    data = {'cultures': cultures}
    return render(request, 'niebe.html', data)

load = tc.load_model('/home/aminadev/PycharmProjects/memoireSr/memoireSr/memoireSr/modellef.model')
@login_required(login_url='/login')
def recom(request):
    cultures = Culture.objects.all()
    data = {'cultures': cultures}
    form = CultureForm(request.POST or None)
    if form.is_valid():
        # Culture.user_id = User.objects.get(pk=request.user.id)
        form.save()
        new_user_info = tc.SFrame({'user_id': [request.user.id],
                                   'temperature': [form.cleaned_data['temperature']], 'ph': [form.cleaned_data['ph']],
                                   'typeCulture': [form.cleaned_data['typeCulture']],
                                   'sol': [form.cleaned_data['sol']]})
        recommendations = load.recommend([request.user.id], new_user_data=new_user_info,exclude_known=False, k=5)
        r = list(recommendations)
        form = CultureForm()
        return render(request, 'status.html', {"r": r, "cultures": cultures})
        # return HttpResponse(' submitted successfully ')
    context = {'form': form}
    return render(request, 'recom.html', context)

def search(request):
    if request.method == "POST":
        searched = request.POST['searched']
        cultures = Culture.objects.filter(nomCulture__contains=searched)
        # paginator = Paginator(cultures, 3)
        # page = request.GET.get('page')
        # culturs = paginator.get_page(page)
        return render(request, 'culture.html', {'searched': searched,'cultures':cultures})
    else:
        return render(request, 'culture.html')

@login_required(login_url='/admin')
def dashboard(request):
    profiles = UserProfile.objects.all()
    users = User.objects.all()
    cultures = Culture.objects.all()
    total_users = users.count()
    total_recom = profiles.count()
    riz_total = cultures.filter(nomCulture='riz').count()
    arachide_total = cultures.filter(nomCulture='arachide').count()
    mil_total = cultures.filter(nomCulture='mil').count()
    mais_total = cultures.filter(nomCulture='maïs').count()
    niebe_total = cultures.filter(nomCulture='niébé').count()
    sorgho_total = cultures.filter(nomCulture='sorgho').count()
    tomate_total = cultures.filter(nomCulture='tomate').count()
    last_ten = UserProfile.objects.order_by('-id')[:5:-1]
    paginator = Paginator(users, 7)
    page = request.GET.get('page')
    culturs = paginator.get_page(page)
    context = {'profiles': profiles,
             'users': users,
             'total_users': total_users,
             'total_recom': total_recom,
             'riz_total': riz_total,
             'arachide_total': arachide_total,
             'mil_total': mil_total,
             'mais_total': mais_total,
             'niebe_total': niebe_total,
             'sorgho_total': sorgho_total,
             'tomate_total': tomate_total,
             'last_ten': last_ten,
             'culturs': culturs,
             }
    if  request.user.is_staff:
        return render(request, 'dashboard/dashboard.html',context)
    else:
        return HttpResponse('Page reserver aux administrateurs')




@login_required(login_url='/login')
def profil(request):
    #games = V_GAMES.query.paginate(per_page=10, page=page_num, error_out=True)
    users = User.objects.all()
    profile = UserProfile.objects.all()
    if request.method == 'POST':
        check = request.POST.getlist('checks[]')
        print(check)
        for i in check:
            ID_NCULTURE = Culture.objects.get(pk=i).nomCulture
            ID_VARIETE = Culture.objects.get(pk=i).variete
            ID_RENDEMENT =Culture.objects.get(pk=i).rendement
            ID_HUMIDITE = Culture.objects.get(pk=i).humidite
            ID_CM = Culture.objects.get(pk=i).cycleDeMaturation
            profiles = UserProfile(request.user.id,ID_NCULTURE=ID_NCULTURE, ID_VARIETE=ID_VARIETE, ID_RENDEMENT=ID_RENDEMENT,ID_HUMIDITE=ID_HUMIDITE, ID_CM=ID_CM)
            profiles.save()

           # print(profiles)

        #
        #     flash('Games have been successfully added to your profile.')
        #
        # else:
        #     flash('You have to check at least one game to add to your profile!')

    return  render(request, 'profil.html', {'profile': profile,'users':users})

