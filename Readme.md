# Assignment Submission Portal Backend

This project is a backend system built using Flask for managing user and admin roles, where users can submit assignments and admins can approve or reject them. It uses MongoDB for data storage and JWT (JSON Web Tokens) for authentication.

## Features
- User registration and login with password hashing.
- JWT authentication for secured routes.
- Users can upload assignments.
- Admins can view pending assignments and either accept or reject them.

## Technologies Used
- Python (Flask)
- MongoDB (as the database)
- Flask-JWT-Extended (for JWT-based authentication)
- Flask-Bcrypt (for password hashing)

---

## Setup Instructions


### Installation Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/assignment-portal.git
   cd assignment-portal
   ```
2. **Set up a Virtual Environment**
   ```bash
   python3 -m venv venv
      source venv/bin/activate 
   ```
3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
4. **Set Up Environment Variables**
   ```bash
   JWT_SECRET_KEY=""
   MONGO_URI=""
   ```
5. **Run the Flask Application**
   ```bash
   python run.py
   ```
6. **Access the API**
   ```bash
   http://127.0.0.1:5000/
   ```   

## Endpoints

Here is a list of available endpoints for users and admins:

### User Endpoints

- `POST /register`: Register a new user.
  - **Headers**: `Content-Type: application/json`
  - **Payload**:
    ```bash
    {
      "username": "user1",
      "password": "userpassword",
      "role": "user"
    }
    ```

- `POST /login`: Login as a user and receive a JWT token.
  - **Headers**: `Content-Type: application/json`
  - **Payload**:
    ```bash
    {
      "username": "user1",
      "password": "userpassword"
    }
    ```
  - **Response**:
    ```bash
    {
      "token": "your_jwt_token"
    }
    ```

- `POST /upload`: Upload an assignment (requires JWT token).
  - **Headers**:
    ```bash
    Content-Type: application/json
    Authorization: Bearer {token}
    ```
  - **Payload**:
    ```bash
    {
      "task": "Assignment 1",
      "admin": "admin_username"
    }
    ```
  - **Response**:
    ```bash
    {
      "message": "Assignment uploaded successfully"
    }
    ```

- `GET /admins`: Fetch a list of all admins.
  - **Headers**: `Content-Type: application/json`
  - **Response**:
    ```bash
    [
      {
        "username": "admin1"
      },
      {
        "username": "admin2"
      }
    ]
    ```

---

### Admin Endpoints

- `GET /assignments`: View all pending assignments tagged to the admin (requires JWT token).
  - **Headers**:
    ```bash
    Content-Type: application/json
    Authorization: Bearer {token}
    ```
  - **Response**:
    ```bash
    [
      {
        "_id": "assignment_id1",
        "task": "Assignment 1",
        "status": "pending"
      },
      {
        "_id": "assignment_id2",
        "task": "Assignment 2",
        "status": "pending"
      }
    ]
    ```

- `POST /assignments/<assignment_id>/<action>`: Accept or reject an assignment (requires JWT token).
  - **Headers**:
    ```bash
    Content-Type: application/json
    Authorization: Bearer {token}
    ```
  - **Actions**: Either `accept` or `reject`
  - **Response** for `accept`:
    ```bash
    {
      "message": "Assignment accepted"
    }
    ```
  - **Response** for `reject`:
    ```bash
    {
      "message": "Assignment rejected"
    }
    ```
