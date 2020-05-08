from django.shortcuts import render, HttpResponse,redirect
from django.template import loader
from django.http import HttpResponse

from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.conf import settings

from uuid import uuid4

from gyms.models import *

# Create your views here.
def index(request):

	template = loader.get_template('index.html')
	context = {
		    'post_title': "This is a new post", 
		    'author':'RamB',
		    'post_content':'This is the content os a post',
		    'item_list':['D1', 'D2', 'D3'],
		    'comments':'This is a comment'
			}
	return HttpResponse(template.render(context, request))


def login(request):
	context = {}
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = User.objects.filter(username = username, password = password, status = 'Active').first()
		if user:
			request.session['username'] = username
			template = loader.get_template('index.html')
			context = {
			   'logged_in':True,
			   'user' : user
			}	
		else:
			template = loader.get_template('login.html')
			context = {
					'logged_in':False,
					'message':"Please enter the valid credentials or have you activated your account??"
			   
			}	
		return HttpResponse(template.render(context, request))
			
	template = loader.get_template('login.html')
	return HttpResponse(template.render(context, request))


def register(request):
	if request.method == 'GET':
		template = loader.get_template('register.html')
		context = {
	
				}	

	elif request.method == 'POST':
		full_name = request.POST.get('full_name')
		username = request.POST.get('username')
		email = request.POST.get('email')
		password = request.POST.get('password')

		rand_token = uuid4().hex

		user = User()
		user.full_name = full_name
		user.username = username
		user.email = email
		user.password = password
		user.status = "Inactive"
		user.token = rand_token
		user.save()

		subject = 'Gymaholic: Activate your account.'
		body = 'Please click on the below link to activate your account..'
		sender_email = 'corona.ncit12@gmail.com'
		recipients = email.strip().split(" ")

		
		try:

			email_context = { 'full_name' : full_name, 'token':rand_token,'email':email, 'host':request.get_host()}
			send_html_email(recipients, subject, 'email.html', email_context)
			#send_mail(subject, body, sender_email, recipients)
		except Exception as e:
			print("Email could not be sent. %s", e)
			
		context = {
			"message":"Success",
			"full_name": full_name,
			"email": email
			}	
		template = loader.get_template('register.html')


	return HttpResponse(template.render(context, request))

def activate(request):
	token = request.GET.get('token')
	email = request.GET.get('email')
	user = User.objects.filter(email = email, token = token).first()
	if user:
		user.status = "Active"
		user.token = ""
		user.save()
		context = {
			"message":"Success",
			"activate":True
			}	
		template = loader.get_template('register.html')
	else:
		context = {
			"message":"Failure",
			"activate":False
			}
		template = loader.get_template('register.html')		
	return HttpResponse(template.render(context, request))

def profile(request):
		context = {}
		template = loader.get_template('profile.html')	
		if is_authenticated(request):
			context = {'logged_in': True}
			return HttpResponse(template.render(context, request))
		else:
			return redirect('/login')

	


def logout(request):
		context = {}
		del request.session['username']

		return redirect('/')


def send_html_email(to_list, subject, template_name, context, sender=settings.DEFAULT_FROM_EMAIL):
    msg_html = render_to_string(template_name, context)
    msg = EmailMessage(subject=subject, body=msg_html, from_email=sender, bcc=to_list)
    msg.content_subtype = "html"  # Main content is now text/html
    return msg.send()	

def email(request):
	context = {'full_name':"Sabbu Giri", 'token': "1234", 'email':"sabbugiri50@gmail.com", 'host': request.get_host()}
	template = loader.get_template('email.html')
	return HttpResponse(template.render(context, request))

def is_authenticated(request):
	user = request.session.get('username')
	return user



		


	
	