# InsureTech Backend: Authentication & Authorization

## Authentication System

### User Roles
- **Admin**: Full system access, can create users
- **Finance**: Limited access to financial data

### Authentication Endpoints

#### 1. Obtain Token
- **URL**: `/api/auth/token/`
- **Method**: POST
- **Body**:
  ```json
  {
    "username": "your_username",
    "password": "your_password"
  }
  ```
- **Response**: 
  ```json
  {
    "access": "jwt_access_token",
    "refresh": "jwt_refresh_token"
  }
  ```

#### 2. Refresh Token
- **URL**: `/api/auth/token/refresh/`
- **Method**: POST
- **Body**:
  ```json
  {
    "refresh": "jwt_refresh_token"
  }
  ```

#### 3. User Registration (Admin Only)
- **URL**: `/api/auth/register/`
- **Method**: POST
- **Headers**: `Authorization: Bearer <admin_access_token>`
- **Body**:
  ```json
  {
    "username": "new_user",
    "password": "secure_password",
    "confirm_password": "secure_password",
    "role": "Finance",
    "organization": 1
  }
  ```

#### 4. Logout
- **URL**: `/api/auth/logout/`
- **Method**: POST
- **Headers**: `Authorization: Bearer <access_token>`
- **Body**:
  ```json
  {
    "refresh_token": "jwt_refresh_token"
  }
  ```

### Authorization
- Tokens are valid for 60 minutes
- Refresh tokens are valid for 1 day
- Role-based access control implemented

### Security Features
- JWT Authentication
- Password hashing with bcrypt
- Role-based permissions
- Secure token management

## Development Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run migrations:
   ```bash
   python manage.py migrate
   ```

3. Create superuser:
   ```bash
   python manage.py createsuperuser
   ```

## Testing Authentication
- Use Postman or curl to test endpoints
- Always include `Authorization: Bearer <token>` for protected routes
