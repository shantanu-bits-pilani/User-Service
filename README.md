User Service

Description
The User Service handles user profiles and related data.

Endpoints

Create User Profile


URL: /create


Method: POST


Request Body:

{
  "username": "string",
  "profile": {
    "name": "string",
    "email": "string"
  }
}





Response:

201 Created if the user profile is created successfully.
400 Bad Request if the user already exists.




Get User Profile


URL: /profile/<username>


Method: GET


Response:

200 OK with the user profile.
404 Not Found if the user does not exist.




Running the Service
To run the service, use Docker Compose:
bash docker-compose up --build user-service
