import React, { useState } from 'react';
import { 
  PhotoIcon,
  HashtagIcon,
  DocumentDuplicateIcon,
  SparklesIcon,
  ChartBarIcon,
  LinkIcon,
  CheckCircleIcon,
  EyeIcon,
  PaintBrushIcon,
  TagIcon,
  GlobeAltIcon
} from '@heroicons/react/24/outline';
import { Card, CardContent, CardHeader, CardTitle } from './ui/Card';
import { Button } from './ui/Button';
import { cn } from '../lib/utils';

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

interface InstagramPostContent {
  visual_concept: string;
  caption: {
    first_line_hook: string;
    text: string;
    cta: string;
    seo: {
      keywords_used: string[];
      lsi_terms_used: string[];
    };
  };
  hashtags: string[];
  hashtags_grouped: {
    broad: string[];
    niche: string[];
    micro_niche: string[];
    intent: string[];
    branded: string[];
  };
  location_tag_suggestions: string[];
  image_prompts: ImagePrompt[];
  compliance: {
    caption_word_count: number;
    first_line_hook_char_count: number;
    hashtag_count: number;
    image_prompt_count: number;
    checks: string[];
  };
}

interface InstagramPostViewProps {
  content: {
    job_id: string;
    platform: string;
    format: string;
    envelope: {
      content: InstagramPostContent;
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

const InstagramPostView: React.FC<InstagramPostViewProps> = ({ content, onCopy }) => {
  const [activeTab, setActiveTab] = useState<'caption' | 'hashtags' | 'images'>('caption');
  const [expandedSection, setExpandedSection] = useState<string | null>(null);
  
  // Extract content
  const post = content.envelope.content;
  const meta = content.meta || {};

  const getHashtagColor = (type: string) => {
    switch (type) {
      case 'broad': return 'bg-primary-100 dark:bg-primary-900/20 text-primary-800 dark:text-primary-400 border-primary-200 dark:border-primary-700';
      case 'niche': return 'bg-secondary-100 dark:bg-secondary-900/20 text-secondary-800 dark:text-secondary-400 border-secondary-200 dark:border-secondary-700';
      case 'micro_niche': return 'bg-success-100 dark:bg-success-900/20 text-success-800 dark:text-success-400 border-success-200 dark:border-success-700';
      case 'intent': return 'bg-warning-100 dark:bg-warning-900/20 text-warning-800 dark:text-warning-400 border-warning-200 dark:border-warning-700';
      case 'branded': return 'bg-error-100 dark:bg-error-900/20 text-error-800 dark:text-error-400 border-error-200 dark:border-error-700';
      default: return 'bg-gray-100 dark:bg-gray-800 text-gray-800 dark:text-gray-300 border-gray-200 dark:border-gray-700';
    }
  };

  return (
    <div className="bg-white dark:bg-gray-900 rounded-3xl shadow-2xl max-w-6xl w-full max-h-[90vh] overflow-hidden flex flex-col">
      {/* Header */}
      <div className="bg-gradient-to-r from-purple-500 via-pink-500 to-rose-500 text-white p-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="p-3 bg-white/20 backdrop-blur-sm rounded-xl">
              <PhotoIcon className="h-8 w-8" />
            </div>
            <div>
              <h2 className="text-2xl font-bold">Instagram Post</h2>
              {meta.topic_title && (
                <p className="text-purple-100 text-sm mt-1">{meta.topic_title}</p>
              )}
            </div>
          </div>
          <Button
            onClick={onCopy}
            variant="ghost"
            className="bg-white/20 hover:bg-white/30 text-white border-white/30"
            leftIcon={<DocumentDuplicateIcon className="h-4 w-4" />}
          >
            Copy All
          </Button>
        </div>
      </div>

      {/* Tab Navigation */}
      <div className="border-b border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800">
        <div className="flex space-x-1 p-2">
          <Button
            variant={activeTab === 'caption' ? 'primary' : 'ghost'}
            onClick={() => setActiveTab('caption')}
            className={cn(
              "flex-1",
              activeTab === 'caption' && "shadow-sm"
            )}
          >
            <SparklesIcon className="h-4 w-4 mr-2" />
            Caption
          </Button>
          <Button
            variant={activeTab === 'hashtags' ? 'primary' : 'ghost'}
            onClick={() => setActiveTab('hashtags')}
            className={cn(
              "flex-1",
              activeTab === 'hashtags' && "shadow-sm"
            )}
          >
            <HashtagIcon className="h-4 w-4 mr-2" />
            Hashtags
          </Button>
          <Button
            variant={activeTab === 'images' ? 'primary' : 'ghost'}
            onClick={() => setActiveTab('images')}
            className={cn(
              "flex-1",
              activeTab === 'images' && "shadow-sm"
            )}
          >
            <PhotoIcon className="h-4 w-4 mr-2" />
            Images
          </Button>
        </div>
      </div>

      {/* Content Area */}
      <div className="flex-1 overflow-y-auto p-6 bg-gray-50 dark:bg-gray-950">
        {/* Caption Tab */}
        {activeTab === 'caption' && (
          <div className="space-y-6 animate-fade-in">
            {/* Visual Concept */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <EyeIcon className="h-5 w-5 mr-2 text-primary-600 dark:text-primary-400" />
                  Visual Concept
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
                  {post.visual_concept}
                </p>
              </CardContent>
            </Card>

            {/* Caption Content */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <SparklesIcon className="h-5 w-5 mr-2 text-secondary-600 dark:text-secondary-400" />
                  Caption Content
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {/* First Line Hook */}
                <div className="bg-gradient-to-r from-purple-50 to-pink-50 dark:from-purple-900/20 dark:to-pink-900/20 p-4 rounded-xl border border-purple-200 dark:border-purple-700">
                  <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">First Line Hook ({post.compliance.first_line_hook_char_count} chars)</p>
                  <p className="text-lg font-semibold text-gray-900 dark:text-gray-100">
                    {post.caption.first_line_hook}
                  </p>
                </div>

                {/* Main Text */}
                <div>
                  <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Main Content ({post.compliance.caption_word_count} words)</p>
                  <div className="bg-white dark:bg-gray-800 p-4 rounded-xl border border-gray-200 dark:border-gray-700">
                    <p className="text-gray-700 dark:text-gray-300 whitespace-pre-wrap leading-relaxed">
                      {post.caption.text}
                    </p>
                  </div>
                </div>

                {/* CTA */}
                <div className="bg-gradient-to-r from-green-50 to-emerald-50 dark:from-green-900/20 dark:to-emerald-900/20 p-4 rounded-xl border border-green-200 dark:border-green-700">
                  <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2 flex items-center">
                    <LinkIcon className="h-4 w-4 mr-1" />
                    Call to Action
                  </p>
                  <p className="text-green-800 dark:text-green-400 font-medium">
                    {post.caption.cta}
                  </p>
                </div>

                {/* SEO Info */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <Card variant="filled">
                    <CardContent className="p-4">
                      <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Keywords Used</p>
                      <div className="flex flex-wrap gap-2">
                        {post.caption.seo.keywords_used.map((keyword, idx) => (
                          <span key={idx} className="px-2 py-1 bg-primary-100 dark:bg-primary-900/20 text-primary-800 dark:text-primary-400 rounded text-xs font-medium">
                            {keyword}
                          </span>
                        ))}
                      </div>
                    </CardContent>
                  </Card>
                  <Card variant="filled">
                    <CardContent className="p-4">
                      <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">LSI Terms Used</p>
                      <div className="flex flex-wrap gap-2">
                        {post.caption.seo.lsi_terms_used.map((term, idx) => (
                          <span key={idx} className="px-2 py-1 bg-secondary-100 dark:bg-secondary-900/20 text-secondary-800 dark:text-secondary-400 rounded text-xs font-medium">
                            {term}
                          </span>
                        ))}
                      </div>
                    </CardContent>
                  </Card>
                </div>
              </CardContent>
            </Card>
          </div>
        )}

        {/* Hashtags Tab */}
        {activeTab === 'hashtags' && (
          <div className="space-y-6 animate-fade-in">
            {/* All Hashtags */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center justify-between">
                  <span className="flex items-center">
                    <HashtagIcon className="h-5 w-5 mr-2 text-primary-600 dark:text-primary-400" />
                    All Hashtags ({post.hashtags.length})
                  </span>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => navigator.clipboard.writeText(post.hashtags.join(' '))}
                    leftIcon={<DocumentDuplicateIcon className="h-4 w-4" />}
                  >
                    Copy All
                  </Button>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="bg-gray-50 dark:bg-gray-800 p-4 rounded-xl border border-gray-200 dark:border-gray-700">
                  <p className="text-sm text-gray-700 dark:text-gray-300 font-mono break-all">
                    {post.hashtags.join(' ')}
                  </p>
                </div>
              </CardContent>
            </Card>

            {/* Grouped Hashtags */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <TagIcon className="h-5 w-5 mr-2 text-secondary-600 dark:text-secondary-400" />
                  Hashtags by Category
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {Object.entries(post.hashtags_grouped).map(([category, tags]) => (
                  <div
                    key={category}
                    className={cn(
                      "border rounded-xl p-4 cursor-pointer transition-all",
                      expandedSection === category ? "shadow-lg" : "hover:shadow-md"
                    )}
                    onClick={() => setExpandedSection(expandedSection === category ? null : category)}
                  >
                    <div className="flex items-center justify-between mb-2">
                      <h4 className="font-medium text-gray-900 dark:text-gray-100 capitalize">
                        {category.replace('_', ' ')} ({tags.length})
                      </h4>
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={(e) => {
                          e.stopPropagation();
                          navigator.clipboard.writeText(tags.join(' '));
                        }}
                      >
                        Copy
                      </Button>
                    </div>
                    <div className={cn(
                      "flex flex-wrap gap-2",
                      !expandedSection || expandedSection !== category ? "max-h-12 overflow-hidden" : ""
                    )}>
                      {tags.map((tag, idx) => (
                        <span
                          key={idx}
                          className={cn(
                            "px-3 py-1 rounded-full text-sm font-medium border",
                            getHashtagColor(category)
                          )}
                        >
                          {tag}
                        </span>
                      ))}
                    </div>
                  </div>
                ))}
              </CardContent>
            </Card>

            {/* Location Tags */}
            {post.location_tag_suggestions && post.location_tag_suggestions.length > 0 && (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <GlobeAltIcon className="h-5 w-5 mr-2 text-success-600 dark:text-success-400" />
                    Location Tags
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="flex flex-wrap gap-2">
                    {post.location_tag_suggestions.map((location, idx) => (
                      <span key={idx} className="px-3 py-1 bg-success-100 dark:bg-success-900/20 text-success-800 dark:text-success-400 rounded-full text-sm font-medium border border-success-200 dark:border-success-700">
                        {location}
                      </span>
                    ))}
                  </div>
                </CardContent>
              </Card>
            )}
          </div>
        )}

        {/* Images Tab */}
        {activeTab === 'images' && (
          <div className="space-y-6 animate-fade-in">
            {post.image_prompts.map((imagePrompt, index) => (
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

                  {/* Alt Text */}
                  <div>
                    <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Alt Text</p>
                    <div className="bg-gray-50 dark:bg-gray-800 p-3 rounded-xl border border-gray-200 dark:border-gray-700">
                      <p className="text-sm text-gray-600 dark:text-gray-400 italic">
                        {imagePrompt.alt_text}
                      </p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </div>

      {/* Footer with Compliance Info */}
      <div className="border-t border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900 p-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-6 text-sm">
            <div className="flex items-center">
              <ChartBarIcon className="h-4 w-4 mr-1 text-gray-500 dark:text-gray-400" />
              <span className="text-gray-600 dark:text-gray-400">
                {post.compliance.caption_word_count} words
              </span>
            </div>
            <div className="flex items-center">
              <HashtagIcon className="h-4 w-4 mr-1 text-gray-500 dark:text-gray-400" />
              <span className="text-gray-600 dark:text-gray-400">
                {post.compliance.hashtag_count} hashtags
              </span>
            </div>
            <div className="flex items-center">
              <PhotoIcon className="h-4 w-4 mr-1 text-gray-500 dark:text-gray-400" />
              <span className="text-gray-600 dark:text-gray-400">
                {post.compliance.image_prompt_count} images
              </span>
            </div>
          </div>
          <div className="flex items-center text-success-600 dark:text-success-400">
            <CheckCircleIcon className="h-4 w-4 mr-1" />
            <span className="text-sm font-medium">
              {post.compliance.checks.length} checks passed
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default InstagramPostView;