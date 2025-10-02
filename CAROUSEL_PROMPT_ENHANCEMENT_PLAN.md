# Instagram Carousel Prompt Enhancement Plan 🎯

## Based on Instagram Reel Prompt Analysis

### Current Status
- ✅ Carousel prompt is decent but missing many enhancements
- ✅ Basic visual guidelines exist
- ⚠️ Missing comprehensive engagement, accessibility, and structured output

### Required Enhancements (From Reel Prompt)

---

## 1. ✨ MANDATORY IMAGE GENERATION RULES

**Current:** Optional image count (2-10), flexible roles  
**Need:** MANDATORY core images + domain-specific

### CORE IMAGES (ALWAYS GENERATE - NO EXCEPTIONS):
1. **cover** - Main carousel cover (slide 1)
2. **cover_alt** - Alternative cover for A/B testing
3. **architecture_panel** / **diagram_hero** - Primary teaching visual
4. **stat_card** - Key metrics visualization
5. **before_after** / **comparison** - Comparison visual
6. **process_flow** - Step-by-step diagram
7. **cta_card** - Final slide CTA visual

**PLUS Domain-Specific (1-3):**
- System Design: architecture_diagram, data_flow, scale_metrics
- DSA/Algorithms: algorithm_viz, complexity_chart, execution_steps
- Programming: code_snippet, bug_fix, error_highlight
- AI/ML: model_architecture, training_curve, feature_importance
- Database: query_optimization, index_viz, schema_diagram
- DevOps: pipeline_flow, deployment_strategy, monitoring_dashboard

---

## 2. 🎯 SWIPE COMPLETION OPTIMIZATION

**Current:** Basic swipe triggers mentioned  
**Need:** Complete swipe psychology system

### Add to Each Slide:
```json
{
  "swipe_trigger": "Curiosity gap or incomplete thought driving swipe"
}
```

### Slide-Specific Swipe Triggers:
- **Slide 1 (Hook):** End with "But there's a catch..." or "5 patterns inside →"
- **Slide 2 (Problem):** "But there's a way out... swipe →"
- **Slide 3 (Core Idea):** "Here's how it works... →"
- **Slides 4-7:** Progressive reveals, each ending with curiosity
- **Slide 8 (Summary):** "One more thing..."
- **Slide 9-10 (CTA):** "Link in bio →", "Save this →"

---

## 3. ♿ ACCESSIBILITY (WCAG AA) - MANDATORY

**Current:** Basic alt_text  
**Need:** Complete accessibility compliance

### Add to Meta:
```json
"accessibility": {
  "compliance_level": "WCAG AA",
  "features": [
    "All text contrast 4.5:1 minimum (7:1 for headlines)",
    "Alt text for every slide (≤160 chars)",
    "Dyslexic-friendly fonts (Outfit, Inter, DM Sans)",
    "Readable at thumbnail size (350x437px)",
    "No reliance on color alone for information"
  ],
  "slide_alt_texts_provided": true,
  "contrast_validated": true
}
```

### Add to Each Slide:
```json
"accessibility": {
  "alt_text": "Descriptive text for screen readers",
  "color_contrast_ratio": "4.5:1 minimum",
  "font_accessibility": "Dyslexic-friendly geometric sans"
}
```

### Add to Each Image Prompt:
```json
"accessibility": {
  "alt_text": "What's shown in the image",
  "color_contrast_ratio": "7:1 for headline, 4.5:1 for body",
  "font_accessibility": "Dyslexic-friendly"
}
```

---

## 4. 🔥 ENGAGEMENT TACTICS - MANDATORY

**Current:** Basic mention in algorithm section  
**Need:** Dedicated engagement_tactics object

### Add to Content:
```json
"engagement_tactics": {
  "swipe_completion_strategy": "How slides 1-3 hook user to swipe through all",
  "save_trigger": "What makes this save-worthy (checklist, reference guide)",
  "share_trigger": "Why someone would share with team",
  "comment_bait": "Question in caption sparking discussion",
  "thumbnail_hook": "Why slide 1 stops scroll in <0.8s"
}
```

---

## 5. 📝 STRUCTURED CAPTION FORMAT

**Current:** Basic caption with SEO  
**Need:** Exact structured format like Reel

### Add caption_structured Object:
```json
"caption_structured": {
  "hook_125chars": "First 125 characters creating curiosity gap",
  "problem_statement": "2-3 lines with specific numbers",
  "solution_tease": "1 line hinting without revealing",
  "value_props": [
    "✓ Benefit 1",
    "✓ Benefit 2",
    "✓ Benefit 3"
  ],
  "keywords_woven": "Natural keyword integration (2-5% density)",
  "comment_bait": "Question with emoji",
  "cta": "Multi-layered: Save 🔖 + Follow + Share 📲",
  "link": "URL with UTM"
}
```

### Then Assemble Full Caption:
```json
"caption": {
  "text": "Full assembled caption from caption_structured",
  "emojis_used": ["🧠","⚙️","🚀","🔖","📲","👇"],
  "seo": {
    "keywords_used": [...],
    "lsi_terms_used": [...],
    "keyword_density_percent": 3.2
  }
}
```

---

## 6. 📱 THUMBNAIL OPTIMIZATION

**Current:** Basic mention  
**Need:** First frame optimization guidelines

### Add to Slide 1:
```
THUMBNAIL OPTIMIZED: Readable at 350x437px (Instagram feed size)
- First 3 words must convey core value
- Text contrast 7:1 minimum (headline)
- Bold, high-contrast, simple visual
- No mid-motion blur
- Bright accent color
```

---

## 7. 🎨 ENHANCED VISUAL SPECS

**Current:** Good, but can be more specific  
**Need:** Add these details

### For Each Image Prompt:
- **Thumbnail test:** Must be readable at 350x437px
- **Contrast specs:** 7:1 for headlines, 4.5:1 for body
- **Font sizes:** Specific px sizes for each element
- **Safe margins:** ≥64px from all edges
- **Whitespace:** 60%+ empty space for clarity

---

## 8. 📊 HASHTAG FORMULA

**Current:** Mix of sizes mentioned  
**Need:** Exact formula

### Update Hashtags Rule:
```
EXACTLY 30 hashtags:
- 10 small (<100K posts)
- 15 medium (100K-1M posts)
- 5 large (1M+ posts)

Mix: broad + niche + micro-niche + intent + branded
```

---

## 9. 🎯 ENHANCED SLIDE STRUCTURE

**Current:** Basic slide fields  
**Need:** Add these to EACH slide

### Required Fields Per Slide:
```json
{
  "index": 1,
  "role": "hook",
  "title": "≤10 words (must include number/metric)",
  "subtitle": "≤14 words amplifying promise",
  "bullets": ["Optional stats"],
  "overlay_text": "Swipe → (must include arrow)",
  "swipe_trigger": "Curiosity gap driving swipe",  // NEW
  "design_note": "THUMBNAIL OPTIMIZED + specific guidance",
  "layout": "Detailed layout with px sizes",
  "iconography": "Specific icons/glyphs",
  "contrast_notes": "7:1 headline, 4.5:1 body",
  "accessibility": {  // NEW
    "alt_text": "≤160 chars",
    "color_contrast_ratio": "4.5:1 minimum",
    "font_accessibility": "Dyslexic-friendly"
  }
}
```

---

## 10. 🔍 VALIDATION CHECKS

**Current:** Basic compliance checks  
**Need:** Comprehensive validation

### Add to Compliance:
```json
"compliance": {
  "slides_total": 0,
  "hook_title_char_count": 0,
  "caption_word_count": 0,
  "hashtag_count": 30,
  "checks": [
    "≤10 slides",
    "titles ≤10 words",
    "bullets ≤14 words",
    "alt_text present for every slide",
    "accessibility object for every slide",  // NEW
    "swipe_trigger for slides 1-8",  // NEW
    "exactly 30 hashtags (10 small + 15 medium + 5 large)",  // NEW
    "caption 200–300 words",
    "caption_structured object present",  // NEW
    "engagement_tactics object present",  // NEW
    "image_prompts length ≥7",
    "all 7 core image roles present"  // NEW
  ]
}
```

---

## Summary of Missing Elements

### From Reel Prompt → Add to Carousel:

1. ✅ Mandatory 7 core images + domain-specific
2. ✅ Swipe triggers for each slide
3. ✅ Accessibility compliance (WCAG AA)
4. ✅ Engagement tactics object
5. ✅ Structured caption format
6. ✅ Thumbnail optimization guidelines
7. ✅ Enhanced contrast specs (7:1 headlines)
8. ✅ Hashtag formula (10+15+5)
9. ✅ Accessibility object for each slide
10. ✅ Accessibility object for each image

---

## Implementation Order

1. **First:** Add accessibility to meta
2. **Second:** Update slide structure with swipe_trigger + accessibility
3. **Third:** Add caption_structured object
4. **Fourth:** Add engagement_tactics object
5. **Fifth:** Update image prompt structure with accessibility
6. **Sixth:** Update validation/compliance checks
7. **Seventh:** Enhance visual specs with thumbnail optimization

---

## Expected Output After Enhancement

### Meta Level:
- ✅ accessibility object (WCAG AA compliance)
- ✅ image_plan with mandatory core + domain-specific

### Content Level:
- ✅ caption_structured (7 sections)
- ✅ caption (full assembled)
- ✅ engagement_tactics (5 strategies)
- ✅ accessibility (compliance features)
- ✅ hashtags (30 with exact formula)

### Slide Level (Each):
- ✅ swipe_trigger
- ✅ accessibility object

### Image Level (Each):
- ✅ accessibility object
- ✅ thumbnail optimization specs
- ✅ contrast ratios specified

---

## Next Steps

1. Update Instagram Carousel prompt with all enhancements
2. Test with sample content generation
3. Verify all new fields appear in output
4. Update frontend component if needed (already done for Reel)

**Goal:** Make Carousel prompt as comprehensive as Reel prompt! 🚀
