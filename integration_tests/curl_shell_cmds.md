
http://wiki.servicenow.com/index.php?title=Table_API_Curl_Examples#gsc.tab=0

# curl get test

# Some curl commands to test the API manually on shell.

curl -i -H "Accept: application/json" -H "Content-Type: application/json" http://127.0.0.1:8000/carroceiro/
curl -i -H "Accept: application/json" -H "Content-Type: application/json" http://127.0.0.1:8000/carroceiro/1

# curl post test

curl -i -H "Accept: application/json" -H "Content-Type: application/json" -X POST -d '{"name":"test","phone":"11111111111","address":"Av Independencia, 500","latitude":-11.111111,"longitude":-22.222222}' http://127.0.0.1:8000/carroceiro/

# curl put test

curl -i -H "Accept: application/json" -H "Content-Type: application/json" -X PUT -d '{"name":"test","phone":"22222222222","address":"Av Independencia, 500","latitude":-11.111111,"longitude":-22.222222}' http://127.0.0.1:8000/carroceiro/20/

# curl delete test

curl -i -H "Accept: application/json" -H "Content-Type: application/json" -X DELETE -d '{"name":"test","phone":"22222222222","address":"Av Independencia, 500","latitude":-11.111111,"longitude":-22.222222}' http://127.0.0.1:8000/carroceiro/20/

#############################
# curl Token authentication #
#############################

right token:

curl -i -H "Accept: application/json" -H "Content-Type: application/json" -H "Authorization: Token 2ad7cd83134a4908f8277c058a7b7da23b2876bc" -X POST -d '{"name": "carroceiro_test", "type": "carroceiro", "phone": "999111111", "address": "Av test, 9999", "latitude": -11.11, "longitude": -22.22}' http://127.0.0.1:8000/carroceiro/

wrong token: 401 return..

curl -i -H "Accept: application/json" -H "Content-Type: application/json" -H "Authorization: Token 3ad7cd83134a4908f8277c058a7b7da23b2876bc" -X POST -d '{"name": "carroceiro_test", "type": "carroceiro", "phone": "999111111", "address": "Av test, 9999", "latitude": -11.11, "longitude": -22.22}' http://127.0.0.1:8000/carroceiro/