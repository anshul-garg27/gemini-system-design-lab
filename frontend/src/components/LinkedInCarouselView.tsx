import React, { useState } from 'react';
import { 
  DocumentTextIcon,
  HashtagIcon,
  DocumentDuplicateIcon,
  PhotoIcon,
  CheckCircleIcon,
  ChartBarIcon,
  ArrowRightIcon,
  ChevronLeftIcon,
  ChevronRightIcon,
  ExclamationTriangleIcon,
  LightBulbIcon,
  ShieldCheckIcon,
  PlayIcon,
  DocumentIcon
} from '@heroicons/react/24/outline';
import { Card, CardContent, CardHeader, CardTitle } from './ui/Card';
import { Button } from './ui/Button';
import { cn } from '../lib/utils';

// Interfaces
interface Slide {
  index: number;
  role: string;
  title: string;
  subtitle: string;
  bullets: string[];
  overlay_text: string;
  design_note: string;
  layout: string;
  iconography: string;
  contrast_notes: string;
  alt_text: string;
  data_points?: any[];
}

interface HashtagsGrouped {
  broad: string[];
  niche: string[];
  micro_niche: string[];
  intent: string[];
  branded: string[];
}

interface ImagePrompt {
  role: string;
  title: string;
  prompt: string;
  negative_prompt: string;
  style_notes: string;
  ratio: string;
  size_px: string;
  alt_text: string;
}

interface DocExport {
  filename_suggestion: string;
  ratio: string;
  size_px: string;
  safe_margins_px: number;
  page_count: number;
}

interface Compliance {
  slides_total: number;
  numbers_slides_count: number;
  hashtags_count: number;
  image_prompt_count: number;
  description_chars_count: number;
  checks: string[];
}

interface LinkedInCarouselContent {
  doc_title: string;
  slides: Slide[];
  description: string;
  chars_count: number;
  hashtags: string[];
  hashtags_grouped: HashtagsGrouped;
  image_prompts: ImagePrompt[];
  image_prompts_by_slide?: any[];
  doc_export: DocExport;
  compliance: Compliance;
}

interface LinkedInCarouselViewProps {
  content: any;
}

export const LinkedInCarouselView: React.FC<LinkedInCarouselViewProps> = ({ content }) => {
  const [activeTab, setActiveTab] = useState<'slides' | 'images' | 'analytics'>('slides');
  const [currentSlide, setCurrentSlide] = useState(0);
  const [viewMode, setViewMode] = useState<'single' | 'grid'>('single');

  // Parse content
  const carousel: LinkedInCarouselContent = content.envelope?.content || content.content || content;
  const {
    doc_title = '',
    slides = [],
    description = '',
    chars_count = 0,
    hashtags = [],
    hashtags_grouped = { broad: [], niche: [], micro_niche: [], intent: [], branded: [] },
    image_prompts = [],
    doc_export = {
      filename_suggestion: '',
      ratio: '',
      size_px: '',
      safe_margins_px: 0,
      page_count: 0
    },
    compliance = {
      slides_total: 0,
      numbers_slides_count: 0,
      hashtags_count: 0,
      image_prompt_count: 0,
      description_chars_count: 0,
      checks: []
    }
  } = carousel;

  // Copy functions
  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
  };

  const copySlideContent = (slide: Slide) => {
    const content = `${slide.title}\n\n${slide.subtitle}\n\n${slide.bullets.filter(b => b).join('\n')}`;
    copyToClipboard(content);
  };

  const copyFullDocument = () => {
    const fullContent = slides.map(slide => 
      `Slide ${slide.index}: ${slide.title}\n${slide.subtitle}\n${slide.bullets.filter(b => b).join('\n')}`
    ).join('\n\n---\n\n');
    copyToClipboard(fullContent);
  };

  const copyDescription = () => {
    const fullDescription = `${description}\n\n${hashtags.join(' ')}`;
    copyToClipboard(fullDescription);
  };

  // Navigation
  const goToSlide = (index: number) => {
    setCurrentSlide(Math.max(0, Math.min(slides.length - 1, index)));
  };

  const nextSlide = () => goToSlide(currentSlide + 1);
  const prevSlide = () => goToSlide(currentSlide - 1);

  // Get role icon
  const getRoleIcon = (role: string) => {
    switch (role) {
      case 'cover':
        return <DocumentTextIcon className="h-5 w-5" />;
      case 'problem':
        return <ExclamationTriangleIcon className="h-5 w-5" />;
      case 'core_idea':
        return <LightBulbIcon className="h-5 w-5" />;
      case 'diagram':
        return <ChartBarIcon className="h-5 w-5" />;
      case 'metrics_roi':
        return <ChartBarIcon className="h-5 w-5" />;
      case 'mini_case':
        return <DocumentIcon className="h-5 w-5" />;
      case 'steps':
        return <PlayIcon className="h-5 w-5" />;
      case 'risks':
        return <ShieldCheckIcon className="h-5 w-5" />;
      case 'cta':
        return <ArrowRightIcon className="h-5 w-5" />;
      default:
        return <DocumentTextIcon className="h-5 w-5" />;
    }
  };

  const getRoleColor = (role: string) => {
    switch (role) {
      case 'cover':
        return 'border-blue-500 bg-blue-50 dark:bg-blue-900/20';
      case 'problem':
        return 'border-red-500 bg-red-50 dark:bg-red-900/20';
      case 'core_idea':
        return 'border-green-500 bg-green-50 dark:bg-green-900/20';
      case 'diagram':
        return 'border-purple-500 bg-purple-50 dark:bg-purple-900/20';
      case 'metrics_roi':
        return 'border-yellow-500 bg-yellow-50 dark:bg-yellow-900/20';
      case 'mini_case':
        return 'border-indigo-500 bg-indigo-50 dark:bg-indigo-900/20';
      case 'steps':
        return 'border-teal-500 bg-teal-50 dark:bg-teal-900/20';
      case 'risks':
        return 'border-orange-500 bg-orange-50 dark:bg-orange-900/20';
      case 'cta':
        return 'border-pink-500 bg-pink-50 dark:bg-pink-900/20';
      default:
        return 'border-gray-500 bg-gray-50 dark:bg-gray-900/20';
    }
  };

  return (
    <div className="bg-white dark:bg-gray-900 rounded-3xl shadow-2xl max-w-7xl w-full max-h-[90vh] overflow-hidden flex flex-col">
      {/* Header */}
      <div className="bg-blue-700 text-white p-6">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold flex items-center">
              <DocumentTextIcon className="h-8 w-8 mr-3" />
              LinkedIn Carousel
            </h2>
            <p className="text-blue-100 mt-1">
              {doc_title || content.meta?.topic_title || 'LinkedIn Carousel Document'}
            </p>
          </div>
          <div className="flex space-x-4 text-sm">
            <div className="text-center">
              <div className="text-2xl font-bold">{slides.length}</div>
              <div className="text-blue-100">Slides</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold">{chars_count}</div>
              <div className="text-blue-100">Characters</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold">{hashtags.length}</div>
              <div className="text-blue-100">Hashtags</div>
            </div>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex border-b border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800/50">
        {(['slides', 'images', 'analytics'] as const).map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={cn(
              'flex-1 px-6 py-3 text-sm font-medium transition-all capitalize',
              activeTab === tab
                ? 'text-blue-700 dark:text-blue-400 border-b-2 border-blue-700 dark:border-blue-400 bg-white dark:bg-gray-800'
                : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-100'
            )}
          >
            {tab === 'slides' && <DocumentTextIcon className="h-4 w-4 inline mr-2" />}
            {tab === 'images' && <PhotoIcon className="h-4 w-4 inline mr-2" />}
            {tab === 'analytics' && <ChartBarIcon className="h-4 w-4 inline mr-2" />}
            {tab}
          </button>
        ))}
      </div>

      {/* Content */}
      <div className="flex-1 overflow-y-auto p-6">
        {/* Slides Tab */}
        {activeTab === 'slides' && (
          <div className="space-y-6">
            {/* View Mode Toggle */}
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
                Document Slides
              </h3>
              <div className="flex space-x-2">
                <Button
                  variant={viewMode === 'single' ? 'primary' : 'ghost'}
                  size="sm"
                  onClick={() => setViewMode('single')}
                >
                  Single View
                </Button>
                <Button
                  variant={viewMode === 'grid' ? 'primary' : 'ghost'}
                  size="sm"
                  onClick={() => setViewMode('grid')}
                >
                  Grid View
                </Button>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={copyFullDocument}
                  leftIcon={<DocumentDuplicateIcon className="h-4 w-4" />}
                >
                  Copy All
                </Button>
              </div>
            </div>

            {viewMode === 'single' && slides.length > 0 && (
              <>
                {/* Current Slide */}
                <Card className={cn('border-2', getRoleColor(slides[currentSlide].role))}>
                  <CardHeader>
                    <CardTitle className="flex items-center justify-between">
                      <span className="flex items-center">
                        {getRoleIcon(slides[currentSlide].role)}
                        <span className="ml-2">
                          Slide {slides[currentSlide].index} - {slides[currentSlide].role.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
                        </span>
                      </span>
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => copySlideContent(slides[currentSlide])}
                        leftIcon={<DocumentDuplicateIcon className="h-4 w-4" />}
                      >
                        Copy
                      </Button>
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      <div>
                        <h4 className="text-xl font-bold text-gray-900 dark:text-gray-100 mb-2">
                          {slides[currentSlide].title}
                        </h4>
                        <p className="text-gray-700 dark:text-gray-300 text-lg">
                          {slides[currentSlide].subtitle}
                        </p>
                      </div>

                      {slides[currentSlide].bullets.filter(b => b).length > 0 && (
                        <div className="space-y-2">
                          {slides[currentSlide].bullets.filter(b => b).map((bullet, index) => (
                            <div key={index} className="flex items-start">
                              <span className="text-blue-700 dark:text-blue-400 mr-2">•</span>
                              <span className="text-gray-700 dark:text-gray-300">{bullet}</span>
                            </div>
                          ))}
                        </div>
                      )}

                      <div className="grid grid-cols-2 gap-4 pt-4 border-t border-gray-200 dark:border-gray-700">
                        <div>
                          <p className="text-sm font-medium text-gray-600 dark:text-gray-400 mb-1">
                            Design Note:
                          </p>
                          <p className="text-sm text-gray-600 dark:text-gray-400">
                            {slides[currentSlide].design_note}
                          </p>
                        </div>
                        <div>
                          <p className="text-sm font-medium text-gray-600 dark:text-gray-400 mb-1">
                            Layout:
                          </p>
                          <p className="text-sm text-gray-600 dark:text-gray-400">
                            {slides[currentSlide].layout}
                          </p>
                        </div>
                        <div>
                          <p className="text-sm font-medium text-gray-600 dark:text-gray-400 mb-1">
                            Iconography:
                          </p>
                          <p className="text-sm text-gray-600 dark:text-gray-400">
                            {slides[currentSlide].iconography}
                          </p>
                        </div>
                        <div>
                          <p className="text-sm font-medium text-gray-600 dark:text-gray-400 mb-1">
                            Overlay Text:
                          </p>
                          <p className="text-sm font-semibold text-blue-700 dark:text-blue-400">
                            {slides[currentSlide].overlay_text}
                          </p>
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                {/* Navigation */}
                <div className="flex items-center justify-between">
                  <Button
                    variant="ghost"
                    onClick={prevSlide}
                    disabled={currentSlide === 0}
                    leftIcon={<ChevronLeftIcon className="h-4 w-4" />}
                  >
                    Previous
                  </Button>
                  <div className="flex space-x-2">
                    {slides.map((_, index) => (
                      <button
                        key={index}
                        onClick={() => setCurrentSlide(index)}
                        className={cn(
                          'w-2 h-2 rounded-full transition-all',
                          currentSlide === index
                            ? 'bg-blue-700 dark:bg-blue-400 w-8'
                            : 'bg-gray-300 dark:bg-gray-600 hover:bg-gray-400 dark:hover:bg-gray-500'
                        )}
                      />
                    ))}
                  </div>
                  <Button
                    variant="ghost"
                    onClick={nextSlide}
                    disabled={currentSlide === slides.length - 1}
                    rightIcon={<ChevronRightIcon className="h-4 w-4" />}
                  >
                    Next
                  </Button>
                </div>
              </>
            )}

            {viewMode === 'grid' && (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {slides.map((slide) => (
                  <Card
                    key={slide.index}
                    className={cn(
                      'cursor-pointer hover:shadow-lg transition-all',
                      'border-2',
                      getRoleColor(slide.role),
                      currentSlide === slide.index - 1 ? 'ring-2 ring-blue-500' : ''
                    )}
                    onClick={() => setCurrentSlide(slide.index - 1)}
                  >
                    <CardContent className="p-4">
                      <div className="flex items-start justify-between mb-2">
                        <div className="flex items-center">
                          {getRoleIcon(slide.role)}
                          <span className="ml-2 text-sm font-medium text-gray-600 dark:text-gray-400">
                            Slide {slide.index}
                          </span>
                        </div>
                        <span className="text-xs bg-gray-200 dark:bg-gray-700 px-2 py-1 rounded text-gray-700 dark:text-gray-300">
                          {slide.role.replace('_', ' ')}
                        </span>
                      </div>
                      <h5 className="font-semibold text-gray-900 dark:text-gray-100 mb-1 line-clamp-2">
                        {slide.title}
                      </h5>
                      <p className="text-sm text-gray-600 dark:text-gray-400 line-clamp-2">
                        {slide.subtitle}
                      </p>
                      {slide.bullets.filter(b => b).length > 0 && (
                        <p className="text-xs text-gray-500 dark:text-gray-500 mt-2">
                          {slide.bullets.filter(b => b).length} bullet points
                        </p>
                      )}
                    </CardContent>
                  </Card>
                ))}
              </div>
            )}

            {/* Description */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center justify-between">
                  <span className="flex items-center">
                    <DocumentTextIcon className="h-5 w-5 mr-2 text-blue-700 dark:text-blue-400" />
                    Post Description
                  </span>
                  <div className="flex items-center space-x-2">
                    <span className="text-sm text-gray-600 dark:text-gray-400">
                      {chars_count}/3000
                    </span>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={copyDescription}
                      leftIcon={<DocumentDuplicateIcon className="h-4 w-4" />}
                    >
                      Copy
                    </Button>
                  </div>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="bg-gray-50 dark:bg-gray-800 p-4 rounded-xl">
                  <p className="text-gray-700 dark:text-gray-300 whitespace-pre-wrap">
                    {description}
                  </p>
                  <div className="mt-4 flex flex-wrap gap-2">
                    {hashtags.map((tag, index) => (
                      <span
                        key={index}
                        className="inline-flex items-center px-3 py-1 rounded-full text-sm bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300"
                      >
                        <HashtagIcon className="h-3 w-3 mr-1" />
                        {tag.replace('#', '')}
                      </span>
                    ))}
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        )}

        {/* Images Tab */}
        {activeTab === 'images' && (
          <div className="space-y-6">
            {/* Document Export Settings */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <DocumentIcon className="h-5 w-5 mr-2 text-blue-700 dark:text-blue-400" />
                  Document Export Settings
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <div>
                    <p className="text-sm font-medium text-gray-700 dark:text-gray-300">Ratio</p>
                    <p className="text-gray-600 dark:text-gray-400">{doc_export.ratio}</p>
                  </div>
                  <div>
                    <p className="text-sm font-medium text-gray-700 dark:text-gray-300">Size</p>
                    <p className="text-gray-600 dark:text-gray-400">{doc_export.size_px}</p>
                  </div>
                  <div>
                    <p className="text-sm font-medium text-gray-700 dark:text-gray-300">Margins</p>
                    <p className="text-gray-600 dark:text-gray-400">{doc_export.safe_margins_px}px</p>
                  </div>
                  <div>
                    <p className="text-sm font-medium text-gray-700 dark:text-gray-300">Pages</p>
                    <p className="text-gray-600 dark:text-gray-400">{doc_export.page_count}</p>
                  </div>
                </div>
                <div className="mt-3">
                  <p className="text-sm font-medium text-gray-700 dark:text-gray-300">Filename</p>
                  <p className="text-gray-600 dark:text-gray-400 text-sm font-mono">
                    {doc_export.filename_suggestion}
                  </p>
                </div>
              </CardContent>
            </Card>

            {/* Image Prompts */}
            {image_prompts.map((prompt, index) => (
              <Card key={index}>
                <CardHeader>
                  <CardTitle className="flex items-center justify-between">
                    <span className="flex items-center">
                      <PhotoIcon className="h-5 w-5 mr-2 text-purple-600 dark:text-purple-400" />
                      {prompt.title}
                    </span>
                    <span className="text-sm font-normal text-gray-500 dark:text-gray-400">
                      {prompt.ratio} • {prompt.size_px}
                    </span>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div>
                      <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Prompt:</p>
                      <div className="bg-gray-50 dark:bg-gray-800 p-4 rounded-lg">
                        <p className="text-gray-700 dark:text-gray-300 text-sm">{prompt.prompt}</p>
                      </div>
                    </div>
                    
                    {prompt.negative_prompt && (
                      <div>
                        <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Negative Prompt:</p>
                        <div className="bg-red-50 dark:bg-red-900/20 p-4 rounded-lg">
                          <p className="text-red-700 dark:text-red-300 text-sm">{prompt.negative_prompt}</p>
                        </div>
                      </div>
                    )}
                    
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Style Notes:</p>
                        <p className="text-gray-600 dark:text-gray-400 text-sm">{prompt.style_notes}</p>
                      </div>
                      <div>
                        <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Alt Text:</p>
                        <p className="text-gray-600 dark:text-gray-400 text-sm">{prompt.alt_text}</p>
                      </div>
                    </div>

                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => copyToClipboard(prompt.prompt)}
                      leftIcon={<DocumentDuplicateIcon className="h-4 w-4" />}
                    >
                      Copy Prompt
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        )}

        {/* Analytics Tab */}
        {activeTab === 'analytics' && (
          <div className="space-y-6">
            {/* Key Metrics */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <ChartBarIcon className="h-5 w-5 mr-2 text-blue-700 dark:text-blue-400" />
                  Document Analytics
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <div className="bg-blue-50 dark:bg-blue-900/20 p-4 rounded-lg">
                    <p className="text-2xl font-bold text-gray-900 dark:text-gray-100">
                      {compliance.slides_total}
                    </p>
                    <p className="text-sm text-gray-600 dark:text-gray-400">Total Slides</p>
                  </div>
                  <div className="bg-green-50 dark:bg-green-900/20 p-4 rounded-lg">
                    <p className="text-2xl font-bold text-gray-900 dark:text-gray-100">
                      {compliance.numbers_slides_count}
                    </p>
                    <p className="text-sm text-gray-600 dark:text-gray-400">Data Slides</p>
                  </div>
                  <div className="bg-purple-50 dark:bg-purple-900/20 p-4 rounded-lg">
                    <p className="text-2xl font-bold text-gray-900 dark:text-gray-100">
                      {compliance.hashtags_count}
                    </p>
                    <p className="text-sm text-gray-600 dark:text-gray-400">Hashtags</p>
                  </div>
                  <div className="bg-yellow-50 dark:bg-yellow-900/20 p-4 rounded-lg">
                    <p className="text-2xl font-bold text-gray-900 dark:text-gray-100">
                      {compliance.description_chars_count}
                    </p>
                    <p className="text-sm text-gray-600 dark:text-gray-400">Description Chars</p>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Slide Role Distribution */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <DocumentTextIcon className="h-5 w-5 mr-2 text-purple-600 dark:text-purple-400" />
                  Slide Type Distribution
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {Object.entries(
                    slides.reduce((acc: Record<string, number>, slide) => {
                      acc[slide.role] = (acc[slide.role] || 0) + 1;
                      return acc;
                    }, {})
                  ).map(([role, count]) => (
                    <div key={role} className="flex items-center justify-between">
                      <div className="flex items-center">
                        {getRoleIcon(role)}
                        <span className="ml-2 text-sm text-gray-700 dark:text-gray-300">
                          {role.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
                        </span>
                      </div>
                      <span className="text-sm font-medium text-gray-900 dark:text-gray-100">
                        {count}
                      </span>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Hashtag Groups */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <HashtagIcon className="h-5 w-5 mr-2 text-green-600 dark:text-green-400" />
                  Hashtag Categories
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {Object.entries(hashtags_grouped).map(([category, tags]) => (
                    <div key={category}>
                      <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2 capitalize">
                        {category.replace('_', ' ')}:
                      </p>
                      <div className="flex flex-wrap gap-2">
                        {tags.map((tag, index) => (
                          <span
                            key={index}
                            className="text-xs px-2 py-1 rounded-full bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300"
                          >
                            {tag}
                          </span>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Compliance Checks */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <CheckCircleIcon className="h-5 w-5 mr-2 text-green-600 dark:text-green-400" />
                  Compliance Checks
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  {compliance.checks.map((check, index) => (
                    <div key={index} className="flex items-start">
                      <CheckCircleIcon className="h-5 w-5 text-green-500 mr-2 flex-shrink-0 mt-0.5" />
                      <span className="text-sm text-gray-600 dark:text-gray-400">{check}</span>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>
        )}
      </div>

      {/* Footer */}
      <div className="border-t border-gray-200 dark:border-gray-700 p-4 bg-gray-50 dark:bg-gray-800/50">
        <div className="flex items-center justify-between text-sm text-gray-600 dark:text-gray-400">
          <span>
            Generated with {content.meta?.model_version || 'AI'} • 
            Prompt v{content.meta?.prompt_version || '1.0'}
          </span>
          <div className="flex items-center space-x-4">
            <span className="flex items-center">
              <DocumentTextIcon className="h-4 w-4 mr-1" />
              {slides.length} slides
            </span>
            <span className="flex items-center">
              <HashtagIcon className="h-4 w-4 mr-1" />
              {hashtags.length} hashtags
            </span>
            <span className="flex items-center">
              <PhotoIcon className="h-4 w-4 mr-1" />
              {image_prompts.length} images
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};
