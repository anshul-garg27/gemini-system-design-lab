# Accessibility Testing Guide

## 🎯 Color Palette Accessibility Verification

This guide helps verify that all color contrast fixes meet WCAG 2.1 AA standards.

## 🔍 Manual Testing Checklist

### 1. Visual Inspection
- [ ] All headings use solid colors (no gradient text)
- [ ] All body text has sufficient contrast
- [ ] No `text-secondary-500` on white backgrounds
- [ ] Gradients limited to 3-5 brand elements per page
- [ ] Dark mode colors have sufficient contrast

### 2. Text Contrast Testing

#### Tools Needed
- **WebAIM Contrast Checker**: https://webaim.org/resources/contrastchecker/
- **Chrome DevTools**: Built-in accessibility audit
- **axe DevTools**: Browser extension

#### Test Cases

**Primary Text Colors:**
```
Test 1: Primary Text on White
- Foreground: #0369a1 (primary-700)
- Background: #FFFFFF (white)
- Expected: 4.5:1 ✅
- Status: PASS

Test 2: Primary Text on Dark
- Foreground: #7dd3fc (primary-300)
- Background: #0f172a (slate-900)
- Expected: 7:1+ ✅
- Status: PASS
```

**Secondary Text Colors:**
```
Test 3: Secondary Text on White
- Foreground: #a21caf (secondary-700)
- Background: #FFFFFF (white)
- Expected: 4.8:1 ✅
- Status: PASS

Test 4: Secondary Text on Dark
- Foreground: #e879f9 (secondary-400)
- Background: #0f172a (slate-900)
- Expected: 7:1+ ✅
- Status: PASS
```

**Deprecated (Should NOT be found):**
```
❌ Test 5: Secondary-500 on White (SHOULD FAIL)
- Foreground: #d946ef (secondary-500)
- Background: #FFFFFF (white)
- Expected: 2.7:1 ❌
- Status: SHOULD NOT EXIST IN CODEBASE
```

### 3. Gradient Usage Audit

#### Approved Gradients (Should be limited)

**Count per page:**
- Dashboard: Max 3-5 gradients
- Topics: Max 3-5 gradients
- Content Generator: Max 3-5 gradients
- Navigation: 1 gradient (logo only)

**Approved locations:**
```
✅ Logo icon: .gradient-brand
✅ Primary CTA button: .gradient-primary-cta
✅ Active navigation item: .gradient-brand
✅ Loading spinner: .gradient-brand
✅ Page backgrounds: .gradient-bg-subtle
```

**Forbidden locations:**
```
❌ Text (bg-clip-text)
❌ Body copy
❌ Form labels
❌ Navigation text
❌ Status indicators
```

## 🧪 Automated Testing

### 1. Chrome Lighthouse Audit

```bash
# Build the project
cd frontend
npm run build

# Serve the build
npm run preview

# Run Lighthouse (in another terminal)
npx lighthouse http://localhost:4173 \
  --only-categories=accessibility \
  --output=html \
  --output-path=./accessibility-report.html

# Open the report
open accessibility-report.html
```

**Expected Results:**
- Accessibility Score: 90+ ✅
- Contrast Issues: 0 ✅
- Color-related warnings: 0 ✅

### 2. axe DevTools

```bash
# Install axe DevTools browser extension
# Chrome: https://chrome.google.com/webstore/detail/axe-devtools/lhdoppojpmngadmnindnejefpokejbdd
# Firefox: https://addons.mozilla.org/en-US/firefox/addon/axe-devtools/

# Steps:
1. Open the application in browser
2. Open DevTools (F12)
3. Go to "axe DevTools" tab
4. Click "Scan ALL of my page"
5. Review results

# Expected:
- Color contrast issues: 0 ✅
- Critical issues: 0 ✅
```

### 3. WAVE Evaluation Tool

```bash
# Online: https://wave.webaim.org/
# Or install browser extension

# Steps:
1. Navigate to the application page
2. Click WAVE extension icon
3. Review errors and contrast issues

# Expected:
- Contrast errors: 0 ✅
- All alerts addressed ✅
```

## 📋 Component-Specific Tests

### Dashboard Component

**Test headings:**
```tsx
// ✅ Should find:
<h1 className="text-primary-700 dark:text-primary-300">
  System Design Topic Generator
</h1>

// ❌ Should NOT find:
<h1 className="gradient-text-primary">...</h1>
<h1 className="bg-gradient-to-r ... bg-clip-text text-transparent">...</h1>
```

**Test buttons:**
```tsx
// ✅ Should find:
<Button className="gradient-primary-cta">
  Generate Topics
</Button>

// ❌ Should NOT find (excessive inline gradients):
<Button className="bg-gradient-to-r from-primary-500 to-secondary-500">
```

### Layout Component

**Test navigation:**
```tsx
// ✅ Should find:
<h1 className="text-primary-700 dark:text-primary-300">
  System Design Generator
</h1>

// ✅ Should find:
<div className="gradient-brand">
  {/* Logo icon */}
</div>

// ✅ Should find (active nav):
className={isActive ? 'gradient-brand text-white' : '...'}

// ❌ Should NOT find:
<h1 className="gradient-text-primary">...</h1>
```

### Topics Component

**Test titles:**
```tsx
// ✅ Should find:
<h2 className="text-primary-700 dark:text-primary-300">
  {topic.title}
</h2>

// ❌ Should NOT find:
<h2 className="gradient-text-primary">{topic.title}</h2>
```

## 🎨 Color Blindness Testing

### Deuteranopia (Red-Green)
```bash
# Chrome DevTools:
1. Open DevTools (F12)
2. Press Cmd/Ctrl + Shift + P
3. Type "Rendering"
4. Enable "Emulate vision deficiencies"
5. Select "Deuteranopia"

# Verify:
- Text is still readable ✅
- Interactive elements distinguishable ✅
- Not relying on color alone ✅
```

### Protanopia (Red-Green)
- Repeat above steps with "Protanopia"
- Verify same criteria

### Tritanopia (Blue-Yellow)
- Repeat above steps with "Tritanopia"
- Verify same criteria

## 📊 Expected Test Results

### Before Fixes
| Test | Result | Issues |
|------|--------|--------|
| Gradient text | ❌ FAIL | 4 instances found |
| Secondary-500 on white | ❌ FAIL | Low contrast (2.7:1) |
| Inline gradients | ⚠️ WARNING | 10+ instances |
| Lighthouse score | 85/100 | Contrast issues |

### After Fixes
| Test | Result | Score |
|------|--------|-------|
| Gradient text | ✅ PASS | 0 instances |
| Text contrast | ✅ PASS | All 4.5:1+ |
| Gradient usage | ✅ PASS | 3-5 per page |
| Lighthouse score | ✅ PASS | 95+/100 |

## 🐛 Common Issues to Look For

### 1. Gradient Text
```tsx
// ❌ BAD - Hard to read
<h1 className="bg-gradient-to-r from-primary-600 to-secondary-600 bg-clip-text text-transparent">
  Title
</h1>

// ✅ GOOD - Accessible
<h1 className="text-primary-700 dark:text-primary-300">
  Title
</h1>
```

### 2. Low Contrast Text
```tsx
// ❌ BAD - Only 2.7:1 contrast
<p className="text-secondary-500">Text</p>

// ✅ GOOD - 4.8:1 contrast
<p className="text-secondary-700 dark:text-secondary-400">Text</p>
```

### 3. Excessive Gradients
```tsx
// ❌ BAD - Too many inline gradients
<button className="bg-gradient-to-r from-primary-500 to-secondary-500">
<div className="bg-gradient-to-br from-primary-400/20 to-secondary-400/20">
<span className="bg-gradient-to-l from-blue-500 to-purple-500">

// ✅ GOOD - Reusable utility classes
<button className="gradient-primary-cta">
<div className="gradient-bg-accent">
<div className="gradient-brand">
```

## 🔧 Fixing Issues

### If you find gradient text:
1. Identify the element
2. Replace with solid color: `text-primary-700 dark:text-primary-300`
3. Test contrast ratio
4. Verify readability

### If you find low contrast:
1. Check color combination with WebAIM tool
2. Use darker shade for light backgrounds
3. Use lighter shade for dark backgrounds
4. Test with WCAG AA standard (4.5:1)

### If you find too many gradients:
1. Count gradients per page
2. Keep only 3-5 key brand moments
3. Replace inline gradients with utility classes
4. Remove decorative gradients that don't add value

## 📚 Resources

### Tools
- **WebAIM Contrast Checker**: https://webaim.org/resources/contrastchecker/
- **Chrome Lighthouse**: Built into Chrome DevTools
- **axe DevTools**: https://www.deque.com/axe/devtools/
- **WAVE**: https://wave.webaim.org/
- **Color Oracle**: Free color blindness simulator

### Standards
- **WCAG 2.1**: https://www.w3.org/WAI/WCAG21/quickref/
- **WCAG AA**: 4.5:1 for normal text, 3:1 for large text
- **WCAG AAA**: 7:1 for normal text, 4.5:1 for large text

### Design System
- `frontend/src/design-system/COLOR_GUIDELINES.md` - Complete guidelines
- `frontend/src/design-system/colors.ts` - Color definitions with annotations
- `frontend/src/index.css` - Gradient utility classes

## ✅ Sign-Off Checklist

- [ ] All text has 4.5:1+ contrast ratio
- [ ] No gradient text in production
- [ ] Gradients limited to 3-5 per page
- [ ] Lighthouse accessibility score 90+
- [ ] axe DevTools shows 0 critical issues
- [ ] WAVE shows 0 contrast errors
- [ ] Color blindness simulations pass
- [ ] Dark mode contrast verified
- [ ] Documentation complete
- [ ] Team trained on guidelines

---

**Created**: 2025-10-01
**Version**: 1.0
**Status**: ✅ Ready for Testing
