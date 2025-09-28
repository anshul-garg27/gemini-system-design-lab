import React, { useState } from 'react';
import { 
  DocumentTextIcon,
  HashtagIcon,
  DocumentDuplicateIcon,
  PhotoIcon,
  CheckCircleIcon,
  ChartBarIcon,
  LightBulbIcon,
  LinkIcon,
  ChatBubbleBottomCenterTextIcon,
  BeakerIcon
} from '@heroicons/react/24/outline';
import { Card, CardContent, CardHeader, CardTitle } from './ui/Card';
import { Button } from './ui/Button';
import { cn } from '../lib/utils';

// Interfaces
interface HashtagsGrouped {
  broad: string[];
  niche: string[];
  micro_niche: string[];
  intent: string[];
  branded: string[];
}

interface AltVersions {
  short: string;
  long: string;
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

interface Compliance {
  hashtags_count: number;
  image_prompt_count: number;
  body_chars_count: number;
  checks: string[];
}

interface LinkedInPostContent {
  hook: string;
  context: string;
  key_insights: string[];
  mini_example: string;
  cta: string;
  question: string;
  body: string;
  chars_count: number;
  hashtags: string[];
  hashtags_grouped: HashtagsGrouped;
  alt_versions: AltVersions;
  image_prompts: ImagePrompt[];
  compliance: Compliance;
}

interface LinkedInPostViewProps {
  content: any;
}

export const LinkedInPostView: React.FC<LinkedInPostViewProps> = ({ content }) => {
  const [activeTab, setActiveTab] = useState<'post' | 'versions' | 'images' | 'analytics'>('post');
  const [selectedVersion, setSelectedVersion] = useState<'main' | 'short' | 'long'>('main');

  // Parse content
  const linkedinPost: LinkedInPostContent = content.envelope?.content || content.content || content;
  const {
    hook = '',
    context = '',
    key_insights = [],
    mini_example = '',
    cta = '',
    question = '',
    body = '',
    chars_count = 0,
    hashtags = [],
    hashtags_grouped = { broad: [], niche: [], micro_niche: [], intent: [], branded: [] },
    alt_versions = { short: '', long: '' },
    image_prompts = [],
    compliance = {
      hashtags_count: 0,
      image_prompt_count: 0,
      body_chars_count: 0,
      checks: []
    }
  } = linkedinPost;

  // Copy functions
  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
  };

  const copyPost = () => {
    let postContent = body;
    if (selectedVersion === 'short') {
      postContent = alt_versions.short;
    } else if (selectedVersion === 'long') {
      postContent = alt_versions.long;
    }
    
    const fullPost = `${postContent}\n\n${hashtags.map(tag => `#${tag.replace('#', '')}`).join(' ')}`;
    copyToClipboard(fullPost);
  };

  const copySection = (text: string) => {
    copyToClipboard(text);
  };

  const getVersionLabel = (version: 'main' | 'short' | 'long') => {
    switch (version) {
      case 'main':
        return 'Standard';
      case 'short':
        return 'Short';
      case 'long':
        return 'Long';
    }
  };

  const getCharCount = (version: 'main' | 'short' | 'long') => {
    switch (version) {
      case 'main':
        return chars_count;
      case 'short':
        return alt_versions.short.length;
      case 'long':
        return alt_versions.long.length;
    }
  };

  const getCharCountColor = (count: number) => {
    if (count > 3000) return 'text-red-600 dark:text-red-400';
    if (count > 2800) return 'text-yellow-600 dark:text-yellow-400';
    return 'text-green-600 dark:text-green-400';
  };

  return (
    <div className="bg-white dark:bg-gray-900 rounded-3xl shadow-2xl max-w-7xl w-full max-h-[90vh] overflow-hidden flex flex-col">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-700 to-blue-800 text-white p-6">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold flex items-center">
              <DocumentTextIcon className="h-8 w-8 mr-3" />
              LinkedIn Post
            </h2>
            <p className="text-blue-100 mt-1">
              {content.meta?.topic_title || 'LinkedIn Post Content'}
            </p>
          </div>
          <div className="flex space-x-4 text-sm">
            <div className="text-center">
              <div className="text-2xl font-bold">{chars_count}</div>
              <div className="text-blue-100">Characters</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold">{key_insights.length}</div>
              <div className="text-blue-100">Insights</div>
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
        {(['post', 'versions', 'images', 'analytics'] as const).map((tab) => (
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
            {tab === 'post' && <DocumentTextIcon className="h-4 w-4 inline mr-2" />}
            {tab === 'versions' && <BeakerIcon className="h-4 w-4 inline mr-2" />}
            {tab === 'images' && <PhotoIcon className="h-4 w-4 inline mr-2" />}
            {tab === 'analytics' && <ChartBarIcon className="h-4 w-4 inline mr-2" />}
            {tab}
          </button>
        ))}
      </div>

      {/* Content */}
      <div className="flex-1 overflow-y-auto p-6">
        {/* Post Tab */}
        {activeTab === 'post' && (
          <div className="space-y-6">
            {/* Main Post Structure */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center justify-between">
                  <span className="flex items-center">
                    <DocumentTextIcon className="h-5 w-5 mr-2 text-blue-700 dark:text-blue-400" />
                    Post Structure
                  </span>
                  <Button
                    variant="primary"
                    size="sm"
                    onClick={copyPost}
                    leftIcon={<DocumentDuplicateIcon className="h-4 w-4" />}
                  >
                    Copy Full Post
                  </Button>
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {/* Hook */}
                <div className="bg-blue-50 dark:bg-blue-900/20 p-4 rounded-lg">
                  <div className="flex items-start justify-between mb-2">
                    <h4 className="font-semibold text-gray-900 dark:text-gray-100 flex items-center">
                      <ChatBubbleBottomCenterTextIcon className="h-4 w-4 mr-2 text-blue-600 dark:text-blue-400" />
                      Hook
                    </h4>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => copySection(hook)}
                      leftIcon={<DocumentDuplicateIcon className="h-3 w-3" />}
                    >
                      Copy
                    </Button>
                  </div>
                  <p className="text-gray-700 dark:text-gray-300 whitespace-pre-wrap">
                    {hook}
                  </p>
                </div>

                {/* Context */}
                <div className="bg-purple-50 dark:bg-purple-900/20 p-4 rounded-lg">
                  <div className="flex items-start justify-between mb-2">
                    <h4 className="font-semibold text-gray-900 dark:text-gray-100">
                      Context
                    </h4>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => copySection(context)}
                      leftIcon={<DocumentDuplicateIcon className="h-3 w-3" />}
                    >
                      Copy
                    </Button>
                  </div>
                  <p className="text-gray-700 dark:text-gray-300">
                    {context}
                  </p>
                </div>

                {/* Key Insights */}
                {key_insights.length > 0 && (
                  <div className="bg-green-50 dark:bg-green-900/20 p-4 rounded-lg">
                    <h4 className="font-semibold text-gray-900 dark:text-gray-100 mb-3 flex items-center">
                      <LightBulbIcon className="h-4 w-4 mr-2 text-green-600 dark:text-green-400" />
                      Key Insights
                    </h4>
                    <ul className="space-y-2">
                      {key_insights.map((insight, index) => (
                        <li key={index} className="flex items-start">
                          <span className="text-green-600 dark:text-green-400 mr-2">•</span>
                          <span className="text-gray-700 dark:text-gray-300">{insight}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                {/* Mini Example */}
                <div className="bg-yellow-50 dark:bg-yellow-900/20 p-4 rounded-lg">
                  <div className="flex items-start justify-between mb-2">
                    <h4 className="font-semibold text-gray-900 dark:text-gray-100 flex items-center">
                      <BeakerIcon className="h-4 w-4 mr-2 text-yellow-600 dark:text-yellow-400" />
                      Example
                    </h4>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => copySection(mini_example)}
                      leftIcon={<DocumentDuplicateIcon className="h-3 w-3" />}
                    >
                      Copy
                    </Button>
                  </div>
                  <p className="text-gray-700 dark:text-gray-300 italic">
                    {mini_example}
                  </p>
                </div>

                {/* Question */}
                <div className="bg-pink-50 dark:bg-pink-900/20 p-4 rounded-lg">
                  <div className="flex items-start justify-between mb-2">
                    <h4 className="font-semibold text-gray-900 dark:text-gray-100 flex items-center">
                      <ChatBubbleBottomCenterTextIcon className="h-4 w-4 mr-2 text-pink-600 dark:text-pink-400" />
                      Engagement Question
                    </h4>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => copySection(question)}
                      leftIcon={<DocumentDuplicateIcon className="h-3 w-3" />}
                    >
                      Copy
                    </Button>
                  </div>
                  <p className="text-gray-700 dark:text-gray-300">
                    {question}
                  </p>
                </div>

                {/* CTA */}
                <div className="bg-indigo-50 dark:bg-indigo-900/20 p-4 rounded-lg">
                  <div className="flex items-start justify-between mb-2">
                    <h4 className="font-semibold text-gray-900 dark:text-gray-100 flex items-center">
                      <LinkIcon className="h-4 w-4 mr-2 text-indigo-600 dark:text-indigo-400" />
                      Call to Action
                    </h4>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => copySection(cta)}
                      leftIcon={<DocumentDuplicateIcon className="h-3 w-3" />}
                    >
                      Copy
                    </Button>
                  </div>
                  <p className="text-gray-700 dark:text-gray-300">
                    {cta}
                  </p>
                </div>
              </CardContent>
            </Card>

            {/* Full Post Preview */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <DocumentTextIcon className="h-5 w-5 mr-2 text-blue-700 dark:text-blue-400" />
                  Full Post Preview
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="bg-gray-50 dark:bg-gray-800 p-6 rounded-xl">
                  <p className="text-gray-800 dark:text-gray-200 whitespace-pre-wrap leading-relaxed">
                    {body}
                  </p>
                  <div className="mt-4 pt-4 border-t border-gray-200 dark:border-gray-700">
                    <div className="flex flex-wrap gap-2">
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
                </div>
              </CardContent>
            </Card>
          </div>
        )}

        {/* Versions Tab */}
        {activeTab === 'versions' && (
          <div className="space-y-6">
            {/* Version Selector */}
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
                Post Versions
              </h3>
              <div className="flex space-x-2">
                {(['main', 'short', 'long'] as const).map((version) => (
                  <button
                    key={version}
                    onClick={() => setSelectedVersion(version)}
                    className={cn(
                      'px-4 py-2 rounded-lg text-sm font-medium transition-all',
                      selectedVersion === version
                        ? 'bg-blue-700 text-white'
                        : 'bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-300 dark:hover:bg-gray-600'
                    )}
                  >
                    {getVersionLabel(version)}
                  </button>
                ))}
              </div>
            </div>

            {/* Selected Version */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center justify-between">
                  <span className="flex items-center">
                    <DocumentTextIcon className="h-5 w-5 mr-2 text-blue-700 dark:text-blue-400" />
                    {getVersionLabel(selectedVersion)} Version
                  </span>
                  <div className="flex items-center space-x-3">
                    <span className={cn('text-sm font-medium', getCharCountColor(getCharCount(selectedVersion)))}>
                      {getCharCount(selectedVersion)}/3000
                    </span>
                    <Button
                      variant="primary"
                      size="sm"
                      onClick={copyPost}
                      leftIcon={<DocumentDuplicateIcon className="h-4 w-4" />}
                    >
                      Copy Version
                    </Button>
                  </div>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="bg-gray-50 dark:bg-gray-800 p-6 rounded-xl">
                  <p className="text-gray-800 dark:text-gray-200 whitespace-pre-wrap leading-relaxed">
                    {selectedVersion === 'main' ? body : 
                     selectedVersion === 'short' ? alt_versions.short : 
                     alt_versions.long}
                  </p>
                  {selectedVersion !== 'short' && (
                    <div className="mt-4 pt-4 border-t border-gray-200 dark:border-gray-700">
                      <div className="flex flex-wrap gap-2">
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
                  )}
                </div>
              </CardContent>
            </Card>

            {/* Version Comparison */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <ChartBarIcon className="h-5 w-5 mr-2 text-purple-600 dark:text-purple-400" />
                  Version Comparison
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {(['main', 'short', 'long'] as const).map((version) => {
                    const charCount = getCharCount(version);
                    const percentage = (charCount / 3000) * 100;
                    
                    return (
                      <div key={version}>
                        <div className="flex items-center justify-between mb-1">
                          <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                            {getVersionLabel(version)}
                          </span>
                          <span className={cn('text-sm font-medium', getCharCountColor(charCount))}>
                            {charCount} chars
                          </span>
                        </div>
                        <div className="h-6 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                          <div
                            className={cn(
                              'h-full transition-all',
                              charCount > 3000 ? 'bg-red-500' :
                              charCount > 2800 ? 'bg-yellow-500' : 'bg-green-500'
                            )}
                            style={{ width: `${Math.min(percentage, 100)}%` }}
                          />
                        </div>
                      </div>
                    );
                  })}
                </div>
              </CardContent>
            </Card>
          </div>
        )}

        {/* Images Tab */}
        {activeTab === 'images' && (
          <div className="space-y-6">
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
                  Content Metrics
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <div className="bg-blue-50 dark:bg-blue-900/20 p-4 rounded-lg">
                    <p className="text-2xl font-bold text-gray-900 dark:text-gray-100">
                      {compliance.body_chars_count}
                    </p>
                    <p className="text-sm text-gray-600 dark:text-gray-400">Characters</p>
                  </div>
                  <div className="bg-green-50 dark:bg-green-900/20 p-4 rounded-lg">
                    <p className="text-2xl font-bold text-gray-900 dark:text-gray-100">
                      {key_insights.length}
                    </p>
                    <p className="text-sm text-gray-600 dark:text-gray-400">Key Insights</p>
                  </div>
                  <div className="bg-purple-50 dark:bg-purple-900/20 p-4 rounded-lg">
                    <p className="text-2xl font-bold text-gray-900 dark:text-gray-100">
                      {compliance.hashtags_count}
                    </p>
                    <p className="text-sm text-gray-600 dark:text-gray-400">Hashtags</p>
                  </div>
                  <div className="bg-yellow-50 dark:bg-yellow-900/20 p-4 rounded-lg">
                    <p className="text-2xl font-bold text-gray-900 dark:text-gray-100">
                      {compliance.image_prompt_count}
                    </p>
                    <p className="text-sm text-gray-600 dark:text-gray-400">Images</p>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Hashtag Categories */}
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
              {chars_count} chars
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
