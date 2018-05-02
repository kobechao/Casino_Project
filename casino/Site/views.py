# django settings
from django.shortcuts import render, redirect
from django.forms.models import modelform_factory
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed
from django.contrib import auth, messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User


# Create your views here.
from .models import Login1, User1
from hashlib import sha256

import sys
import os

from . import util

from datetime import datetime


@csrf_exempt
def index( request ) :
	
	today = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

	if request.user.is_authenticated :
		
		personal_info = Login1.objects.get( account=request.session['account'] )
		betNote, canBet = util.isValidBetTime()


		if request.POST :
			posts = request.POST

			btn = posts.get('bet_btn', None)
			betMoney = int( posts.get( 'bet', 0 ) )
			number = 0

			if ( personal_info.money < betMoney ) :
				messages.info( request, "Money is Not Enough!")
				return redirect( '/index/', { 
					'personal_info': personal_info
					})


			if btn is not None :

				if btn == 'first_bet':
					number = 1
				elif btn == 'second_bet':
					number = 2

			User1( date = today, account = request.session['account'], bet = betMoney * -1, number=number, durationBet=0 ).save()
			personal_info.money -= betMoney
			personal_info.bet = 1
			personal_info.save()
			return redirect( '/index/', { 
					'personal_info': personal_info
					})

		
		return render( request, 'index.html', { 
			'personal_info': personal_info,
			'bet_note': betNote,
			'can_bet': canBet
			})
	else :
		return render( request, 'index.html' )


@csrf_exempt
def manage( request ) :

	today = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

	msg = ''
	userBetDatas = userInfoData = None

	if request.POST :

		post = request.POST

		phone = post.get('phone', None)
		money = post.get('money', None)
		authButtonValue = post.get('authBtn', None)

		if phone is not None :

			try :
				obj = Login1.objects.get( account=phone )
				print( obj )

			except Exception as e :
				print( str(e) )
				msg = 'No Such User! Please Check!'
				messages.error(request, msg)
				return render( request, 'manage.html' )

			if obj.name == request.session['name'] :
				msg = 'Cannot Manage Yourself!'
				messages.error(request, msg)
				return render( request, 'manage.html' )

			# account money management
			if money is not None :

				if obj.authority == 1 :
					msg = 'Cannot Add Money To Authorized User!'
					messages.info(request, msg)
					return render( request, 'manage.html', { 
						'authority': request.session['auth']
						})

				obj.money += int(money)
				User1( date=today, account=phone, bet=money, number=0, durationBet=0 ).save()
				obj.save()

				messages.success(request, 'Success')


			# account management function
			elif money is None :

				if authButtonValue is not None :

					if str(authButtonValue).lower() == 'enable' :
						obj.authority = 0
						messages.success( request, 'Enable Account %s' % (phone) )

					elif str(authButtonValue).lower() == 'disable' :
						obj.authority = 2
						messages.success( request, 'Disable Account %s' % (phone) )

					elif str(authButtonValue).lower() == 'certified_account_btn' :
						obj.certified = post.get('certified', 0)
						messages.success( request, 'Certified Account %s' % (phone) )
					
					elif str(authButtonValue).lower() == 'account_info' :
						userInfoData = Login1.objects.get( account=phone )
						messages.success( request, 'Search Account Info %s' % (phone) )


					elif str(authButtonValue).lower() == 'account_log' :
						userBetDatas = User1.objects.filter ( account = phone )
						messages.success( request, 'Search Account Bet %s' % (phone) )

					
				obj.save()



		elif phone is None :
			if authButtonValue is not None :
				if str(authButtonValue).lower() == 'search_all_btn' :
					messages.success( request, 'Search All Account' )



	# print( userBetDatas, userInfoData )

	if request.user.is_authenticated and request.session['auth']  == 1 :
		return render( request, 'manage.html', { 
			'authority': request.session['auth'],
			'userBetDatas': userBetDatas,
			'userInfoData': userInfoData
			})
	else :
		
		return render( request, 'manage.html' )



@csrf_exempt
def login_register_page( request ) :

	try :

		if request.POST :
			post = request.POST
			print( post )
			isLogin = post.get('phone_login', None)

			# Login
			if isLogin is not None :


				try :
					obj = Login1.objects.get( account=post.get('phone_login', ''))
				except :
					messages.info( request, 'No Such User!')
					return HttpResponseRedirect('/signin/')

				name = obj.name
				phone = obj.account
				success = obj.password == post.get('pwd_login', '')
				authority = obj.authority

				myIntroCode = obj.sn2

				recaptchaVerified = util.recaptcha_verify( post.get('g-recaptcha-response', ''))
				# recaptchaVerified = True
				if recaptchaVerified :
					if success :

						if request.user.is_authenticated: 
							messages.info( request, 'The User is Logined!')
							return HttpResponseRedirect('/index/')
						
						user = auth.authenticate( username=phone, password=obj.password )

						if user is not None and user.is_active :
							auth.login( request, user )
							request.session['name'] = name
							request.session['account'] = phone
							request.session['introCode'] = myIntroCode
							request.session['auth'] = authority

							if authority == 0:
								messages.success( request,'Success Login!')
								path = '/index/'
							
							elif authority == 1 or authority == 2 :
								messages.info( request,'Login In Management!')
								path = '/manage/'

							return redirect( path, { 
									'user_name': request.session['name'],
									'intro_code': request.session['introCode'],
									'authority': request.session['auth']
									})	

					else :

						messages.error( request, 'Wrong Password!')
						return HttpResponseRedirect('/signin/')

				else:
					messages.error( request, 'Recaptcha Error. Check Your Validity!')
					return HttpResponseRedirect('/signin/')

				
			# signup
			else :
				
				msg = ''
				
				name = post.get('user_signup', None)
				phone = post.get('phone_signup', None)
				password = post.get('pwd_signup', None)
				password_confirm = post.get('pwd2_signup', None)

				# sn2
				other_introCode = post.get('introducer_signup', '')


				if all( [name, phone, password, password_confirm] ) :
					
					if password == password_confirm :
						
						Successed = False; Registered = False

						try :
							Login1.objects.get( account=phone )
							Registered = True

						except Exception as e :
							Registered = False

						recaptchaVerified = util.recaptcha_verify( post.get('g-recaptcha-response', ''))

						# print( 'recaptcha_verify', recaptchaVerified, type(recaptchaVerified) )
						if recaptchaVerified :

							if not Registered :

								# sn1
								myIntroCode = util.generate_introducer_code(6)
								
								Login1( name=name, account=phone, password=password, sn1=other_introCode, sn2=myIntroCode, certified=0, money=0, bet=0, totalMoney=0, totalIntro=0, totalPer=0, introBet=0, authority=0).save()
								user = User.objects.create_user( username=phone, password=password)
								user.save()


								msg = 'Register Successed!!'; Successed = True

							else :
								msg = 'The User Has Signed Up Before!'; Successed = False
						else :
							msg = 'Recaptcha Error. Check Your Validity!'; Successed = False

					else :
						msg = 'Check The Confirm Password!'; Successed = False

				else :
					msg = 'Empty Values!'; Successed = False


				if Successed :
					messages.success( request, msg )
					return HttpResponseRedirect('/index/')
				else :
					messages.info( request, msg ) 
					return HttpResponseRedirect('/signin/')


				

		else :
			print( 'not post')

		
		return render( request, 'login.html' )

	except Exception as e :
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		print(exc_type, fname, exc_tb.tb_lineno)
		return HttpResponse( '%s %s %s\n%s' % (str(exc_type), str(fname), str(exc_tb.tb_lineno), str(e) ) )


@csrf_exempt
def logout( request ) :
	msg = ''
	try :
		auth.logout( request )
		msg = 'Success Logout'
	except Exception as e :
		msg = 'Fail To Logout: %s' % ( str(e) )

	messages.info( request, msg )
	return HttpResponseRedirect( '/index/' )


@csrf_exempt
def game( request ):

	data =  {
		'number_of_balls': 10,
		'number_can_select': 6
	}
	return render( request, 'game.html', data)


