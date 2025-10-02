# Instagram Carousel View Component - Updates Needed

## ✅ Already Done
1. Updated interfaces to include new fields
2. Updated header to subtle design
3. Added new tabs (caption, engagement, accessibility)
4. Changed activeTab type

## 🚀 Remaining Updates

### 1. **Slide Display** (Lines 300-355)
Add after "Bullets" section:
```tsx
{/* Swipe Trigger - NEW */}
{carousel.slides[currentSlide].swipe_trigger && (
  <div className="bg-blue-50 dark:bg-blue-900/20 p-3 rounded-lg border border-blue-200 dark:border-blue-700">
    <p className="text-xs font-medium text-blue-700 dark:text-blue-400 mb-1">Swipe Trigger</p>
    <p className="text-sm text-blue-900 dark:text-blue-300">{carousel.slides[currentSlide].swipe_trigger}</p>
  </div>
)}
```

Replace Alt Text section (line 348-352) with:
```tsx
{/* Accessibility Info - ENHANCED */}
{carousel.slides[currentSlide].accessibility && (
  <div className="bg-green-50 dark:bg-green-900/20 p-4 rounded-lg border border-green-200 dark:border-green-700">
    <p className="text-sm font-medium text-green-700 dark:text-green-400 mb-3">Accessibility (WCAG AA)</p>
    <div className="space-y-2 text-sm">
      <p className="text-gray-700 dark:text-gray-300">
        <span className="font-medium">Alt Text:</span> {carousel.slides[currentSlide].accessibility.alt_text}
      </p>
      <p className="text-gray-700 dark:text-gray-300">
        <span className="font-medium">Contrast:</span> {carousel.slides[currentSlide].accessibility.color_contrast_ratio}
      </p>
      <p className="text-gray-700 dark:text-gray-300">
        <span className="font-medium">Font:</span> {carousel.slides[currentSlide].accessibility.font_accessibility}
      </p>
    </div>
  </div>
)}
```

### 2. **Caption Tab** (After line 460, before Design Tab)
```tsx
{/* Caption Tab - NEW */}
{activeTab === 'caption' && carousel.caption_structured && (
  <div className="space-y-6 animate-fade-in">
    {/* Structured Caption */}
    <Card>
      <CardHeader>
        <CardTitle>Structured Caption (7 Sections)</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        {/* Hook */}
        <div className="bg-yellow-50 dark:bg-yellow-900/20 p-4 rounded-lg border-l-4 border-yellow-500">
          <div className="flex justify-between mb-2">
            <p className="text-xs font-semibold text-yellow-700 dark:text-yellow-400 uppercase">Hook (125 chars)</p>
            <span className="text-xs text-yellow-600">{carousel.caption_structured.hook_125chars.length} chars</span>
          </div>
          <p className="text-sm text-gray-900 dark:text-gray-100 font-medium">{carousel.caption_structured.hook_125chars}</p>
        </div>
        
        {/* Problem */}
        <div className="bg-gray-50 dark:bg-gray-800 p-4 rounded-lg">
          <p className="text-xs font-semibold text-gray-600 dark:text-gray-400 uppercase mb-2">Problem Statement</p>
          <p className="text-sm text-gray-700 dark:text-gray-300">{carousel.caption_structured.problem_statement}</p>
        </div>
        
        {/* Solution Tease */}
        <div className="bg-gray-50 dark:bg-gray-800 p-4 rounded-lg">
          <p className="text-xs font-semibold text-gray-600 dark:text-gray-400 uppercase mb-2">Solution Tease</p>
          <p className="text-sm text-gray-700 dark:text-gray-300">{carousel.caption_structured.solution_tease}</p>
        </div>
        
        {/* Value Props */}
        <div className="bg-gray-50 dark:bg-gray-800 p-4 rounded-lg">
          <p className="text-xs font-semibold text-gray-600 dark:text-gray-400 uppercase mb-2">Value Propositions</p>
          <div className="space-y-2">
            {carousel.caption_structured.value_props.map((prop, idx) => (
              <p key={idx} className="text-sm text-gray-700 dark:text-gray-300">{prop}</p>
            ))}
          </div>
        </div>
        
        {/* Keywords */}
        <div className="bg-gray-50 dark:bg-gray-800 p-4 rounded-lg">
          <p className="text-xs font-semibold text-gray-600 dark:text-gray-400 uppercase mb-2">Keywords Integration</p>
          <p className="text-sm text-gray-700 dark:text-gray-300">{carousel.caption_structured.keywords_woven}</p>
        </div>
        
        {/* Comment Bait */}
        <div className="bg-blue-50 dark:bg-blue-900/20 p-4 rounded-lg border border-blue-200 dark:border-blue-700">
          <p className="text-xs font-semibold text-blue-700 dark:text-blue-400 uppercase mb-2">Comment Bait</p>
          <p className="text-sm text-gray-900 dark:text-gray-100">{carousel.caption_structured.comment_bait}</p>
        </div>
        
        {/* CTA */}
        <div className="bg-green-50 dark:bg-green-900/20 p-4 rounded-lg border border-green-200 dark:border-green-700">
          <p className="text-xs font-semibold text-green-700 dark:text-green-400 uppercase mb-2">CTA & Link</p>
          <p className="text-sm text-gray-900 dark:text-gray-100 mb-2">{carousel.caption_structured.cta}</p>
          <p className="text-xs text-green-600 dark:text-green-500 break-all">{carousel.caption_structured.link}</p>
        </div>
      </CardContent>
    </Card>

    {/* Full Caption with SEO */}
    <Card>
      <CardHeader>
        <CardTitle>Full Assembled Caption</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="bg-gray-50 dark:bg-gray-800 p-4 rounded-lg mb-4">
          <p className="text-sm text-gray-700 dark:text-gray-300 whitespace-pre-wrap">{carousel.caption.text}</p>
        </div>
        
        {carousel.caption.seo.keyword_density_percent && (
          <div className="text-center p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
            <p className="text-xs text-blue-600 dark:text-blue-400">Keyword Density</p>
            <p className="text-2xl font-bold text-blue-700 dark:text-blue-300">
              {(carousel.caption.seo.keyword_density_percent * 100).toFixed(1)}%
            </p>
          </div>
        )}
      </CardContent>
    </Card>
  </div>
)}
```

### 3. **Engagement Tab** (After Caption Tab)
```tsx
{/* Engagement Tab - NEW */}
{activeTab === 'engagement' && carousel.engagement_tactics && (
  <div className="space-y-6 animate-fade-in">
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center">
          <FireIcon className="h-5 w-5 mr-2 text-orange-600" />
          Engagement Optimization Tactics
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        {/* Swipe Completion */}
        <div className="bg-blue-50 dark:bg-blue-900/20 p-4 rounded-lg border border-blue-200 dark:border-blue-700">
          <p className="text-sm font-semibold text-blue-700 dark:text-blue-400 mb-2">Swipe Completion Strategy</p>
          <p className="text-sm text-gray-700 dark:text-gray-300">{carousel.engagement_tactics.swipe_completion_strategy}</p>
        </div>
        
        {/* Save Trigger */}
        <div className="bg-green-50 dark:bg-green-900/20 p-4 rounded-lg border border-green-200 dark:border-green-700">
          <p className="text-sm font-semibold text-green-700 dark:text-green-400 mb-2">Save Trigger</p>
          <p className="text-sm text-gray-700 dark:text-gray-300">{carousel.engagement_tactics.save_trigger}</p>
        </div>
        
        {/* Share Trigger */}
        <div className="bg-purple-50 dark:bg-purple-900/20 p-4 rounded-lg border border-purple-200 dark:border-purple-700">
          <p className="text-sm font-semibold text-purple-700 dark:text-purple-400 mb-2">Share Trigger</p>
          <p className="text-sm text-gray-700 dark:text-gray-300">{carousel.engagement_tactics.share_trigger}</p>
        </div>
        
        {/* Comment Bait */}
        <div className="bg-indigo-50 dark:bg-indigo-900/20 p-4 rounded-lg border border-indigo-200 dark:border-indigo-700">
          <p className="text-sm font-semibold text-indigo-700 dark:text-indigo-400 mb-2">Comment Bait</p>
          <p className="text-sm text-gray-700 dark:text-gray-300">{carousel.engagement_tactics.comment_bait}</p>
        </div>
        
        {/* Thumbnail Hook */}
        <div className="bg-orange-50 dark:bg-orange-900/20 p-4 rounded-lg border border-orange-200 dark:border-orange-700">
          <p className="text-sm font-semibold text-orange-700 dark:text-orange-400 mb-2">Thumbnail Hook (Slide 1)</p>
          <p className="text-sm text-gray-700 dark:text-gray-300">{carousel.engagement_tactics.thumbnail_hook}</p>
        </div>
      </CardContent>
    </Card>
  </div>
)}
```

### 4. **Accessibility Tab** (After Engagement Tab)
```tsx
{/* Accessibility Tab - NEW */}
{activeTab === 'accessibility' && carousel.accessibility && (
  <div className="space-y-6 animate-fade-in">
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center">
          <CheckCircleIcon className="h-5 w-5 mr-2 text-green-600" />
          Accessibility Compliance ({carousel.accessibility.compliance_level})
        </CardTitle>
      </CardHeader>
      <CardContent>
        {/* Compliance Status */}
        <div className="grid grid-cols-2 gap-4 mb-6">
          <div className={cn(
            "p-4 rounded-lg text-center",
            carousel.accessibility.slide_alt_texts_provided 
              ? "bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-700"
              : "bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-700"
          )}>
            <CheckCircleIcon className={cn(
              "h-8 w-8 mx-auto mb-2",
              carousel.accessibility.slide_alt_texts_provided ? "text-green-600" : "text-red-600"
            )} />
            <p className="text-sm font-medium">Alt Texts</p>
            <p className="text-xs text-gray-600 dark:text-gray-400">
              {carousel.accessibility.slide_alt_texts_provided ? 'All Provided' : 'Missing'}
            </p>
          </div>
          
          <div className={cn(
            "p-4 rounded-lg text-center",
            carousel.accessibility.contrast_validated 
              ? "bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-700"
              : "bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-700"
          )}>
            <CheckCircleIcon className={cn(
              "h-8 w-8 mx-auto mb-2",
              carousel.accessibility.contrast_validated ? "text-green-600" : "text-red-600"
            )} />
            <p className="text-sm font-medium">Contrast</p>
            <p className="text-xs text-gray-600 dark:text-gray-400">
              {carousel.accessibility.contrast_validated ? 'Validated' : 'Not Validated'}
            </p>
          </div>
        </div>
        
        {/* Features */}
        <div className="bg-gray-50 dark:bg-gray-800 p-4 rounded-lg">
          <p className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-3">Accessibility Features</p>
          <ul className="space-y-2">
            {carousel.accessibility.features.map((feature, idx) => (
              <li key={idx} className="flex items-start text-sm">
                <CheckCircleIcon className="h-4 w-4 text-green-600 mr-2 mt-0.5 flex-shrink-0" />
                <span className="text-gray-700 dark:text-gray-300">{feature}</span>
              </li>
            ))}
          </ul>
        </div>
      </CardContent>
    </Card>
  </div>
)}
```

### 5. **Image Prompts - Add Accessibility** (Line 630-641)
Replace Alt Text section with:
```tsx
{/* Accessibility Info - ENHANCED */}
{imagePrompt.accessibility && (
  <div className="bg-green-50 dark:bg-green-900/20 p-4 rounded-lg border border-green-200 dark:border-green-700">
    <p className="text-sm font-medium text-green-700 dark:text-green-400 mb-3">Accessibility</p>
    <div className="space-y-2 text-sm">
      <p className="text-gray-700 dark:text-gray-300">
        <span className="font-medium">Alt Text:</span> {imagePrompt.accessibility.alt_text}
      </p>
      <p className="text-gray-700 dark:text-gray-300">
        <span className="font-medium">Contrast:</span> {imagePrompt.accessibility.color_contrast_ratio}
      </p>
      <p className="text-gray-700 dark:text-gray-300">
        <span className="font-medium">Font:</span> {imagePrompt.accessibility.font_accessibility}
      </p>
    </div>
  </div>
)}
```

### 6. **Footer - Add Image Count** (Line 680-683)
Add after slides count:
```tsx
{carousel.compliance.image_count && (
  <div className="flex items-center">
    <PaintBrushIcon className="h-4 w-4 mr-1 text-gray-500 dark:text-gray-400" />
    <span className="text-gray-600 dark:text-gray-400">
      {carousel.compliance.image_count} images
    </span>
  </div>
)}
```

## 🎨 Design Changes Summary
- **Header:** Gray gradient instead of purple/pink
- **Tabs:** Underline style instead of filled buttons
- **Cards:** Subtle borders, minimal shadows
- **Colors:** Gray-first palette, accent colors only for emphasis
- **Spacing:** More compact, cleaner layout

## 📝 Quick Apply Guide
1. Add `FireIcon` and `ChatBubbleLeftIcon` to imports
2. Update slide display (add swipe_trigger, enhance accessibility)
3. Add Caption tab content (after line 460)
4. Add Engagement tab content
5. Add Accessibility tab content
6. Update Image prompts accessibility
7. Add image count to footer

**Total New Lines:** ~400 lines
**Estimated Time:** 10 minutes for manual application
