# Blog API

Base URL: https://blog-505j.onrender.com/

## Features

- User authentication with JWT tokens
- Full CRUD operations for blog posts
- Comment system
- Like/unlike functionality
- PostgreSQL database integration
- Secure password hashing
- Token-based authorization

## API Documentation

### Authentication Endpoints

#### Create a New User

```bash
curl -X POST https://blog-505j.onrender.com/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "your.email@example.com",
    "password": "your_password"
  }'
```

#### Login (Get Access Token)

```bash
curl -X POST https://blog-505j.onrender.com/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=your.email@example.com&password=your_password"
```

After login, store the token for use in subsequent requests:

```bash
export TOKEN="your_access_token_here"
```

### Blog Post Endpoints

#### Create a New Blog Post

```bash
curl -X POST https://blog-505j.onrender.com/blogs/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My First Blog Post",
    "content": "This is the content of my first blog post."
  }'
```

#### Get All Blog Posts

```bash
curl -X GET https://blog-505j.onrender.com/blogs/
```

#### Get a Specific Blog Post

```bash
curl -X GET https://blog-505j.onrender.com/blogs/1
```

#### Update a Blog Post

```bash
curl -X PUT https://blog-505j.onrender.com/blogs/1 \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Blog Post Title",
    "content": "This is the updated content of my blog post."
  }'
```

#### Delete a Blog Post

```bash
curl -X DELETE https://blog-505j.onrender.com/blogs/1 \
  -H "Authorization: Bearer $TOKEN"
```

### Comment Endpoints

#### Add a Comment to a Blog Post

```bash
curl -X POST https://blog-505j.onrender.com/blogs/1/comments/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "This is a great post! Thanks for sharing."
  }'
```

### Like Endpoints

#### Like/Unlike a Blog Post

```bash
curl -X PUT https://blog-505j.onrender.com/blogs/1/like \
  -H "Authorization: Bearer $TOKEN"
```

## Local Development Setup

1. Clone the repository

```bash
git clone https://github.com/satuiro/blog
cd blog-api
```

2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Set up environment variables
   Create a `.env` file in the root directory:

```
DATABASE_URL=your_postgresql_connection_string
SECRET_KEY=your_secret_key
```

5. Initialize the database

```bash
python create_tables.py
```

6. Run the development server

```bash
uvicorn main:app --reload
```
