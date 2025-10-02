# Instagram Reel View - Quick Start Guide 🚀

## 🎯 What You Can Do Now

Your Instagram Reel View component is now a **complete content production suite**. Here's everything you can do:

---

## 📱 Tab 1: Timeline (Original + Enhanced)

**What You See:**
- List of all segments (Hook, Problem, Solution, CTA, etc.)
- Click any segment to see details
- Color-coded bars for visual identification

**What You Get:**
- Full narration script
- On-screen text recommendations
- Visual descriptions
- B-roll suggestions
- Text motion effects

---

## 📱 Tab 2: Phone Preview ✨ NEW!

**What You See:**
```
┌─────────────────┐
│   ┌─────────┐   │  ← Realistic phone frame
│   │ Instagram│   │
│   │   Reel   │   │
│   │          │   │  ← Your content displayed
│   │  BURSTY  │   │     exactly as it appears
│   │  TRAFFIC │   │     on Instagram
│   │ KILLING  │   │
│   │YOUR API? │   │
│   │          │   │
│   │ ♥ 2.4K   │   │  ← Engagement indicators
│   │ 💬 156    │   │
│   │ ↗ 89     │   │
│   └─────────┘   │
└─────────────────┘
```

**Interactive Controls:**
- ⏯ **Play/Pause** - Watch timeline animation
- 🔄 **Reset** - Start from beginning
- 📊 **Timeline Scrubber** - Visual progress bar with segments
- 🎯 **Auto-segment selection** - Syncs with playback

**What You Get:**
- See exactly how reel looks on mobile
- Test timing and flow
- Verify on-screen text readability
- Check caption preview

---

## 💬 Tab 3: Caption & Tags

**What You See:**
- Full caption (with character count)
- All 30 hashtags (clickable to copy)
- Call-to-action text
- Music suggestions

**One-Click Actions:**
- 📋 Copy caption
- 📋 Copy all hashtags
- 📋 Copy individual hashtag

---

## 🖼️ Tab 4: Visuals

**What You See:**
For each image (3 total):
- **Prompt** (for AI image generation)
- **Negative prompt** (what to avoid)
- **Ratio** (9:16 vertical)
- **Size** (1080x1920 px)
- **Style notes** (editorial poster, clean, etc.)
- **Alt text** (for accessibility)

**How to Use:**
1. Copy prompt
2. Paste into DALL-E/Midjourney/Ideogram
3. Generate image
4. Use in your reel

---

## 📊 Tab 5: Analytics ✨ NEW!

### Engagement Score (0-100)
```
━━━━━━━━━━ 85 / 100 🟢

Based on:
✓ Hook Length: 105 chars (Optimal)
✓ Hashtags: 30 tags (Perfect)
✓ Duration: 45s (Optimal)
✓ Caption: 787 chars (Good)
✓ Visuals: 3 images (Perfect)
```

### SEO Score (0-100)
```
━━━━━━━━ 75 / 100 🟡

Based on:
✓ Keywords in Title: 2 found
✓ Hashtag Diversity: All tiers present
✓ Keyword Density: 3.2% (Optimal)
✓ CTA Present: Yes
```

### Estimated Performance
```
👁️ Reach:         15,000 accounts
❤️ Likes:         1,200 (8% rate)
↗️ Shares:        300 (2% rate)
```

### Hook Analysis
```
"Stop letting unpredictable bursty traffic 
 crush your API stability. Here is the 
 classic solution."

✅ Length: 105 chars (Optimal)
✅ Question: No (Consider adding)
✅ Power Words: 3 (stop, crush, classic)
```

### Hashtag Strategy
```
┌──────────────┬─────────┐
│ Broad        │ 5 tags  │  #tech #programming #coding
├──────────────┼─────────┤
│ Niche        │ 7 tags  │  #systemdesign #architecture
├──────────────┼─────────┤
│ Micro-Niche  │ 5 tags  │  #ratelimiting #leakybucket
├──────────────┼─────────┤
│ Intent       │ 4 tags  │  #interview #learning
└──────────────┴─────────┘
```

---

## 💾 Tab 6: Export ✨ NEW!

### Download Formats

**1. JSON Export** 📄
```json
{
  "meta": { /* all metadata */ },
  "content": { /* all content */ }
}
```
**Use Case:** API integration, automation, archival

**2. Production Script** 📝
```
INSTAGRAM REEL SCRIPT

Title: Leaky Bucket vs. Token Bucket
Duration: 45s
Hook: Stop letting bursty traffic...

SEGMENTS:

[0-3s] HOOK
Narration: Is bursty traffic destroying...
On-screen: BURSTY TRAFFIC KILLING YOUR API?
Visuals: Fast zoom onto main text...

[3-10s] PROBLEM
...
```
**Use Case:** Video editor handoff, production team

### Quick Copy Options

**Full Caption** 📋
```
When designing high-scale APIs...
[entire caption + hashtags]
```

**All Hashtags** 📋
```
#systemdesign #ratelimiting #trafficshaping
#leakybucket #tokenbucket [... 30 total]
```

**Image Prompts** 📋
```
Image 1 (cover_typography):
Minimalist vertical cover emphasizing...

Negative: no clutter, no busy backgrounds...
---
Image 2 (diagram_hero):
...
```

### Integration Ready 🔜
- Notion (Coming Soon)
- Airtable (Coming Soon)
- Trello (Coming Soon)

---

## 🎯 Recommended Workflow

### Step 1: Generate Content
```bash
POST /api/generate
{
  "topic_id": "19111",
  "platform": "instagram",
  "format": "reel"
}
```

### Step 2: Preview
1. Open **Phone Preview** tab
2. Click **Play** to watch timeline
3. Verify on-screen text displays correctly
4. Check timing feels natural

### Step 3: Analyze
1. Open **Analytics** tab
2. Check **Engagement Score** (aim for 80+)
3. Check **SEO Score** (aim for 75+)
4. Review **Hook Analysis**
5. Verify **Hashtag Strategy** balance

### Step 4: Optimize (if needed)
If scores are low:
- **Hook:** Add power words, make it 50-120 chars
- **Hashtags:** Balance broad/niche/micro tiers
- **Caption:** Add more primary keywords (2-5% density)
- **Duration:** Keep between 30-60 seconds

### Step 5: Export
1. Open **Export** tab
2. Click **Download Script** for video team
3. Click **Copy Full Caption** for posting
4. Click **Copy Image Prompts** for image generation

### Step 6: Generate Images
1. Copy each image prompt
2. Paste into DALL-E/Midjourney
3. Generate with specifications:
   - Ratio: 9:16
   - Size: 1080x1920
   - Style: Follow style_notes

### Step 7: Produce Video
1. Follow production script (timestamps, narration, visuals)
2. Use generated images at specified timestamps
3. Add music (BPM: 90-120, minimal tech beat)
4. Apply motion graphics (type-on keywords, arrow flow)

### Step 8: Post
1. Upload to Instagram Reels
2. Paste full caption (from Quick Copy)
3. Add cover image (first generated image)
4. Publish and track performance

---

## 💡 Pro Tips

### Get High Engagement Scores
1. **Hook:** Use "Stop", "Why", "Secret", "Proven" (power words)
2. **Hook:** Include a question mark (curiosity trigger)
3. **Duration:** Aim for 45-60 seconds (sweet spot)
4. **Caption:** Write 800-1500 characters (detailed but not too long)
5. **Hashtags:** Use all 30 slots (Instagram allows up to 30)

### Get High SEO Scores
1. **Title:** Include 2-3 primary keywords
2. **Caption:** Maintain 2-5% keyword density
3. **Hashtags:** Use all 4 tiers (broad, niche, micro, intent)
4. **CTA:** Always include one (crucial for 25 points)

### Optimize Estimated Reach
```
Reach Formula: engagementScore * 150 + 2000

Examples:
- Score 60 → Reach ~11,000
- Score 80 → Reach ~14,000
- Score 100 → Reach ~17,000
```

To maximize reach, focus on:
1. Perfect hook (50-120 chars + power words + question)
2. Optimal hashtags (20-30 tags, all tiers)
3. Ideal duration (30-60 seconds)

---

## 🐛 Troubleshooting

### "Preview tab shows no content"
**Solution:** Check that `content.content.content_segments` exists and has data.

### "Scores show 0"
**Solution:** Ensure content has `hook`, `hashtags`, `caption`, and `image_prompts`.

### "Timeline doesn't play"
**Solution:** Click **Reset** then **Play**. Check browser console for errors.

### "Export downloads blank file"
**Solution:** Verify `content` object is properly structured with all required fields.

---

## 🎨 Keyboard Shortcuts (Future)

*Coming Soon:*
- `Space` - Play/Pause timeline
- `R` - Reset timeline
- `Tab` - Switch between tabs
- `Cmd/Ctrl + C` - Copy current segment
- `Cmd/Ctrl + E` - Export JSON
- `Cmd/Ctrl + S` - Export Script

---

## 📚 API Reference

### Content Structure Expected
```typescript
{
  meta: {
    topic_id: string,
    topic_title: string,
    platform: 'instagram',
    format: 'reel',
    primary_keywords: string[],
    keyword_tiers: {
      broad: string[],
      niche: string[],
      micro_niche: string[],
      intent: string[],
    }
  },
  content: {
    title: string,
    hook: string,
    content_segments: Array<{
      label: string,
      time_range: string, // "0-3s"
      narration: string,
      on_screen_text: string,
      visuals: string,
      b_roll?: string[],
      text_motion?: string,
    }>,
    caption: string,
    hashtags: string[],
    call_to_action: string,
    music_suggestion: string,
    image_prompts: Array<{
      role: string,
      title: string,
      prompt: string,
      negative_prompt: string,
      ratio: string,
      size_px: string,
      style_notes: string,
      alt_text: string,
    }>,
    visual_plan?: {
      color_palette: string,
      motion_graphics: string[],
    }
  }
}
```

---

## 🎯 Success Metrics

### Your Reel is Ready to Post When:
- ✅ Engagement Score ≥ 80
- ✅ SEO Score ≥ 75
- ✅ Hook length 50-120 chars
- ✅ 20-30 hashtags
- ✅ Duration 30-60s
- ✅ Caption 500-2200 chars
- ✅ 3+ images generated
- ✅ Preview looks good on phone mockup
- ✅ Timeline animation flows naturally

---

## 🚀 You're All Set!

Your Instagram Reel View component now includes:

✅ **6 comprehensive tabs**
✅ **Phone preview mockup**
✅ **Interactive timeline scrubber**
✅ **Dual scoring system**
✅ **Performance predictions**
✅ **Multiple export formats**

**Start creating amazing Instagram Reels with confidence!** 🎬✨
