# Database Setup Guide

This Users API now supports **persistent database storage** with both SQLite (for development) and MySQL (for production).

## Quick Start (SQLite - Development)

By default, the API uses **SQLite for development**. No additional setup required:

```bash
# Activate virtual environment
venv\Scripts\activate

# Run migrations
python manage.py migrate

# Start the server
python manage.py runserver
```

The SQLite database file (`db.sqlite3`) will be automatically created in the project root.

---

## MySQL Setup (Production-Ready)

### Prerequisites

- **MySQL Server** installed and running (version 5.7+ or 8.0+)
- **MySQL user** with database creation privileges
- **python-mysqlclient** already installed (included in `requirements.txt`)

### Step 1: Create MySQL Database

Connect to MySQL and create the database:

```sql
-- Connect to MySQL
mysql -u root -p

-- Create database
CREATE DATABASE users_api_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Create a user (optional but recommended for security)
CREATE USER 'api_user'@'localhost' IDENTIFIED BY 'secure_password_here';
GRANT ALL PRIVILEGES ON users_api_db.* TO 'api_user'@'localhost';
FLUSH PRIVILEGES;
```

### Step 2: Update `.env` Configuration

Edit the `.env` file in your project root:

```env
# Database Configuration
DATABASE_ENGINE=mysql
DATABASE_HOST=localhost
DATABASE_PORT=3306
DATABASE_NAME=users_api_db
DATABASE_USER=api_user
DATABASE_PASSWORD=secure_password_here

# Django Settings
ENVIRONMENT=production
DEBUG=False
SECRET_KEY=your-production-secret-key-here

# Connection Timeout (seconds)
DB_POOL_TIMEOUT=600
```

**Important:** Replace credentials with your actual MySQL user and password.

### Step 3: Run Migrations

Apply all database migrations:

```bash
python manage.py migrate
```

You should see output like:

```
Operations to perform:
  Apply all migrations: admin, auth, blog, contenttypes, sessions, users
Running migrations:
  Applying users.0003_alter_user_options_...OK
  Applying blog.0002_alter_comment_author_...OK
```

### Step 4: Test the Connection

Verify the setup works:

```bash
python manage.py dbshell
```

This should open a MySQL prompt. Type `exit` to close it.

### Step 5: Run Tests

Verify all functionality with the database backend:

```bash
python manage.py test users
```

Expected output:

```
Found 7 test(s).
Creating test database...
System check identified no issues (0 silenced).
.......
Ran 7 tests in 0.313s
OK
```

---

## Database Configuration Options

### Environment Variables

Add these to your `.env` file to customize the database connection:

| Variable            | Default        | Description                         |
| ------------------- | -------------- | ----------------------------------- |
| `DATABASE_ENGINE`   | `mysql`        | `mysql` or leave blank for SQLite   |
| `DATABASE_HOST`     | `` (empty)     | MySQL hostname (empty = use SQLite) |
| `DATABASE_PORT`     | `3306`         | MySQL port                          |
| `DATABASE_NAME`     | `users_api_db` | Database name                       |
| `DATABASE_USER`     | `root`         | MySQL username                      |
| `DATABASE_PASSWORD` | `root`         | MySQL password                      |
| `DB_POOL_TIMEOUT`   | `600`          | Connection timeout in seconds       |
| `ENVIRONMENT`       | `development`  | `development` or `production`       |
| `DEBUG`             | `True`         | Set to `False` for production       |

### Switching Databases

**To use SQLite (development):**

```env
DATABASE_HOST=
```

**To use MySQL (production):**

```env
DATABASE_HOST=localhost
DATABASE_NAME=users_api_db
DATABASE_USER=api_user
DATABASE_PASSWORD=your_password
```

---

## Connection Pooling

The MySQL connection is configured with connection pooling built into Django:

- **CONN_MAX_AGE**: 600 seconds (connections are recycled after 10 minutes)
- **Charset**: `utf8mb4` (full Unicode support)
- **Auto-commit**: Enabled for better transaction handling

To customize pool settings, modify `.env`:

```env
DB_POOL_TIMEOUT=900  # Increase to 15 minutes
```

---

## Database Schema

The Users table has the following structure:

```sql
CREATE TABLE users (
  id CHAR(36) PRIMARY KEY,                    -- UUID
  name VARCHAR(100) NOT NULL,                 -- User full name
  email VARCHAR(254) UNIQUE NOT NULL,         -- Email address
  age INT NOT NULL,                           -- Age (>=0)
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_email ON users(email);
```

---

## Troubleshooting

### MySQL Connection Error: "Access denied for user 'root'@'localhost'"

**Solution:**

1. Verify MySQL is running: `mysql -u root -p`
2. Confirm credentials in `.env` file
3. Or leave `DATABASE_HOST` empty to use SQLite

### Migration Error: "table already exists"

**Solution:**

```bash
# Reset and reapply migrations (development only!)
python manage.py migrate users zero
python manage.py migrate
```

### Database is locked (SQLite only)

**Solution:**

```bash
# Delete the SQLite database and recreate
del db.sqlite3
python manage.py migrate
```

---

## Performance Tips

1. **Use indexes** for frequently queried columns (email is already indexed)
2. **Enable connection pooling** for MySQL (default: 600 seconds)
3. **Set `DEBUG = False`** in production to improve query performance
4. **Monitor slow queries** using MySQL's slow query log
5. **Backup regularly**:

```bash
# MySQL backup
mysqldump -u api_user -p users_api_db > backup_$(date +%Y%m%d).sql

# SQLite backup
cp db.sqlite3 db.sqlite3.backup
```

---

## Migration Guide

If you need to move data from SQLite to MySQL:

1. Export data from SQLite:

   ```bash
   python manage.py dumpdata users > users_data.json
   ```

2. Switch to MySQL in `.env`

3. Run migrations and load data:
   ```bash
   python manage.py migrate
   python manage.py loaddata users_data.json
   ```

---

## Additional Resources

- [Django Database Documentation](https://docs.djangoproject.com/en/6.0/ref/databases/)
- [MySQL Documentation](https://dev.mysql.com/doc/)
- [Django Migrations](https://docs.djangoproject.com/en/6.0/topics/migrations/)
