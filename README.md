# WriteSpace

A modern blogging platform built with Django where users can create, share, and manage blog posts. Features role-based access control with admin dashboards, user management, and a responsive UI powered by Tailwind CSS.

## Tech Stack

- **Backend:** Python 3.12, Django 5.0+
- **Database:** PostgreSQL (Neon) in production, SQLite for local development
- **Styling:** Tailwind CSS (CDN)
- **Static Files:** Whitenoise with compressed manifest storage
- **Deployment:** Vercel (Python runtime)

## Features

- **Public Landing Page** — Hero section with gradient design, feature highlights, and latest posts preview
- **Authentication** — Login and registration with session management via signed cookies
- **Blog CRUD** — Create, read, update, and delete posts with UUID primary keys and ownership enforcement
- **Admin Dashboard** — Platform statistics and quick action links for staff users
- **User Management** — Staff-only panel to create and delete users with role assignment
- **Avatar System** — Emoji-based avatars with role-differentiated styling
- **Responsive Design** — Mobile-friendly layout with hamburger menus and card-based components
- **Custom Error Pages** — Styled 404 and 500 pages

## Folder Structure

```
writespace/
├── accounts/                  # Authentication & user management app
│   ├── management/
│   │   └── commands/
│   │       └── create_default_admin.py
│   ├── forms.py
│   ├── urls.py
│   └── views.py
├── blog/                      # Blog posts app
│   ├── templatetags/
│   │   └── avatar_tags.py
│   ├── admin.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── static/
│   └── images/
├── templates/
│   ├── accounts/
│   │   ├── admin_dashboard.html
│   │   ├── login.html
│   │   ├── register.html
│   │   └── user_management.html
│   ├── blog/
│   │   ├── blog_detail.html
│   │   ├── blog_form.html
│   │   ├── blog_list.html
│   │   └── landing_page.html
│   ├── base.html
│   ├── 404.html
│   └── 500.html
├── writespace/                # Django project configuration
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
└── manage.py
```

## Local Development Setup

### Prerequisites

- Python 3.12+
- pip

### 1. Clone the Repository

```bash
git clone <repository-url>
cd writespace
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy the example environment file and adjust values as needed:

```bash
cp .env.example .env
```

For local development, the defaults in `.env.example` work out of the box with SQLite.

### 5. Run Migrations

```bash
cd writespace
python manage.py migrate
```

### 6. Create the Default Admin User

```bash
python manage.py create_default_admin
```

This reads `DEFAULT_ADMIN_USERNAME`, `DEFAULT_ADMIN_PASSWORD`, and `DEFAULT_ADMIN_EMAIL` from your environment variables (or uses the defaults: `admin` / `admin` / `admin@example.com`).

### 7. Start the Development Server

```bash
python manage.py runserver
```

Visit [http://localhost:8000](http://localhost:8000) to view the application.

## Vercel Deployment

### 1. Configure Vercel Project

The project includes a `vercel.json` that targets the WSGI application at `writespace/writespace/wsgi.py` using the Python 3.12 runtime.

### 2. Set Environment Variables

In your Vercel project settings, add the following environment variables:

| Variable | Description |
|---|---|
| `SECRET_KEY` | Django secret key (use a strong, unique value) |
| `DEBUG` | Set to `False` for production |
| `DATABASE_URL` | PostgreSQL connection string (e.g., Neon) |
| `ALLOWED_HOSTS` | Comma-separated list of allowed hostnames |
| `CSRF_TRUSTED_ORIGINS` | Comma-separated list of trusted origins |
| `DEFAULT_ADMIN_USERNAME` | Username for the default admin account |
| `DEFAULT_ADMIN_PASSWORD` | Password for the default admin account |
| `DEFAULT_ADMIN_EMAIL` | Email for the default admin account |

### 3. Deploy

Push to your connected Git repository or run:

```bash
vercel --prod
```

### 4. Run Migrations in Production

After deploying, run migrations against your production database. You can do this locally by setting the `DATABASE_URL` environment variable to your production database connection string:

```bash
DATABASE_URL=<your-production-database-url> python writespace/manage.py migrate
DATABASE_URL=<your-production-database-url> python writespace/manage.py create_default_admin
```

## Environment Variables Reference

| Variable | Default | Description |
|---|---|---|
| `SECRET_KEY` | `your-secret-key-here-change-in-production` | Django secret key for cryptographic signing |
| `DEBUG` | `False` | Enable debug mode (set `True` for local development) |
| `DATABASE_URL` | `sqlite:///db.sqlite3` | Database connection URL |
| `ALLOWED_HOSTS` | `localhost,127.0.0.1` | Comma-separated allowed hostnames |
| `CSRF_TRUSTED_ORIGINS` | `http://localhost:8000,http://127.0.0.1:8000` | Comma-separated trusted origins for CSRF |
| `DEFAULT_ADMIN_USERNAME` | `admin` | Default admin username |
| `DEFAULT_ADMIN_PASSWORD` | `admin` | Default admin password |
| `DEFAULT_ADMIN_EMAIL` | `admin@example.com` | Default admin email |

## License

This project is proprietary and private. All rights reserved.