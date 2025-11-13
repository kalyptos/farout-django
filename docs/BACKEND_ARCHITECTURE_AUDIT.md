# Far Out Corporation Backend Architecture Audit

**Date**: November 13, 2025
**Project**: Far Out Corporation Portal
**Framework**: Django 5.1.3
**Database**: PostgreSQL (Multi-database setup)

---

## Executive Summary

Your Far Out Corporation portal is a well-structured Django application designed to manage a Star Citizen organization. The backend follows Django best practices with a modular app structure, multi-database architecture, and Discord OAuth integration.

---

## 1. ARCHITECTURE OVERVIEW

### Tech Stack
- **Framework**: Django 5.1.3
- **Database**: PostgreSQL (2 separate databases)
- **Authentication**: Discord OAuth via django-allauth 65.0.2
- **Rich Text**: TinyMCE
- **Web Server**: Gunicorn
- **Containerization**: Docker + Docker Compose

### Database Architecture

Your application uses a **multi-database setup** with intelligent routing:

#### Default Database (`farout`)
- User accounts
- Organization data
- Ships & fleet management
- Squadron management
- Blog posts
- Items inventory

#### Communications Database (`farout_communications`)
- Internal messages
- Contact form submissions
- Isolated for performance and horizontal scaling

**Database Router**: `CommunicationsRouter` in `/farout/db_router.py` automatically routes communications app queries to the separate database, preventing cross-database foreign key relationships.

---

## 2. DATABASE STRUCTURE & RELATIONSHIPS

### Core Entity Relationship Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                      DEFAULT DATABASE                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌────────────┐         ┌──────────────┐                   │
│  │    User    │◄────────│  BlogPost    │                   │
│  │  (Custom)  │         │              │                   │
│  └──────┬─────┘         └──────────────┘                   │
│         │                      │                            │
│         │                      │ManyToMany                  │
│         │                ┌─────▼─────┐                     │
│         │                │ Tag       │                      │
│         │                └───────────┘                      │
│         │                                                   │
│         │owns        ┌──────────────┐                      │
│         ├───────────►│  FleetShip   │                      │
│         │            └──────┬───────┘                      │
│         │                   │references                     │
│         │                   ▼                               │
│         │            ┌──────────────┐                      │
│         │            │     Ship     │                      │
│         │            └──────┬───────┘                      │
│         │                   │has                            │
│         │                   ▼                               │
│         │            ┌──────────────┐                      │
│         │            │ ShipComponent│                      │
│         │            └──────────────┘                      │
│         │                   ▲                               │
│         │                   │manufactured_by                │
│         │            ┌──────┴───────┐                      │
│         │            │ Manufacturer │                      │
│         │            └──────────────┘                      │
│         │                                                   │
│         │member_of   ┌──────────────┐                      │
│         ├───────────►│ Squadron     │                      │
│         │            │              │                      │
│         │            └──────┬───────┘                      │
│         │                   │via                            │
│         │                   ▼                               │
│         │            ┌──────────────────┐                  │
│         └───────────►│ SquadronMember   │                  │
│                      └──────────────────┘                  │
│                                                              │
│  ┌────────────────┐       ┌──────────────┐                │
│  │   Member       │◄──────┤ShipOwnership │                │
│  │  (Separate)    │       └──────────────┘                │
│  └────────────────┘                                        │
│                                                              │
│  ┌────────────────────┐                                    │
│  │   Organization     │                                    │
│  │                    │                                    │
│  └─────────┬──────────┘                                    │
│            │                                                │
│            ▼                                                │
│  ┌────────────────────┐                                    │
│  │ OrganizationMember │                                    │
│  └────────────────────┘                                    │
│                                                              │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                  COMMUNICATIONS DATABASE                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌────────────────────┐                                    │
│  │ InternalMessage    │ (user IDs, no FK)                  │
│  │ - sender_id        │                                    │
│  │ - recipient_id     │                                    │
│  │ - parent_message_id│                                    │
│  └────────────────────┘                                    │
│                                                              │
│  ┌────────────────────┐                                    │
│  │ ContactSubmission  │                                    │
│  │                    │                                    │
│  └────────────────────┘                                    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. DJANGO APPS BREAKDOWN

### 3.1 Accounts (`apps/accounts`)
**Purpose**: Custom user management with Discord OAuth

**Models**:
- **User** (extends AbstractUser)
  - **Table**: `users`
  - **Discord fields**: `discord_id`, `discriminator`, `avatar`
  - **Profile**: `profile_picture` (ImageField)
  - **Role-based access**: `role` (member/admin)
  - **Indexes**: discord_id, role, username, is_active

**Key Features**:
- Discord OAuth integration
- Avatar priority system (uploaded → Discord → default)
- Role-based permissions (`is_admin` property)
- Last login tracking

**Key Fields**:
```python
discord_id = CharField(max_length=100, unique=True)
profile_picture = ImageField(upload_to='profile_pictures/')
role = CharField(choices=ROLE_CHOICES, default='member')
rank_image = URLField()
must_change_password = BooleanField(default=False)
last_login_at = DateTimeField()
```

**Methods**:
- `is_admin` - Check if user has admin role
- `discord_avatar_url` - Generate full Discord avatar URL
- `get_avatar_url()` - Get avatar with priority (uploaded > Discord > default)
- `update_last_login()` - Update last login timestamp

---

### 3.2 Organization (`apps/organization`)
**Purpose**: Star Citizen organization management

**Models**:

#### Organization
- **Table**: Default table name
- **Purpose**: Track external Star Citizen organization data

**Key Fields**:
```python
sid = CharField(max_length=10, unique=True)  # e.g., FAROUTCORP
name = CharField(max_length=200)
archetype = CharField(max_length=100)
commitment = CharField(max_length=100)
primary_language = CharField(max_length=50)
recruiting = BooleanField(default=False)
member_count = IntegerField(default=0)
headline = TextField()
description = TextField()
history = TextField()
manifesto = TextField()
charter = TextField()
logo_url = URLField()
banner_url = URLField()
api_data = JSONField(default=dict)
```

#### OrganizationMember
- **Table**: Default table name
- **Purpose**: Track external SC organization members

**Key Fields**:
```python
handle = CharField(max_length=100, unique=True)
display_name = CharField(max_length=200)
rank = CharField(max_length=100)
stars = IntegerField(default=0)
avatar_url = URLField()
bio = TextField()
api_data = JSONField(default=dict)
```

**Indexes**: handle, stars (descending)

**Use Case**: Integration with Star Citizen API for organization data

---

### 3.3 Members (`apps/members`)
**Purpose**: Internal organization member management

**Models**:

#### Member
- **Table**: `members`
- **Purpose**: Portal user profiles with SC-specific data

**Key Fields**:
```python
discord_id = CharField(max_length=100, unique=True)
display_name = CharField(max_length=255)
bio = TextField()
avatar_url = URLField()
profile_image = ImageField(upload_to='member_profiles/')
rank = CharField(choices=RANK_CHOICES, default='private')
role = CharField(choices=ROLE_CHOICES, default='user')
squadron = CharField(max_length=100)
missions_completed = JSONField(default=list)
trainings_completed = JSONField(default=list)
stats = JSONField(default=dict)
```

**Rank System** (10 ranks):
- Private
- Corporal
- Sergeant
- Lieutenant
- Captain
- Major
- Colonel
- Commander
- Admiral
- Fleet Admiral

**Role System**:
- User
- Member
- Admin

**Methods**:
- `total_missions` - Get count of completed missions
- `total_trainings` - Get count of completed trainings
- `get_rank_image_url()` - Get rank badge image from starcitizen.tools
- `get_profile_image_url()` - Get profile image (uploaded > avatar)

**Indexes**: discord_id, rank, display_name

#### ShipOwnership
- **Table**: `ship_ownerships`
- **Purpose**: Track member ship ownership

**Key Fields**:
```python
member = ForeignKey(Member, on_delete=CASCADE)
ship = ForeignKey('starships.Ship', on_delete=CASCADE)
quantity = PositiveIntegerField(default=1)
acquired_date = DateTimeField(auto_now_add=True)
notes = TextField()
```

**Constraints**: unique_together = ['member', 'ship']

**Key Difference**: This is separate from `OrganizationMember` - represents internal portal users vs external SC org members

---

### 3.4 Squadron (`apps/squadron`)
**Purpose**: Organize members into specialized groups

**Models**:

#### Squadron
- **Table**: `squadrons`
- **Purpose**: Create divisions/teams within organization

**Key Fields**:
```python
name = CharField(max_length=100, unique=True)
slug = SlugField(max_length=100, unique=True)
callsign = CharField(max_length=50, unique=True)
description = TextField()
motto = CharField(max_length=200)
commander = ForeignKey(User, on_delete=SET_NULL)
focus = CharField(choices=FOCUS_CHOICES, default='mixed')
is_active = BooleanField(default=True)
is_recruiting = BooleanField(default=False)
max_members = IntegerField(null=True)
logo_url = URLField()
color_code = CharField(max_length=7, default='#55E6A5')
```

**Focus Categories**:
- Combat Operations
- Exploration
- Trading & Commerce
- Mining Operations
- Security & Escort
- Support & Logistics
- Mixed Operations

**Methods**:
- `get_member_count()` - Get current member count
- `is_full()` - Check if at capacity
- `can_accept_members()` - Check if can accept new members (active + recruiting + not full)
- `save()` - Auto-generate slug from name

#### SquadronMember
- **Table**: `squadron_members`
- **Purpose**: Junction table linking users to squadrons

**Key Fields**:
```python
squadron = ForeignKey(Squadron, on_delete=CASCADE)
user = ForeignKey(User, on_delete=CASCADE)
role = CharField(choices=ROLE_CHOICES, default='member')
is_active = BooleanField(default=True)
joined_at = DateTimeField(auto_now_add=True)
left_at = DateTimeField(null=True)
notes = TextField()
```

**Squadron Roles**:
- Member
- Squad Lead
- Officer
- Specialist

**Constraints**: unique_together = [['squadron', 'user']]

**Indexes**:
- [squadron, is_active]
- [user, is_active]

**Methods**:
- `leave_squadron()` - Mark member as having left

---

### 3.5 Starships (`apps/starships`)
**Purpose**: Star Citizen ship database

**Models**:

#### Manufacturer
- **Table**: Default table name
- **Purpose**: Ship manufacturers

**Key Fields**:
```python
code = CharField(max_length=10, unique=True)  # e.g., AEGS
name = CharField(max_length=100)
description = TextField()
logo_url = URLField()
api_id = CharField(max_length=50)
api_data = JSONField(default=dict)
```

#### Ship
- **Table**: Default table name
- **Purpose**: Star Citizen ships catalog

**Key Fields**:
```python
name = CharField(max_length=200)
manufacturer = ForeignKey(Manufacturer, on_delete=PROTECT)
type = CharField(max_length=100)
size = CharField(choices=SIZE_CHOICES, default='small')
focus = CharField(max_length=200)
description = TextField()
career = CharField(max_length=100)
role = CharField(max_length=100)

# Technical specs
length = DecimalField(max_digits=10, decimal_places=2)
beam = DecimalField(max_digits=10, decimal_places=2)
height = DecimalField(max_digits=10, decimal_places=2)
mass = DecimalField(max_digits=15, decimal_places=2)
min_crew = IntegerField()
max_crew = IntegerField()
cargo_capacity = IntegerField()

# Status
is_flight_ready = BooleanField(default=False)
is_concept = BooleanField(default=False)
production_status = CharField(max_length=50)
pledge_price = DecimalField(max_digits=10, decimal_places=2)

# Media
image_url = URLField()
store_url = URLField()

# API
api_id = CharField(max_length=50, unique=True)
api_data = JSONField(default=dict)
```

**Size Categories**:
- Vehicle
- Snub
- Small
- Medium
- Large
- Capital

**Indexes**:
- [manufacturer, name]
- type
- size
- is_flight_ready

#### ShipComponent
- **Table**: Default table name
- **Purpose**: Ship components and hardpoints

**Key Fields**:
```python
ship = ForeignKey(Ship, on_delete=CASCADE)
component_type = CharField(choices=COMPONENT_TYPE_CHOICES)
name = CharField(max_length=200)
size = CharField(max_length=10)
quantity = IntegerField(default=1)
mount_name = CharField(max_length=200)
details = TextField()
api_data = JSONField(default=dict)
```

**Component Types**:
- Weapon
- Shield
- Power Plant
- Cooler
- Quantum Drive
- Fuel Tank
- Cargo Hold
- Miscellaneous

---

### 3.6 Fleet (`apps/fleet`)
**Purpose**: Track member-owned ships

**Models**:

#### FleetShip
- **Table**: `fleet_fleetship`
- **Purpose**: Individual ship instances owned by members

**Key Fields**:
```python
ship = ForeignKey('starships.Ship', on_delete=PROTECT)
owner = ForeignKey(User, on_delete=CASCADE)
name = CharField(max_length=200)  # Custom ship name
purchased_date = DateField()
status = CharField(choices=STATUS_CHOICES, default='active')
notes = TextField()
is_available_for_missions = BooleanField(default=False)
```

**Status Options**:
- Active
- Pledged
- On Loan
- Sold

**Indexes**:
- [owner, status]
- [ship, status]

**Use Case**: Personal ship inventories for organization members

---

### 3.7 Communications (`apps/communications`)
**Purpose**: Internal messaging and contact forms

**Database**: Separate `farout_communications` database

**Models**:

#### ContactSubmission
- **Table**: `contact_submissions`
- **Purpose**: Public contact form submissions

**Key Fields**:
```python
name = CharField(max_length=200)
email = EmailField()
subject = CharField(max_length=300)
message = TextField()
ip_address = GenericIPAddressField()
user_agent = TextField()
status = CharField(choices=STATUS_CHOICES, default='new')
response_sent = BooleanField(default=False)
response_sent_at = DateTimeField()
is_spam = BooleanField(default=False)
```

**Status Workflow**:
- New
- Read
- Replied
- Archived

**Indexes**:
- [-created_at, status]
- email

#### InternalMessage
- **Table**: `internal_messages`
- **Purpose**: Internal messages between organization members

**Key Fields**:
```python
# No foreign keys - uses integer IDs to avoid cross-database relations
sender_id = IntegerField()
sender_name = CharField(max_length=200)
recipient_id = IntegerField()
recipient_name = CharField(max_length=200)

# Content
subject = CharField(max_length=300)
message = TextField()
parent_message_id = IntegerField()  # For threading

# Status
is_read = BooleanField(default=False)
read_at = DateTimeField()
is_deleted_by_sender = BooleanField(default=False)
is_deleted_by_recipient = BooleanField(default=False)

# System messages
is_system_message = BooleanField(default=False)
is_announcement = BooleanField(default=False)
```

**Indexes**:
- [recipient_id, -created_at]
- [sender_id, -created_at]
- [recipient_id, is_read]

**Methods**:
- `mark_as_read()` - Mark message as read with timestamp

**Design Note**: Uses integer user IDs instead of foreign keys to maintain database isolation

---

### 3.8 Blog (`apps/blog`)
**Purpose**: News and announcements

**Models**:

#### Category
- **Table**: `blog_categories`

**Key Fields**:
```python
name = CharField(max_length=100, unique=True)
slug = SlugField(max_length=100, unique=True)
```

#### Tag
- **Table**: `blog_tags`

**Key Fields**:
```python
name = CharField(max_length=50, unique=True)
slug = SlugField(max_length=50, unique=True)
```

#### BlogPost
- **Table**: `blog_posts`

**Key Fields**:
```python
heading = CharField(max_length=255)
slug = SlugField(max_length=255, unique=True)
content = HTMLField()  # TinyMCE
author = ForeignKey(User, on_delete=CASCADE)
category = ForeignKey(Category, on_delete=SET_NULL)
tags = ManyToManyField(Tag)
feature_image = URLField(max_length=500)
published = BooleanField(default=True)
```

**Indexes**:
- slug
- [published, -created_at]

**Methods**:
- `get_absolute_url()` - Get URL for post
- `get_excerpt(length=150)` - Generate excerpt from HTML content
- `save()` - Auto-generate slug from heading

---

### 3.9 Items (`apps/items`)
**Purpose**: Generic inventory management

**Models**:

#### Item
- **Table**: `items`

**Key Fields**:
```python
title = CharField(max_length=255)
description = TextField()
quantity = IntegerField(default=0)
image_url = URLField(max_length=500)
```

**Status**: Basic implementation, ready for expansion

---

### 3.10 Core (`apps/core`)
**Purpose**: Base views and utilities

**No models**, provides:
- home view
- dashboard view
- about view
- health_check endpoint

---

### 3.11 Dashboard (`apps/dashboard`)
**Purpose**: Dashboard functionality

**No models currently**, likely contains views/templates only

---

## 4. AUTHENTICATION & AUTHORIZATION

### Authentication System
- **Primary Method**: Discord OAuth (via django-allauth)
- **Social App Config**: Stored in database (`socialaccount_socialapp` table)
- **Settings**:
  - `SOCIALACCOUNT_ONLY = False` - Allows login page display
  - `SOCIALACCOUNT_AUTO_SIGNUP = True` - Auto-create accounts
  - `ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'` - Use HTTPS for OAuth callbacks
- **Discord Scopes**: identify, email
- **Provider ID**: Must be lowercase 'discord'

### Custom User Model
- **Table**: `users`
- **Extends**: `AbstractUser`
- **Username-based**: Not email-based
- **Email**: Optional and non-unique

### Authorization Levels

**User Model**:
1. `ROLE_MEMBER` - Basic member access
2. `ROLE_ADMIN` - Full administrative access

**Member Model**:
1. `user` - Basic user
2. `member` - Organization member
3. `admin` - Administrative access

**Squadron Member Roles**:
1. `member` - Regular squadron member
2. `lead` - Squad lead
3. `officer` - Squadron officer
4. `specialist` - Specialized role

**Note**: There's duplication between `User.role` and `Member.role` that could be consolidated

---

## 5. URL STRUCTURE

### Main URLs (`farout/urls.py`)

```python
# Admin
/admin/                      # Django admin panel

# Health
/health/                     # Health check endpoint

# Authentication (django-allauth)
/accounts/                   # Allauth URLs (login, logout, etc.)
/accounts/discord/login/     # Discord OAuth start
/accounts/login/             # Login page
/accounts/logout/            # Logout

# Core
/                           # Homepage
/dashboard/                 # Main dashboard (requires auth)
/about/                     # About page
/contact/                   # Contact form submission

# Ships
/ships/                     # Ship list
/ships/<id>/                # Ship detail

# Organization
/organization/              # Organization URLs

# Blog
/blog/                      # Blog URLs

# Squadron
/squadron/                  # Squadron list
/squadron/my/               # User's squadron
/squadron/<slug>/           # Squadron detail

# Messages
/messages/inbox/            # Message inbox
/messages/send/             # Send message

# TinyMCE
/tinymce/                   # TinyMCE editor URLs
```

---

## 6. DATABASE ROUTING

### CommunicationsRouter (`farout/db_router.py`)

**Purpose**: Route communications app to separate database

**Key Methods**:

```python
def db_for_read(model, **hints):
    # Route communications models to 'communications' database
    if model._meta.app_label == 'communications':
        return 'communications'
    return None

def db_for_write(model, **hints):
    # Route communications models to 'communications' database
    if model._meta.app_label == 'communications':
        return 'communications'
    return None

def allow_relation(obj1, obj2, **hints):
    # Only allow relations within communications app
    # Prevent cross-database foreign keys

def allow_migrate(db, app_label, model_name=None, **hints):
    # Ensure communications only migrates to communications DB
    # Allow Django internal tables on communications DB
    # Block other apps from communications DB
```

**Allowed on Communications DB**:
- communications app models
- Django internal tables (contenttypes, admin, auth, sessions)
- django_migrations table

---

## 7. INTEGRATION POINTS

### Star Citizen API
- **Purpose**: Fetch organization and ship data
- **Storage**: `api_data` JSONField in models
- **Models with API Integration**:
  - Organization
  - OrganizationMember
  - Manufacturer
  - Ship
  - ShipComponent

### Discord OAuth
- **Provider**: django-allauth
- **Scopes**: identify, email
- **Data Captured**:
  - discord_id
  - discriminator (deprecated by Discord)
  - avatar hash
- **Adapter**: Custom `DiscordAccountAdapter` (`apps.accounts.adapters`)

### TinyMCE
- **Purpose**: Rich text editing for blog posts
- **Field Type**: `HTMLField`
- **Used In**: BlogPost.content
- **URL**: `/tinymce/`

---

## 8. CURRENT ISSUES

### Issue 1: Discord Login MultipleObjectsReturned Error
**Status**: UNRESOLVED
**Error**: `django.core.exceptions.MultipleObjectsReturned`
**Location**: Login page (`/accounts/login/`)
**Root Cause**: django-allauth finding duplicate Discord app configurations
**Recent Fixes Attempted**:
- Removed duplicate APP config from settings (only in database now)
- Changed `SOCIALACCOUNT_ONLY = False`
- Fixed provider_id to lowercase 'discord'

**Next Steps**:
```bash
# Clear Python bytecode cache
find /home/user/farout-django -type d -name "__pycache__" -exec rm -r {} +

# Rebuild containers completely
docker compose down
docker compose build --no-cache
docker compose up -d
```

### Issue 2: Missing Static File
**Error**: `Not Found: /static/img/hero-sc.avif`
**Impact**: Minor - cosmetic only
**Fix**: Add missing image or update template

---

## 9. RECOMMENDATIONS FOR FUTURE EXPANSION

### 9.1 Immediate Improvements

#### A. Consolidate User/Member Models
**Issue**: Duplication between `User` (accounts) and `Member` (members) creates confusion

**Recommendation**:
```python
# Option 1: Merge into single User model
# Move Member fields to User model
# Remove Member model entirely

# Option 2: Keep separate with clear distinction
# User = Authentication & Portal Access
# Member = Extended SC-specific profile
# Add FK: Member.user = models.OneToOneField(User)
```

**Benefits**:
- Single source of truth
- Eliminates duplicate Discord IDs
- Clearer data model

#### B. Add API Versioning
**Current**: No API versioning
**Recommendation**:
```python
# In urls.py
urlpatterns = [
    path('api/v1/', include('apps.api.v1.urls')),
]
```

**Benefits**:
- Future-proof for breaking changes
- Support multiple client versions

#### C. Implement Permissions System
**Current**: Basic role checking
**Recommendation**:
```python
from django.contrib.auth.decorators import permission_required

@permission_required('squadron.can_manage_members')
def squadron_admin_view(request):
    pass

# Define custom permissions in Meta
class Squadron(models.Model):
    class Meta:
        permissions = [
            ("can_manage_members", "Can manage squadron members"),
            ("can_edit_squadron", "Can edit squadron details"),
        ]
```

**Benefits**:
- Fine-grained access control
- Better security
- Scalable as features grow

---

### 9.2 Database Optimization

#### A. Add Database Indexes
**Recommended Additions**:
```python
# User model
class Meta:
    indexes = [
        models.Index(fields=['email']),
        models.Index(fields=['last_login_at']),
    ]

# InternalMessage
class Meta:
    indexes = [
        models.Index(fields=['is_read', 'recipient_id']),
    ]
```

#### B. Implement Connection Pooling
```python
# settings/production.py
DATABASES = {
    'default': {
        'CONN_MAX_AGE': 600,  # Already set
        'OPTIONS': {
            'connect_timeout': 10,
            'options': '-c statement_timeout=30000',
        }
    }
}
```

---

### 9.3 Feature Enhancements

#### A. Advanced Fleet Management
```python
class FleetShip(models.Model):
    # New fields for expansion
    insurance_status = models.CharField(max_length=50)
    last_used_date = models.DateTimeField()
    maintenance_log = models.JSONField(default=list)
    current_location = models.CharField(max_length=200)
    available_from = models.DateTimeField()
    available_until = models.DateTimeField()
```

#### B. Mission System
**New App**: `apps/missions`

```python
class Mission(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    mission_type = models.CharField(max_length=50)
    required_ships = models.ManyToManyField('starships.Ship')
    max_participants = models.IntegerField()
    scheduled_time = models.DateTimeField()
    created_by = models.ForeignKey(User)
    squadron = models.ForeignKey('squadron.Squadron', null=True)

class MissionParticipant(models.Model):
    mission = models.ForeignKey(Mission)
    user = models.ForeignKey(User)
    ship = models.ForeignKey('fleet.FleetShip', null=True)
    status = models.CharField(max_length=20)
```

#### C. Advanced Messaging Features
```python
class InternalMessage(models.Model):
    # New fields
    attachments = models.JSONField(default=list)
    is_pinned = models.BooleanField(default=False)
    priority = models.CharField(max_length=20)
    tags = models.JSONField(default=list)
    recipients = models.JSONField(default=list)  # For group chats
    is_group_message = models.BooleanField(default=False)
```

#### D. Analytics & Reporting
**New App**: `apps/analytics`

```python
class ActivityLog(models.Model):
    user_id = models.IntegerField(db_index=True)
    action = models.CharField(max_length=100)
    model_type = models.CharField(max_length=50)
    model_id = models.IntegerField()
    metadata = models.JSONField(default=dict)
    timestamp = models.DateTimeField(auto_now_add=True)

class Report(models.Model):
    title = models.CharField(max_length=200)
    report_type = models.CharField(max_length=50)
    generated_by = models.ForeignKey(User)
    parameters = models.JSONField()
    result_data = models.JSONField()
```

---

### 9.4 API Development

#### A. RESTful API with Django REST Framework
```bash
pip install djangorestframework
```

**Proposed Structure**:
```
apps/
  api/
    __init__.py
    v1/
      __init__.py
      urls.py
      serializers/
        ship_serializers.py
        squadron_serializers.py
        user_serializers.py
      views/
        ship_views.py
        squadron_views.py
        user_views.py
```

**Example Serializer**:
```python
from rest_framework import serializers
from apps.starships.models import Ship

class ShipSerializer(serializers.ModelSerializer):
    manufacturer_name = serializers.CharField(
        source='manufacturer.name',
        read_only=True
    )

    class Meta:
        model = Ship
        fields = [
            'id', 'name', 'manufacturer', 'manufacturer_name',
            'type', 'size', 'focus', 'length', 'beam', 'height',
            'min_crew', 'max_crew', 'cargo_capacity',
            'is_flight_ready', 'pledge_price', 'image_url'
        ]
```

**Example ViewSet**:
```python
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

class ShipViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ship.objects.select_related('manufacturer').all()
    serializer_class = ShipSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['size', 'type', 'is_flight_ready']
    search_fields = ['name', 'manufacturer__name']
    ordering_fields = ['name', 'pledge_price']
```

#### B. API Authentication
```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 25,
}
```

---

### 9.5 Performance Optimization

#### A. Implement Caching
```python
# settings/base.py
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://redis:6379/1',
    }
}

# Usage in views
from django.views.decorators.cache import cache_page

@cache_page(60 * 15)  # Cache for 15 minutes
def ship_list(request):
    ships = Ship.objects.select_related('manufacturer').all()
    return render(request, 'ships/list.html', {'ships': ships})
```

#### B. Query Optimization
```python
# Bad - N+1 query problem
ships = Ship.objects.all()
for ship in ships:
    print(ship.manufacturer.name)  # Additional query per ship

# Good - Use select_related
ships = Ship.objects.select_related('manufacturer').all()

# Good - Use prefetch_related for reverse FK and M2M
squadrons = Squadron.objects.prefetch_related('members__user').all()
```

#### C. Database Read Replicas
```python
# settings/production.py
DATABASES = {
    'default': {
        # Master database (write)
    },
    'replica': {
        # Read replica (read-only)
    }
}

# Usage
User.objects.create(username='test')  # Write to master
users = User.objects.using('replica').all()  # Read from replica
```

---

### 9.6 Monitoring & Logging

#### A. Structured Logging
```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'json': {
            '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'json',
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/app/logs/django.log',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 5,
            'formatter': 'json',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
        },
        'apps': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
        },
    },
}
```

#### B. Performance Monitoring
```bash
pip install django-silk  # SQL query profiling
pip install sentry-sdk    # Error tracking
```

```python
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[DjangoIntegration()],
    traces_sample_rate=0.1,
)
```

---

### 9.7 Security Enhancements

#### A. Rate Limiting
```bash
pip install django-ratelimit
```

```python
from django_ratelimit.decorators import ratelimit

@ratelimit(key='ip', rate='5/m', method='POST')
def contact_submit(request):
    # Limit to 5 submissions per minute per IP
    pass
```

#### B. Enhanced Content Security Policy
```python
CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = ("'self'", "'unsafe-inline'", "cdn.tiny.cloud")
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'", "fonts.googleapis.com")
CSP_FONT_SRC = ("'self'", "fonts.gstatic.com")
CSP_IMG_SRC = ("'self'", "data:", "blob:", "https:", "*.discordapp.com")
CSP_CONNECT_SRC = ("'self'",)
```

---

### 9.8 Testing Strategy

#### A. Unit Tests
```python
# apps/squadron/tests/test_models.py
from django.test import TestCase
from apps.squadron.models import Squadron
from apps.accounts.models import User

class SquadronModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser')
        self.squadron = Squadron.objects.create(
            name='Alpha Squadron',
            callsign='ALPHA',
            commander=self.user
        )

    def test_squadron_creation(self):
        self.assertEqual(self.squadron.name, 'Alpha Squadron')
        self.assertEqual(self.squadron.slug, 'alpha-squadron')

    def test_is_full(self):
        self.squadron.max_members = 5
        self.assertFalse(self.squadron.is_full())
```

#### B. Integration Tests
```python
# apps/communications/tests/test_views.py
from django.test import TestCase, Client
from django.urls import reverse

class MessageViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='test',
            password='test123'
        )
        self.client.login(username='test', password='test123')

    def test_inbox_view(self):
        response = self.client.get(reverse('communications:inbox'))
        self.assertEqual(response.status_code, 200)
```

---

### 9.9 Data Management

#### A. Management Commands
```python
# apps/starships/management/commands/import_ships.py
from django.core.management.base import BaseCommand
from apps.starships.models import Ship, Manufacturer
import requests

class Command(BaseCommand):
    help = 'Import ships from Star Citizen API'

    def handle(self, *args, **kwargs):
        response = requests.get('https://api.starcitizen-api.com/ships')
        ships_data = response.json()

        for ship_data in ships_data:
            manufacturer, _ = Manufacturer.objects.get_or_create(
                code=ship_data['manufacturer_code'],
                defaults={'name': ship_data['manufacturer_name']}
            )

            Ship.objects.update_or_create(
                api_id=ship_data['id'],
                defaults={
                    'name': ship_data['name'],
                    'manufacturer': manufacturer,
                }
            )

        self.stdout.write(
            self.style.SUCCESS(f'Imported {len(ships_data)} ships')
        )
```

#### B. Backup Strategy
```bash
#!/bin/bash
# scripts/backup_databases.sh

# Backup default database
docker exec farout-django-db-1 pg_dump -U farout farout | \
  gzip > backups/farout_$(date +%Y%m%d_%H%M%S).sql.gz

# Backup communications database
docker exec farout-django-db-1 pg_dump -U farout farout_communications | \
  gzip > backups/farout_communications_$(date +%Y%m%d_%H%M%S).sql.gz

# Keep only last 30 days
find backups/ -name "*.sql.gz" -mtime +30 -delete
```

---

### 9.10 Enhanced Health Check

```python
# apps/core/views.py
from django.http import JsonResponse
from django.db import connections
from django.core.cache import cache

def health_check(request):
    """Enhanced health check with database and cache status."""
    health = {
        'status': 'healthy',
        'checks': {}
    }

    # Check default database
    try:
        connections['default'].ensure_connection()
        health['checks']['database_default'] = 'ok'
    except Exception as e:
        health['checks']['database_default'] = f'error: {str(e)}'
        health['status'] = 'unhealthy'

    # Check communications database
    try:
        connections['communications'].ensure_connection()
        health['checks']['database_communications'] = 'ok'
    except Exception as e:
        health['checks']['database_communications'] = f'error: {str(e)}'
        health['status'] = 'unhealthy'

    # Check cache
    try:
        cache.set('health_check', 'ok', 10)
        health['checks']['cache'] = 'ok'
    except Exception as e:
        health['checks']['cache'] = f'error: {str(e)}'
        health['status'] = 'unhealthy'

    status_code = 200 if health['status'] == 'healthy' else 503
    return JsonResponse(health, status=status_code)
```

---

## 10. SUMMARY

### Strengths
✅ Well-structured Django apps with clear separation of concerns
✅ Multi-database architecture for performance and scaling
✅ Discord OAuth integration for seamless authentication
✅ Comprehensive ship and fleet management system
✅ Squadron system with role management
✅ Proper use of database indexes
✅ JSONField usage for flexible data storage
✅ Database router for proper query routing

### Areas for Improvement
⚠️ User/Member model duplication
⚠️ No API versioning
⚠️ Limited test coverage
⚠️ Basic permission system
⚠️ No caching layer
⚠️ Discord login error (MultipleObjectsReturned)

### Priority Recommendations
1. **Fix Discord login** (CRITICAL - immediate)
2. **Consolidate User/Member models** (HIGH - data integrity)
3. **Implement comprehensive testing** (HIGH - stability)
4. **Add REST API** (MEDIUM - feature expansion)
5. **Implement caching** (MEDIUM - performance)
6. **Add mission system** (LOW - future feature)

---

## 11. FILE LOCATIONS

### Key Configuration Files
- **Main URLs**: `farout/urls.py`
- **Database Router**: `farout/db_router.py`
- **Settings**: `farout/settings/base.py`
- **Docker Compose**: `docker-compose.yml`
- **Requirements**: `requirements.txt`

### App Locations
```
apps/
├── accounts/         # User authentication
├── blog/            # News & announcements
├── communications/  # Messages & contact forms
├── core/            # Base views
├── dashboard/       # Dashboard views
├── fleet/           # Member ship ownership
├── items/           # Inventory
├── members/         # Member profiles
├── organization/    # SC org data
├── squadron/        # Squadron management
└── starships/       # Ship database
```

### Database Tables

**Default Database (`farout`)**:
- users
- members
- squadrons
- squadron_members
- starships_manufacturer
- starships_ship
- starships_shipcomponent
- fleet_fleetship
- ship_ownerships
- blog_posts
- blog_categories
- blog_tags
- items
- organization (models)
- organizationmember

**Communications Database (`farout_communications`)**:
- internal_messages
- contact_submissions

---

## 12. MIGRATION HISTORY

### Recent Migration Issues & Fixes

#### Blog Migrations Conflict
- **Issue**: Migrations 0001 and 0002 both tried to create Category/Tag tables
- **Fix**: Faked migration 0002 and 0003
- **Status**: Resolved

#### Database Configuration Fix
- **Issue**: Communications DB using wrong connection method
- **Fix**: Changed from `dj_database_url.config()` to `dj_database_url.parse()`
- **Location**: `farout/settings/base.py:95`
- **Status**: Resolved

#### Database Router Fix
- **Issue**: Router blocking Django internal tables from communications DB
- **Fix**: Updated `allow_migrate` to allow contenttypes, admin, auth, sessions
- **Location**: `farout/db_router.py:55-79`
- **Status**: Resolved

---

## 13. ENVIRONMENT VARIABLES

### Required Environment Variables

```env
# Database
POSTGRES_DB=farout
POSTGRES_USER=farout
POSTGRES_PASSWORD=<password>
DATABASE_URL=postgresql://farout:<password>@db:5432/farout
COMMUNICATIONS_DB_URL=postgresql://farout:<password>@db:5432/farout_communications

# Django
SECRET_KEY=<django-secret-key>
ALLOWED_HOSTS=localhost,127.0.0.1,test.hugoforge.com

# Discord OAuth (REQUIRED)
DISCORD_CLIENT_ID=<your-discord-client-id>
DISCORD_CLIENT_SECRET=<your-discord-client-secret>

# Star Citizen API (Optional)
STARCITIZEN_API_KEY=<api-key>
SC_ORGANIZATION_SID=FAROUTCORP
```

### Discord OAuth Setup

1. Go to https://discord.com/developers/applications
2. Create new application
3. Go to OAuth2 section
4. Add redirect URIs:
   - Local: `http://localhost:8000/accounts/discord/login/callback/`
   - Production: `https://test.hugoforge.com/accounts/discord/login/callback/`
5. Copy Client ID and Secret to environment variables
6. Create Social Application in Django admin:
   - Provider: discord (lowercase)
   - Provider ID: discord (lowercase)
   - Client ID: <from Discord>
   - Secret: <from Discord>
   - Sites: Add your domain

---

## 14. DEPLOYMENT CHECKLIST

### Pre-Deployment
- [ ] Run migrations on both databases
- [ ] Collect static files
- [ ] Update environment variables
- [ ] Configure Discord OAuth redirect URIs
- [ ] Test Discord login flow
- [ ] Verify database connections
- [ ] Check health endpoint

### Post-Deployment
- [ ] Monitor logs for errors
- [ ] Test user registration flow
- [ ] Verify squadron functionality
- [ ] Check ship data imports
- [ ] Test messaging system
- [ ] Verify contact form submissions

### Database Maintenance
- [ ] Regular backups (daily recommended)
- [ ] Monitor connection pool usage
- [ ] Review slow queries
- [ ] Check database size growth
- [ ] Optimize indexes as needed

---

## APPENDIX A: Common Commands

### Development
```bash
# Run migrations
python manage.py migrate
python manage.py migrate --database=communications

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver

# Collect static files
python manage.py collectstatic

# Create new app
python manage.py startapp <app_name> apps/<app_name>
```

### Docker
```bash
# Start containers
docker compose up -d

# View logs
docker compose logs web --tail 50

# Restart services
docker compose restart web

# Rebuild and start
docker compose up -d --build

# Execute commands in container
docker exec farout-django-web-1 python manage.py migrate

# Database shell
docker exec -it farout-django-db-1 psql -U farout -d farout
```

### Database
```bash
# Backup
docker exec farout-django-db-1 pg_dump -U farout farout > backup.sql

# Restore
docker exec -i farout-django-db-1 psql -U farout farout < backup.sql

# List databases
docker exec farout-django-db-1 psql -U farout -c "\l"

# List tables
docker exec farout-django-db-1 psql -U farout -d farout -c "\dt"
```

---

## APPENDIX B: Useful Queries

### Get user count by role
```sql
SELECT role, COUNT(*)
FROM users
GROUP BY role;
```

### Get squadron member counts
```sql
SELECT s.name, COUNT(sm.id) as member_count
FROM squadrons s
LEFT JOIN squadron_members sm ON s.id = sm.squadron_id AND sm.is_active = true
GROUP BY s.id, s.name
ORDER BY member_count DESC;
```

### Get fleet statistics
```sql
SELECT
    u.username,
    COUNT(DISTINCT fs.id) as ship_count,
    COUNT(DISTINCT fs.ship_id) as unique_ships
FROM users u
LEFT JOIN fleet_fleetship fs ON u.id = fs.owner_id
GROUP BY u.id, u.username
ORDER BY ship_count DESC;
```

### Get unread message counts
```sql
SELECT
    recipient_id,
    COUNT(*) as unread_count
FROM internal_messages
WHERE is_read = false
  AND is_deleted_by_recipient = false
GROUP BY recipient_id;
```

---

**End of Backend Architecture Audit**

*For questions or updates, contact the development team.*
