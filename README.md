# Backend API

This is a FastAPI backend API for supporting a Machine Learning-based mobile application. The API provides endpoints for authentication, predictions, and user management. This project is designed to be deployed to Google Cloud Run.

Key Features:

- Authentication
- User Management 
- Scalable Deployment (docker)

Technologies Used:
- python
- docker
- fastapi ( backend framework )

## How To Use

1. **Kloning Repositori**
   ```bash
   
   https://github.com/CultureConnect2024/Backend-API.git
   
   cd Backend-API
2. **Create Virtual ENV**
   ```bash
   python -m venv venv

3. **Activate the virtual env (gitbash)**
   ```bash
   source venv/Scripts/activate
   
4. **Activate the virtual env (cmd)**
   ```bash
   venv/Scripts/activate.bat

5. **Install the requirements**
   ```bash
   pip install -r requirements.txt

5. **Run Project**
   ```bash
   fastapi dev main.py


# API Documentation

This API allows for user registration, login, logout, and health check, as well as testing the database connection.

## Endpoints

### 1. Root Endpoints
#### `GET /`
Check if the API is conected correctly.

**Response:**
- **200 OK** - If the api is connected successfully.
- **404 Not Found** - If the api connection not found.

  Response:
  ```bash
   {
    "status": "success",
    "message": "API connection successful",
    "timestamp": "2024-12-07T03:55:15.972101"
  }

### 2. Check Connection DB
#### `GET /check`
Check if the API is conected with database server correctly.

**Response:**
- **200 OK** - If the api is connected successfully.
- **500 Internal Server Error** - If the database connection fails..

  Response:
  ```bash
  {
    "status": "success",
    "message": "Database connection successful",
    "database_version": "PostgreSQL 13.18 (Debian 13.18-0+deb11u1) on x86_64-pc-linux-gnu, compiled by gcc (Debian 10.2.1-6) 10.2.1 20210110, 64-bit"
  }


### 3. Auth Endpoints
#### `POST /auth/register`
For handling register user account.

**Response:**
- **200 OK** - If the register sucessfully.
- **500 Internal Server Error** - If the database connection fails or register fails.


**Request Body:**
  ```bash
  {

  "username": "example",
  "email": "example@example.com",
  "password": "examplePass"

  }
   ```

  Response:
  ```bash
  
  {
    "message": "User successfully registered",
    "session_id": "8cd22fbe-6e27-44e5-938e-67f62188d79a",
    "expires_at": "2024-12-07T10:00:00"
  }
 ```

#### `POST /auth/login`
For handling login user account.

**Response:**
- **200 OK** - If the login sucessfully.
- **401 Unauthorized** - If the login failt with Incorrect username or password .
- **500 Internal Server Error** - If the database connection fails or login fails.


**Request Body:**
  ```bash
  {

  "username": "example",
  "password": "examplePass"

  }
   ```

  Response:
  ```bash

 {
    "status": "success",
    "message": "Login successfully",
    "session_id": "26f0f94b-b382-4f68-a38b-183b5cd17b7b",
    "expires_at": "2024-12-08T04:11:01.843276"
}
 ```


#### `POST /auth/logout`
For handling logout user account.

**Response:**
- **200 OK** - If the logout sucessfully.
- **404 NOT FOUND** - If the session was not found.
- **500 Internal Server Error** - If the database connection fails or logout fails.


**Request Body:**
  ```bash
  {
  "session-id": "26f0f94b-b382-4f68-a38b-183b5cd17b7b"
  }
   ```

  Response:
  ```bash

 {
    "message": "Logged out successfully"
}

 ```
### 4. Users Data Endpoints
#### `GET /users`
For handling get all users data.

**Response:**
- **200 OK** - If successfully retreave all users.
- **404 NOT FOUND** - If no users in the database.
- **500 Internal Server Error** - If the database connection fails or cant retreive all users data.

  Response:
  ```bash

   {
      "status": "success",
      "data": [
         {
               "id": 1,
               "username": "example",
               "email": "example@example.com"
         },
         {
               "id": 2,
               "username": "example",
               "email": "example@example.com"
         }
      ],
      "time": "2024-12-06T12:40:56.789123Z"
   }
   ```

#### `GET /users/{session_id}`
Get User by Session ID

**Path Parameter**
session_id (string): The unique session ID.

**Response Code:**
- **200 OK** - If successfully retreave user data base on session.
- **404 NOT FOUND** - Invalid session ID or user not found
- **500 Internal Server Error** - If the database connection fails or cant retreive user data.

Response:
 ```bash
   {
      "status": "success",
      "data": 
      {
        "id": 1,
        "username": "example",
        "email": "example@example.com" 
      },

      "time": "2024-12-06T12:34:56.789123Z"
   }

   ```
   