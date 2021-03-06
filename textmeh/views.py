from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserForm
from django.contrib.auth.models import User
from .models import UserLanguage, Chat
from django.contrib.sessions.models import Session
from django.utils import timezone
# from microsofttranslator import Translator
from .utils import Translator


@login_required
def home_page(request):
	queryset = get_current_users()
	currentusers = []
	for user in queryset:
		if user != request.user:
			currentusers.append((user.username, UserLanguage.objects.get(user=user).language))
	
	return render(request, 'textmeh/home_page.html', { 'currentusers': currentusers })

def get_current_users():
    active_sessions = Session.objects.filter(expire_date__gte=timezone.now())
    user_id_list = []
    for session in active_sessions:
        data = session.get_decoded()
        user_id_list.append(data.get('_auth_user_id', None))
    # Query all logged in users based on id list
    return User.objects.filter(id__in=user_id_list)

def registration(request):
	if request.method == 'POST':
		userform = UserForm(request.POST)
		if userform.is_valid():
			username = userform.cleaned_data['username']
			password = userform.cleaned_data['password']
			language = userform.cleaned_data['language']
			user = User.objects.create_user(username=username, password=password)
			user.save()
			userlanguage = UserLanguage.objects.create(user=user, language=language, language_code=UserLanguage.getLanguageCode(language))	
			userlanguage.save()
			return redirect('home_page')
	else:
		userform = UserForm()
	return  render(request, 'textmeh/registration.html', { 'form': userform, 'language_list': sorted(UserLanguage.getLanguageList()) })

@login_required
def chat(request, username):
	if request.method == 'POST':
		message = request.POST.get('textarea', None)
		if message:
			ok = True
			while (ok):
				try:
					translator = Translator('74857aa273724df793371c715124228d')
					# translator = Translator('TextMeh', 'DX4su+1nsJeXzH0t+HbyHQDbzOpXeX4nXL4ScOiPQKc=')
					translation = translator.translate(message, UserLanguage.objects.get(user=User.objects.get(username=username)).language_code)
					ok = False
				except:
					pass
			chat = Chat(sender=request.user, receiver=User.objects.get(username=username), message=message, translation=translation, time=timezone.now())
			chat.save()
			return redirect('chat', username=username)
	chat = Chat.objects.filter(sender=request.user, receiver=User.objects.get(username=username)) | Chat.objects.filter(sender=User.objects.get(username=username), receiver=request.user)
	chat = chat.order_by('time')
	return  render(request, 'textmeh/chat.html', { 'chat': chat })

@login_required
def messages(request, username):
	chat = Chat.objects.filter(sender=request.user, receiver=User.objects.get(username=username)) | Chat.objects.filter(sender=User.objects.get(username=username), receiver=request.user)
	chat = chat.order_by('time')
	return  render(request, 'textmeh/messages.html', { 'chat': chat , 'username': username})	















