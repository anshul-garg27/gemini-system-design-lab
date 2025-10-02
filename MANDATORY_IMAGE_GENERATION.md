# ⚠️ MANDATORY Image Generation - ENFORCED

## 🎯 Critical Change

Image generation is now **MANDATORY** and **COUNT-BASED** (not flexible) for both Instagram Reel and Carousel!

---

## 📸 Instagram Carousel - FORCED IMAGE COUNT

### ✅ ALWAYS GENERATE: 8-10 Images (NO FLEXIBILITY)

#### 7 CORE IMAGES (MANDATORY - NO EXCEPTIONS):

1. **cover** - Main carousel cover (slide 1 thumbnail)
2. **cover_alt** - Alternative cover for A/B testing
3. **architecture_panel** OR **diagram_hero** - Primary teaching visual
4. **stat_card** - Hero metric + supporting stats
5. **before_after** OR **comparison** - Comparison visual
6. **process_flow** OR **checklist_card** - Step-by-step or checklist
7. **cta_card** - Final CTA visual for slide 9-10

#### DOMAIN-SPECIFIC (1-3 MANDATORY based on topic):

| Topic Domain | Required Images (Pick 1-3) |
|--------------|----------------------------|
| **System Design** | architecture_diagram, data_flow, scale_metrics |
| **DSA/Algorithms** | algorithm_viz, complexity_chart, execution_steps |
| **Programming** | code_snippet, bug_fix, error_highlight |
| **AI/ML** | model_architecture, training_curve, feature_importance |
| **Database** | query_optimization, index_visualization, schema_diagram |
| **DevOps** | pipeline_flow, deployment_strategy, monitoring_dashboard |

**Total: 7 core + 1-3 domain = 8-10 images ALWAYS**

---

## 📸 Instagram Reel - FORCED IMAGE COUNT

### ✅ ALWAYS GENERATE: 7-10 Images (NO FLEXIBILITY)

#### 7 CORE IMAGES (MANDATORY - NO EXCEPTIONS):

1. **cover_hook** - Main reel cover (scroll-stopping)
2. **cover_alt** - Alternative cover for A/B testing
3. **diagram_hero** - Core concept visualization
4. **comparison** - Before/After or This vs That
5. **stat_card** - Key metrics/numbers
6. **process_flow** - Step-by-step process (vertical)
7. **cta_endcard** - Final CTA frame with Save/Follow/Share

#### DOMAIN-SPECIFIC (0-3 based on topic):

| Topic Domain | Optional Images (Pick 0-3) |
|--------------|---------------------------|
| **System Design** | architecture_diagram, data_flow, scale_metrics |
| **DSA/Algorithms** | algorithm_viz, complexity_chart, execution_steps |
| **Programming** | code_snippet, bug_fix, error_highlight |
| **AI/ML** | model_architecture, training_curve, feature_importance |
| **Database** | query_optimization, index_visualization, schema_diagram |
| **DevOps** | pipeline_flow, deployment_strategy, monitoring_dashboard |

**Total: 7 core + 0-3 domain = 7-10 images ALWAYS**

---

## 🚨 Key Changes Made

### Before (Flexible):
```
- Analyze topic complexity and determine optimal image count (2-10 images)
- Choose appropriate image roles based on what best serves content
```

### After (MANDATORY):
```
⚠️ CRITICAL: You MUST generate ALL 7 CORE IMAGES + domain-specific images. 
This is NOT optional.

CORE 7 IMAGES (ALWAYS GENERATE - NO EXCEPTIONS):
1. cover / cover_hook
2. cover_alt
3. architecture_panel / diagram_hero
4. stat_card
5. before_after / comparison
6. process_flow / checklist_card
7. cta_card / cta_endcard

DOMAIN-SPECIFIC (1-3 MANDATORY):
[Based on topic domain]

TOTAL: 8-10 images (Carousel) or 7-10 images (Reel)
```

---

## ✅ Validation Rules

### Carousel:
```
VALIDATION:
- image_prompts array length MUST be ≥8 (7 core + 1+ domain-specific)
- image_prompts array length MUST be ≤10
- Each prompt MUST include: role, title, prompt, negative_prompt, 
  style_notes, ratio, size_px, accessibility object
- Set meta.image_plan.count to actual total generated (8-10)
- Set meta.image_plan.mandatory_roles with all 7 core roles
- Set meta.image_plan.domain_specific_roles based on topic
- VALIDATION: image_prompts.length MUST equal meta.image_plan.count
```

### Reel:
```
VALIDATION:
- image_prompts array length MUST be ≥7 (7 core + 0+ domain-specific)
- image_prompts array length MUST be ≤10
- Each prompt MUST include: role, title, prompt, negative_prompt,
  style_notes, ratio, size_px, accessibility object
- Set meta.image_plan.count to actual total generated (7-10)
- Set meta.image_plan.mandatory_roles with all 7 core roles
```

---

## 📊 Expected Output

### Meta.image_plan Structure:

```json
"image_plan": {
  "count": 8,                    // Actual total (8-10 for Carousel, 7-10 for Reel)
  "mandatory_roles": [            // 7 core roles (ALWAYS present)
    "cover",
    "cover_alt",
    "architecture_panel",
    "stat_card",
    "before_after",
    "process_flow",
    "cta_card"
  ],
  "domain_specific_roles": [      // 1-3 based on topic
    "algorithm_viz",
    "complexity_chart"
  ],
  "total_images": 9,              // count = mandatory (7) + domain_specific (2)
  "ratio": "4:5",                 // or "9:16" for Reel
  "size_px": "1080x1350",         // or "1080x1920" for Reel
  "reasoning": "7 core images + 2 algorithm-specific images for complete DSA visualization"
}
```

### Image_prompts Array:

```json
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
  // ... 7 more images (total 8-10)
]
```

---

## 🎯 Why This Matters

### 1. **Consistency**
- Every carousel/reel has complete visual storytelling
- No missing critical visuals (cover, CTA, etc.)

### 2. **A/B Testing**
- Always have cover_alt for testing
- Data-driven optimization

### 3. **Accessibility**
- Every image has accessibility specs
- WCAG AA compliance enforced

### 4. **Production-Ready**
- Designers know exactly what to expect
- No guesswork on image count

### 5. **Algorithm Optimization**
- Complete visual coverage = better retention
- Cover + CTA optimization built-in

---

## ⚠️ What AI Cannot Skip

The AI model **CANNOT** skip any of these:

### ❌ Cannot Skip:
- Any of the 7 core images
- Domain-specific images (must generate 1-3)
- Accessibility object for each image
- meta.image_plan with mandatory_roles

### ✅ Flexibility Only In:
- Choice between alternatives (architecture_panel OR diagram_hero)
- Which 1-3 domain-specific to include
- Exact total (8-10 for Carousel, 7-10 for Reel)

---

## 📁 Files Updated

1. **`app/prompts/bodies/instagram-carousel.txt`**
   - Lines 27-61: MANDATORY IMAGE GENERATION RULES
   - Lines 84-88: Image generation enforcement
   - Lines 223-239: meta.image_plan structure
   - Lines 602-624: Validation with 7 core + domain-specific

2. **`app/prompts/bodies/instagram-reel.txt`**
   - Already had mandatory image generation
   - 7 core + domain-specific enforced

---

## ✅ Summary

| Aspect | Before | After |
|--------|--------|-------|
| **Image Count** | 2-10 (flexible) | 8-10 (Carousel), 7-10 (Reel) |
| **Core Images** | Optional | 7 MANDATORY |
| **Domain Images** | Optional | 1-3 MANDATORY (Carousel), 0-3 (Reel) |
| **Flexibility** | High | Low (only in alternatives) |
| **Validation** | Basic | Strict count enforcement |
| **Skippable** | Yes | NO - Enforced |

**Image generation is now MANDATORY and COUNT-ENFORCED! No flexibility!** ⚠️

---

## 🚀 Impact

### For Content Quality:
- ✅ Every carousel/reel has complete visual coverage
- ✅ A/B testing capability built-in
- ✅ Accessibility enforced on all images
- ✅ Production-ready specs

### For AI Model:
- ✅ Clear requirements (7 core + 1-3 domain)
- ✅ No ambiguity on what to generate
- ✅ Validation catches missing images
- ✅ Consistent output structure

**Status: COMPLETE** ✅
