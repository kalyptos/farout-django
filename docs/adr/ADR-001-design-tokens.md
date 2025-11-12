# ADR-001: Design Token System

**Status**: Accepted
**Date**: 2025-01-12
**Deciders**: Development Team
**Technical Story**: Frontend 2025 Refactoring - Phase 1

## Context and Problem Statement

The Far Out Corporation Django application uses the Agznko dark sci-fi gaming template, which has numerous hardcoded colors, spacing values, and design constants scattered throughout CSS files and inline styles. This creates several problems:

1. **Inconsistency**: Same colors/values duplicated with slight variations
2. **Maintainability**: Changing brand colors requires finding/replacing across many files
3. **Developer Experience**: New developers don't know which values to use
4. **Theme Switching**: Implementing alternate themes (light mode) would require extensive changes
5. **Design Drift**: Easy for UI to diverge from design system over time

We needed a centralized, maintainable way to manage design values while preserving the existing Agznko dark theme aesthetic.

## Decision Drivers

* Must maintain pixel-perfect visual parity with current design
* Must work with existing Bootstrap 5 and Agznko theme CSS
* Must be easy for developers to use and discover
* Must support future theming capabilities (light/dark modes)
* Must follow modern CSS standards (CSS Custom Properties)
* Must reduce CSS duplication and hardcoded values

## Considered Options

1. **CSS Custom Properties (CSS Variables)** - Modern, browser-native solution
2. **Sass Variables** - Requires build step, compile-time only
3. **CSS-in-JS** - Would require major refactoring, overkill for Django templates
4. **Design Tokens with Style Dictionary** - Over-engineered for this project size

## Decision Outcome

Chosen option: **CSS Custom Properties in `/static/css/tokens.css`**

### Rationale

CSS Custom Properties (CSS Variables) provide the best balance of:
- **Browser support**: Supported in all modern browsers (95%+ global usage)
- **No build step**: Works directly in browser, no compilation needed
- **Runtime flexibility**: Can be changed via JavaScript if needed
- **Scoped theming**: Can create theme variants by overriding at :root or component level
- **Developer ergonomics**: Autocomplete in modern IDEs, clear naming conventions
- **Performance**: Negligible performance impact, resolved at render time

### Token Categories Implemented

```css
:root {
    /* Brand Colors */
    --color-accent: #55E6A5;        /* Primary teal */
    --color-accent-2: #BFF747;      /* Secondary lime */
    --color-accent-3: #FFD531;      /* Tertiary yellow */

    /* Surface & Backgrounds */
    --bg-body: #121212;
    --bg-card-gradient: linear-gradient(135deg, #1a1a2e 0%, #2d2d44 100%);

    /* Text */
    --text-primary: #fff;
    --text-body: #ccc;
    --text-muted: #aaa;

    /* Borders */
    --border: #333;
    --border-accent: var(--color-accent);

    /* Spacing Scale (0.5rem increments) */
    --space-1: 0.5rem;   /* 8px */
    --space-2: 1rem;     /* 16px */
    --space-3: 1.5rem;   /* 24px */
    --space-4: 2rem;     /* 32px */
    --space-5: 2.5rem;   /* 40px */
    --space-6: 3rem;     /* 48px */

    /* Border Radius */
    --radius: 10px;
    --radius-sm: 5px;
    --radius-pill: 120px;

    /* Transitions */
    --transition: 0.3s ease;
    --transition-fast: 0.2s ease;

    /* Component-Specific */
    --card-padding: 30px;
    --input-bg: rgba(255, 255, 255, 0.05);
    --focus-ring: 0 0 0 0.2rem rgba(85, 230, 165, 0.25);
}
```

### Naming Conventions

- **Semantic names** over descriptive: `--color-accent` not `--color-teal`
- **Purpose-based** grouping: backgrounds, text, borders, spacing
- **Component tokens** reference base tokens: `--border-accent: var(--color-accent)`
- **Kebab-case** for consistency: `--bg-card-start` not `--bgCardStart`

### Usage Patterns

```css
/* ✅ GOOD - Use tokens */
.my-component {
    background: var(--bg-card-gradient);
    color: var(--text-primary);
    padding: var(--space-4);
    border-radius: var(--radius);
    transition: all var(--transition);
}

.my-component:focus {
    box-shadow: var(--focus-ring);
}

/* ❌ BAD - Don't hardcode values */
.my-component {
    background: linear-gradient(135deg, #1a1a2e 0%, #2d2d44 100%);
    color: #fff;
    padding: 32px;
    border-radius: 10px;
}
```

### Load Order

Tokens must load **first** before any other CSS:

```html
<link rel="stylesheet" href="/static/css/tokens.css">       <!-- 1. FIRST -->
<link rel="stylesheet" href="/static/css/bootstrap.min.css"> <!-- 2. Vendor -->
<link rel="stylesheet" href="/static/css/main.css">          <!-- 3. Theme -->
<link rel="stylesheet" href="/static/css/custom.css">        <!-- 4. Project -->
```

## Positive Consequences

* ✅ **Single Source of Truth**: Change brand color in one place, updates everywhere
* ✅ **No Inline Styles**: All inline `<style>` blocks removed, use tokens instead
* ✅ **Future-Proof Theming**: Can add dark/light modes by swapping token values
* ✅ **Reduced CSS Size**: Eliminated ~400 lines of duplicate color/spacing definitions
* ✅ **Developer Velocity**: New components use existing tokens, faster development
* ✅ **Design Consistency**: Enforces use of approved colors/spacing from design system

## Negative Consequences

* ⚠️ **Browser Compatibility**: IE11 not supported (acceptable for 2025 project)
* ⚠️ **Learning Curve**: Team must learn token names (mitigated with good docs)
* ⚠️ **Fallback Strategy**: No fallbacks for ancient browsers (design choice)

## Validation

- [x] All hardcoded colors replaced with tokens in `custom.css`
- [x] All inline styles removed from templates
- [x] Visual parity maintained (screenshots compared)
- [x] Lighthouse performance score unchanged
- [x] Token usage documented in README-frontend.md

## Future Enhancements

1. **Theme Switching**: Add data-theme attribute to switch token sets
2. **Reduced Motion Tokens**: Add `--duration-none` for accessibility
3. **Responsive Tokens**: Add breakpoint-specific spacing scales
4. **Color Modes**: Auto dark/light based on `prefers-color-scheme`

## References

- [MDN: Using CSS Custom Properties](https://developer.mozilla.org/en-US/docs/Web/CSS/Using_CSS_custom_properties)
- [Design Tokens Community Group](https://www.w3.org/community/design-tokens/)
- [tokens.css source](/static/css/tokens.css)
- [README-frontend.md - Token Usage](/README-frontend.md#using-design-tokens)

## Related ADRs

- ADR-002: Responsive Images Policy
- ADR-003: Template Fragment Caching Strategy
