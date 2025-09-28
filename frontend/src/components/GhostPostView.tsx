import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { 
  DocumentTextIcon,
  HashtagIcon,
  DocumentDuplicateIcon,
  PhotoIcon,
  CodeBracketIcon,
  EnvelopeIcon,
  GlobeAltIcon,
  EyeIcon,
  UserGroupIcon,
  NewspaperIcon
} from '@heroicons/react/24/outline';
import { Card, CardContent, CardHeader, CardTitle } from './ui/Card';
import { Button } from './ui/Button';
import { cn } from '../lib/utils';

// Interfaces
interface PostContent {
  title: string;
  excerpt: string;
  tags: string[];
  internal_tags: string[];
  feature_image: string;
  feature_image_alt: string;
  visibility: string;
  html: string;
  member_teaser_html: string;
  newsletter_html: string;
}

interface MetaFields {
  meta_title: string;
  meta_description: string;
  og_title: string;
  og_description: string;
  og_image: string;
  twitter_title: string;
  twitter_description: string;
  twitter_image: string;
  canonical_url: string;
}

interface Newsletter {
  subject: string;
  preheader: string;
  html: string;
}

interface GhostPostContent {
  post: PostContent;
  meta_fields: MetaFields;
  newsletter: Newsletter;
}

interface GhostPostViewProps {
  content: any;
}

export const GhostPostView: React.FC<GhostPostViewProps> = ({ content }) => {
  const [activeTab, setActiveTab] = useState<'post' | 'meta' | 'newsletter' | 'preview'>('post');
  const [previewMode, setPreviewMode] = useState<'desktop' | 'mobile'>('desktop');

  // Parse content
  const ghostPost: GhostPostContent = content.envelope?.content || content.content || content;
  const {
    post = {
      title: '',
      excerpt: '',
      tags: [],
      internal_tags: [],
      feature_image: '',
      feature_image_alt: '',
      visibility: 'public',
      html: '',
      member_teaser_html: '',
      newsletter_html: ''
    },
    meta_fields = {
      meta_title: '',
      meta_description: '',
      og_title: '',
      og_description: '',
      og_image: '',
      twitter_title: '',
      twitter_description: '',
      twitter_image: '',
      canonical_url: ''
    },
    newsletter = {
      subject: '',
      preheader: '',
      html: ''
    }
  } = ghostPost;

  // Copy functions
  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
  };

  const copyHtml = () => {
    copyToClipboard(post.html);
  };

  const copyNewsletterHtml = () => {
    copyToClipboard(newsletter.html);
  };

  // Convert HTML to Markdown for preview (simplified)
  const htmlToText = (html: string) => {
    const div = document.createElement('div');
    div.innerHTML = html;
    return div.textContent || div.innerText || '';
  };

  return (
    <div className="bg-white dark:bg-gray-900 rounded-3xl shadow-2xl max-w-7xl w-full max-h-[90vh] overflow-hidden flex flex-col">
      {/* Header */}
      <div className="bg-gradient-to-r from-purple-800 to-purple-900 text-white p-6">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold flex items-center">
              <DocumentTextIcon className="h-8 w-8 mr-3" />
              Ghost Post
            </h2>
            <p className="text-purple-100 mt-1">
              {post.title || content.meta?.topic_title || 'Ghost Blog Post'}
            </p>
          </div>
          <div className="flex space-x-4 text-sm">
            <div className="text-center">
              <div className="text-2xl font-bold">{post.tags.length}</div>
              <div className="text-purple-100">Tags</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold">{post.visibility}</div>
              <div className="text-purple-100">Visibility</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold">{htmlToText(post.html).split(' ').length}</div>
              <div className="text-purple-100">Words</div>
            </div>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex border-b border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800/50">
        {(['post', 'meta', 'newsletter', 'preview'] as const).map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={cn(
              'flex-1 px-6 py-3 text-sm font-medium transition-all capitalize',
              activeTab === tab
                ? 'text-purple-700 dark:text-purple-400 border-b-2 border-purple-700 dark:border-purple-400 bg-white dark:bg-gray-800'
                : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-100'
            )}
          >
            {tab === 'post' && <DocumentTextIcon className="h-4 w-4 inline mr-2" />}
            {tab === 'meta' && <GlobeAltIcon className="h-4 w-4 inline mr-2" />}
            {tab === 'newsletter' && <EnvelopeIcon className="h-4 w-4 inline mr-2" />}
            {tab === 'preview' && <EyeIcon className="h-4 w-4 inline mr-2" />}
            {tab}
          </button>
        ))}
      </div>

      {/* Content */}
      <div className="flex-1 overflow-y-auto p-6">
        {/* Post Tab */}
        {activeTab === 'post' && (
          <div className="space-y-6">
            {/* Basic Info */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <DocumentTextIcon className="h-5 w-5 mr-2 text-purple-600 dark:text-purple-400" />
                  Post Information
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Title</p>
                  <p className="text-lg font-semibold text-gray-900 dark:text-gray-100">{post.title}</p>
                </div>
                
                <div>
                  <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Excerpt</p>
                  <p className="text-gray-700 dark:text-gray-300">{post.excerpt}</p>
                </div>

                <div>
                  <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Tags</p>
                  <div className="flex flex-wrap gap-2">
                    {post.tags.map((tag, index) => (
                      <span
                        key={index}
                        className="inline-flex items-center px-3 py-1 rounded-full text-sm bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-300"
                      >
                        <HashtagIcon className="h-3 w-3 mr-1" />
                        {tag}
                      </span>
                    ))}
                    {post.internal_tags.map((tag, index) => (
                      <span
                        key={index}
                        className="inline-flex items-center px-3 py-1 rounded-full text-sm bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300"
                      >
                        {tag}
                      </span>
                    ))}
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Visibility</p>
                    <span className={cn(
                      'inline-flex items-center px-2 py-1 rounded text-xs font-medium',
                      post.visibility === 'public' 
                        ? 'bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-300'
                        : 'bg-yellow-100 dark:bg-yellow-900/30 text-yellow-700 dark:text-yellow-300'
                    )}>
                      {post.visibility}
                    </span>
                  </div>
                  <div>
                    <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Feature Image</p>
                    <p className="text-sm text-gray-600 dark:text-gray-400">
                      {post.feature_image ? '✓ Provided' : '✗ Not provided'}
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Post HTML */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center justify-between">
                  <span className="flex items-center">
                    <CodeBracketIcon className="h-5 w-5 mr-2 text-purple-600 dark:text-purple-400" />
                    Post HTML
                  </span>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={copyHtml}
                    leftIcon={<DocumentDuplicateIcon className="h-4 w-4" />}
                  >
                    Copy HTML
                  </Button>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="bg-gray-900 text-gray-100 p-4 rounded-lg overflow-x-auto">
                  <pre className="text-sm font-mono whitespace-pre-wrap">{post.html}</pre>
                </div>
              </CardContent>
            </Card>

            {/* Member Teaser */}
            {post.member_teaser_html && (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <UserGroupIcon className="h-5 w-5 mr-2 text-indigo-600 dark:text-indigo-400" />
                    Member Teaser
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="bg-indigo-50 dark:bg-indigo-900/20 p-4 rounded-lg">
                    <div dangerouslySetInnerHTML={{ __html: post.member_teaser_html }} />
                  </div>
                </CardContent>
              </Card>
            )}
          </div>
        )}

        {/* Meta Tab */}
        {activeTab === 'meta' && (
          <div className="space-y-6">
            {/* SEO Meta */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <GlobeAltIcon className="h-5 w-5 mr-2 text-blue-600 dark:text-blue-400" />
                  SEO Meta Tags
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Meta Title</p>
                  <p className="text-gray-700 dark:text-gray-300 font-mono text-sm bg-gray-100 dark:bg-gray-800 p-2 rounded">
                    {meta_fields.meta_title}
                  </p>
                </div>
                <div>
                  <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Meta Description</p>
                  <p className="text-gray-700 dark:text-gray-300 font-mono text-sm bg-gray-100 dark:bg-gray-800 p-2 rounded">
                    {meta_fields.meta_description}
                  </p>
                </div>
                <div>
                  <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Canonical URL</p>
                  <p className="text-gray-700 dark:text-gray-300 font-mono text-sm bg-gray-100 dark:bg-gray-800 p-2 rounded">
                    {meta_fields.canonical_url}
                  </p>
                </div>
              </CardContent>
            </Card>

            {/* Open Graph */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <PhotoIcon className="h-5 w-5 mr-2 text-green-600 dark:text-green-400" />
                  Open Graph Tags
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">OG Title</p>
                  <p className="text-gray-700 dark:text-gray-300 font-mono text-sm bg-gray-100 dark:bg-gray-800 p-2 rounded">
                    {meta_fields.og_title}
                  </p>
                </div>
                <div>
                  <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">OG Description</p>
                  <p className="text-gray-700 dark:text-gray-300 font-mono text-sm bg-gray-100 dark:bg-gray-800 p-2 rounded">
                    {meta_fields.og_description}
                  </p>
                </div>
                <div>
                  <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">OG Image</p>
                  <p className="text-gray-700 dark:text-gray-300 font-mono text-sm bg-gray-100 dark:bg-gray-800 p-2 rounded break-all">
                    {meta_fields.og_image}
                  </p>
                </div>
              </CardContent>
            </Card>

            {/* Twitter Card */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <span className="text-gray-900 dark:text-gray-100">𝕏</span>
                  <span className="ml-2">Twitter Card Tags</span>
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Twitter Title</p>
                  <p className="text-gray-700 dark:text-gray-300 font-mono text-sm bg-gray-100 dark:bg-gray-800 p-2 rounded">
                    {meta_fields.twitter_title}
                  </p>
                </div>
                <div>
                  <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Twitter Description</p>
                  <p className="text-gray-700 dark:text-gray-300 font-mono text-sm bg-gray-100 dark:bg-gray-800 p-2 rounded">
                    {meta_fields.twitter_description}
                  </p>
                </div>
                <div>
                  <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Twitter Image</p>
                  <p className="text-gray-700 dark:text-gray-300 font-mono text-sm bg-gray-100 dark:bg-gray-800 p-2 rounded break-all">
                    {meta_fields.twitter_image}
                  </p>
                </div>
              </CardContent>
            </Card>
          </div>
        )}

        {/* Newsletter Tab */}
        {activeTab === 'newsletter' && (
          <div className="space-y-6">
            {/* Newsletter Info */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <EnvelopeIcon className="h-5 w-5 mr-2 text-pink-600 dark:text-pink-400" />
                  Newsletter Configuration
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Subject Line</p>
                  <p className="text-lg font-semibold text-gray-900 dark:text-gray-100">
                    {newsletter.subject}
                  </p>
                </div>
                <div>
                  <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Preheader Text</p>
                  <p className="text-gray-700 dark:text-gray-300">
                    {newsletter.preheader}
                  </p>
                </div>
              </CardContent>
            </Card>

            {/* Newsletter HTML */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center justify-between">
                  <span className="flex items-center">
                    <NewspaperIcon className="h-5 w-5 mr-2 text-pink-600 dark:text-pink-400" />
                    Newsletter HTML
                  </span>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={copyNewsletterHtml}
                    leftIcon={<DocumentDuplicateIcon className="h-4 w-4" />}
                  >
                    Copy HTML
                  </Button>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="bg-gray-50 dark:bg-gray-800 p-4 rounded-lg">
                  <div dangerouslySetInnerHTML={{ __html: newsletter.html }} />
                </div>
              </CardContent>
            </Card>
          </div>
        )}

        {/* Preview Tab */}
        {activeTab === 'preview' && (
          <div className="space-y-6">
            {/* Preview Mode Toggle */}
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
                Post Preview
              </h3>
              <div className="flex space-x-2">
                <Button
                  variant={previewMode === 'desktop' ? 'primary' : 'ghost'}
                  size="sm"
                  onClick={() => setPreviewMode('desktop')}
                >
                  Desktop
                </Button>
                <Button
                  variant={previewMode === 'mobile' ? 'primary' : 'ghost'}
                  size="sm"
                  onClick={() => setPreviewMode('mobile')}
                >
                  Mobile
                </Button>
              </div>
            </div>

            {/* Preview Container */}
            <Card>
              <CardContent className="p-0">
                <div className={cn(
                  'mx-auto bg-white dark:bg-gray-900 shadow-xl',
                  previewMode === 'desktop' ? 'max-w-4xl' : 'max-w-sm'
                )}>
                  {/* Feature Image */}
                  {post.feature_image && (
                    <div className="w-full h-64 bg-gradient-to-br from-purple-400 to-pink-400 flex items-center justify-center">
                      <PhotoIcon className="h-16 w-16 text-white/50" />
                      <span className="sr-only">{post.feature_image_alt}</span>
                    </div>
                  )}
                  
                  {/* Content */}
                  <div className="p-8">
                    <article className="prose prose-lg dark:prose-invert max-w-none">
                      <div dangerouslySetInnerHTML={{ __html: post.html }} />
                    </article>
                  </div>
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
              {htmlToText(post.html).split(' ').length} words
            </span>
            <span className="flex items-center">
              <HashtagIcon className="h-4 w-4 mr-1" />
              {post.tags.length} tags
            </span>
            <span className="flex items-center">
              <EyeIcon className="h-4 w-4 mr-1" />
              {post.visibility}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};
