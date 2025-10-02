import React, { useState } from 'react';
import { 
  PhotoIcon,
  HashtagIcon,
  DocumentDuplicateIcon,
  ChevronLeftIcon,
  ChevronRightIcon,
  SparklesIcon,
  ChartBarIcon,
  PaintBrushIcon,
  CheckCircleIcon,
  Squares2X2Icon,
  SwatchIcon,
  BeakerIcon,
  FireIcon,
  ChatBubbleLeftIcon
} from '@heroicons/react/24/outline';
import { Card, CardContent, CardHeader, CardTitle } from './ui/Card';
import { Button } from './ui/Button';
import { cn } from '../lib/utils';

interface CarouselSlide {
  index: number;
  role: string;
  title: string;
  subtitle: string;
  bullets: string[];
  overlay_text: string;
  swipe_trigger?: string;
  design_note: string;
  layout: string;
  iconography: string;
  contrast_notes: string;
  alt_text?: string;
  accessibility?: {
    alt_text: string;
    color_contrast_ratio: string;
    font_accessibility: string;
  };
}

interface ImagePrompt {
  role: string;
  title: string;
  prompt: string;
  negative_prompt: string;
  style_notes: string;
  ratio: string;
  size_px: string;
  alt_text?: string;
  accessibility?: {
    alt_text: string;
    color_contrast_ratio: string;
    font_accessibility: string;
  };
}

interface InstagramCarouselContent {
  slides: CarouselSlide[];
  caption_structured?: {
    hook_125chars: string;
    problem_statement: string;
    solution_tease: string;
    value_props: string[];
    keywords_woven: string;
    comment_bait: string;
    cta: string;
    link: string;
  };
  caption: {
    text: string;
    emojis_used: string[];
    seo: {
      keywords_used: string[];
      lsi_terms_used: string[];
      keyword_density_percent?: number;
    };
  };
  hashtags: string[];
  engagement_tactics?: {
    swipe_completion_strategy: string;
    save_trigger: string;
    share_trigger: string;
    comment_bait: string;
    thumbnail_hook: string;
  };
  accessibility?: {
    compliance_level: string;
    features: string[];
    slide_alt_texts_provided: boolean;
    contrast_validated: boolean;
  };
  design_system: {
    color_palette: Array<{
      name: string;
      values: string[];
    }>;
    font_pairings: Array<{
      headline: string;
      body: string;
      code?: string;
    }>;
    grid: {
      ratio: string;
      size_px: string;
      safe_margins_px: number;
      column_system: string;
    };
  };
  image_prompts: ImagePrompt[];
  image_prompts_by_slide?: Array<{
    slide_index: number;
    role: string;
    note: string;
  }>;
  compliance?: {
    slides_total: number;
    hook_title_char_count: number;
    caption_word_count: number;
    hashtag_count: number;
    image_count?: number;
    checks: string[];
  };
}

interface InstagramCarouselViewProps {
  content: {
    job_id: string;
    platform: string;
    format: string;
    envelope: {
      content: InstagramCarouselContent;
    };
    meta?: {
      topic_title?: string;
      primary_keywords?: string[];
      secondary_keywords?: string[];
      lsi_terms?: string[];
    };
  };
  onCopy: () => void;
}

const InstagramCarouselView: React.FC<InstagramCarouselViewProps> = ({ content, onCopy }) => {
  const [currentSlide, setCurrentSlide] = useState(0);
  const [activeTab, setActiveTab] = useState<'slides' | 'caption' | 'engagement' | 'accessibility' | 'design' | 'images'>('slides');
  
  // Extract content
  const carousel = content.envelope.content;
  const meta = content.meta || {};

  const getRoleColor = (role: string) => {
    switch (role) {
      case 'hook': return 'bg-primary-100 dark:bg-primary-900/20 text-primary-800 dark:text-primary-400 border-primary-200 dark:border-primary-700';
      case 'problem': return 'bg-error-100 dark:bg-error-900/20 text-error-800 dark:text-error-400 border-error-200 dark:border-error-700';
      case 'core_idea': return 'bg-success-100 dark:bg-success-900/20 text-success-800 dark:text-success-400 border-success-200 dark:border-success-700';
      case 'architecture': return 'bg-secondary-100 dark:bg-secondary-900/20 text-secondary-800 dark:text-secondary-400 border-secondary-200 dark:border-secondary-700';
      case 'tradeoffs': return 'bg-warning-100 dark:bg-warning-900/20 text-warning-800 dark:text-warning-400 border-warning-200 dark:border-warning-700';
      case 'metrics': return 'bg-purple-100 dark:bg-purple-900/20 text-purple-800 dark:text-purple-400 border-purple-200 dark:border-purple-700';
      case 'mini_case': return 'bg-indigo-100 dark:bg-indigo-900/20 text-indigo-800 dark:text-indigo-400 border-indigo-200 dark:border-indigo-700';
      case 'summary': return 'bg-teal-100 dark:bg-teal-900/20 text-teal-800 dark:text-teal-400 border-teal-200 dark:border-teal-700';
      case 'cta': return 'bg-pink-100 dark:bg-pink-900/20 text-pink-800 dark:text-pink-400 border-pink-200 dark:border-pink-700';
      default: return 'bg-gray-100 dark:bg-gray-800 text-gray-800 dark:text-gray-300 border-gray-200 dark:border-gray-700';
    }
  };

  const navigateSlide = (direction: 'prev' | 'next') => {
    if (direction === 'prev') {
      setCurrentSlide(prev => prev > 0 ? prev - 1 : carousel.slides.length - 1);
    } else {
      setCurrentSlide(prev => prev < carousel.slides.length - 1 ? prev + 1 : 0);
    }
  };

  return (
    <div className="bg-white dark:bg-gray-900 rounded-2xl shadow-sm border border-gray-200 dark:border-gray-800 max-w-6xl w-full max-h-[90vh] overflow-hidden flex flex-col">
      {/* Header - Subtle Design */}
      <div className="bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-800 dark:to-gray-900 border-b border-gray-200 dark:border-gray-700 p-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="p-2.5 bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700">
              <Squares2X2Icon className="h-6 w-6 text-gray-700 dark:text-gray-300" />
            </div>
            <div>
              <h2 className="text-xl font-semibold text-gray-900 dark:text-gray-100">Instagram Carousel</h2>
              {meta.topic_title && (
                <p className="text-gray-600 dark:text-gray-400 text-sm mt-0.5">{meta.topic_title}</p>
              )}
              <p className="text-gray-500 dark:text-gray-500 text-xs mt-0.5">{carousel.slides.length} slides</p>
            </div>
          </div>
          <Button
            onClick={onCopy}
            variant="ghost"
            size="sm"
            className="bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-300 border border-gray-300 dark:border-gray-600"
            leftIcon={<DocumentDuplicateIcon className="h-4 w-4" />}
          >
            Copy All
          </Button>
        </div>
      </div>

      {/* Tab Navigation - Subtle */}
      <div className="border-b border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900">
        <div className="flex overflow-x-auto scrollbar-hide">
          {[
            { id: 'slides', label: 'Slides', icon: PhotoIcon },
            { id: 'caption', label: 'Caption', icon: SparklesIcon },
            { id: 'engagement', label: 'Engagement', icon: ChartBarIcon },
            { id: 'accessibility', label: 'Accessibility', icon: CheckCircleIcon },
            { id: 'design', label: 'Design', icon: SwatchIcon },
            { id: 'images', label: 'Images', icon: PaintBrushIcon },
          ].map((tab) => {
            const Icon = tab.icon;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as any)}
                className={cn(
                  "flex items-center px-4 py-3 text-sm font-medium border-b-2 transition-colors whitespace-nowrap",
                  activeTab === tab.id
                    ? "border-gray-900 dark:border-gray-100 text-gray-900 dark:text-gray-100"
                    : "border-transparent text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300 hover:border-gray-300 dark:hover:border-gray-600"
                )}
              >
                <Icon className="h-4 w-4 mr-2" />
                {tab.label}
              </button>
            );
          })}
        </div>
      </div>

      {/* Content Area */}
      <div className="flex-1 overflow-y-auto p-6 bg-gray-50 dark:bg-gray-950">
        {/* Slides Tab */}
        {activeTab === 'slides' && (
          <div className="space-y-6 animate-fade-in">
            {/* Slide Navigation */}
            <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6">
              <div className="flex items-center justify-between mb-4">
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => navigateSlide('prev')}
                  leftIcon={<ChevronLeftIcon className="h-4 w-4" />}
                >
                  Previous
                </Button>
                <div className="flex items-center space-x-2">
                  {carousel.slides.map((_, index) => (
                    <button
                      key={index}
                      onClick={() => setCurrentSlide(index)}
                      className={cn(
                        "w-2 h-2 rounded-full transition-all",
                        currentSlide === index
                          ? "bg-primary-500 w-8"
                          : "bg-gray-300 dark:bg-gray-600 hover:bg-gray-400 dark:hover:bg-gray-500"
                      )}
                    />
                  ))}
                </div>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => navigateSlide('next')}
                  rightIcon={<ChevronRightIcon className="h-4 w-4" />}
                >
                  Next
                </Button>
              </div>

              {/* Current Slide Display */}
              <Card className="animate-fade-in">
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <CardTitle className="flex items-center space-x-2">
                      <span>Slide {carousel.slides[currentSlide].index}</span>
                      <span className={cn(
                        "px-3 py-1 rounded-full text-xs font-medium border",
                        getRoleColor(carousel.slides[currentSlide].role)
                      )}>
                        {carousel.slides[currentSlide].role}
                      </span>
                    </CardTitle>
                    <span className="text-sm text-gray-500 dark:text-gray-400">
                      {carousel.slides[currentSlide].overlay_text}
                    </span>
                  </div>
                </CardHeader>
                <CardContent className="space-y-4">
                  {/* Title & Subtitle */}
                  <div>
                    <h3 className="text-2xl font-bold text-gray-900 dark:text-gray-100">
                      {carousel.slides[currentSlide].title}
                    </h3>
                    <p className="text-gray-600 dark:text-gray-400 mt-1">
                      {carousel.slides[currentSlide].subtitle}
                    </p>
                  </div>

                  {/* Bullets */}
                  {carousel.slides[currentSlide].bullets.length > 0 && (
                    <div className="bg-gray-50 dark:bg-gray-800 rounded-lg p-4">
                      <ul className="space-y-2">
                        {carousel.slides[currentSlide].bullets.map((bullet, idx) => (
                          <li key={idx} className="flex items-start">
                            <span className="text-primary-500 mr-2 mt-1">•</span>
                            <span className="text-gray-700 dark:text-gray-300">{bullet}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {/* Swipe Trigger - NEW */}
                  {carousel.slides[currentSlide].swipe_trigger && (
                    <div className="bg-blue-50 dark:bg-blue-900/20 p-3 rounded-lg border border-blue-200 dark:border-blue-700">
                      <p className="text-xs font-medium text-blue-700 dark:text-blue-400 mb-1">Swipe Trigger</p>
                      <p className="text-sm text-blue-900 dark:text-blue-300">{carousel.slides[currentSlide].swipe_trigger}</p>
                    </div>
                  )}

                  {/* Design Details */}
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <Card variant="filled">
                      <CardContent className="p-4">
                        <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Layout</p>
                        <p className="text-sm text-gray-600 dark:text-gray-400">{carousel.slides[currentSlide].layout}</p>
                      </CardContent>
                    </Card>
                    <Card variant="filled">
                      <CardContent className="p-4">
                        <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Iconography</p>
                        <p className="text-sm text-gray-600 dark:text-gray-400">{carousel.slides[currentSlide].iconography}</p>
                      </CardContent>
                    </Card>
                  </div>

                  {/* Design Notes */}
                  <Card variant="filled">
                    <CardContent className="p-4">
                      <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Design Note</p>
                      <p className="text-sm text-gray-600 dark:text-gray-400">{carousel.slides[currentSlide].design_note}</p>
                    </CardContent>
                  </Card>

                  {/* Contrast Notes */}
                  <Card variant="filled">
                    <CardContent className="p-4">
                      <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Contrast Notes</p>
                      <p className="text-sm text-gray-600 dark:text-gray-400">{carousel.slides[currentSlide].contrast_notes}</p>
                    </CardContent>
                  </Card>

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
                </CardContent>
              </Card>
            </div>

            {/* All Slides Grid */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Squares2X2Icon className="h-5 w-5 mr-2 text-primary-600 dark:text-primary-400" />
                  All Slides Overview
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {carousel.slides.map((slide, index) => (
                    <Card
                      key={index}
                      className={cn(
                        "cursor-pointer hover:shadow-lg transition-all",
                        currentSlide === index && "ring-2 ring-primary-500 dark:ring-primary-400"
                      )}
                      onClick={() => setCurrentSlide(index)}
                    >
                      <CardContent className="p-4">
                        <div className="flex items-center justify-between mb-2">
                          <span className="font-medium text-gray-900 dark:text-gray-100">
                            Slide {slide.index}
                          </span>
                          <span className={cn(
                            "px-2 py-1 rounded text-xs font-medium border",
                            getRoleColor(slide.role)
                          )}>
                            {slide.role}
                          </span>
                        </div>
                        <h4 className="font-semibold text-gray-800 dark:text-gray-200 mb-1 line-clamp-2">
                          {slide.title}
                        </h4>
                        <p className="text-sm text-gray-600 dark:text-gray-400 line-clamp-2">
                          {slide.subtitle}
                        </p>
                        {slide.bullets.length > 0 && (
                          <p className="text-xs text-gray-500 dark:text-gray-500 mt-2">
                            {slide.bullets.length} bullet points
                          </p>
                        )}
                      </CardContent>
                    </Card>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Caption */}
            {carousel.caption && (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <SparklesIcon className="h-5 w-5 mr-2 text-secondary-600 dark:text-secondary-400" />
                    Caption
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="bg-white dark:bg-gray-800 p-4 rounded-xl border border-gray-200 dark:border-gray-700">
                    <p className="text-gray-700 dark:text-gray-300 whitespace-pre-wrap">{carousel.caption.text}</p>
                  </div>
                  
                  {/* Emojis Used */}
                  {carousel.caption.emojis_used && carousel.caption.emojis_used.length > 0 && (
                    <div>
                      <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Emojis Used</p>
                      <div className="flex gap-3">
                        {carousel.caption.emojis_used.map((emoji, idx) => (
                          <span key={idx} className="text-2xl">{emoji}</span>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* SEO Info */}
                  {carousel.caption.seo && (
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      {carousel.caption.seo.keywords_used && carousel.caption.seo.keywords_used.length > 0 && (
                        <Card variant="filled">
                          <CardContent className="p-4">
                            <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Keywords Used</p>
                            <div className="flex flex-wrap gap-2">
                              {carousel.caption.seo.keywords_used.map((keyword, idx) => (
                                <span key={idx} className="px-2 py-1 bg-primary-100 dark:bg-primary-900/20 text-primary-800 dark:text-primary-400 rounded text-xs font-medium">
                                  {keyword}
                                </span>
                              ))}
                            </div>
                          </CardContent>
                        </Card>
                      )}
                      {carousel.caption.seo.lsi_terms_used && carousel.caption.seo.lsi_terms_used.length > 0 && (
                        <Card variant="filled">
                          <CardContent className="p-4">
                            <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">LSI Terms Used</p>
                            <div className="flex flex-wrap gap-2">
                              {carousel.caption.seo.lsi_terms_used.map((term, idx) => (
                                <span key={idx} className="px-2 py-1 bg-secondary-100 dark:bg-secondary-900/20 text-secondary-800 dark:text-secondary-400 rounded text-xs font-medium">
                                  {term}
                                </span>
                              ))}
                            </div>
                          </CardContent>
                        </Card>
                      )}
                    </div>
                  )}
                </CardContent>
              </Card>
            )}

            {/* Hashtags */}
            {carousel.hashtags && carousel.hashtags.length > 0 && (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center justify-between">
                    <span className="flex items-center">
                      <HashtagIcon className="h-5 w-5 mr-2 text-primary-600 dark:text-primary-400" />
                      Hashtags ({carousel.hashtags.length})
                    </span>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => navigator.clipboard.writeText(carousel.hashtags.map(h => `#${h}`).join(' '))}
                      leftIcon={<DocumentDuplicateIcon className="h-4 w-4" />}
                    >
                      Copy All
                    </Button>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="flex flex-wrap gap-2">
                    {carousel.hashtags.map((hashtag, idx) => (
                      <span key={idx} className="px-3 py-1 bg-primary-100 dark:bg-primary-900/20 text-primary-800 dark:text-primary-400 rounded-full text-sm font-medium border border-primary-200 dark:border-primary-700">
                        #{hashtag}
                      </span>
                    ))}
                  </div>
                </CardContent>
              </Card>
            )}
          </div>
        )}

        {/* Caption Tab - NEW */}
        {activeTab === 'caption' && carousel.caption_structured && (
          <div className="space-y-6 animate-fade-in">
            {/* Structured Caption */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <SparklesIcon className="h-5 w-5 mr-2 text-secondary-600 dark:text-secondary-400" />
                  Structured Caption (7 Sections)
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {/* Hook */}
                <div className="bg-yellow-50 dark:bg-yellow-900/20 p-4 rounded-lg border-l-4 border-yellow-500">
                  <div className="flex justify-between mb-2">
                    <p className="text-xs font-semibold text-yellow-700 dark:text-yellow-400 uppercase">Hook (125 chars)</p>
                    <span className="text-xs text-yellow-600 dark:text-yellow-500">{carousel.caption_structured.hook_125chars.length} chars</span>
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

        {/* Engagement Tab - NEW */}
        {activeTab === 'engagement' && carousel.engagement_tactics && (
          <div className="space-y-6 animate-fade-in">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <FireIcon className="h-5 w-5 mr-2 text-orange-600 dark:text-orange-400" />
                  Engagement Optimization Tactics
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {/* Swipe Completion */}
                <div className="bg-blue-50 dark:bg-blue-900/20 p-4 rounded-lg border border-blue-200 dark:border-blue-700">
                  <div className="flex items-center space-x-2 mb-2">
                    <PhotoIcon className="h-4 w-4 text-blue-600 dark:text-blue-400" />
                    <p className="text-sm font-semibold text-blue-700 dark:text-blue-400">Swipe Completion Strategy</p>
                  </div>
                  <p className="text-sm text-gray-700 dark:text-gray-300">{carousel.engagement_tactics.swipe_completion_strategy}</p>
                </div>
                
                {/* Save Trigger */}
                <div className="bg-green-50 dark:bg-green-900/20 p-4 rounded-lg border border-green-200 dark:border-green-700">
                  <div className="flex items-center space-x-2 mb-2">
                    <CheckCircleIcon className="h-4 w-4 text-green-600 dark:text-green-400" />
                    <p className="text-sm font-semibold text-green-700 dark:text-green-400">Save Trigger</p>
                  </div>
                  <p className="text-sm text-gray-700 dark:text-gray-300">{carousel.engagement_tactics.save_trigger}</p>
                </div>
                
                {/* Share Trigger */}
                <div className="bg-purple-50 dark:bg-purple-900/20 p-4 rounded-lg border border-purple-200 dark:border-purple-700">
                  <div className="flex items-center space-x-2 mb-2">
                    <SparklesIcon className="h-4 w-4 text-purple-600 dark:text-purple-400" />
                    <p className="text-sm font-semibold text-purple-700 dark:text-purple-400">Share Trigger</p>
                  </div>
                  <p className="text-sm text-gray-700 dark:text-gray-300">{carousel.engagement_tactics.share_trigger}</p>
                </div>
                
                {/* Comment Bait */}
                <div className="bg-indigo-50 dark:bg-indigo-900/20 p-4 rounded-lg border border-indigo-200 dark:border-indigo-700">
                  <div className="flex items-center space-x-2 mb-2">
                    <ChatBubbleLeftIcon className="h-4 w-4 text-indigo-600 dark:text-indigo-400" />
                    <p className="text-sm font-semibold text-indigo-700 dark:text-indigo-400">Comment Bait</p>
                  </div>
                  <p className="text-sm text-gray-700 dark:text-gray-300">{carousel.engagement_tactics.comment_bait}</p>
                </div>
                
                {/* Thumbnail Hook */}
                <div className="bg-orange-50 dark:bg-orange-900/20 p-4 rounded-lg border border-orange-200 dark:border-orange-700">
                  <div className="flex items-center space-x-2 mb-2">
                    <FireIcon className="h-4 w-4 text-orange-600 dark:text-orange-400" />
                    <p className="text-sm font-semibold text-orange-700 dark:text-orange-400">Thumbnail Hook (Slide 1)</p>
                  </div>
                  <p className="text-sm text-gray-700 dark:text-gray-300">{carousel.engagement_tactics.thumbnail_hook}</p>
                </div>
              </CardContent>
            </Card>
          </div>
        )}

        {/* Accessibility Tab - NEW */}
        {activeTab === 'accessibility' && carousel.accessibility && (
          <div className="space-y-6 animate-fade-in">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <CheckCircleIcon className="h-5 w-5 mr-2 text-green-600 dark:text-green-400" />
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
                    <p className="text-sm font-medium text-gray-900 dark:text-gray-100">Alt Texts</p>
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
                    <p className="text-sm font-medium text-gray-900 dark:text-gray-100">Contrast</p>
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

        {/* Design System Tab */}
        {activeTab === 'design' && (
          <div className="space-y-6 animate-fade-in">
            {/* Color Palettes */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <SwatchIcon className="h-5 w-5 mr-2 text-secondary-600 dark:text-secondary-400" />
                  Color Palettes
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {carousel.design_system.color_palette.map((palette, idx) => (
                  <div key={idx} className="space-y-2">
                    <h4 className="font-medium text-gray-900 dark:text-gray-100">{palette.name}</h4>
                    <div className="flex gap-2">
                      {palette.values.map((color, colorIdx) => (
                        <div key={colorIdx} className="flex flex-col items-center">
                          <div
                            className="w-16 h-16 rounded-lg shadow-md border border-gray-200 dark:border-gray-700"
                            style={{ backgroundColor: color }}
                          />
                          <span className="text-xs text-gray-600 dark:text-gray-400 mt-1 font-mono">
                            {color}
                          </span>
                        </div>
                      ))}
                    </div>
                  </div>
                ))}
              </CardContent>
            </Card>

            {/* Font Pairings */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <BeakerIcon className="h-5 w-5 mr-2 text-primary-600 dark:text-primary-400" />
                  Typography
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {carousel.design_system.font_pairings.map((pairing, idx) => (
                  <Card key={idx} variant="filled">
                    <CardContent className="p-4">
                      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <div>
                          <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Headline</p>
                          <p className="text-lg font-semibold text-gray-900 dark:text-gray-100">{pairing.headline}</p>
                        </div>
                        <div>
                          <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Body</p>
                          <p className="text-gray-700 dark:text-gray-300">{pairing.body}</p>
                        </div>
                        {pairing.code && (
                          <div>
                            <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Code</p>
                            <p className="font-mono text-sm text-gray-700 dark:text-gray-300">{pairing.code}</p>
                          </div>
                        )}
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </CardContent>
            </Card>

            {/* Grid System */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Squares2X2Icon className="h-5 w-5 mr-2 text-success-600 dark:text-success-400" />
                  Grid System
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <Card variant="filled">
                    <CardContent className="p-4 text-center">
                      <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Ratio</p>
                      <p className="text-lg font-semibold text-gray-900 dark:text-gray-100">{carousel.design_system.grid.ratio}</p>
                    </CardContent>
                  </Card>
                  <Card variant="filled">
                    <CardContent className="p-4 text-center">
                      <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Size</p>
                      <p className="text-lg font-semibold text-gray-900 dark:text-gray-100">{carousel.design_system.grid.size_px}</p>
                    </CardContent>
                  </Card>
                  <Card variant="filled">
                    <CardContent className="p-4 text-center">
                      <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Safe Margins</p>
                      <p className="text-lg font-semibold text-gray-900 dark:text-gray-100">{carousel.design_system.grid.safe_margins_px}px</p>
                    </CardContent>
                  </Card>
                  <Card variant="filled">
                    <CardContent className="p-4 text-center">
                      <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Columns</p>
                      <p className="text-lg font-semibold text-gray-900 dark:text-gray-100">{carousel.design_system.grid.column_system}</p>
                    </CardContent>
                  </Card>
                </div>
              </CardContent>
            </Card>
          </div>
        )}

        {/* Images Tab */}
        {activeTab === 'images' && (
          <div className="space-y-6 animate-fade-in">
            {carousel.image_prompts.map((imagePrompt, index) => (
              <Card key={index} className="hover:shadow-lg transition-shadow">
                <CardHeader>
                  <CardTitle className="flex items-center justify-between">
                    <span className="flex items-center">
                      <PaintBrushIcon className="h-5 w-5 mr-2 text-primary-600 dark:text-primary-400" />
                      {imagePrompt.title}
                    </span>
                    <span className="px-3 py-1 bg-primary-100 dark:bg-primary-900/20 text-primary-800 dark:text-primary-400 rounded-full text-sm font-medium">
                      {imagePrompt.role}
                    </span>
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  {/* Main Prompt */}
                  <div>
                    <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Prompt</p>
                    <div className="bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-blue-900/20 dark:to-indigo-900/20 p-4 rounded-xl border border-blue-200 dark:border-blue-700">
                      <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
                        {imagePrompt.prompt}
                      </p>
                    </div>
                  </div>

                  {/* Negative Prompt */}
                  <div>
                    <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Negative Prompt</p>
                    <div className="bg-error-50 dark:bg-error-900/20 p-4 rounded-xl border border-error-200 dark:border-error-700">
                      <p className="text-error-700 dark:text-error-400">
                        {imagePrompt.negative_prompt}
                      </p>
                    </div>
                  </div>

                  {/* Style Notes */}
                  <div>
                    <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Style Notes</p>
                    <div className="bg-warning-50 dark:bg-warning-900/20 p-4 rounded-xl border border-warning-200 dark:border-warning-700">
                      <p className="text-warning-700 dark:text-warning-400">
                        {imagePrompt.style_notes}
                      </p>
                    </div>
                  </div>

                  {/* Technical Details */}
                  <div className="grid grid-cols-2 gap-4">
                    <Card variant="filled">
                      <CardContent className="p-3">
                        <p className="text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">Dimensions</p>
                        <p className="text-sm font-semibold text-gray-900 dark:text-gray-100">{imagePrompt.size_px}</p>
                      </CardContent>
                    </Card>
                    <Card variant="filled">
                      <CardContent className="p-3">
                        <p className="text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">Aspect Ratio</p>
                        <p className="text-sm font-semibold text-gray-900 dark:text-gray-100">{imagePrompt.ratio}</p>
                      </CardContent>
                    </Card>
                  </div>

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
                </CardContent>
              </Card>
            ))}

            {/* Image Prompts by Slide */}
            {carousel.image_prompts_by_slide && carousel.image_prompts_by_slide.length > 0 && (
              <Card>
                <CardHeader>
                  <CardTitle>Image Assignments by Slide</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    {carousel.image_prompts_by_slide.map((assignment, idx) => (
                      <div key={idx} className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
                        <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                          Slide {assignment.slide_index}
                        </span>
                        <span className="px-2 py-1 bg-primary-100 dark:bg-primary-900/20 text-primary-800 dark:text-primary-400 rounded text-xs font-medium">
                          {assignment.role}
                        </span>
                        <span className="text-sm text-gray-600 dark:text-gray-400 italic">
                          {assignment.note}
                        </span>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            )}
          </div>
        )}
      </div>

      {/* Footer with Compliance Info */}
      <div className="border-t border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900 p-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-6 text-sm">
            <div className="flex items-center">
              <PhotoIcon className="h-4 w-4 mr-1 text-gray-500 dark:text-gray-400" />
              <span className="text-gray-600 dark:text-gray-400">
                {carousel.slides?.length || 0} slides
              </span>
            </div>
            <div className="flex items-center">
              <ChartBarIcon className="h-4 w-4 mr-1 text-gray-500 dark:text-gray-400" />
              <span className="text-gray-600 dark:text-gray-400">
                {carousel.compliance?.caption_word_count || 0} words
              </span>
            </div>
            <div className="flex items-center">
              <HashtagIcon className="h-4 w-4 mr-1 text-gray-500 dark:text-gray-400" />
              <span className="text-gray-600 dark:text-gray-400">
                {carousel.hashtags?.length || 0} hashtags
              </span>
            </div>
            {carousel.image_prompts && carousel.image_prompts.length > 0 && (
              <div className="flex items-center">
                <PaintBrushIcon className="h-4 w-4 mr-1 text-gray-500 dark:text-gray-400" />
                <span className="text-gray-600 dark:text-gray-400">
                  {carousel.image_prompts.length} images
                </span>
              </div>
            )}
          </div>
          {carousel.compliance?.checks && (
            <div className="flex items-center text-success-600 dark:text-success-400">
              <CheckCircleIcon className="h-4 w-4 mr-1" />
              <span className="text-sm font-medium">
                {carousel.compliance.checks.length} checks passed
              </span>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default InstagramCarouselView;
