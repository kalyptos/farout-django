# Far Out Corporation - Design & Frontend Guide

**Generated:** November 12, 2025
**Project:** Far Out Django - Star Citizen Organization Management Portal
**Template:** Agznko Creative Agency and Portfolio HTML Template v1.0.0

---

## 📋 Table of Contents

1. [Design System Overview](#design-system-overview)
2. [File Structure](#file-structure)
3. [Color Palette & Branding](#color-palette--branding)
4. [Typography System](#typography-system)
5. [Template Architecture](#template-architecture)
6. [Component Library](#component-library)
7. [How to Edit Content](#how-to-edit-content)
8. [How to Add New Pages](#how-to-add-new-pages)
9. [Customizing Styles](#customizing-styles)
10. [Static Assets Management](#static-assets-management)
11. [Responsive Design Guide](#responsive-design-guide)
12. [JavaScript & Animations](#javascript--animations)
13. [Common Tasks Guide](#common-tasks-guide)
14. [Troubleshooting](#troubleshooting)

---

## 🎨 Design System Overview

### Framework
**Agznko Template** - Premium HTML template adapted for Star Citizen organization management

### Design Philosophy
- **Dark Theme:** Space-themed aesthetic with dark backgrounds and light text
- **Sci-Fi Gaming:** Bold colors, gradients, and futuristic elements
- **Card-Based Layout:** Modular components with consistent styling
- **Animation-Rich:** Scroll-triggered animations and smooth transitions
- **Mobile-First Responsive:** Fully responsive across all devices

### Technical Stack
- **CSS Framework:** Bootstrap 5 + Custom Agznko theme
- **JavaScript:** jQuery 3.7.1, Bootstrap Bundle, Swiper, WOW.js
- **Fonts:** Google Fonts (Teko, Kanit) + Font Awesome icons
- **Template Engine:** Django Templates with Jinja2 syntax

---

## 📁 File Structure

### Complete Directory Structure

```
farout-django/
├── templates/                          # All HTML templates
│   ├── base.html                      # Main base template (all pages extend this)
│   ├── home.html                      # Homepage
│   ├── dashboard.html                 # User dashboard
│   ├── about.html                     # About Us page
│   ├── contact.html                   # Contact page
│   ├── starships/
│   │   ├── ship_list.html            # Ship catalog
│   │   └── ship_detail.html          # Ship details
│   └── organization/
│       ├── member_list.html          # Member roster
│       └── member_detail.html        # Member profile
│
├── static/                            # Static files
│   ├── css/                          # Stylesheets
│   │   ├── main.css                  # Main Agznko theme (4,880 lines)
│   │   ├── bootstrap.min.css         # Bootstrap 5
│   │   ├── animate.css               # Animation library
│   │   ├── all.min.css              # Font Awesome icons
│   │   ├── swiper-bundle.min.css    # Slider styles
│   │   └── color.css                 # (Empty - for future use)
│   │
│   ├── js/                           # JavaScript files
│   │   ├── main.js                   # Main theme JS (330 lines)
│   │   ├── jquery-3.7.1.min.js      # jQuery library
│   │   ├── bootstrap.bundle.min.js   # Bootstrap JS
│   │   └── swiper-bundle.min.js     # Swiper slider
│   │
│   ├── img/                          # Images
│   │   ├── breadcrumb.jpg           # Page header backgrounds
│   │   ├── hero-sc.jpg              # Homepage hero image
│   │   ├── placeholder-ship.jpg     # Default ship image
│   │   ├── favicon.svg              # Browser icon
│   │   ├── default-avatar.svg       # User placeholder
│   │   ├── logo/
│   │   │   └── white-logo.svg       # Organization logo
│   │   └── ranks/                    # Rank badge icons
│   │       ├── private.svg
│   │       ├── captain.svg
│   │       ├── ceo.svg
│   │       └── member.svg
│   │
│   └── webfonts/                     # Font files
│       ├── fa-brands-400.woff2
│       ├── fa-regular-400.woff2
│       └── fa-solid-900.woff2
```

---

## 🎨 Color Palette & Branding

### Primary Colors

**Main Theme Colors (from main.css):**
```css
--theme: #BFF747        /* Lime Green - Primary brand color */
--theme2: #FFD531       /* Yellow - Secondary accent */
```

**Used in Templates (inline styles):**
```css
Primary Accent: #55E6A5  /* Teal/Turquoise - Most commonly used */
```

### Background Colors

```css
--body-bg: #121212      /* Main background */
--bg: #171717           /* Secondary background */
--header: #121212       /* Header background */

/* Card backgrounds (gradients): */
background: linear-gradient(135deg, #1a1a2e 0%, #2d2d44 100%)
```

### Text Colors

```css
--white: #fff           /* Primary text */
--text: #f5f5f4cc      /* Body text with opacity */

/* Text variations: */
#fff                    /* Headers, important text */
#ccc                    /* Body paragraphs */
#aaa                    /* Muted text, labels */
#666                    /* Placeholder text */
```

### Border & Accent Colors

```css
--border: #2A2A2A       /* Main borders */
#333                    /* Card borders, subtle dividers */
#55E6A5                 /* Accent borders on hover */
```

### Semantic Colors

```css
/* Success/Active */
.bg-success: #55E6A5
Green: #28a745

/* Warning */
.bg-warning: #ffc107
Yellow: #FFD531

/* Info/Admin */
.bg-info: #17a2b8
Blue: #0dcaf0

/* Secondary/Muted */
.bg-secondary: #6c757d
Gray: #aaa
```

### Color Usage Guide

**Where to Use Each Color:**

| Color | Usage | Example |
|-------|-------|---------|
| `#55E6A5` (Teal) | Hover borders, accents, icons, links | Card hover, icon colors, active states |
| `#BFF747` (Lime) | Buttons, CTAs, highlights | `.theme-btn`, important actions |
| `#FFD531` (Yellow) | Secondary accents, badges | Warning badges, secondary highlights |
| `#1a1a2e → #2d2d44` | Card backgrounds | All card gradients |
| `#121212` / `#171717` | Page backgrounds | Body, sections |
| `#333` | Borders | Card borders, dividers |
| `#fff` | Headings, important text | H1-H6, labels |
| `#ccc` / `#aaa` | Body text, muted content | Paragraphs, descriptions |

---

## 📝 Typography System

### Font Families

**Loaded from Google Fonts (in base.html):**
```html
<link href="https://fonts.googleapis.com/css2?family=Kanit:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&family=Teko:wght@300;400;500;600;700&display=swap" rel="stylesheet">
```

**Font Usage:**
- **Headings:** `"Teko"` - Display font, weights 300-700
- **Body:** `"Kanit"` - Sans-serif, weights 100-900

### Heading Sizes

```css
h1 {
    font-size: 100px;        /* Desktop */
    font-size: 60-80px;      /* Tablet */
    font-size: 40-50px;      /* Mobile */
    font-weight: 700;
    line-height: 120%;
}

h2 {
    font-size: 40px;         /* Desktop */
    font-size: 36px;         /* Mobile */
    font-weight: 700;
    line-height: 120%;
}

h3 {
    font-size: 24px;         /* Desktop */
    font-size: 20px;         /* Mobile */
    font-weight: 600;
}

h4 {
    font-size: 20px;
    font-weight: 700;
    line-height: 130%;
}

h5 {
    font-size: 18px;
    font-weight: 700;
}

h6 {
    font-size: 16px;
    font-weight: 600;
    line-height: 145%;
}
```

### Body Text

```css
body {
    font-family: "Kanit", sans-serif;
    font-size: 18px;
    font-weight: 300;
    line-height: 28px;
    color: #f5f5f4cc;
}

p {
    font-size: 18px;
    line-height: 28px;
    color: #ccc;
}
```

### Typography Classes

```html
<!-- Large display text -->
<h1 class="display-1">Large Display</h1>

<!-- Section headings -->
<h2 class="mb-4">Section Title</h2>

<!-- Card headings -->
<h3 class="mb-3">Card Title</h3>

<!-- Muted text -->
<p class="text-muted">Secondary information</p>

<!-- Small text -->
<small class="text-muted">Fine print</small>
```

---

## 🏗️ Template Architecture

### Template Inheritance System

All pages extend `base.html` and override specific blocks:

```django
{% extends 'base.html' %}
{% load static %}

{% block title %}Your Page Title{% endblock %}

{% block content %}
    <!-- Your page content here -->
{% endblock %}
```

### Base Template Structure

**File:** `/home/user/farout-django/templates/base.html`

**Available Blocks:**

```django
{% block title %}        <!-- Page title (required) -->
{% block meta_description %}  <!-- SEO description (optional) -->
{% block extra_css %}    <!-- Additional CSS (optional) -->
{% block content %}      <!-- Main page content (required) -->
{% block extra_js %}     <!-- Additional JavaScript (optional) -->
```

**Base Template Sections:**

1. **HTML Head (lines 1-28)**
   - Meta tags, title, CSS loading
   - Google Fonts, Font Awesome, Bootstrap, Animate.css
   - Main.css, Swiper, Color.css
   - Favicon

2. **Preloader (lines 31-36)**
   - Loading animation with spinner
   - Auto-hides on page load

3. **Header Navigation (lines 39-111)**
   - Logo (left side)
   - Main navigation menu (center)
   - User menu (right side)
   - Mobile hamburger toggle

4. **Django Messages (lines 114-123)**
   - Bootstrap alerts for notifications
   - Success, error, warning, info

5. **Content Block (line 126)**
   - Main page content area
   - All child templates inject content here

6. **Footer (lines 129-234)**
   - Four-column layout
   - About, Quick Links, Resources, Contact Info
   - Social media icons
   - Copyright

7. **Scroll to Top Button (lines 237-241)**
   - Appears after scrolling
   - Smooth scroll animation

8. **Scripts (lines 245-263)**
   - jQuery, Bootstrap, Swiper, WOW.js, CounterUp
   - Main.js, Preloader hide script

### Navigation Menu Structure

**Location:** `base.html` lines 50-84

**Menu Items:**
```html
<nav class="main-menu">
    <ul>
        <li><a href="/">Home</a></li>
        <li><a href="{% url 'about' %}">About</a></li>
        <li class="has-dropdown">
            <a href="#">Organization</a>
            <ul class="submenu">
                <li><a href="{% url 'organization:member_list' %}">Members</a></li>
                <!-- Add more organization submenu items here -->
            </ul>
        </li>
        <li><a href="{% url 'starships:ship_list' %}">Ships</a></li>
        <li><a href="{% url 'contact' %}">Contact</a></li>
    </ul>
</nav>
```

**User Menu (Authenticated):**
```html
<li><a href="{% url 'dashboard' %}">Dashboard</a></li>
<li><a href="{% url 'account_logout' %}">Logout</a></li>
```

**User Menu (Not Authenticated):**
```html
<a href="{% url 'account_login' %}" class="theme-btn">
    <i class="fab fa-discord"></i> Login with Discord
</a>
```

### Footer Structure

**Location:** `base.html` lines 129-234

**Four Columns:**

1. **About Widget**
   - Organization logo
   - Description text
   - Social icons (Discord, Twitter, YouTube, Twitch)

2. **Quick Links**
   - About Us
   - Members
   - Ships
   - Contact

3. **Resources**
   - Dashboard
   - Privacy Policy (placeholder)
   - Terms of Service (placeholder)

4. **Contact Info**
   - Email
   - Discord link

---

## 🧩 Component Library

### 1. Buttons

#### Primary Button
```html
<a href="#" class="theme-btn">
    <i class="fas fa-icon"></i> Button Text
</a>
```

**Styling:**
- Background: `#BFF747` (lime green)
- Padding: 22px 40px
- Border-radius: 120px (pill shape)
- Hover: Animated clip-path effect

**Variations:**
```html
<!-- Button with icon -->
<button type="submit" class="theme-btn">
    <i class="fas fa-search"></i> Search
</button>

<!-- Full width button -->
<a href="#" class="theme-btn w-100">Full Width</a>

<!-- Outlined button (custom inline style) -->
<a href="#" class="theme-btn btn-outline">Outline Style</a>
```

#### Secondary Button/Link
```html
<a href="#" class="theme-btn-2">
    Text Link <i class="fa-solid fa-arrow-right"></i>
</a>
```

---

### 2. Cards

#### Standard Card
```html
<div class="card-wrapper">
    <div class="content-card wow fadeInUp" data-wow-delay=".3s">
        <h3 class="mb-4">
            <i class="fas fa-icon"></i> Card Title
        </h3>
        <p class="content-text">Card content goes here...</p>
    </div>
</div>
```

**Card Styling (add to page or inline):**
```css
<style>
.content-card {
    background: linear-gradient(135deg, #1a1a2e 0%, #2d2d44 100%);
    padding: 35px;
    border-radius: 10px;
    border: 1px solid #333;
}

.content-card h3 {
    color: #fff;
    border-bottom: 2px solid #55E6A5;
    padding-bottom: 15px;
}

.content-card h3 i {
    color: #55E6A5;
    margin-right: 10px;
}

.content-text {
    color: #ccc;
    line-height: 1.8;
}
</style>
```

#### Statistics Card
```html
<div class="col-lg-4 col-md-6">
    <div class="stat-card wow fadeInUp" data-wow-delay=".3s">
        <div class="stat-icon">
            <i class="fas fa-users"></i>
        </div>
        <div class="stat-content">
            <h3>150+</h3>
            <p>Active Members</p>
        </div>
    </div>
</div>
```

**Stat Card CSS:**
```css
<style>
.stat-card {
    background: linear-gradient(135deg, #1a1a2e 0%, #2d2d44 100%);
    padding: 30px;
    border-radius: 10px;
    border: 1px solid #333;
    text-align: center;
    transition: all 0.3s;
}

.stat-card:hover {
    transform: translateY(-10px);
    border-color: #55E6A5;
}

.stat-icon {
    font-size: 3rem;
    color: #55E6A5;
    margin-bottom: 20px;
}

.stat-content h3 {
    font-size: 2.5rem;
    font-weight: 700;
    color: #fff;
}

.stat-content p {
    color: #aaa;
    font-size: 1.1rem;
}
</style>
```

#### Profile/Info Card
```html
<div class="profile-card">
    <div class="profile-info">
        <div class="info-item">
            <div class="info-label">
                <i class="fas fa-medal"></i> Rank
            </div>
            <div class="info-value">
                Captain
            </div>
        </div>
        <!-- More info items -->
    </div>
</div>
```

**Profile Card CSS:**
```css
<style>
.profile-card {
    background: linear-gradient(135deg, #1a1a2e 0%, #2d2d44 100%);
    padding: 30px;
    border-radius: 10px;
    border: 1px solid #333;
}

.info-item {
    padding: 15px 0;
    border-bottom: 1px solid #333;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.info-item:last-child {
    border-bottom: none;
}

.info-label {
    color: #aaa;
    font-weight: 600;
}

.info-label i {
    color: #55E6A5;
    margin-right: 8px;
}

.info-value {
    color: #fff;
    font-weight: 600;
}
</style>
```

---

### 3. Breadcrumbs

```html
<div class="breadcrumb-wrapper section-padding bg-cover"
     style="background-image: url('{% static 'img/breadcrumb.jpg' %}');">
    <div class="container">
        <div class="page-heading">
            <h1 class="wow fadeInUp" data-wow-delay=".3s">Page Title</h1>
            <ul class="breadcrumb-items wow fadeInUp" data-wow-delay=".5s">
                <li>
                    <a href="{% url 'home' %}">Home</a>
                </li>
                <li>
                    <i class="fa-sharp fa-solid fa-slash-forward"></i>
                </li>
                <li>
                    Current Page
                </li>
            </ul>
        </div>
    </div>
</div>
```

**Features:**
- Background image with overlay
- White text
- Icon separators
- Animated fade-in

---

### 4. Forms

#### Search/Filter Form
```html
<form method="get" class="filter-form">
    <div class="row g-4">
        <div class="col-lg-4 col-md-6">
            <input type="search"
                   name="q"
                   value="{{ request.GET.q }}"
                   placeholder="Search..."
                   class="form-control">
        </div>
        <div class="col-lg-4 col-md-6">
            <select name="filter" class="form-select">
                <option value="">All Items</option>
                <option value="option1">Option 1</option>
            </select>
        </div>
        <div class="col-lg-4 col-md-12">
            <button type="submit" class="theme-btn w-100">
                <i class="fas fa-search"></i> Search
            </button>
        </div>
    </div>
</form>
```

**Form Styling:**
```css
<style>
.filter-form .form-control,
.filter-form .form-select {
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid #333;
    color: #fff;
    padding: 12px 20px;
}

.filter-form .form-control:focus,
.filter-form .form-select:focus {
    background: rgba(255, 255, 255, 0.15);
    border-color: #55E6A5;
    color: #fff;
    box-shadow: 0 0 0 0.2rem rgba(85, 230, 165, 0.25);
}

.filter-form .form-control::placeholder {
    color: #666;
}

.filter-form .form-select option {
    background: #1a1a2e;
    color: #fff;
}
</style>
```

#### Contact Form
```html
<form id="contactForm" class="contact-form">
    <div class="row g-4">
        <div class="col-md-6">
            <div class="form-group">
                <label for="name">
                    <i class="fas fa-user"></i> Your Name *
                </label>
                <input type="text"
                       id="name"
                       name="name"
                       class="form-control"
                       placeholder="Enter your name"
                       required>
            </div>
        </div>
        <div class="col-12">
            <div class="form-group">
                <label for="message">
                    <i class="fas fa-comment"></i> Message *
                </label>
                <textarea id="message"
                          name="message"
                          class="form-control"
                          rows="6"
                          placeholder="Your message..."
                          required></textarea>
            </div>
        </div>
        <div class="col-12">
            <button type="submit" class="theme-btn w-100">
                <i class="fas fa-paper-plane"></i> Send Message
            </button>
        </div>
    </div>
</form>
```

---

### 5. Badges

```html
<!-- Status badges -->
<span class="badge bg-success">Active</span>
<span class="badge bg-warning">Pledged</span>
<span class="badge bg-info">Admin</span>
<span class="badge bg-secondary">Member</span>

<!-- Custom colored badges -->
<span class="badge" style="background: #55E6A5;">Custom</span>
```

---

### 6. Icons

**Font Awesome (all available):**
```html
<!-- UI Icons -->
<i class="fas fa-users"></i>
<i class="fas fa-rocket"></i>
<i class="fas fa-search"></i>
<i class="fas fa-envelope"></i>

<!-- Social Icons -->
<i class="fab fa-discord"></i>
<i class="fab fa-twitter"></i>
<i class="fab fa-youtube"></i>
<i class="fab fa-twitch"></i>

<!-- Arrows -->
<i class="fa-solid fa-arrow-right"></i>
<i class="fa-solid fa-arrow-left"></i>
<i class="fa-sharp fa-solid fa-slash-forward"></i>
```

**Icon Sizes:**
```html
<i class="fas fa-icon fa-2x"></i>  <!-- 2x size -->
<i class="fas fa-icon fa-3x"></i>  <!-- 3x size -->
```

**Colored Icons:**
```css
<style>
i.accent-icon {
    color: #55E6A5;
}
</style>
```

---

### 7. Grid Layouts

#### Two-Column Layout
```html
<div class="row g-4">
    <div class="col-lg-6">
        <!-- Left column content -->
    </div>
    <div class="col-lg-6">
        <!-- Right column content -->
    </div>
</div>
```

#### Three-Column Layout
```html
<div class="row g-4">
    <div class="col-lg-4 col-md-6">
        <!-- Column 1 -->
    </div>
    <div class="col-lg-4 col-md-6">
        <!-- Column 2 -->
    </div>
    <div class="col-lg-4 col-md-12">
        <!-- Column 3 -->
    </div>
</div>
```

#### Dashboard Layout (Asymmetric)
```html
<div class="row g-4">
    <!-- Left sidebar -->
    <div class="col-lg-4">
        <!-- Sidebar content -->
    </div>

    <!-- Main content -->
    <div class="col-lg-5">
        <!-- Main content -->
    </div>

    <!-- Right sidebar -->
    <div class="col-lg-3">
        <!-- Right sidebar content -->
    </div>
</div>
```

---

### 8. Pagination

```html
{% if is_paginated %}
<div class="page-nav-wrap text-center wow fadeInUp pt-60" data-wow-delay=".3s">
    <ul>
        {% if page_obj.has_previous %}
        <li>
            <a class="page-numbers icon" href="?page={{ page_obj.previous_page_number }}">
                <i class="fa-solid fa-arrow-left-long"></i>
            </a>
        </li>
        {% endif %}

        {% for num in page_obj.paginator.page_range %}
            {% if page_obj.number == num %}
            <li><a class="page-numbers active" href="javascript:void(0)">{{ num }}</a></li>
            {% elif num > page_obj.number|add:'-3' and num < page_obj.number|add:'3' %}
            <li><a class="page-numbers" href="?page={{ num }}">{{ num }}</a></li>
            {% endif %}
        {% endfor %}

        {% if page_obj.has_next %}
        <li>
            <a class="page-numbers icon" href="?page={{ page_obj.next_page_number }}">
                <i class="fa-solid fa-arrow-right-long"></i>
            </a>
        </li>
        {% endif %}
    </ul>
</div>
{% endif %}
```

---

## ✏️ How to Edit Content

### Editing Navigation Menu

**File:** `templates/base.html` (lines 50-84)

**Add a menu item:**
```html
<li><a href="{% url 'your_url_name' %}">Menu Item</a></li>
```

**Add a dropdown menu:**
```html
<li class="has-dropdown">
    <a href="#">Parent Item <i class="fa-regular fa-angle-down"></i></a>
    <ul class="submenu">
        <li><a href="{% url 'submenu_item_1' %}">Submenu Item 1</a></li>
        <li><a href="{% url 'submenu_item_2' %}">Submenu Item 2</a></li>
    </ul>
</li>
```

---

### Editing Footer

**File:** `templates/base.html` (lines 129-234)

**Change organization info:**
```html
<!-- Line 145 -->
<div class="footer-widget">
    <a href="/" class="f-logo">
        <img src="{% static 'img/logo/white-logo.svg' %}" alt="Logo">
    </a>
    <p>
        Your organization description here...
    </p>
</div>
```

**Add/remove footer links:**
```html
<!-- Line 163 -->
<div class="footer-widget">
    <h4 class="fw-heading">Quick Links</h4>
    <ul class="link-list">
        <li><a href="{% url 'about' %}">About Us</a></li>
        <li><a href="{% url 'new_page' %}">New Page</a></li>
    </ul>
</div>
```

**Update social media links:**
```html
<!-- Line 154 -->
<div class="social-icon d-flex align-items-center">
    <a href="https://discord.gg/your-server"><i class="fab fa-discord"></i></a>
    <a href="https://twitter.com/your-handle"><i class="fab fa-twitter"></i></a>
    <!-- Add more social links -->
</div>
```

---

### Editing Homepage

**File:** `templates/home.html`

**Change hero section:**
```html
<!-- Lines 8-40 -->
<section class="hero-section hero-1 style-gaming bg-cover"
         style="background-image: url('{% static 'img/hero-sc.jpg' %}');">
    <div class="container">
        <div class="row g-4">
            <div class="col-lg-9">
                <div class="hero-content">
                    <h1 class="wow fadeInUp" data-wow-delay=".3s">
                        Your Hero Title
                    </h1>
                    <p class="wow fadeInUp" data-wow-delay=".5s">
                        Your hero description...
                    </p>
                </div>
            </div>
        </div>
    </div>
</section>
```

**Edit service cards:**
```html
<!-- Lines 51-83 -->
<div class="col-xl-4 col-lg-6 col-md-6 wow fadeInUp" data-wow-delay=".3s">
    <div class="choose-us-card-items">
        <div class="icon">
            <i class="fas fa-your-icon"></i>
        </div>
        <div class="content">
            <h4>
                <a href="#">Your Service Title</a>
            </h4>
            <p>
                Your service description...
            </p>
        </div>
    </div>
</div>
```

**Modify featured ships count:**
```python
# In apps/core/views.py (line 22)
featured_ships = Ship.objects.filter(
    is_flight_ready=True
).order_by('?')[:6]  # Change this number
```

---

### Editing Dashboard

**File:** `templates/dashboard.html`

**Add new stat card:**
```html
<!-- After line 63 -->
<div class="col-lg-3 col-md-6">
    <div class="stats-card wow fadeInUp" data-wow-delay=".3s">
        <div class="stats-icon">
            <i class="fas fa-your-icon"></i>
        </div>
        <div class="stats-content">
            <h3>{{ your_stat_value }}</h3>
            <p>Your Stat Label</p>
        </div>
    </div>
</div>
```

**Pass data from view:**
```python
# In apps/core/views.py dashboard function
context = {
    # ... existing context
    'your_stat_value': 100,  # Add your stat
}
```

**Add new dashboard section:**
```html
<!-- Add anywhere in the row g-4 -->
<div class="col-lg-12">
    <div class="content-card wow fadeInUp" data-wow-delay=".3s">
        <h3 class="mb-4">
            <i class="fas fa-icon"></i> New Section Title
        </h3>
        <p>Your section content...</p>
    </div>
</div>
```

---

### Editing About Page

**File:** `templates/about.html`

**Change organization description:**
```html
<!-- Lines 92-108 -->
<div class="content-card wow fadeInLeft" data-wow-delay=".3s">
    <h3 class="mb-4">
        <i class="fas fa-info-circle"></i> About Our Organization
    </h3>
    <p class="content-text">
        Your organization description here...
    </p>
</div>
```

**Edit service boxes:**
```html
<!-- Lines 161-196 -->
<div class="col-md-3">
    <div class="service-box">
        <div class="service-icon">
            <i class="fas fa-your-icon"></i>
        </div>
        <h5>Your Service</h5>
        <p>Service description</p>
    </div>
</div>
```

---

### Editing Contact Page

**File:** `templates/contact.html`

**Update contact information:**
```html
<!-- Lines 43-96 -->
<div class="info-item">
    <div class="info-icon">
        <i class="fas fa-envelope"></i>
    </div>
    <div class="info-content">
        <h5>Email</h5>
        <p>your-email@example.com</p>
    </div>
</div>
```

**Add form field:**
```html
<!-- Add in form row -->
<div class="col-md-6">
    <div class="form-group">
        <label for="field_name">
            <i class="fas fa-icon"></i> Field Label *
        </label>
        <input type="text"
               id="field_name"
               name="field_name"
               class="form-control"
               placeholder="Placeholder text"
               required>
    </div>
</div>
```

---

## 🆕 How to Add New Pages

### Step 1: Create Template File

Create a new file in `templates/` directory:

**Example:** `templates/fleet.html`

```django
{% extends 'base.html' %}
{% load static %}

{% block title %}Fleet Management - Far Out Corporation{% endblock %}

{% block content %}
<!-- Breadcrumb Section -->
<div class="breadcrumb-wrapper section-padding bg-cover"
     style="background-image: url('{% static 'img/breadcrumb.jpg' %}');">
    <div class="container">
        <div class="page-heading">
            <h1 class="wow fadeInUp" data-wow-delay=".3s">Fleet Management</h1>
            <ul class="breadcrumb-items wow fadeInUp" data-wow-delay=".5s">
                <li>
                    <a href="{% url 'home' %}">Home</a>
                </li>
                <li>
                    <i class="fa-sharp fa-solid fa-slash-forward"></i>
                </li>
                <li>
                    Fleet
                </li>
            </ul>
        </div>
    </div>
</div>

<!-- Main Content Section -->
<section class="section-padding fix">
    <div class="container">
        <div class="row g-4">
            <div class="col-12">
                <div class="content-card wow fadeInUp" data-wow-delay=".3s">
                    <h3 class="mb-4">
                        <i class="fas fa-rocket"></i> Your Content Title
                    </h3>
                    <p class="content-text">
                        Your page content goes here...
                    </p>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- Add page-specific styles -->
<style>
.content-card {
    background: linear-gradient(135deg, #1a1a2e 0%, #2d2d44 100%);
    padding: 35px;
    border-radius: 10px;
    border: 1px solid #333;
}

.content-card h3 {
    color: #fff;
    border-bottom: 2px solid #55E6A5;
    padding-bottom: 15px;
}

.content-card h3 i {
    color: #55E6A5;
    margin-right: 10px;
}

.content-text {
    color: #ccc;
    line-height: 1.8;
}
</style>
{% endblock %}
```

---

### Step 2: Create View Function

**File:** `apps/core/views.py` (or relevant app)

```python
def fleet_management(request):
    """Fleet management page."""
    # Your logic here
    context = {
        'your_data': 'value',
    }
    return render(request, 'fleet.html', context)
```

**Or use Class-Based View:**

```python
from django.views.generic import TemplateView

class FleetManagementView(TemplateView):
    template_name = 'fleet.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['your_data'] = 'value'
        return context
```

---

### Step 3: Add URL Pattern

**File:** `farout/urls.py`

```python
from apps.core import views as core_views

urlpatterns = [
    # ... existing patterns
    path('fleet/', core_views.fleet_management, name='fleet'),
    # Or for class-based view:
    # path('fleet/', core_views.FleetManagementView.as_view(), name='fleet'),
]
```

---

### Step 4: Add to Navigation (Optional)

**File:** `templates/base.html` (lines 50-84)

```html
<li><a href="{% url 'fleet' %}">Fleet</a></li>
```

---

### Complete Example: Adding a "News" Page

**1. Create template:** `templates/news.html`

```django
{% extends 'base.html' %}
{% load static %}

{% block title %}News - Far Out Corporation{% endblock %}

{% block content %}
<div class="breadcrumb-wrapper section-padding bg-cover"
     style="background-image: url('{% static 'img/breadcrumb.jpg' %}');">
    <div class="container">
        <div class="page-heading">
            <h1 class="wow fadeInUp" data-wow-delay=".3s">Latest News</h1>
            <ul class="breadcrumb-items wow fadeInUp" data-wow-delay=".5s">
                <li><a href="{% url 'home' %}">Home</a></li>
                <li><i class="fa-sharp fa-solid fa-slash-forward"></i></li>
                <li>News</li>
            </ul>
        </div>
    </div>
</div>

<section class="section-padding fix">
    <div class="container">
        <div class="row g-4">
            {% for post in posts %}
            <div class="col-lg-4 col-md-6">
                <div class="news-card wow fadeInUp" data-wow-delay=".{{ forloop.counter }}s">
                    <h4><a href="#">{{ post.heading }}</a></h4>
                    <p>{{ post.content|truncatewords:20|safe }}</p>
                    <a href="#" class="theme-btn-2">Read More</a>
                </div>
            </div>
            {% endfor %}
        </div>
    </div>
</section>

<style>
.news-card {
    background: linear-gradient(135deg, #1a1a2e 0%, #2d2d44 100%);
    padding: 30px;
    border-radius: 10px;
    border: 1px solid #333;
    transition: all 0.3s;
}

.news-card:hover {
    transform: translateY(-5px);
    border-color: #55E6A5;
}

.news-card h4 a {
    color: #fff;
    text-decoration: none;
}

.news-card p {
    color: #ccc;
    margin: 15px 0;
}
</style>
{% endblock %}
```

**2. Create view:** `apps/core/views.py`

```python
from apps.blog.models import BlogPost

def news(request):
    """News listing page."""
    posts = BlogPost.objects.filter(published=True).order_by('-created_at')

    context = {
        'posts': posts,
    }
    return render(request, 'news.html', context)
```

**3. Add URL:** `farout/urls.py`

```python
path('news/', core_views.news, name='news'),
```

**4. Add to menu:** `templates/base.html`

```html
<li><a href="{% url 'news' %}">News</a></li>
```

---

## 🎨 Customizing Styles

### Method 1: Inline Styles (Quick Changes)

Add `<style>` block in your template before `{% endblock %}`:

```django
{% block content %}
<!-- Your content -->
{% endblock %}

<!-- Add at the end, before closing content block -->
<style>
.your-custom-class {
    background: #1a1a2e;
    color: #55E6A5;
}
</style>
```

**Pros:** Quick, page-specific, no file changes
**Cons:** Not reusable, increases HTML size

---

### Method 2: Custom CSS File (Best Practice)

**Create:** `static/css/custom.css`

```css
/* Custom styles for Far Out Corporation */

.my-custom-card {
    background: linear-gradient(135deg, #1a1a2e 0%, #2d2d44 100%);
    padding: 30px;
    border-radius: 10px;
    border: 1px solid #333;
}

.my-custom-button {
    background: #55E6A5;
    color: #1a1a2e;
    padding: 12px 30px;
    border-radius: 50px;
}
```

**Link in base.html:**

```django
<!-- In base.html head section, after main.css -->
<link rel="stylesheet" href="{% static 'css/custom.css' %}">
```

**Pros:** Reusable, maintainable, cached
**Cons:** Requires collectstatic in production

---

### Method 3: Override Main.css Variables

**Edit:** `static/css/main.css` (lines 1-20)

```css
:root {
    /* Change these to customize globally */
    --theme: #YOUR_PRIMARY_COLOR;      /* Change primary color */
    --theme2: #YOUR_SECONDARY_COLOR;   /* Change secondary color */
    --body-bg: #YOUR_BG_COLOR;         /* Change background */
    --text: #YOUR_TEXT_COLOR;          /* Change text color */
}
```

**Warning:** Changes affect entire site. Test thoroughly!

---

### Common Customizations

#### Change Primary Accent Color

**Replace all instances of `#55E6A5` with your color:**

Find and replace in your templates or add to custom.css:

```css
/* Override accent color */
.content-card h3 {
    border-bottom-color: #YOUR_COLOR !important;
}

.content-card h3 i,
.info-label i,
.stat-icon {
    color: #YOUR_COLOR !important;
}

.theme-btn:hover,
.card:hover {
    border-color: #YOUR_COLOR !important;
}
```

#### Change Card Background Gradient

```css
/* New gradient for all cards */
.content-card,
.stat-card,
.profile-card {
    background: linear-gradient(135deg, #YOUR_START 0%, #YOUR_END 100%) !important;
}
```

#### Change Button Style

```css
/* Override button appearance */
.theme-btn {
    background: #YOUR_COLOR !important;
    border-radius: 5px !important; /* Square corners */
    padding: 15px 30px !important;
}

.theme-btn:hover {
    background: #YOUR_HOVER_COLOR !important;
    transform: scale(1.05);
}
```

#### Change Font

**In base.html, replace Google Fonts link:**

```html
<!-- Replace Teko and Kanit with your fonts -->
<link href="https://fonts.googleapis.com/css2?family=Your+Font+Family&display=swap" rel="stylesheet">
```

**In custom.css:**

```css
/* Override fonts */
body {
    font-family: "Your Body Font", sans-serif !important;
}

h1, h2, h3, h4, h5, h6 {
    font-family: "Your Heading Font", sans-serif !important;
}
```

---

## 📦 Static Assets Management

### Adding Images

**1. Save image to:** `static/img/your-image.jpg`

**2. Use in template:**

```django
{% load static %}

<img src="{% static 'img/your-image.jpg' %}" alt="Description">
```

**3. Background images:**

```html
<div style="background-image: url('{% static 'img/your-image.jpg' %}');">
```

---

### Adding Icons (SVG)

**1. Save SVG to:** `static/img/icons/your-icon.svg`

**2. Use as image:**

```django
<img src="{% static 'img/icons/your-icon.svg' %}" alt="Icon" width="50">
```

**3. Use as background:**

```html
<div class="icon" style="background-image: url('{% static 'img/icons/your-icon.svg' %}');"></div>
```

---

### Using Font Awesome Icons

**Available classes:** All Font Awesome 5 icons

```html
<!-- Solid icons -->
<i class="fas fa-user"></i>
<i class="fas fa-rocket"></i>
<i class="fas fa-heart"></i>

<!-- Regular icons -->
<i class="far fa-user"></i>

<!-- Brand icons -->
<i class="fab fa-discord"></i>
<i class="fab fa-twitter"></i>
```

**Browse icons:** https://fontawesome.com/v5/search

---

### Updating Logo

**1. Replace file:** `static/img/logo/white-logo.svg`

**2. Or change path in base.html:**

```django
<!-- Line 43 -->
<a href="/" class="logo">
    <img src="{% static 'img/logo/your-new-logo.svg' %}" alt="Logo">
</a>

<!-- Line 145 (footer) -->
<a href="/" class="f-logo">
    <img src="{% static 'img/logo/your-new-logo.svg' %}" alt="Logo">
</a>
```

---

### Favicon

**Replace:** `static/img/favicon.svg`

**Or update in base.html:**

```django
<!-- Line 27 -->
<link rel="shortcut icon" type="image/x-icon" href="{% static 'img/your-favicon.ico' %}">
```

---

### Collecting Static Files (Production)

**Run after adding/changing static files:**

```bash
python manage.py collectstatic --noinput
```

This copies all static files to `STATIC_ROOT` for serving.

---

## 📱 Responsive Design Guide

### Bootstrap Breakpoints

```css
/* Extra small devices (portrait phones, less than 576px) */
/* No media query (mobile-first) */

/* Small devices (landscape phones, 576px and up) */
@media (min-width: 576px) { ... }

/* Medium devices (tablets, 768px and up) */
@media (min-width: 768px) { ... }

/* Large devices (desktops, 992px and up) */
@media (min-width: 992px) { ... }

/* Extra large devices (large desktops, 1200px and up) */
@media (min-width: 1200px) { ... }

/* Extra extra large devices (larger desktops, 1400px and up) */
@media (min-width: 1400px) { ... }
```

---

### Responsive Column Classes

```html
<!-- Stack on mobile, 2 cols on tablet, 3 cols on desktop -->
<div class="col-12 col-md-6 col-lg-4">
    <!-- Content -->
</div>

<!-- Full width on mobile, half on tablet, third on desktop -->
<div class="col-12 col-sm-6 col-lg-4">
    <!-- Content -->
</div>

<!-- Full on mobile and tablet, third on desktop -->
<div class="col-12 col-lg-4">
    <!-- Content -->
</div>
```

---

### Responsive Utilities

```html
<!-- Show on mobile only -->
<div class="d-block d-md-none">Mobile only</div>

<!-- Hide on mobile -->
<div class="d-none d-md-block">Desktop only</div>

<!-- Show on tablet and up -->
<div class="d-none d-sm-block">Tablet and desktop</div>

<!-- Responsive text alignment -->
<div class="text-center text-md-start">
    Centered on mobile, left on tablet+
</div>
```

---

### Responsive Spacing

```html
<!-- Different padding on different screens -->
<div class="p-3 p-md-4 p-lg-5">
    <!-- 1rem on mobile, 1.5rem on tablet, 3rem on desktop -->
</div>

<!-- Responsive margins -->
<div class="mb-3 mb-md-4 mb-lg-5">
    <!-- Bottom margin increases on larger screens -->
</div>
```

---

### Testing Responsive Design

**1. Browser DevTools:**
- Press F12
- Click device toggle icon
- Select device or resize manually

**2. Breakpoints to test:**
- 375px (iPhone)
- 768px (iPad)
- 1024px (Desktop)
- 1920px (Large desktop)

---

## ⚡ JavaScript & Animations

### Available JS Libraries

**jQuery 3.7.1:**
```javascript
$(document).ready(function() {
    // Your code here
});
```

**Bootstrap 5:**
```javascript
// Tooltips
var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl)
})

// Modals
var myModal = new bootstrap.Modal(document.getElementById('myModal'))
myModal.show()
```

---

### WOW.js Animations

**Add to any element:**

```html
<div class="wow fadeInUp" data-wow-delay=".3s">
    Animated content
</div>
```

**Available animations:**
- `fadeInUp`, `fadeInDown`, `fadeInLeft`, `fadeInRight`
- `fadeIn`, `fadeOut`
- `slideInUp`, `slideInDown`
- `zoomIn`, `zoomOut`
- `bounceIn`, `bounceOut`

**Delay pattern:**
```html
<div class="wow fadeInUp" data-wow-delay=".3s">First</div>
<div class="wow fadeInUp" data-wow-delay=".5s">Second</div>
<div class="wow fadeInUp" data-wow-delay=".7s">Third</div>
```

---

### Adding Custom JavaScript

**Method 1: Inline in template**

```django
{% block extra_js %}
<script>
$(document).ready(function() {
    // Your custom code
    console.log('Page loaded!');
});
</script>
{% endblock %}
```

**Method 2: External file**

**Create:** `static/js/custom.js`

```javascript
// Custom JavaScript for Far Out Corporation

$(document).ready(function() {
    // Your code here
});
```

**Include in base.html:**

```django
<!-- After main.js -->
<script src="{% static 'js/custom.js' %}"></script>
```

---

### Counter Animation Example

**From homepage:**

```html
<div class="counter-item">
    <h2><span class="count">150</span>+</h2>
    <p>Active Members</p>
</div>

<script>
$('.count').each(function () {
    $(this).prop('Counter', 0).animate({
        Counter: $(this).text()
    }, {
        duration: 2000,
        easing: 'swing',
        step: function (now) {
            $(this).text(Math.ceil(now));
        }
    });
});
</script>
```

---

### Swiper Slider Example

```html
<div class="swiper mySwiper">
    <div class="swiper-wrapper">
        <div class="swiper-slide">
            <!-- Slide content -->
        </div>
        <div class="swiper-slide">
            <!-- Slide content -->
        </div>
    </div>
    <!-- Add Pagination -->
    <div class="swiper-pagination"></div>
    <!-- Add Navigation -->
    <div class="swiper-button-next"></div>
    <div class="swiper-button-prev"></div>
</div>

<script>
var swiper = new Swiper(".mySwiper", {
    slidesPerView: 3,
    spaceBetween: 30,
    pagination: {
        el: ".swiper-pagination",
        clickable: true,
    },
    navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
    },
    breakpoints: {
        768: {
            slidesPerView: 2,
        },
        1024: {
            slidesPerView: 3,
        },
    },
});
</script>
```

---

## 🔧 Common Tasks Guide

### Task 1: Change Color Scheme

**1. Choose your colors:**
- Primary: `#YOUR_PRIMARY`
- Accent: `#YOUR_ACCENT`
- Background: `#YOUR_BG`

**2. Create custom.css:**

```css
/* static/css/custom.css */

/* Override primary color */
:root {
    --theme: #YOUR_PRIMARY;
    --theme2: #YOUR_ACCENT;
}

/* Override accent color (used in templates) */
.content-card h3,
.stat-card:hover,
.info-label i,
.stat-icon,
.service-icon,
.quick-link-icon {
    border-color: #YOUR_ACCENT !important;
    color: #YOUR_ACCENT !important;
}

/* Override backgrounds */
body {
    background: #YOUR_BG !important;
}

.content-card,
.stat-card,
.profile-card {
    background: linear-gradient(135deg, #YOUR_BG_START 0%, #YOUR_BG_END 100%) !important;
}
```

**3. Link in base.html after main.css**

---

### Task 2: Add a Modal Popup

**1. Add modal HTML to template:**

```html
<!-- Modal -->
<div class="modal fade" id="myModal" tabindex="-1" aria-labelledby="myModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content" style="background: #1a1a2e; border: 1px solid #333;">
            <div class="modal-header" style="border-bottom: 1px solid #333;">
                <h5 class="modal-title" id="myModalLabel" style="color: #fff;">Modal Title</h5>
                <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body" style="color: #ccc;">
                Modal content goes here...
            </div>
            <div class="modal-footer" style="border-top: 1px solid #333;">
                <button type="button" class="theme-btn" data-bs-dismiss="modal">Close</button>
            </div>
        </div>
    </div>
</div>
```

**2. Add trigger button:**

```html
<button type="button" class="theme-btn" data-bs-toggle="modal" data-bs-target="#myModal">
    Open Modal
</button>
```

---

### Task 3: Add a Carousel/Slider

**1. Add Swiper HTML:**

```html
<div class="swiper shipSlider">
    <div class="swiper-wrapper">
        {% for ship in ships %}
        <div class="swiper-slide">
            <div class="ship-card">
                <img src="{{ ship.image_url }}" alt="{{ ship.name }}">
                <h4>{{ ship.name }}</h4>
            </div>
        </div>
        {% endfor %}
    </div>
    <div class="swiper-pagination"></div>
</div>
```

**2. Initialize Swiper:**

```html
<script>
var shipSlider = new Swiper(".shipSlider", {
    slidesPerView: 1,
    spaceBetween: 30,
    loop: true,
    autoplay: {
        delay: 3000,
    },
    pagination: {
        el: ".swiper-pagination",
        clickable: true,
    },
    breakpoints: {
        768: {
            slidesPerView: 2,
        },
        1024: {
            slidesPerView: 3,
        },
    },
});
</script>
```

---

### Task 4: Add Search Functionality

**1. Add search form:**

```html
<form method="get" action="{% url 'your_search_url' %}">
    <div class="search-box">
        <input type="search"
               name="q"
               value="{{ request.GET.q }}"
               placeholder="Search..."
               class="form-control">
        <button type="submit" class="theme-btn">
            <i class="fas fa-search"></i>
        </button>
    </div>
</form>
```

**2. Handle in view:**

```python
def your_search_view(request):
    query = request.GET.get('q', '')
    if query:
        results = YourModel.objects.filter(name__icontains=query)
    else:
        results = YourModel.objects.all()

    return render(request, 'your_template.html', {'results': results, 'query': query})
```

---

### Task 5: Add Tooltips

**1. Add tooltip to element:**

```html
<button type="button"
        class="theme-btn"
        data-bs-toggle="tooltip"
        data-bs-placement="top"
        title="Tooltip text">
    Hover me
</button>
```

**2. Initialize tooltips:**

```html
<script>
$(document).ready(function(){
    $('[data-bs-toggle="tooltip"]').tooltip();
});
</script>
```

---

### Task 6: Add Loading Spinner

**1. Add spinner HTML:**

```html
<div id="loadingSpinner" class="loading-overlay" style="display: none;">
    <div class="spinner-border text-light" role="status">
        <span class="visually-hidden">Loading...</span>
    </div>
</div>

<style>
.loading-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.8);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 9999;
}
</style>
```

**2. Show/hide with JavaScript:**

```javascript
// Show spinner
$('#loadingSpinner').show();

// Hide spinner
$('#loadingSpinner').hide();

// Show during AJAX
$.ajax({
    url: '/your-endpoint/',
    beforeSend: function() {
        $('#loadingSpinner').show();
    },
    success: function(data) {
        // Handle success
    },
    complete: function() {
        $('#loadingSpinner').hide();
    }
});
```

---

## 🐛 Troubleshooting

### Styles Not Applying

**Problem:** CSS changes not visible

**Solutions:**
1. **Clear browser cache:** Ctrl+Shift+R (hard reload)
2. **Run collectstatic:**
   ```bash
   python manage.py collectstatic --noinput
   ```
3. **Check CSS file location:** Must be in `static/css/`
4. **Verify static tag:** `{% load static %}` at top of template
5. **Check for typos:** Class names are case-sensitive

---

### Images Not Loading

**Problem:** Images show broken icon

**Solutions:**
1. **Check file exists:** Verify path in `static/img/`
2. **Check file extension:** Must match exactly (case-sensitive on Linux)
3. **Run collectstatic:**
   ```bash
   python manage.py collectstatic --noinput
   ```
4. **Check template syntax:**
   ```django
   <!-- Correct -->
   <img src="{% static 'img/photo.jpg' %}" alt="Photo">

   <!-- Wrong -->
   <img src="static/img/photo.jpg" alt="Photo">
   ```
5. **Check STATIC_URL setting:** Should be `/static/` in settings

---

### JavaScript Not Working

**Problem:** JS functionality broken

**Solutions:**
1. **Check browser console:** F12 → Console tab for errors
2. **Verify jQuery loaded:** Check Network tab for jquery file
3. **Check load order:** jQuery must load before custom scripts
4. **Wrap in document.ready:**
   ```javascript
   $(document).ready(function() {
       // Your code here
   });
   ```
5. **Check for conflicts:** Comment out custom code to isolate issue

---

### Responsive Issues

**Problem:** Layout broken on mobile

**Solutions:**
1. **Check Bootstrap classes:** Ensure proper col-* classes
2. **Test at breakpoints:** 375px, 768px, 1024px, 1920px
3. **Check for fixed widths:** Remove any `width: 500px` styles
4. **Use responsive units:** `rem`, `%`, `vw` instead of `px`
5. **Check viewport meta:** Should be in base.html head

---

### Template Not Rendering

**Problem:** Template shows wrong content or error

**Solutions:**
1. **Check template name:** Must match exactly in view
2. **Check template location:** Must be in `templates/` directory
3. **Verify view imports template:** `render(request, 'your_template.html', context)`
4. **Check URL pattern:** Verify URL is mapped to correct view
5. **Check Django errors:** Read error message carefully

---

### Static Files 404 in Production

**Problem:** CSS/JS files return 404 in production

**Solutions:**
1. **Run collectstatic:**
   ```bash
   python manage.py collectstatic --noinput
   ```
2. **Check STATIC_ROOT:** Should be set in production settings
3. **Check web server config:** Nginx/Apache should serve static files
4. **Verify WhiteNoise:** Should be in MIDDLEWARE and STATICFILES_STORAGE
5. **Check permissions:** Static files directory must be readable

---

### Animations Not Working

**Problem:** WOW.js animations don't trigger

**Solutions:**
1. **Check WOW.js loaded:** Verify in Network tab
2. **Check initialization:** Should be in main.js
3. **Verify class names:** Must be exact: `wow fadeInUp`
4. **Check element visibility:** Must be below fold initially
5. **Test scroll:** Animations trigger on scroll into view

---

## 📚 Quick Reference

### Essential File Paths

```
Base Template:     templates/base.html
Homepage:          templates/home.html
Dashboard:         templates/dashboard.html
About:             templates/about.html
Contact:           templates/contact.html
Main CSS:          static/css/main.css
Main JS:           static/js/main.js
Logo:              static/img/logo/white-logo.svg
Favicon:           static/img/favicon.svg
```

### Common Django Template Tags

```django
{% load static %}                     # Load static files
{% static 'path/to/file' %}          # Static file URL
{% url 'url_name' %}                 # URL by name
{% url 'url_name' arg %}             # URL with argument
{% if condition %}...{% endif %}     # Conditional
{% for item in items %}...{% endfor %} # Loop
{{ variable }}                        # Output variable
{{ variable|filter }}                 # Apply filter
{% extends 'base.html' %}            # Template inheritance
{% block name %}...{% endblock %}    # Define block
{% include 'partial.html' %}         # Include template
{{ variable|safe }}                   # Render HTML
{{ text|truncatewords:20 }}          # Truncate text
```

### Bootstrap Grid Classes

```html
.container                    # Responsive container
.row                         # Row wrapper
.col-*                       # Column (auto width)
.col-{breakpoint}-{size}     # Responsive column
.g-{size}                    # Gap between columns
.d-{value}                   # Display utility
.d-{breakpoint}-{value}      # Responsive display
.text-{align}                # Text alignment
.mb-{size}                   # Margin bottom
.p-{size}                    # Padding
```

### Font Awesome Icons

```html
<i class="fas fa-{icon}"></i>     # Solid
<i class="far fa-{icon}"></i>     # Regular
<i class="fab fa-{icon}"></i>     # Brands
<i class="fas fa-{icon} fa-2x"></i> # Size
```

**Common icons:**
- `fa-users`, `fa-rocket`, `fa-ship`, `fa-star`
- `fa-envelope`, `fa-phone`, `fa-map-marker`
- `fa-search`, `fa-filter`, `fa-bars`, `fa-times`
- `fa-discord`, `fa-twitter`, `fa-youtube`, `fa-twitch`

---

## 🎯 Best Practices

### Design Consistency

1. **Use template inheritance:** All pages extend base.html
2. **Follow card pattern:** Use standard gradients and styling
3. **Consistent spacing:** Use Bootstrap spacing utilities
4. **Icon placement:** Icons before text in headings
5. **Animation delays:** Stagger by .2s (.3s, .5s, .7s, etc.)

### Performance

1. **Optimize images:** Compress before uploading
2. **Use SVG for icons:** Scalable and small file size
3. **Lazy load images:** For long pages with many images
4. **Minimize custom CSS:** Use Bootstrap utilities when possible
5. **Run collectstatic:** Before deployment

### Accessibility

1. **Alt text for images:** Always include descriptive alt text
2. **Aria labels:** For icon-only buttons
3. **Color contrast:** Ensure text is readable
4. **Keyboard navigation:** Test tab navigation
5. **Semantic HTML:** Use proper heading hierarchy

### Mobile-First

1. **Test on mobile first:** Start with 375px viewport
2. **Use responsive units:** rem, %, vw instead of px
3. **Touch targets:** Minimum 44px for buttons
4. **Readable text:** Minimum 16px font size
5. **Stack on mobile:** Use appropriate col-12 classes

---

## 📖 Resources

### Documentation
- **Django Templates:** https://docs.djangoproject.com/en/5.1/topics/templates/
- **Bootstrap 5:** https://getbootstrap.com/docs/5.0/
- **Font Awesome:** https://fontawesome.com/v5/search
- **Swiper:** https://swiperjs.com/
- **WOW.js:** https://wowjs.uk/

### Tools
- **Color Picker:** https://htmlcolorcodes.com/
- **Gradient Generator:** https://cssgradient.io/
- **SVG Editor:** https://www.figma.com/ or Inkscape
- **Image Compression:** https://tinypng.com/
- **Google Fonts:** https://fonts.google.com/

---

**Document Version:** 1.0
**Last Updated:** November 12, 2025
**Maintained By:** Far Out Corporation Development Team

---

*This guide covers all design and frontend aspects of the Far Out Django application. For backend features and functionality, see FEATURES_AUDIT.md*
