# Login Microservice

This service handles CRUD operations and authentication for users.

**⚠️ Requirements:** PostgreSQL database is required.

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

## Database Schema
The user table must have these required fields and name:

```sql
CREATE TABLE usuari(
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    mail VARCHAR(50) NOT NULL UNIQUE,
    hash VARCHAR(60) NOT NULL UNIQUE
);
```

**Note:** The table can have additional fields, but the microservice will only use the fields listed above.

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

## Usage

### Setup and Installation
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Application
```bash
# Start the FastAPI server
# Make sure that the database is running
./venv/bin/uvicorn SRC.main:app --reload --host 0.0.0.0 --port 8443
```

### Access the API
- **API Base URL**: http://localhost:8443
- **Interactive Documentation**: http://localhost:8443/docs
- **Alternative Documentation**: http://localhost:8443/redoc

