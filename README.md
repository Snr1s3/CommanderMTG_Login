# Login Microservice

## Configuration

Create a `settings.py` file in the `SRC/` directory with the following database configuration:

```python
db_config = {
    'host': 'localhost',        # Database host (e.g., localhost)
    'user': 'postgres',         # Database username
    'password': 'your_password', # Database password
    'database': 'proj',         # Database name
    'port': 5432             # Database port (5432 default)
}
```

## API Endpoints

### Root Endpoint
- **GET /** - Check API status
  ```bash
  curl http://localhost:8443/
  ```

### User Management

#### Get All Users
- **GET /all_users** - Retrieve all users
  ```bash
  curl http://localhost:8443/all_users
  ```

#### Get User by ID
- **GET /user/{id}** - Get specific user by ID
  ```bash
  curl http://localhost:8443/user/1
  ```

#### Create New User
- **POST /user/create** - Create a new user
  ```bash
  curl -X POST http://localhost:8443/user/create \
    -H "Content-Type: application/json" \
    -d '{
      "name": "john_doe",
      "mail": "john@example.com",
      "hash": "your_password_hash"
    }'
  ```

#### Authenticate User
- **POST /user/authenticate/** - Authenticate user credentials
  ```bash
  curl -X POST http://localhost:8443/user/authenticate/ \
    -H "Content-Type: application/json" \
    -d '{
      "name": "john_doe",
      "hash": "your_password_hash"
    }'
  ```

#### Update User
- **PUT /user/update** - Update user information
  ```bash
  curl -X PUT http://localhost:8443/user/update \
    -H "Content-Type: application/json" \
    -d '{
      "id": 1,
      "name": "john_updated",
      "mail": "john_new@example.com",
      "hash": "new_password_hash"
    }'
  ```

#### Delete User
- **DELETE /user/delete?id={id}** - Delete user by ID
  ```bash
  curl -X DELETE http://localhost:8443/user/delete?id=1
  ```

## Interactive Documentation

Access the auto-generated API documentation at:
- **Swagger UI**: http://localhost:8443/docs
- **ReDoc**: http://localhost:8443/redoc



