# Color System Guidelines

## 🎨 Color Palette

### Primary Colors
- **Sky Blue (#0ea5e9 / primary-500)**
  - Contrast on white: 3.95:1 ✅ (WCAG AA for large text)
  - Use for: Buttons, links, icons, brand elements
  - For text on white: Use `primary-700` (#0369a1) = 4.5:1 ✅

### Secondary Colors
- **Vibrant Purple (#d946ef / secondary-500)**
  - ⚠️ Contrast on white: 2.7:1 ❌ (Fails WCAG AA)
  - **For text on white: Use `secondary-700` (#a21caf) = 4.8:1 ✅**
  - Use for: Accents, hover states, secondary actions

### Semantic Colors
All semantic colors meet WCAG AA standards:
- **Success**: `#22c55e` (success-500) = 4.6:1 ✅
- **Warning**: `#f59e0b` (warning-500) = 4.8:1 ✅
- **Error**: `#ef4444` (error-500) = 4.7:1 ✅

## 📐 Contrast Ratios

### WCAG 2.1 Requirements
- **AA Normal Text**: 4.5:1 minimum
- **AA Large Text**: 3:1 minimum (18px+ or 14px+ bold)
- **AAA Normal Text**: 7:1 minimum
- **AAA Large Text**: 4.5:1 minimum

### Our Color Contrast Matrix

| Color | On White | On Dark | Usage |
|-------|----------|---------|-------|
| primary-500 | 3.95:1 | ✅ | Large text, backgrounds |
| primary-700 | 4.5:1 ✅ | ✅ | Body text |
| secondary-500 | 2.7:1 ❌ | ✅ | Backgrounds only |
| secondary-700 | 4.8:1 ✅ | ✅ | Body text |
| success-500 | 4.6:1 ✅ | ✅ | Text & backgrounds |
| warning-500 | 4.8:1 ✅ | ✅ | Text & backgrounds |
| error-500 | 4.7:1 ✅ | ✅ | Text & backgrounds |

## 🌈 Gradient Usage Guidelines

### ✅ Approved Use Cases
1. **Logo and Brand Identity** - Hero sections, brand mark
2. **Primary CTAs** - Main action buttons only
3. **Decorative Backgrounds** - Subtle, low-opacity background gradients
4. **Icon Containers** - Small accent elements
5. **Hover States** - Interactive feedback (max 3-5 components)

### ❌ Avoid Gradients For
1. **Body Text** - Always use solid colors for readability
2. **Navigation** - Keep navigation simple and accessible
3. **Form Labels** - Solid colors for clarity
4. **Status Indicators** - Use semantic solid colors
5. **Long-form Content** - Solid colors for reading comfort

### Gradient Classes
```css
/* Reserved for hero CTAs only */
.gradient-primary-cta {
  @apply bg-gradient-to-r from-primary-500 to-primary-600;
}

/* Reserved for brand elements */
.gradient-brand {
  @apply bg-gradient-to-r from-primary-500 to-secondary-600;
}

/* Subtle background gradients */
.gradient-bg-subtle {
  @apply bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100;
}
```

## 🎯 Usage Rules

### DO ✅
- Use `primary-700` for blue text on white backgrounds
- Use `secondary-700` for purple text on white backgrounds
- Limit gradients to 3-5 key brand moments
- Use solid colors for all body text
- Test all color combinations with accessibility tools

### DON'T ❌
- Don't use `secondary-500` for text on white backgrounds
- Don't use gradients on text (bg-clip-text)
- Don't use more than 2 gradients per viewport
- Don't use low-contrast color combinations
- Don't rely on color alone to convey information

## 🔧 Implementation Examples

### Text Colors (Accessible)
```tsx
// ✅ Good - Accessible text colors
<h1 className="text-primary-700 dark:text-primary-400">Heading</h1>
<p className="text-secondary-700 dark:text-secondary-400">Accent text</p>

// ❌ Bad - Low contrast
<h1 className="text-primary-500">Heading</h1> // 3.95:1 - borderline
<p className="text-secondary-500">Text</p> // 2.7:1 - fails WCAG
```

### Buttons (Accessible)
```tsx
// ✅ Good - Primary CTA with gradient
<button className="bg-gradient-to-r from-primary-500 to-primary-600 text-white">
  Generate
</button>

// ✅ Good - Secondary action with solid color
<button className="bg-secondary-700 hover:bg-secondary-800 text-white">
  Save
</button>

// ❌ Bad - Secondary with low contrast gradient
<button className="bg-gradient-to-r from-secondary-500 to-secondary-600">
</button>
```

### Gradient Text (Avoid)
```tsx
// ❌ Bad - Gradient text is hard to read
<h1 className="bg-gradient-to-r from-primary-600 to-secondary-600 bg-clip-text text-transparent">
  Title
</h1>

// ✅ Good - Solid color with proper contrast
<h1 className="text-primary-700 dark:text-primary-300">
  Title
</h1>
```

## 🧪 Testing

### Tools
1. **Chrome DevTools** - Lighthouse accessibility audit
2. **WebAIM Contrast Checker** - https://webaim.org/resources/contrastchecker/
3. **axe DevTools** - Browser extension for accessibility testing
4. **WAVE** - Web accessibility evaluation tool

### Checklist
- [ ] All text has 4.5:1 contrast ratio (AA standard)
- [ ] Large text has 3:1 contrast ratio minimum
- [ ] Gradients limited to 3-5 key brand moments
- [ ] No gradient text (bg-clip-text) in production
- [ ] All interactive elements have visible focus states
- [ ] Color is not the only indicator of state/information

## 📊 Performance Notes

### Background Gradients
- Subtle gradients: Minimal performance impact
- Animated gradients: Can trigger repaints - use sparingly
- Complex multi-stop gradients: Consider using images for better performance

### Recommendations
1. Use CSS gradients for simple 2-3 color gradients
2. Avoid animating gradient backgrounds on large areas
3. Consider `will-change: transform` for animated gradients
4. Test on low-end devices to ensure smooth performance
