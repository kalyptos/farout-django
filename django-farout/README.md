# Farout - Django Rewrite

**Complete Django rewrite of the Farout Star Citizen Organization Portal**

A modern, production-ready Django 5.1+ application for managing Star Citizen gaming organizations with Discord OAuth authentication, role-based access control, and comprehensive member management features.

## 🚀 Features

### Core Functionality
- **Discord OAuth Authentication** - Seamless login via Discord using django-allauth
- **User Management** - Custom User model with Discord fields and role-based access (Admin/Member)
- **Organization Members** - Manage member profiles, ranks, missions, and stats
- **Blog System** - Rich text blog posts with TinyMCE editor
- **Inventory Management** - Track organization items and resources
- **Admin Dashboard** - Comprehensive Django admin interface

### Technical Features
- **Django 5.1+** with Python 3.12+ for modern features
- **PostgreSQL 16** for robust data storage
- **Django Allauth** for Discord OAuth integration
- **TinyMCE** for rich text editing
- **Tailwind CSS 4.0+** (ready for implementation)
- **Docker & Docker Compose** for easy deployment
- **Gunicorn** with gthread workers for production
- **WhiteNoise** for efficient static file serving
- **Security Hardened** - All 2025 best practices implemented

## 📋 Table of Contents

- [Quick Start](#quick-start)
- [Architecture](#architecture)
- [Installation](#installation)
- [Configuration](#configuration)
- [Development](#development)
- [Deployment](#deployment)
- [Security](#security)
- [API Reference](#api-reference)
- [Troubleshooting](#troubleshooting)

## 🎯 Quick Start

### Prerequisites
- Docker & Docker Compose
- Discord Application (for OAuth)
- PostgreSQL 16 (if running locally without Docker)

### 1. Clone and Setup

```bash
# Navigate to django-farout directory
cd django-farout

# Copy environment file
cp .env.example .env

# Edit .env with your values
nano .env
```

### 2. Configure Discord OAuth

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application
3. Go to OAuth2 → Add redirect URI: `https://your-domain.com/accounts/discord/login/callback/`
4. Copy Client ID and Client Secret to `.env`

### 3. Start with Docker

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f web

# Create superuser (if needed)
docker-compose exec web python manage.py createsuperuser
```

### 4. Access the Application

- **Main Site**: http://localhost:8000 (or your configured domain)
- **Admin Panel**: http://localhost:8000/admin
- **Health Check**: http://localhost:8000/health/

**Default Admin Credentials**:
- Username: `admin`
- Password: `TorOve78!`
- ⚠️ **Change this immediately after first login!**

## 🏗️ Architecture

### Project Structure

```
django-farout/
├── farout/                     # Django project settings
│   ├── settings/
│   │   ├── __init__.py         # Settings selector
│   │   ├── base.py             # Base settings
│   │   ├── development.py      # Dev settings
│   │   └── production.py       # Production settings
│   ├── urls.py                 # Main URL configuration
│   ├── wsgi.py                 # WSGI application
│   └── asgi.py                 # ASGI application
├── apps/                       # Django applications
│   ├── accounts/               # User authentication & OAuth
│   │   ├── models.py           # Custom User model
│   │   ├── adapters.py         # Discord OAuth adapter
│   │   ├── admin.py            # User admin interface
│   │   └── management/commands/
│   │       └── create_default_admin.py
│   ├── members/                # Organization members
│   │   ├── models.py           # Member model
│   │   └── admin.py            # Member admin
│   ├── blog/                   # Blog posts
│   │   ├── models.py           # BlogPost model
│   │   └── admin.py            # Blog admin
│   ├── items/                  # Inventory management
│   │   ├── models.py           # Item model
│   │   └── admin.py            # Item admin
│   ├── dashboard/              # Dashboard views
│   └── core/                   # Core utilities
│       ├── views.py            # Health check, home, dashboard
│       └── management/commands/
│           └── wait_for_db.py
├── templates/                  # Django templates
├── static/                     # Static files (CSS, JS, images)
├── staticfiles/                # Collected static files
├── media/                      # User-uploaded files
├── logs/                       # Application logs
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker image definition
├── docker-compose.yml          # Docker services configuration
├── .env.example                # Environment template
├── .gitignore                  # Git ignore rules
└── manage.py                   # Django management script
```

### Database Models

#### User (accounts.User)
- Extends Django's AbstractUser
- Fields: discord_id, avatar, discriminator, role, rank_image
- Roles: Member, Admin
- OAuth integration with Discord

#### Member (members.Member)
- Organization member profiles
- Fields: discord_id, display_name, bio, rank, avatar_url
- JSON fields: missions_completed, trainings_completed, stats
- Ranks: Recruit, Member, Veteran, Officer, Leader

#### BlogPost (blog.BlogPost)
- Rich text blog posts
- Fields: heading, slug, content (HTML), author, feature_image, published
- Auto-slug generation from heading
- TinyMCE integration for rich text

#### Item (items.Item)
- Inventory/resource management
- Fields: title, description, quantity, image_url

## 📦 Installation

### Option 1: Docker (Recommended)

```bash
# Start services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Stop and remove data
docker-compose down -v
```

### Option 2: Local Development

```bash
# Create virtual environment
python3.12 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up database
createdb farout
createuser farout

# Configure environment
cp .env.example .env
export DJANGO_ENVIRONMENT=development

# Run migrations
python manage.py migrate

# Create admin user
python manage.py create_default_admin

# Run development server
python manage.py runserver
```

## ⚙️ Configuration

### Environment Variables

See `.env.example` for all available options. Key variables:

```bash
# Django
SECRET_KEY=generate-with-secrets-token-urlsafe-50
DEBUG=False
DJANGO_ENVIRONMENT=production
ALLOWED_HOSTS=your-domain.com

# Database
DATABASE_URL=postgresql://user:password@host:5432/dbname

# Discord OAuth
DISCORD_CLIENT_ID=your_client_id
DISCORD_CLIENT_SECRET=your_client_secret

# Admin User
DEFAULT_ADMIN_USERNAME=admin
DEFAULT_ADMIN_PASSWORD=TorOve78!
```

### Generating SECRET_KEY

```python
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

### Discord OAuth Setup

1. **Create Discord App**: https://discord.com/developers/applications
2. **OAuth2 Settings**:
   - Redirect URI: `https://your-domain.com/accounts/discord/login/callback/`
   - Scopes: `identify`, `email`
3. **Copy credentials** to `.env`

## 🔧 Development

### Running Migrations

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Check migration status
python manage.py showmigrations
```

### Creating Apps

```bash
# Create new app
python manage.py startapp app_name apps/app_name

# Add to INSTALLED_APPS in settings/base.py
```

### Database Operations

```bash
# Django shell
python manage.py shell

# Database shell
python manage.py dbshell

# Dump data
python manage.py dumpdata > backup.json

# Load data
python manage.py loaddata backup.json
```

### Static Files

```bash
# Collect static files
python manage.py collectstatic

# Clear collected files
python manage.py collectstatic --clear
```

## 🚢 Deployment

### Production Checklist

- [ ] Generate strong `SECRET_KEY`
- [ ] Set `DEBUG=False`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set up PostgreSQL database
- [ ] Configure Discord OAuth with production URL
- [ ] Update `SECURE_SSL_REDIRECT=True`
- [ ] Set strong database passwords
- [ ] Change default admin password
- [ ] Configure email backend (SMTP)
- [ ] Set up SSL/TLS certificates
- [ ] Configure reverse proxy (Traefik/Nginx)
- [ ] Set up logging and monitoring
- [ ] Configure backups

### Docker Deployment (Coolify/Traefik)

1. **Configure .env** with production values
2. **Update docker-compose.yml** with domain labels:

```yaml
labels:
  - "traefik.enable=true"
  - "traefik.http.routers.farout.rule=Host(`your-domain.com`)"
  - "traefik.http.routers.farout.tls.certresolver=letsencrypt"
```

3. **Deploy**:

```bash
docker-compose up -d
```

4. **Access**: https://your-domain.com

### Health Checks

- **Endpoint**: `/health/`
- **Response**: `{"status": "ok", "service": "farout-django", "version": "1.0.0"}`
- **Docker**: Automatic health checks configured in `docker-compose.yml`

## 🔒 Security

### Implemented Security Features

- **HTTPS Enforcement**: `SECURE_SSL_REDIRECT=True`
- **Secure Cookies**: HTTPOnly, Secure, SameSite=Lax
- **HSTS**: 1 year with includeSubDomains and preload
- **Content Security Policy**: Configured via django-csp
- **XSS Protection**: `X-Content-Type-Options: nosniff`
- **Clickjacking Protection**: `X-Frame-Options: DENY`
- **CSRF Protection**: Django's built-in CSRF middleware
- **SQL Injection Prevention**: Django ORM parameterized queries
- **Password Hashing**: PBKDF2 with SHA256
- **Session Security**: Secure session cookies

### Security Best Practices

1. **Never commit `.env`** to version control
2. **Use strong passwords** for all accounts
3. **Rotate SECRET_KEY** periodically
4. **Keep dependencies updated**: `pip list --outdated`
5. **Monitor logs** for suspicious activity
6. **Use HTTPS only** in production
7. **Limit admin access** to trusted IPs (if possible)
8. **Regular backups** of database and media files

## 📚 API Reference

### Health Check

```http
GET /health/
```

Response:
```json
{
  "status": "ok",
  "service": "farout-django",
  "version": "1.0.0"
}
```

### Admin Interface

- **URL**: `/admin/`
- **Users**: Manage users, roles, Discord OAuth data
- **Members**: CRUD operations for organization members
- **Blog**: Create/edit/publish blog posts with rich text
- **Items**: Manage organization inventory

## 🐛 Troubleshooting

### Common Issues

#### Database Connection Errors

```bash
# Check database is running
docker-compose ps db

# View database logs
docker-compose logs db

# Test connection
docker-compose exec db psql -U farout -d farout
```

#### Static Files Not Loading

```bash
# Collect static files
python manage.py collectstatic --noinput

# Check STATIC_ROOT and STATIC_URL in settings
```

#### Discord OAuth Not Working

1. Verify redirect URI in Discord Developer Portal matches exactly
2. Check `DISCORD_CLIENT_ID` and `DISCORD_CLIENT_SECRET` in `.env`
3. Ensure Site ID is correct: `python manage.py shell` → `from django.contrib.sites.models import Site; Site.objects.all()`

#### Migration Errors

```bash
# Reset migrations (⚠️ destroys data)
python manage.py migrate app_name zero
python manage.py migrate

# Or start fresh
docker-compose down -v
docker-compose up -d
```

## 📝 License

This project is proprietary software for Farout Star Citizen Organization.

## 🤝 Contributing

This is an internal project. For issues or feature requests, contact the development team.

## 📞 Support

- **Documentation**: This README
- **Admin Guide**: See Django admin interface
- **Health Status**: `/health/` endpoint

---

**Built with ❤️ for the Farout Star Citizen Organization**

**Technology Stack**: Django 5.1 | Python 3.12 | PostgreSQL 16 | Docker | Gunicorn | WhiteNoise | django-allauth
