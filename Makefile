runserver: 
	uvicorn kundi.server.main:app --reload 

	
API_KEY := AIzaSyDPoYA3017g0HwB1m0ZUUAxLKrbInm1fRg
EMAIL := asdf2@gmail.com
PASSWORD := 123456

sign_in:
	printf '{"email":"$(EMAIL)","password":"$(PASSWORD)","returnSecureToken":true}' > request.json
	curl --request POST \
	  --url 'https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=$(API_KEY)' \
	  --header 'Content-Type: application/json' \
	  --data @request.json > output.txt
	rm request.json
