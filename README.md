# Farout Django Application

A comprehensive Django application for managing Star Citizen organization data, ship catalogs, and fleet management.

## Features

### Phase 1: Core Infrastructure ✅
- Django 5.1 with PostgreSQL
- User authentication with Discord OAuth
- Admin interface
- Base templates with Tailwind CSS

### Phase 2: Star Citizen API Integration ✅
- **Ship Catalog**: Browse and search Star Citizen ships with detailed specifications
- **Organization Management**: Sync and manage organization data from Star Citizen API
- **Fleet Management**: Track ships owned by organization members
- **Management Commands**: Easy sync commands for updating data from SC API

## Installation

### Prerequisites
- Python 3.11+
- PostgreSQL 12+
- pip

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd farout-django
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

## Star Citizen API Integration

### Configuration

#### Getting Your API Key

You can obtain a free API key in two ways:

1. **Via Website** (Recommended):
   - Visit [https://api.starcitizen-api.com](https://api.starcitizen-api.com)
   - Log in with Discord or Google
   - Your API key will be displayed in your account

2. **Via Discord**:
   - Join the [Star Citizen API Discord](https://discord.gg/starcitizen-api)
   - Navigate to the `#keys` channel
   - Type the command: `/api register`
   - The bot will send you a private message with your API key

#### Configure Your Environment

Add your Star Citizen API key to your `.env` file:
```bash
STARCITIZEN_API_KEY=your_api_key_here
```

**Example:**
```bash
STARCITIZEN_API_KEY=0d32404d021613ba948ba0aeef324ef5
```

**Note**: The API client will work without an API key but may have rate limitations. For production use, an API key is highly recommended.

### Syncing Data

#### 1. Sync Ships

Import all Star Citizen ships and manufacturers:
```bash
python manage.py sync_ships
```

Options:
- `--force`: Update existing ships with fresh data from API

#### 2. Sync Organization

Import organization details:
```bash
python manage.py sync_organization FAROUT
```

Replace `FAROUT` with your organization's SID.

Options:
- `--force`: Update existing organization data

#### 3. Sync Organization Members

Import organization members:
```bash
python manage.py sync_org_members FAROUT
```

Replace `FAROUT` with your organization's SID.

Options:
- `--force`: Update existing member data

### Complete Sync Workflow

To fully populate your database with Star Citizen data:

```bash
# 1. Sync all ships (one-time, then periodically)
python manage.py sync_ships

# 2. Sync your organization
python manage.py sync_organization FAROUT

# 3. Sync organization members
python manage.py sync_org_members FAROUT
```

### Periodic Updates

For production deployments, consider setting up scheduled tasks:

```bash
# Update ships weekly (new ships added less frequently)
0 0 * * 0 cd /path/to/farout && python manage.py sync_ships --force

# Update organization data daily
0 2 * * * cd /path/to/farout && python manage.py sync_organization FAROUT --force

# Update members daily
0 3 * * * cd /path/to/farout && python manage.py sync_org_members FAROUT --force
```

## Application Structure

### Apps

- **apps.core**: Core utilities and API client
- **apps.accounts**: User authentication and profiles
- **apps.starships**: Ship catalog and specifications
- **apps.organization**: Organization and member management
- **apps.fleet**: Fleet ship tracking for organization members
- **apps.dashboard**: Main dashboard views
- **apps.members**: Member management features
- **apps.blog**: Blog and news
- **apps.items**: Item management

### Models

#### Starships App
- **Manufacturer**: Ship manufacturers (AEGIS, RSI, etc.)
- **Ship**: Complete ship specifications
- **ShipComponent**: Ship components and hardpoints

#### Organization App
- **Organization**: Organization details and stats
- **OrganizationMember**: Member profiles and ranks

#### Fleet App
- **FleetShip**: Ships owned by organization members

## Usage

### Admin Interface

Access the admin interface at `/admin/` to:
- View and edit all ships and manufacturers
- Manage organization and member data
- Track fleet ships
- Moderate content

### Ship Catalog

Browse the ship catalog at `/ships/`:
- Search by ship name or manufacturer
- Filter by type, size, and status
- View detailed specifications
- See components and loadouts

### API Integration

The Star Citizen API client (`apps.core.starcitizen_api`) provides:
- Automatic caching (1 hour default)
- Error handling and logging
- Rate limiting compliance
- Retry logic for network issues

## Development

### Running Tests

```bash
python manage.py test
```

### Creating Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Code Style

Follow PEP 8 guidelines. Use type hints where appropriate.

## Deployment

### Environment Variables

Required environment variables:
- `SECRET_KEY`: Django secret key
- `DATABASE_URL`: PostgreSQL connection string
- `DEBUG`: Set to `False` in production
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts

Optional:
- `STARCITIZEN_API_KEY`: Star Citizen API key
- `DISCORD_CLIENT_ID`: Discord OAuth client ID
- `DISCORD_CLIENT_SECRET`: Discord OAuth secret

### Static Files

Collect static files for production:
```bash
python manage.py collectstatic --noinput
```

### Production Server

Use gunicorn for production:
```bash
gunicorn farout.wsgi:application --bind 0.0.0.0:8000
```

## Troubleshooting

### API Sync Issues

If you encounter API errors:
1. Check your internet connection
2. Verify the Star Citizen API is accessible
3. Check logs for detailed error messages
4. Try again with `--force` flag

### Database Issues

Reset the database (⚠️ destroys all data):
```bash
python manage.py flush
python manage.py migrate
python manage.py sync_ships
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

[Your License Here]

## Support

For issues and questions, please open a GitHub issue.
