import requests
import random

def recaptcha_verify( g_response ) :
	
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
