import requests


BASE = "http://local.IP.address:port_number/"


''' SWIMMER API '''
# GET - with cURL: curl http://local.IP.address:port_number/swimmer/2
# Use ...swimmer/0 to list all swimmers and their associated IDs
response = requests.get(BASE + "swimmer/2")
print(response.json())

# PUT - with cURL: curl -X PUT -d "name=Sehajvir Singh" -d "birthdate=2001-03-03" -d "swimmer_group=HP" -d "main_event=Backstroke" http://local.IP.address:port_number/swimmer/4
#   This cURL format is possible thanks to Flask's reqparse (see https://flask-restful.readthedocs.io/en/latest/reqparse.html for more info)
response = requests.put(BASE + "swimmer/4", {"name": "Sehajvir Singh", "birthdate": "2001-03-03", "swimmer_group" : "HP", "main_event" : "Backstroke"})
print(response.json())

# PATCH - with cURL: curl -X PATCH -d "main_event=Sprint free" http://local.IP.address:port_number/swimmer/2
#   This cURL format is possible thanks to Flask's reqparse (see https://flask-restful.readthedocs.io/en/latest/reqparse.html for more info)
response = requests.patch(BASE + "swimmer/2", {"main_event" : "Sprint free"})
print(response.json())

# DELETE - with cURL: curl -X DELETE http://local.IP.address:port_number/swimmer/3
response = requests.delete(BASE + "swimmer/3")
print(response) # Delete does not return JSON serializable data


''' COACH API'''
# GET - with cURL: curl http://local.IP.address:port_number/coach/2
# Use ...coach/0 to list all coaches and their associated IDs
response = requests.get(BASE + "coach/2")
print(response.json())

# PUT - with cURL: curl -X PUT -d "name=Siobhan Newell" -d "birthdate=1995-02-23" -d "coach_group=13%2b provincial" http://local.IP.address:port_number/coach/3
#   This cURL format is possible thanks to Flask's reqparse (see https://flask-restful.readthedocs.io/en/latest/reqparse.html for more info)
response = requests.put(BASE + "coach/3", {"name": "Siobhan Newell", "birthdate": "1995-02-23", "coach_group" : "13%2b provincial"})
print(response.json())

# PATCH - with cURL: curl -X PATCH -d "coach_group=13%2b provincial" http://local.IP.address:port_number/coach/2
#   This cURL format is possible thanks to Flask's reqparse (see https://flask-restful.readthedocs.io/en/latest/reqparse.html for more info)
response = requests.patch(BASE + "coach/2", {"coach_group" : "13%2b provincial"})
print(response.json())

# DELETE - with cURL: curl -X DELETE http://local.IP.address:port_number/coach/3
# Delete does not return JSON serializable data
response = requests.delete(BASE + "coach/3")
print(response)