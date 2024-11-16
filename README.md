# User Service

## Description
The User Service handles user profile management and friend requests. It provides endpoints for creating users, managing friend requests, and retrieving user profiles.

## Endpoints
- `POST /create`: Create a new user.
- `GET /profile`: Retrieve the profile of the authenticated user.
- `POST /send-request/<r_username>`: Send a friend request.
- `POST /accept-request/<r_username>`: Accept a friend request.
- `POST /withdraw-request/<r_username>`: Withdraw a friend request.
- `GET /friends`: Retrieve the list of friends.

### Get User Profile
- **URL:** `/profile/<username>`
- **Method:** `GET`
- **Headers**
    - `X-Logged-In-UserName: <username>`
- **Response**:
    - 200 OK with the user profile.
    - 404 Not Found if the user does not exist.

### Send Friend Request
- **URL:** `/send-request/<r_username>`
- **Method:** `POST`
- **Headers**
    - `X-Logged-In-UserName: <username>`
- **Response**: 
    - 200 OK if the friend request is sent successfully.
    - 400 Bad Request if the request is invalid.

### Accept Friend Request
- **URL:** `/accept-request/<r_username>`
- **Method:** `POST`
- **Headers**
    - `X-Logged-In-UserName: <username>`
- **Response**: 
  - 200 OK if the friend request is accepted successfully.
  - 400 Bad Request if the request is invalid.

### Withdraw Friend Request
- **URL:** `/withdraw-request/<r_username>`
- **Method:** `POST`
- **Headers**
    - `X-Logged-In-UserName: <username>`
- **Response**: 
  - 200 OK if the friend request is withdrawn successfully.
  - 400 Bad Request if the request is invalid.

### Get Friends
- **URL:** `/friends`
- **Method:** `GET`
- **Headers**
    - `X-Logged-In-UserName: <username>`
- **Response**: 
  - 200 OK with a list of friends.
  - 404 Not Found if the user does not have any friends.

## Running the Service
To run the service, use Docker Compose:
```bash docker-compose up --build user-service```