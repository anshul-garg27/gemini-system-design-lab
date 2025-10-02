# 🎯 Prompt Enhancement Template v2.0

## 📋 Applied to: Instagram Reel & Instagram Carousel

This document outlines the **complete enhancement pattern** applied to the Instagram Reel and Carousel prompts. Use this as a template to upgrade other prompts.

---

## ✨ Enhancement Categories

### **1. MANDATORY IMAGE GENERATION** ⚠️
### **2. ALGORITHM OPTIMIZATION** 📈
### **3. STRUCTURED CAPTION FORMAT** 📝
### **4. ENGAGEMENT TACTICS** 🔥
### **5. ACCESSIBILITY (WCAG AA)** ♿
### **6. PSYCHOLOGICAL HOOKS** 🧠
### **7. CONTENT ADAPTATION BY TOPIC** 🎨
### **8. ENHANCED OUTPUT JSON** 📊

---

## 1️⃣ MANDATORY IMAGE GENERATION

### **Pattern Applied:**

```
# MANDATORY IMAGE GENERATION RULES (STRICT/ENHANCED):
⚠️ CRITICAL: You MUST generate ALL [X] CORE IMAGES + domain-specific images. This is NOT optional.

CORE [X] IMAGES (ALWAYS GENERATE - NO EXCEPTIONS):
1. "cover" / "cover_hook" - Main attention-grabbing cover
2. "cover_alt" - Alternative cover for A/B testing
3. "diagram_hero" / "architecture_panel" - Primary teaching visual
4. "stat_card" - Key metrics/numbers visualization
5. "comparison" / "before_after" - Before/After OR This vs That
6. "process_flow" / "checklist_card" - Step-by-step process
7. "cta_card" / "cta_endcard" - Final call-to-action frame

DOMAIN-SPECIFIC IMAGES (Add 1-3 based on topic - MANDATORY):
- System Design: Add "architecture_diagram", "data_flow", "scale_metrics"
- DSA/Algorithms: Add "algorithm_viz", "complexity_chart", "execution_steps"
- Programming: Add "code_snippet", "bug_fix", "error_highlight"
- AI/ML: Add "model_architecture", "training_curve", "feature_importance"
- Database: Add "query_optimization", "index_visualization", "schema_diagram"
- DevOps: Add "pipeline_flow", "deployment_strategy", "monitoring_dashboard"

TOTAL IMAGES: 7 core + 1-3 domain = 8-10 images (ALWAYS)

IMAGE SPECS (ALL images):
- Ratio: "[9:16 for Reel | 4:5 for Carousel]"
- Safe margins: ≥[96px for Reel | 64px for Carousel] from all edges
- Thumbnail readable: Must be readable at [200x355px for Reel | 350x437px for Carousel]
- Color contrast: Minimum 4.5:1 ratio (7:1 for headlines)
- Format: PNG, RGB, 72 DPI, <500KB

VALIDATION:
- image_prompts array length MUST be ≥[7-10]
- Each prompt MUST include: role, title, prompt, negative_prompt, style_notes, ratio, size_px, accessibility object
- Set meta.image_plan.count to actual total generated
- Set meta.image_plan.mandatory_roles with all core roles
- Set meta.image_plan.domain_specific_roles based on topic
```

**Key Points:**
- ✅ Force minimum 7 core images
- ✅ Add domain-specific images based on topic
- ✅ A/B testing capability (cover_alt)
- ✅ Accessibility object per image

---

## 2️⃣ ALGORITHM OPTIMIZATION (2025)

### **Pattern Applied:**

```
[PLATFORM] ALGORITHM OPTIMIZATION (2025 - CRITICAL):

[For Carousel:]
- Instagram prioritizes SAVES > Shares > Likes > Comments for reach
- Carousel format: Higher completion rate (swipe to last slide) = better reach
- Hook slide (slide 1): Must stop scroll in <0.8 seconds
  * Thumbnail must be readable at 350x437px (feed size)
  * Text contrast MUST be 4.5:1 minimum (WCAG AA)
  * First 3 words must convey core value
- First 3 slides critical: If user doesn't swipe by slide 3, they won't finish
  * Slide 1: Hook with number/promise
  * Slide 2: Pain amplification with specific cost/impact
  * Slide 3: "But here's what changed..." (cliffhanger)
- Optimal slides: 8-10 (more value = more saves)
- Swipe triggers: Use "→" arrows, "Swipe for...", curiosity gaps between slides
- Posting time: Tuesday-Thursday 10AM-2PM or 7-9PM (tech audience active)
- Caption: First 125 characters appear before "... more" - pack value there
- Hashtags: Mix of small (<100K posts), medium (100K-1M), large (1M+)
  * Formula: 10 small + 15 medium + 5 large = maximum reach
- Call-to-action: "Save this for later 🔖" performs 3x better than "Like if you agree"
- Multi-layered CTA: Save 🔖 + Share with team 📲 + Link in bio

[For Reel:]
- Reels prioritize WATCH TIME (complete views) > Shares > Likes > Comments
- Hook (0-3s) is CRITICAL: 60% of viewers decide to stay/scroll within 3 seconds
- Retention curve: First 3s = 60%, First 10s = 40%, Complete = 25% (aim for 35%+)
- Loop-ability: If last frame connects to first, viewers rewatch = algorithm boost
- Optimal length: 45-60s (longer = more ads shown, higher priority)
- Text overlays: Use ALL the time (85% watch with sound OFF)
- Trending audio: Use within first 7 days of trending (10x reach boost)
- Posting time: Tuesday-Thursday 11AM-1PM or 7-9PM (tech audience peak)
- Hashtags: Mix small (<50K), medium (50K-500K), large (500K-5M)
- Caption: First 125 characters critical (appear before "...more")
```

**Key Points:**
- ✅ Platform-specific metrics
- ✅ Optimal timing for tech audience
- ✅ Specific engagement formulas
- ✅ Hashtag size distribution formula

---

## 3️⃣ STRUCTURED CAPTION FORMAT

### **Pattern Applied:**

```
# 📝 CAPTION STRUCTURE (ENHANCED - FOLLOW EXACTLY):
For maximum engagement and SEO, follow this exact structure:

CAPTION FORMAT:
[HOOK] (First 125 characters - appears before "...more")
↳ One powerful opening line creating curiosity gap
↳ Must contain primary keyword + number/metric if relevant

[PROBLEM] (2-3 lines, 40-60 words)
↳ Describe pain point with specific examples/numbers
↳ Use relatable scenarios: "costs $X/month", "wastes X hours/week"

[SOLUTION TEASE] (1 line, 15-20 words)
↳ Hint at solution without full reveal
↳ Create curiosity to keep reading

[VALUE PROPS] (3-5 bullets with emojis)
✓ Benefit 1 (concise, action-oriented)
✓ Benefit 2 (specific outcome)
✓ Benefit 3 (unique advantage)
✓ Optional: Benefits 4-5 if highly relevant

[KEYWORDS INTEGRATION]
↳ Weave primary/secondary keywords naturally throughout above sections (2-5% density)
↳ Do NOT stuff keywords - must read naturally

[COMMENT BAIT] (1 line with emoji)
↳ Question that sparks discussion
↳ Examples: "Which approach do you prefer? 👇", "Have you faced this issue? Let me know! 💬"

[CTA + LINK] (2-3 lines)
↳ Multi-layered CTA: Save 🔖 + Follow @{handle} for more + Share with team 📲
↳ Link with UTM: "{primary_url}?utm_source={platform}&utm_medium={format}"

[HASHTAGS] (30 hashtags, space-separated on new lines)
↳ Mix: 10 small (<100K) + 15 medium (100K-1M) + 5 large (1M+)
↳ No banned/spam tags; localized when appropriate
```

**Key Points:**
- ✅ 7 distinct sections
- ✅ Character/word limits per section
- ✅ SEO keyword integration (2-5% density)
- ✅ Multi-layered CTA structure
- ✅ Exact hashtag formula

---

## 4️⃣ PSYCHOLOGICAL ENGAGEMENT

### **Pattern Applied:**

```
PSYCHOLOGICAL ENGAGEMENT ([Format]-Specific):

Hook Formulas (choose based on topic):
  * Number promise: "5 Redis Patterns That Handle 1B+ Keys"
  * Curiosity gap: "Everyone uses X wrong. Here's why:"
  * Contrarian: "Stop doing {common practice}. Do this instead:"
  * Result-driven: "From O(n²) to O(n log n) in 3 Steps"
  * Problem-agitation: "Your database is slow. Here's the hidden cause:"
  * Mistake reveal: "You're using Redis wrong. Here's why:"
  * Result tease: "From 500ms to 5ms in 3 steps."

Problem (emphasize with numbers):
  * Show pain with specific metrics ("costs $10K/month", "wastes 5 hours/week")
  * Use relatable scenarios
  * Example: "Your API is slow. 500ms latency. Users leaving."

Solution ([adapt by format]):
  * [Carousel] Slide 3: "But here's what changed everything..." (cliffhanger)
  * [Reel] Fast-paced, numbered points in 10-45s

Content Hooks:
  * Metrics: One HERO number that's impressive (10x, 99.9%, sub-ms)
  * Credibility: Real company examples ("Netflix uses this for...")
  * Actionable: 3 numbered takeaways (easier to remember)
  * Multi-CTA: Layer multiple calls-to-action
```

**Key Points:**
- ✅ 5-7 proven hook formulas
- ✅ Problem amplification with specific numbers
- ✅ Cliffhanger techniques
- ✅ Hero metric strategy

---

## 5️⃣ ACCESSIBILITY (WCAG AA)

### **Pattern Applied:**

```
ACCESSIBILITY REQUIRED (WCAG AA):
  * All text contrast 4.5:1 minimum (7:1 for headlines)
  * Alt text for every [slide/frame/image] (≤160 chars, descriptive)
  * Dyslexic-friendly fonts (Outfit, Inter, DM Sans - no script fonts)
  * Readable at thumbnail size ([specific dimension])
  * No reliance on color alone for information
  
[For each slide/image, add:]
"accessibility": {
  "alt_text": "Descriptive text for screen readers (≤160 chars)",
  "color_contrast_ratio": "4.5:1 minimum (7:1 for headlines)",
  "font_accessibility": "Dyslexic-friendly geometric sans (Outfit/Inter)"
}
```

**Key Points:**
- ✅ WCAG AA compliance mandatory
- ✅ Contrast ratios: 4.5:1 (body), 7:1 (headlines)
- ✅ Alt text ≤160 chars per element
- ✅ Dyslexic-friendly fonts specified
- ✅ Accessibility object in every slide/image

---

## 6️⃣ CONTENT ADAPTATION BY TOPIC

### **Pattern Applied:**

```
CONTENT ADAPTATION BY TOPIC:
- DSA/Algorithms: 
  * Focus on complexity analysis, visual algorithm steps, "aha moment" revelation
  * Big-O notation prominently displayed
  * Tree/graph structures, array visualizations
  
- System Design/HLD: 
  * Component diagrams, service interactions, data flow
  * Scale numbers (handles X QPS), trade-off tables
  * Component boxes with arrows
  
- Programming: 
  * Code snippets (keep to 5-7 lines max)
  * Syntax highlighting, file/folder structure
  * Debugging tips, language-specific gotchas
  
- AI/ML/DL: 
  * Model architecture visual, neural network layers
  * Training curves, confusion matrix, accuracy improvements
  * Feature importance, training time comparisons
  
- Database: 
  * Query examples, execution plans, index strategy
  * Table schemas, index b-trees, ER relationships
  * Before/after performance metrics
  
- DevOps: 
  * Pipeline flows, container flows, deployment strategies
  * Monitoring graphs, deployment diagram, CI/CD stages
  
- Interview Prep: 
  * Checklist format, do/don't comparisons
  * Common mistakes, what interviewers look for
  * Mistake highlights, example answers

VISUAL ADAPTATION:
- Color palette by domain:
  * Backend/Systems: Blue (#2563EB), Cyan (#06B6D4), Slate (#0F172A)
  * Frontend/Web: Orange (#F97316), Yellow (#FACC15), Amber (#F59E0B)
  * Data/ML: Purple (#9333EA), Pink (#EC4899), Violet (#8B5CF6)
  * Database: Indigo (#4F46E5), Blue (#2563EB), Teal (#14B8A6)
  * DevOps: Green (#10B981), Emerald (#059669), Lime (#84CC16)
  * Security: Red (#EF4444), Crimson (#DC2626), Orange (#F97316)
```

**Key Points:**
- ✅ Topic-specific visual guidelines
- ✅ Appropriate metrics per domain
- ✅ Domain-specific color palettes
- ✅ Content structure adaptation

---

## 7️⃣ ENHANCED OUTPUT JSON STRUCTURE

### **New/Enhanced Fields Added:**

```json
{
  "meta": {
    // ... existing fields
    "keyword_overrides": false,
    "keyword_tiers": {
      "broad": [],
      "niche": [],
      "micro_niche": [],
      "intent": [],
      "branded": []
    },
    "image_plan": {
      "count": 8,
      "mandatory_roles": ["cover", "cover_alt", ...],
      "domain_specific_roles": ["algorithm_viz", ...],
      "total_images": 9,
      "ratio": "4:5",
      "size_px": "1080x1350",
      "reasoning": "..."
    },
    "accessibility": {
      "compliance_level": "WCAG AA",
      "features": [
        "All text contrast 4.5:1 minimum (7:1 for headlines)",
        "Alt text for every slide (≤160 chars)",
        "Dyslexic-friendly fonts (Outfit, Inter, DM Sans)",
        "Readable at thumbnail size",
        "No reliance on color alone"
      ],
      "slide_alt_texts_provided": true,
      "contrast_validated": true
    }
  },
  
  "content": {
    // ... existing content
    
    "caption_structured": {
      "hook_125chars": "...",
      "problem_statement": "...",
      "solution_tease": "...",
      "value_props": ["✓ ...", "✓ ...", "✓ ..."],
      "keywords_woven": "...",
      "comment_bait": "...",
      "cta": "...",
      "link": "..."
    },
    
    "caption": {
      "text": "FULL CAPTION assembled from caption_structured",
      "emojis_used": ["🧠", "⚙️", "🚀", "🔖", "📲", "👇"],
      "seo": {
        "keywords_used": [...],
        "lsi_terms_used": [...],
        "keyword_density_percent": 0.027
      }
    },
    
    "engagement_tactics": {
      "swipe_completion_strategy": "How slides 1-3 hook user...",
      "save_trigger": "What makes this save-worthy...",
      "share_trigger": "Why someone would share...",
      "comment_bait": "Question that sparks discussion...",
      "thumbnail_hook": "Why slide 1 stops scroll..."
    },
    
    "accessibility": {
      "compliance_level": "WCAG AA",
      "features": [...],
      "slide_alt_texts_provided": true,
      "contrast_validated": true
    },
    
    "design_system": {
      "color_palette": [...],
      "font_pairings": [...],
      "grid": {
        "ratio": "4:5",
        "size_px": "1080x1350",
        "safe_margins_px": 64,
        "column_system": "8-col mobile grid"
      }
    },
    
    "image_prompts": [
      {
        "role": "cover",
        "title": "...",
        "prompt": "...",
        "negative_prompt": "...",
        "style_notes": "...",
        "ratio": "4:5",
        "size_px": "1080x1350",
        "accessibility": {
          "alt_text": "...",
          "color_contrast_ratio": "7:1",
          "font_accessibility": "Dyslexic-friendly"
        }
      }
      // ... all images with accessibility
    ]
  }
}
```

---

## 8️⃣ PER-SLIDE/FRAME ENHANCEMENTS

### **For Carousel Slides:**

```json
{
  "index": 1,
  "role": "hook",
  "title": "≤10 words high-tension promise (must include number/metric)",
  "subtitle": "≤14 words clarity line",
  "bullets": ["Optional bullets ≤14 words each"],
  "overlay_text": "Swipe →",
  "swipe_trigger": "Curiosity gap driving swipe (e.g., 'But there's a catch...', '5 patterns inside →')",
  "design_note": "THUMBNAIL OPTIMIZED: Readable at 350x437px...",
  "layout": "title top (80-120px), subtitle below (40-60px)...",
  "iconography": "tiny diagram glyph (20-30% of space)",
  "contrast_notes": "max contrast headline (7:1 ratio); subtitle (4.5:1 WCAG AA)",
  "accessibility": {
    "alt_text": "≤160 chars describing content",
    "color_contrast_ratio": "7:1 for headline, 4.5:1 for subtitle",
    "font_accessibility": "Dyslexic-friendly geometric sans (Outfit/Inter)"
  }
}
```

### **For Reel Segments:**

```json
{
  "label": "Hook",
  "time_range": "0-3s",
  "narration": "One-liner hook (≤20 words)",
  "on_screen_text": "Short overlay (≤8 words)",
  "visuals": "Camera framing/motion + keywords",
  "text_motion": "scale_up_bounce",
  "text_position": "center_upper",
  "b_roll": ["list 1-2 cutaway ideas"]
}
```

---

## 📊 VALIDATION SECTION (Enhanced)

### **Pattern Applied:**

```
VALIDATION (STRICT REQUIREMENTS):
- Ensure EXACT structure above is returned
- Total [slides/segments] [specific count]
- **Each [slide/frame] MUST include**: [list all required fields including new ones]
- **Accessibility object per [element]**: alt_text (≤160 chars), color_contrast_ratio (4.5:1 min), font_accessibility
- Caption 200–300 words; **exactly 30** hashtags (10 small + 15 medium + 5 large)
- **caption_structured object REQUIRED** with 7 sections
- **engagement_tactics object REQUIRED** with 5 strategies
- **meta.accessibility object REQUIRED** for WCAG AA compliance
- When options.include_images=true (MANDATORY IMAGE GENERATION):
  - Generate EXACTLY [X] core images + 1-3 domain-specific = [Y-Z] total (NO FLEXIBILITY)
  - [X] Core roles REQUIRED (NO EXCEPTIONS): [list all]
  - Domain-specific (1-3 based on topic - MANDATORY): [list by domain]
  - Each image_prompt MUST have accessibility object
  - Set meta.image_plan.count to actual generated count
  - Set meta.image_plan.mandatory_roles with all core roles
  - Set meta.image_plan.domain_specific_roles based on topic
  - VALIDATION: image_prompts.length MUST equal meta.image_plan.count
- **Thumbnail optimization**: [specific requirements]
- **Contrast requirements**: 7:1 for headlines, 4.5:1 minimum for body text
- Return STRICT JSON. NO EXTRA TEXT. NO NULLS—use "" or [].
```

---

## ✅ Checklist for Applying to New Prompts

### **Step 1: Mandatory Images**
- [ ] Define 7 core image roles for your format
- [ ] Define domain-specific images (1-3 per topic domain)
- [ ] Specify exact image specs (ratio, size, margins)
- [ ] Add validation for image count

### **Step 2: Algorithm Optimization**
- [ ] Add platform-specific algorithm rules (2025)
- [ ] Define optimal timing (posting times)
- [ ] Specify hashtag formula
- [ ] Add engagement metrics

### **Step 3: Structured Caption**
- [ ] Add 7-section caption structure
- [ ] Define character/word limits per section
- [ ] Specify keyword density (2-5%)
- [ ] Add multi-layered CTA format

### **Step 4: Psychological Hooks**
- [ ] Add 5-7 hook formulas
- [ ] Define problem amplification strategy
- [ ] Add cliffhanger/curiosity gap techniques
- [ ] Specify hero metric approach

### **Step 5: Accessibility**
- [ ] Add WCAG AA compliance requirements
- [ ] Specify contrast ratios (4.5:1, 7:1)
- [ ] Require alt text ≤160 chars
- [ ] Mandate dyslexic-friendly fonts
- [ ] Add accessibility object to every element

### **Step 6: Content Adaptation**
- [ ] Define rules for each topic domain (DSA, System Design, etc.)
- [ ] Specify domain-specific visuals
- [ ] Add domain color palettes
- [ ] Define domain-specific metrics

### **Step 7: Enhanced JSON Output**
- [ ] Add `caption_structured` object
- [ ] Add `engagement_tactics` object
- [ ] Add `meta.accessibility` object
- [ ] Add `meta.image_plan` object
- [ ] Add `accessibility` to each slide/image
- [ ] Add `keyword_tiers` for hashtag building
- [ ] Add `keyword_density_percent` to SEO

### **Step 8: Validation**
- [ ] Update compliance checks (was 8 → now 18+)
- [ ] Add mandatory image validation
- [ ] Add accessibility validation
- [ ] Add caption structure validation
- [ ] Add engagement tactics validation

---

## 🎯 Summary

### **What Was Added:**

| Enhancement | Reel | Carousel | Complexity |
|-------------|------|----------|------------|
| Mandatory 7 core images | ✅ | ✅ | High |
| Domain-specific images | ✅ | ✅ | Medium |
| Algorithm optimization | ✅ | ✅ | Medium |
| Structured caption (7 sections) | ✅ | ✅ | High |
| Engagement tactics object | ✅ | ✅ | Medium |
| WCAG AA accessibility | ✅ | ✅ | High |
| Per-element accessibility | ✅ | ✅ | High |
| Psychological hooks | ✅ | ✅ | Low |
| Content adaptation by topic | ✅ | ✅ | Medium |
| Hashtag formula (10+15+5) | ✅ | ✅ | Low |
| Swipe triggers (Carousel) | - | ✅ | Low |
| Text animations (Reel) | ✅ | - | Medium |
| Keyword density tracking | ✅ | ✅ | Low |

### **Lines of Code Added:**
- Reel: ~250 lines of enhancements
- Carousel: ~280 lines of enhancements

### **Output JSON Fields Added:**
- **New objects**: `caption_structured`, `engagement_tactics`, `meta.accessibility`, `meta.image_plan`
- **New per-element fields**: `swipe_trigger`, `accessibility`, `text_animations`
- **Enhanced validation**: 8 checks → 18+ checks

---

## 📝 Usage

Use this template to upgrade any content generation prompt to the **v2.0 enhanced standard**!

**Status:** Production-ready pattern ✅
