# xSwimTeam

This project was a fun little supplement to some reading I've been doing into networking related things.
It consists of a very bare-bones API which acts as the middle man between my iOS app and a MySQL database.
The idea for a swim team themed app came from some friends on the SFU swim team who are currently using an Excel "database" to keep track of various things.

The app doesn't have any sort of design pattern used, I just threw everything together, so I'll definitely need to fix that up.
Also, only the GET endpoints are implemented in the app but I do plan on coming back to this project in the near future.
Credit to [this](https://youtu.be/fCfC6m7XUew) lecture from Stanford's CS193p for showing the inner workings of the Codable protocol.

As for the API, I just used with Flask (or more specifically Flask-RESTful) + MySQL for simplicity since this was my first time trying to create a web API.
You can install the dependencies for the API using the requirements.txt file in a virtual environment or you can just pip install the following API dependencies:
1. Flask
2. flask-restful
3. mysql-connector-python
4. requests (used only in test.py)

To be able to connect the app to my API running locally on a Flask dev server, I set the host on the Flask app equal to “0.0.0.0” which causes it to run on http://local.IP.address:port_number/ instead of localhost.
Also note that the Flask dev server does not use TLS so I had to modify the info.plist of the app. See [this](https://stackoverflow.com/questions/32631184/the-resource-could-not-be-loaded-because-the-app-transport-security-policy-requi) Stack Overflow post for more info.

Project installation and setup:
1. Set up MySQL database with SQL dump provided at root project directory
2. Set up API dependencies as described above and configure the database connection on lines 8-13 in main.py
3. If you'd like to test out the API with the test.py file I included, you need to update the BASE URL on line 4 according to your IP address + port number (an easy way to get this is to run the Flask app and check the URL it spits out)
4. Configure the URLs in CoachesView.swift, CoachesInfoView.swift, SwimmersView.swift, and SwimmerInfoView.swift (all in the app directory) according to your IP address + port number 
5. Run the app and marvel!

To do:
- Implement PUT/PATCH/DELETE endpoints
- Refactor app to use MVVM
- Implement front end for API using something like Swagger?
