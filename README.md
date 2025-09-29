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

## Docker Deployment

### Prerequisites
- Docker installed on your system
- PostgreSQL database running (can be in a container or host machine)

### Building the Docker Image
```bash
# Build the API Docker image
sudo docker build -t login-api .
```

### Running with Docker

#### Option 1: Connect to existing PostgreSQL database
```bash
# Make sure your PostgreSQL database is running first
sudo docker start postgres-db  # if using Docker for database

# Run the API container
sudo docker run -d \
  --name login-api-container \
  -p 8443:8443 \
  -e DB_HOST=172.17.0.1 \
  -e DB_PORT=8888 \
  -e DB_USER=postgres \
  -e DB_PASSWORD=your_password \
  -e DB_NAME=proj \
  login-api
```

#### Option 2: Using host database
```bash
# If database is running on host machine
sudo docker run -d \
  --name login-api-container \
  -p 8443:8443 \
  -e DB_HOST=172.17.0.1 \
  -e DB_PORT=5432 \
  -e DB_USER=postgres \
  -e DB_PASSWORD=your_password \
  -e DB_NAME=proj \
  login-api
```

### Docker Management Commands
```bash
# Check running containers
sudo docker ps

# View API logs
sudo docker logs login-api-container

# Stop the container
sudo docker stop login-api-container

# Start the container
sudo docker start login-api-container

# Remove the container
sudo docker rm login-api-container

# Remove the image
sudo docker rmi login-api
```

### Environment Variables
The Docker container supports these environment variables:
- `DB_HOST` - Database host (default: localhost)
- `DB_PORT` - Database port (default: 8888)  
- `DB_USER` - Database username (default: postgres)
- `DB_PASSWORD` - Database password (default: root)
- `DB_NAME` - Database name (default: proj)

### Docker Network Notes
- Use `172.17.0.1` as DB_HOST to connect to services on the Docker host
- Make sure the PostgreSQL database accepts connections from Docker containers
- Port 8443 will be exposed for API access

