# Color System Quick Reference Card

## 🎨 Text Colors (Always Use These)

```tsx
// ✅ PRIMARY TEXT (Blue)
<h1 className="text-primary-700 dark:text-primary-300">Heading</h1>
// Contrast: 4.5:1 on white ✅

// ✅ ACCENT TEXT (Purple)
<p className="text-secondary-700 dark:text-secondary-400">Accent text</p>
// Contrast: 4.8:1 on white ✅

// ✅ BODY TEXT (Gray)
<p className="text-gray-900 dark:text-gray-100">Body text</p>
// Contrast: 21:1 on white ✅
```

## 🚫 Never Use These for Text

```tsx
// ❌ BANNED - Low contrast (2.7:1)
<p className="text-secondary-500">Text</p>

// ❌ BANNED - Gradient text (unreadable)
<h1 className="gradient-text-primary">Heading</h1>
<h1 className="bg-gradient-to-r ... bg-clip-text text-transparent">Heading</h1>
```

## 🌈 Gradient Utilities (Use Sparingly)

```tsx
// ✅ LOGO ICON (Brand identity)
<div className="gradient-brand">
  <BoltIcon />
</div>

// ✅ PRIMARY CTA (Main action button only)
<Button className="gradient-primary-cta">
  Generate Topics
</Button>

// ✅ PAGE BACKGROUND (Subtle only)
<div className="gradient-bg-subtle">
  {/* Page content */}
</div>

// ✅ DECORATIVE ELEMENT (Low opacity)
<div className="gradient-bg-accent">
  {/* Accent element */}
</div>
```

## 📏 Gradient Limits

**Per Page Maximum**: 3-5 gradients
- 1 logo/brand icon
- 1-2 primary CTAs
- 1 page background
- 1-2 decorative accents

## 🎯 Semantic Colors

```tsx
// SUCCESS
<span className="text-success-600 dark:text-success-400">Success</span>
<div className="bg-success-100 dark:bg-success-900/20">...</div>

// WARNING
<span className="text-warning-600 dark:text-warning-400">Warning</span>
<div className="bg-warning-100 dark:bg-warning-900/20">...</div>

// ERROR
<span className="text-error-600 dark:text-error-400">Error</span>
<div className="bg-error-100 dark:bg-error-900/20">...</div>
```

## ⚡ Quick Checklist

- [ ] Using `text-primary-700` (not `text-primary-500`) for blue text?
- [ ] Using `text-secondary-700` (not `text-secondary-500`) for purple text?
- [ ] No gradient text (bg-clip-text)?
- [ ] Gradients limited to 3-5 per page?
- [ ] Using utility classes (not inline gradients)?
- [ ] Dark mode colors included?

## 📚 Full Documentation

- **Complete Guide**: `src/design-system/COLOR_GUIDELINES.md`
- **Testing**: `/ACCESSIBILITY_TEST_GUIDE.md`
- **Implementation**: `/COLOR_PALETTE_FIX_SUMMARY.md`
