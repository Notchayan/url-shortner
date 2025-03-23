# URL Shortener

A user-friendly URL shortening service built with FastAPI.

## Features

- Shorten long URLs into easy-to-share links
- Custom alias support for personalized short URLs
- URL expiration setting (optional)
- Click tracking and statistics
- Clean and intuitive user interface
- RESTful API for programmatic access

## Requirements

- Python 3.7+
- PostgreSQL
- pip (Python package manager)

## Installation

### Ubuntu/Debian

1. Clone the repository:
```bash
git clone https://github.com/yourusername/url-shortener.git
cd url-shortener
```

2. Install PostgreSQL:
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
```

3. Create a PostgreSQL user and database:
```bash
sudo -u postgres psql
postgres=# CREATE USER urlshortener WITH PASSWORD 'yourpassword';
postgres=# CREATE DATABASE urlshortener OWNER urlshortener;
postgres=# \q
```

4. Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

5. Configure database connection in `.env` file:
```
DATABASE_URL=postgresql://urlshortener:yourpassword@localhost/urlshortener
```

### macOS

1. Clone the repository:
```bash
git clone https://github.com/yourusername/url-shortener.git
cd url-shortener
```

2. Install PostgreSQL using Homebrew:
```bash
brew install postgresql
brew services start postgresql
```

3. Create a PostgreSQL user and database:
```bash
psql postgres
postgres=# CREATE USER urlshortener WITH PASSWORD 'yourpassword';
postgres=# CREATE DATABASE urlshortener OWNER urlshortener;
postgres=# \q
```

4. Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

5. Configure database connection in `.env` file:
```
DATABASE_URL=postgresql://urlshortener:yourpassword@localhost/urlshortener
```

### Windows

1. Clone the repository:
```bash
git clone https://github.com/yourusername/url-shortener.git
cd url-shortener
```

2. Install PostgreSQL:
   - Download and install PostgreSQL from the [official website](https://www.postgresql.org/download/windows/)
   - During installation, set a password for the postgres user
   - Use pgAdmin or psql shell to create a new user and database:
     ```
     CREATE USER urlshortener WITH PASSWORD 'yourpassword';
     CREATE DATABASE urlshortener OWNER urlshortener;
     ```

3. Create a virtual environment and install dependencies:
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

4. Configure database connection in `.env` file:
```
DATABASE_URL=postgresql://urlshortener:yourpassword@localhost/urlshortener
```

## Running the Application

1. Activate the virtual environment:
   - On Ubuntu/macOS: `source venv/bin/activate`
   - On Windows: `venv\Scripts\activate`

2. Start the application:
```bash
uvicorn app.main:app --reload
```

3. Open your browser and navigate to `http://localhost:8000`

## API Documentation

After starting the application, API documentation is available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Home page with URL shortening form |
| `/shorten` | POST | Create a shortened URL |
| `/{short_code}` | GET | Redirect to the original URL |
| `/stats/{short_code}` | GET | Get statistics for a shortened URL |
| `/{short_code}` | DELETE | Delete a shortened URL |

## Example API Usage

### Shorten a URL

```bash
curl -X POST "http://localhost:8000/shorten" \
     -H "Content-Type: application/json" \
     -d '{"original_url": "https://example.com/very/long/url"}'
```

### Shorten a URL with custom alias

```bash
curl -X POST "http://localhost:8000/shorten" \
     -H "Content-Type: application/json" \
     -d '{"original_url": "https://example.com/very/long/url", "alias": "example"}'
```

### Get URL statistics

```bash
curl -X GET "http://localhost:8000/stats/example"
```



