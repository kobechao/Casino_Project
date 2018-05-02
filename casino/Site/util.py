import requests
import random
from datetime import datetime

def recaptcha_verify( g_response ) :

	'''
	Recaptcha for signin and register page 
	'''
	
	url = 'https://www.google.com/recaptcha/api/siteverify'
	secret = '6LcpRVMUAAAAAHMcygyy5SCkmzLrL1kQ1P6xehu3'

	dataload = {
		'secret': secret,
		'response': g_response
	}

	if g_response != '' :
		res = requests.post( url, data=dataload )
		print( res.json() )
		return res.json()['success']
	else :
		return False


def generate_introducer_code( length ) :

	seed = '1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ'
	code = ''
	
	for i in range( length ) :
		code += random.choice(seed)

	assert len(code) == 6
	return code

def isValidBetTime() :

	'''
	Check if the time user bets is valid, which is between 12:00~17:59
	'''
	note = ''
	canBet = False
	
	if( datetime.today().hour >= 12 and datetime.today().hour < 18 ):
		inputNote = "請輸入下注金額"
		canBet = True
	else:
		inputNote = "已過今日下注時間"
		canBet = False

	return ( note, canBet )
