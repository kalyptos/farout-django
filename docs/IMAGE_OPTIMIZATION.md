# Image Optimization Guide

## Overview

This document explains how to create and use optimized images (AVIF/WebP) for the Far Out Corporation website to improve performance and reduce bandwidth usage.

## Benefits

- **AVIF**: 50% smaller than WebP, 20% smaller than JPG (newest format)
- **WebP**: 30% smaller than JPG, wider browser support than AVIF
- **JPG**: Fallback for legacy browsers
- **Progressive enhancement**: Browsers automatically use the best format they support

## Creating Optimized Images

### Using ImageMagick/GraphicsMagick (CLI)

```bash
# Convert JPG to WebP
magick convert hero-sc.jpg -quality 85 hero-sc.webp

# Convert JPG to AVIF
magick convert hero-sc.jpg -quality 75 hero-sc.avif

# Batch convert all JPGs in a directory
for file in *.jpg; do
    magick convert "$file" -quality 85 "${file%.jpg}.webp"
    magick convert "$file" -quality 75 "${file%.jpg}.avif"
done
```

### Using cwebp and avifenc (Dedicated Tools)

```bash
# Install tools
## macOS
brew install webp libavif

## Ubuntu/Debian
apt-get install webp libavif-bin

# Convert to WebP
cwebp -q 85 hero-sc.jpg -o hero-sc.webp

# Convert to AVIF
avifenc -s 2 -q 75 hero-sc.jpg hero-sc.avif
```

### Using Online Tools

- **Squoosh**: https://squoosh.app/ (Google's image optimizer)
- **CloudConvert**: https://cloudconvert.com/jpg-to-avif
- **TinyPNG**: https://tinypng.com/ (supports WebP)

## Directory Structure

```
/static/img/
├── hero-sc.jpg       # Original/fallback (must exist)
├── hero-sc.webp      # WebP version (optional but recommended)
├── hero-sc.avif      # AVIF version (optional, best compression)
├── placeholder-ship.jpg
├── placeholder-ship.webp
└── placeholder-ship.avif
```

## Usage in Templates

### Hero Images (LCP Optimization)

```django
<picture>
    <source srcset="{% static 'img/hero-sc.avif' %}" type="image/avif">
    <source srcset="{% static 'img/hero-sc.webp' %}" type="image/webp">
    <img src="{% static 'img/hero-sc.jpg' %}"
         alt="Descriptive alt text"
         width="1920"
         height="1080"
         fetchpriority="high"
         decoding="async">
</picture>
```

### Regular Images (Lazy Loading)

```django
<picture>
    <source srcset="{% static 'img/ship.avif' %}" type="image/avif">
    <source srcset="{% static 'img/ship.webp' %}" type="image/webp">
    <img src="{% static 'img/ship.jpg' %}"
         alt="Descriptive alt text"
         loading="lazy"
         decoding="async"
         data-placeholder="{% static 'img/placeholder-ship.jpg' %}">
</picture>
```

### With Responsive Sizes

```django
<picture>
    <source
        type="image/avif"
        srcset="{% static 'img/ship-640.avif' %} 640w,
                {% static 'img/ship-960.avif' %} 960w,
                {% static 'img/ship-1280.avif' %} 1280w"
        sizes="(min-width: 992px) 33vw, (min-width: 768px) 50vw, 100vw">
    <source
        type="image/webp"
        srcset="{% static 'img/ship-640.webp' %} 640w,
                {% static 'img/ship-960.webp' %} 960w,
                {% static 'img/ship-1280.webp' %} 1280w"
        sizes="(min-width: 992px) 33vw, (min-width: 768px) 50vw, 100vw">
    <img
        src="{% static 'img/ship-960.jpg' %}"
        srcset="{% static 'img/ship-640.jpg' %} 640w,
                {% static 'img/ship-960.jpg' %} 960w,
                {% static 'img/ship-1280.jpg' %} 1280w"
        sizes="(min-width: 992px) 33vw, (min-width: 768px) 50vw, 100vw"
        alt="Ship name"
        loading="lazy"
        decoding="async">
</picture>
```

## Attributes Explained

### `fetchpriority`

- `high`: Download ASAP (use for LCP images like hero)
- `low`: Defer download
- `auto`: Browser decides (default)

### `loading`

- `lazy`: Load when near viewport (use for below-fold images)
- `eager`: Load immediately (default, use for above-fold)

### `decoding`

- `async`: Decode in parallel, don't block rendering (recommended)
- `sync`: Decode before rendering (use for critical UI)
- `auto`: Browser decides (default)

### `width` and `height`

Always specify to prevent Cumulative Layout Shift (CLS):

```html
<img src="hero.jpg" width="1920" height="1080" alt="Hero" style="width: 100%; height: auto;">
```

The `style` makes it responsive while the attributes prevent layout shift.

## Browser Support

| Format | Chrome | Firefox | Safari | Edge |
|--------|--------|---------|--------|------|
| AVIF   | 85+    | 93+     | 16.4+  | 85+  |
| WebP   | 23+    | 65+     | 14+    | 18+  |
| JPG    | All    | All     | All    | All  |

The `<picture>` element provides automatic fallback to the next supported format.

## Quality Settings Recommendations

### AVIF
- Photos: `-q 65-75`
- Graphics: `-q 75-85`
- Icons: `-q 85-95`

### WebP
- Photos: `-q 75-85`
- Graphics: `-q 85-90`
- Icons: `-q 90-95`

## Automation

### Django Management Command (Future Enhancement)

Create a management command to automate conversion:

```python
# apps/core/management/commands/optimize_images.py
from django.core.management.base import BaseCommand
import subprocess
from pathlib import Path

class Command(BaseCommand):
    help = 'Convert static images to AVIF and WebP'

    def handle(self, *args, **options):
        img_dir = Path('static/img')
        for jpg in img_dir.glob('**/*.jpg'):
            webp = jpg.with_suffix('.webp')
            avif = jpg.with_suffix('.avif')

            if not webp.exists():
                subprocess.run(['cwebp', '-q', '85', str(jpg), '-o', str(webp)])
                self.stdout.write(f'Created {webp}')

            if not avif.exists():
                subprocess.run(['avifenc', '-s', '2', '-q', '75', str(jpg), str(avif)])
                self.stdout.write(f'Created {avif}')
```

Usage:
```bash
python manage.py optimize_images
```

### Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

# Find staged JPG/PNG images
for file in $(git diff --cached --name-only --diff-filter=ACM | grep -E '\.(jpg|jpeg|png)$'); do
    if [ -f "$file" ]; then
        # Generate WebP if it doesn't exist
        webp="${file%.*}.webp"
        if [ ! -f "$webp" ]; then
            cwebp -q 85 "$file" -o "$webp"
            git add "$webp"
        fi

        # Generate AVIF if it doesn't exist
        avif="${file%.*}.avif"
        if [ ! -f "$avif" ]; then
            avifenc -s 2 -q 75 "$file" "$avif"
            git add "$avif"
        fi
    fi
done
```

## Testing

### Visual Comparison

Use Squoosh.app to compare quality and file sizes side-by-side.

### Network Performance

Use Chrome DevTools Network tab to verify:
- Correct format served (AVIF → WebP → JPG)
- Reduced file sizes
- Proper caching headers

### Lighthouse Audit

Run Lighthouse to verify:
- Improved LCP score
- Reduced "Serve images in next-gen formats" warnings
- No CLS issues from missing width/height

## Current Status

### Converted Images

- `hero-sc.jpg` → `hero-sc.webp`, `hero-sc.avif` ⚠️ **TODO: Create these files**
- `placeholder-ship.jpg` → Need WebP/AVIF versions

### Templates Using `<picture>`

- ✅ `templates/home.html` - Hero image
- ⏳ Other hero sections (about, contact) - TODO

### Templates Using `loading="lazy"`

- ✅ `templates/starships/ship_detail.html`
- ✅ `templates/organization/member_list.html`

## Checklist for New Images

When adding a new image:

- [ ] Compress original JPG (TinyJPG, ImageOptim)
- [ ] Create WebP version (`cwebp -q 85`)
- [ ] Create AVIF version (`avifenc -q 75`)
- [ ] Use `<picture>` element in template
- [ ] Add proper `alt` text
- [ ] Include `width` and `height` attributes
- [ ] Use `fetchpriority="high"` for LCP images
- [ ] Use `loading="lazy"` for below-fold images
- [ ] Add `decoding="async"` for all images
- [ ] Test in multiple browsers

## Resources

- [web.dev - Use WebP images](https://web.dev/serve-images-webp/)
- [web.dev - Use AVIF images](https://web.dev/compress-images-avif/)
- [MDN - Responsive Images](https://developer.mozilla.org/en-US/docs/Learn/HTML/Multimedia_and_embedding/Responsive_images)
- [AVIF vs WebP comparison](https://avif.io/blog/comparisons/avif-vs-webp/)

---

**Last Updated**: 2025
**Maintained by**: Far Out Corporation Development Team
