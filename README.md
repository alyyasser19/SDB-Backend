# SDB-Backend
The project's back-end consists of 4 servers. 
Each server is run separately by running its corresponding "app.py" file. 
The dependencies for each server can be found in its "requirements.txt" file. 
The project's servers (branches) are:
- Bike: To manage bike related functions
- Carinfra: To manage car info and the surrounding infrastructures
- Users: To manage the user activities throughout the app
- Main Server: Responsible for decentralizing incoming requests to their appropriate servers and processing their responses. Token security is used to secure the authenticity of the requests received by any of the servers.
