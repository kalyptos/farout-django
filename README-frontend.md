# Frontend Architecture Guide

## Overview

This guide documents the frontend architecture and theming system for the Far Out Corporation Django application. The frontend is built on the **Agznko** dark sci-fi gaming template, enhanced with a design token system, reusable component architecture, and accessibility improvements.

---

## Table of Contents

1. [Design System](#design-system)
2. [File Structure](#file-structure)
3. [Using Design Tokens](#using-design-tokens)
4. [Template Partials](#template-partials)
5. [Component Classes](#component-classes)
6. [Adding a New Page](#adding-a-new-page)
7. [Performance Optimization](#performance-optimization)
8. [Accessibility Features](#accessibility-features)
9. [Customization Guide](#customization-guide)

---

## Design System

The application uses a centralized design token system defined in `/static/css/tokens.css`. This provides consistent colors, spacing, typography, and other design values across the entire application.

### Key Design Tokens

```css
/* Brand Colors */
--color-accent: #55E6A5;        /* Teal - primary accent */
--color-accent-2: #BFF747;      /* Lime green - theme button */
--color-accent-3: #FFD531;      /* Yellow - tertiary */

/* Backgrounds */
--bg-body: #121212;             /* Main body background */
--bg-card-gradient: linear-gradient(135deg, #1a1a2e 0%, #2d2d44 100%);

/* Spacing Scale */
--space-1: 0.5rem;    /* 8px */
--space-2: 1rem;      /* 16px */
--space-3: 1.5rem;    /* 24px */
--space-4: 2rem;      /* 32px */
--space-5: 2.5rem;    /* 40px */
--space-6: 3rem;      /* 48px */

/* Border Radius */
--radius: 10px;       /* Standard radius */
--radius-sm: 5px;     /* Small radius */
--radius-md: 8px;     /* Medium radius */
--radius-pill: 120px; /* Pill-shaped buttons */
```

---

## File Structure

```
/static/
├── css/
│   ├── tokens.css         # Design tokens (load FIRST)
│   ├── bootstrap.min.css  # Bootstrap 5 framework
│   ├── all.min.css        # Font Awesome icons
│   ├── animate.css        # WOW.js animations
│   ├── swiper-bundle.min.css
│   ├── main.css           # Agznko theme styles
│   └── custom.css         # Project-specific components
├── js/
│   ├── jquery-3.7.1.min.js      # jQuery (load FIRST)
│   ├── bootstrap.bundle.min.js   # Bootstrap JS (requires jQuery)
│   ├── swiper-bundle.min.js     # Swiper carousel (defer)
│   ├── main.js                  # Agznko theme scripts (defer)
│   └── custom.js                # Project-specific JS (defer)
└── img/
    ├── logo/
    ├── ranks/
    └── ...

/templates/
├── base.html              # Base template with partials
├── _partials/             # Reusable template components
│   ├── _nav.html         # Navigation with active link highlighting
│   ├── _footer.html      # Footer
│   ├── _messages.html    # Django messages display
│   ├── _breadcrumbs.html # Breadcrumb navigation
│   ├── _pagination.html  # Pagination controls
│   └── _card.html        # Generic card component
├── home.html
├── about.html
├── contact.html
├── dashboard.html
├── starships/
│   ├── ship_list.html
│   └── ship_detail.html
└── organization/
    ├── member_list.html
    └── member_detail.html

/apps/core/templatetags/
└── nav.py                # Custom template tags for navigation
```

---

## Using Design Tokens

### Changing Brand Colors

To change the primary accent color across the entire site, edit `/static/css/tokens.css`:

```css
:root {
    --color-accent: #55E6A5;  /* Change this to your desired color */
}
```

This will update:
- All accent borders
- Icon colors
- Hover states
- Focus rings
- And more...

### Using Tokens in Custom CSS

Always reference tokens instead of hardcoding values:

```css
/* ✅ GOOD - Uses design tokens */
.my-component {
    background: var(--bg-card-gradient);
    padding: var(--card-padding);
    border-radius: var(--radius);
    color: var(--text-primary);
}

/* ❌ BAD - Hardcoded values */
.my-component {
    background: linear-gradient(135deg, #1a1a2e 0%, #2d2d44 100%);
    padding: 30px;
    border-radius: 10px;
    color: #fff;
}
```

---

## Template Partials

Partials are reusable template fragments stored in `/templates/_partials/`. They help maintain DRY (Don't Repeat Yourself) principles.

### Available Partials

#### 1. Navigation (`_nav.html`)

Automatically loaded in `base.html`. Features active link highlighting.

```django
{% include '_partials/_nav.html' %}
```

**Active Link Highlighting:**
The nav uses custom template tags to highlight the current page:

```django
{% load nav %}

<li class="{% active 'home' %}">
    <a href="{% url 'home' %}">Home</a>
</li>

<li class="{% active_parent 'starships:ship_list' 'starships:ship_detail' %}">
    <a href="{% url 'starships:ship_list' %}">Ships</a>
</li>
```

#### 2. Footer (`_footer.html`)

Automatically loaded in `base.html`.

```django
{% include '_partials/_footer.html' %}
```

#### 3. Django Messages (`_messages.html`)

Displays Django messages (success, error, warning, info).

```django
{% include '_partials/_messages.html' %}
```

#### 4. Breadcrumbs (`_breadcrumbs.html`)

**Basic usage (single level):**
```django
{% include '_partials/_breadcrumbs.html' with title="Ship Catalog" current="Ships" %}
```

**With parent link:**
```django
{% include '_partials/_breadcrumbs.html' with
    title="Member Profile"
    parent="Members"
    parent_url="organization:member_list"
    current=member.handle
%}
```

#### 5. Pagination (`_pagination.html`)

Automatically handles Django pagination with accessibility features.

```django
{% if is_paginated %}
    {% include '_partials/_pagination.html' %}
{% endif %}
```

**Required context variables:**
- `page_obj` - Django pagination object
- `is_paginated` - Boolean

#### 6. Card Component (`_card.html`)

Generic animated card with optional icon.

```django
{% include '_partials/_card.html' with
    title="Card Title"
    icon="fas fa-rocket"
    delay=".3s"
    body="<p>Card content goes here</p>"
%}
```

**Parameters:**
- `title` (required) - Card heading
- `icon` (optional) - Font Awesome icon class
- `delay` (optional) - WOW.js animation delay (default: ".3s")
- `body` (required) - HTML content for card body

---

## Component Classes

Custom component classes are defined in `/static/css/custom.css`. All use the `.fo-` prefix (Far Out) to avoid conflicts.

### Card Components

```html
<!-- Standard Card -->
<div class="fo-card">
    <h3 class="fo-card__title">
        <i class="fas fa-rocket"></i> Card Title
    </h3>
    <div class="fo-card__body">
        <p>Card content...</p>
    </div>
</div>

<!-- Stat Card -->
<div class="fo-stat">
    <div class="fo-stat__icon">
        <i class="fas fa-users"></i>
    </div>
    <h3 class="fo-stat__h">150+</h3>
    <p class="fo-stat__p">Active Members</p>
</div>

<!-- Profile/Info Card -->
<div class="fo-profile">
    <div class="fo-info-item">
        <span class="fo-info-label">
            <i class="fas fa-user"></i> Name
        </span>
        <span class="fo-info-value">John Doe</span>
    </div>
</div>
```

### Form Components

```html
<label class="fo-label">
    <i class="fas fa-envelope"></i> Email Address
</label>
<input type="email" class="form-control fo-field" placeholder="your@email.com">
```

### Service/Feature Boxes

```html
<div class="fo-service">
    <div class="fo-service__icon">
        <i class="fas fa-rocket"></i>
    </div>
    <h5>Service Title</h5>
    <p>Service description...</p>
</div>
```

### Utility Classes

```html
<!-- Text Colors -->
<p class="text-accent">Primary accent color text</p>
<p class="text-accent-2">Secondary accent color text</p>
<p class="text-fade">Faded text with opacity</p>

<!-- Backgrounds -->
<div class="bg-card">Card gradient background</div>
<div class="bg-surface">Secondary surface background</div>

<!-- Borders -->
<div class="border-accent">Accent border color</div>

<!-- Spacing (Gap utilities) -->
<div class="d-flex gap-1">Small gap</div>
<div class="d-flex gap-2">Medium gap</div>
<div class="d-flex gap-3">Large gap</div>
```

---

## Adding a New Page

Follow this template to create a new page with standard layout:

```django
{% extends 'base.html' %}
{% load static %}

{% block title %}Page Title - Far Out Corporation{% endblock %}

{% block content %}
<!-- Breadcrumb Section -->
{% include '_partials/_breadcrumbs.html' with title="Page Title" current="Current" %}

<!-- Main Content Section -->
<section class="section-padding fix">
    <div class="container">
        <div class="row">
            <div class="col-12">
                <!-- Use fo-card for content blocks -->
                <div class="fo-card wow fadeInUp" data-wow-delay=".3s">
                    <h2 class="fo-card__title">
                        <i class="fas fa-icon-name"></i> Section Title
                    </h2>
                    <div class="fo-card__body">
                        <p>Your content here...</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>
{% endblock %}
```

### Best Practices for New Pages

1. **Use exactly one `<h1>` per page** (usually in breadcrumbs or hero section)
2. **Use `<h2>` for main sections**, `<h3>` for subsections, etc.
3. **Add WOW.js animations** with `class="wow fadeInUp"` and staggered delays
4. **Use design tokens** instead of hardcoded colors/spacing
5. **Include breadcrumbs** for navigation context
6. **Add ARIA labels** to interactive elements
7. **Use semantic HTML** (nav, main, section, article, etc.)

---

## Performance Optimization

### Asset Loading Strategy

The application uses an optimized loading strategy:

```html
<!-- In <head> -->
<!-- 1. Preconnect to external resources -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>

<!-- 2. Preload critical fonts -->
<link rel="preload" as="style" href="https://fonts.googleapis.com/...">

<!-- 3. CSS load order: tokens → vendor → theme → custom -->
<link rel="stylesheet" href="{% static 'css/tokens.css' %}">
<link rel="stylesheet" href="{% static 'css/bootstrap.min.css' %}">
<link rel="stylesheet" href="{% static 'css/main.css' %}">
<link rel="stylesheet" href="{% static 'css/custom.css' %}">

<!-- Before </body> -->
<!-- 4. Critical JS (no defer) -->
<script src="{% static 'js/jquery-3.7.1.min.js' %}"></script>
<script src="{% static 'js/bootstrap.bundle.min.js' %}"></script>

<!-- 5. Non-critical JS (deferred) -->
<script src="{% static 'js/swiper-bundle.min.js' %}" defer></script>
<script src="{% static 'js/main.js' %}" defer></script>
<script src="{% static 'js/custom.js' %}" defer></script>
```

### Image Optimization

Use lazy loading for images that are below the fold:

```html
<!-- Lazy loading with fallback placeholder -->
<img src="{{ image_url }}"
     alt="Descriptive alt text"
     loading="lazy"
     data-placeholder="{% static 'img/placeholder.jpg' %}">
```

The `custom.js` file automatically handles broken images and replaces them with placeholders.

---

## Accessibility Features

The application includes comprehensive accessibility improvements:

### Keyboard Navigation

- **Focus-visible styles** for all interactive elements (blue outline with offset)
- **Scroll-to-top button** supports Enter and Space keys
- **Skip to main content** link for screen readers (Tab on page load to reveal)
- All form inputs have associated `<label>` elements

### ARIA Labels

```html
<!-- Icon-only buttons MUST have aria-label -->
<button aria-label="Scroll to top" class="scroll-up">
    <i class="fas fa-arrow-up" aria-hidden="true"></i>
</button>

<!-- Links with context -->
<a href="..." aria-label="View details for Aurora MR">
    View Details
</a>

<!-- Pagination -->
<a href="?page=2" aria-label="Go to page 2">2</a>
<span aria-current="page">1</span>
```

### Image Alt Text

All images must have meaningful alt text:

```html
<!-- ✅ GOOD -->
<img src="logo.svg" alt="Far Out Corporation">
<img src="ship.jpg" alt="Anvil Carrack starship">

<!-- ❌ BAD -->
<img src="logo.svg" alt="logo">
<img src="ship.jpg" alt="">
```

Decorative images/icons should use `aria-hidden="true"`:

```html
<i class="fas fa-rocket" aria-hidden="true"></i>
<svg aria-hidden="true">...</svg>
```

### Reduced Motion Support

The site respects `prefers-reduced-motion` settings:

```css
@media (prefers-reduced-motion: reduce) {
    *,
    *::before,
    *::after {
        animation-duration: 0.01ms !important;
        transition-duration: 0.01ms !important;
        scroll-behavior: auto !important;
    }
}
```

---

## Customization Guide

### Changing the Color Scheme

Edit `/static/css/tokens.css`:

```css
:root {
    /* Change primary accent (teal) */
    --color-accent: #55E6A5;

    /* Change secondary accent (lime green) */
    --color-accent-2: #BFF747;

    /* Change background gradient colors */
    --bg-card-start: #1a1a2e;
    --bg-card-end: #2d2d44;
}
```

### Adjusting Spacing

Modify the spacing scale in `tokens.css`:

```css
:root {
    --space-1: 0.5rem;    /* Make smaller for tighter spacing */
    --space-2: 1rem;
    --space-3: 1.5rem;
    --space-4: 2rem;
    --space-5: 2.5rem;
    --space-6: 3rem;
}
```

### Adding New Component Styles

Add new components to `/static/css/custom.css`:

```css
/* ============================================================
   MY NEW COMPONENT
   ============================================================ */

.fo-my-component {
    background: var(--bg-card-gradient);
    padding: var(--card-padding);
    border-radius: var(--radius);
    border: 1px solid var(--border);
    transition: all var(--transition);
}

.fo-my-component:hover {
    border-color: var(--border-accent);
    transform: translateY(-5px);
}
```

### Changing Typography

Edit fonts in `tokens.css`:

```css
:root {
    --font-heading: "Teko", sans-serif;    /* Change heading font */
    --font-body: "Kanit", sans-serif;      /* Change body font */
    --font-size-base: 18px;                /* Adjust base size */
}
```

Don't forget to update the Google Fonts import in `base.html` if changing fonts.

---

## Troubleshooting

### Styles Not Applying

1. **Check CSS load order** - `tokens.css` must load before `custom.css`
2. **Hard refresh** - Ctrl+Shift+R (Windows/Linux) or Cmd+Shift+R (Mac)
3. **Run collectstatic** - `python manage.py collectstatic --noinput`
4. **Check browser console** for 404 errors on CSS files

### Active Navigation Not Highlighting

1. **Ensure nav.py is loaded** - `{% load nav %}` at top of template
2. **Check URL name** - Must match the name in `urls.py`
3. **Verify context processor** - Request must be in template context

### Animations Not Working

1. **Check WOW.js is loaded** - Look for `main.js` in page source
2. **Verify classes** - Must have both `wow` and animation class (e.g., `fadeInUp`)
3. **Check delays** - Use `data-wow-delay=".3s"` format

---

## Additional Resources

- **Bootstrap 5 Docs**: https://getbootstrap.com/docs/5.0/
- **Font Awesome Icons**: https://fontawesome.com/icons
- **WOW.js Animations**: https://wowjs.uk/
- **Django Templates**: https://docs.djangoproject.com/en/5.1/topics/templates/

---

## Version History

- **v1.0** (2025) - Initial frontend refactor with design tokens, partials, and accessibility improvements

---

**Questions or Issues?**
Contact the development team or open an issue in the project repository.
