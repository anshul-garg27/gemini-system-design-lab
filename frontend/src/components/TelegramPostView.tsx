import React, { useState } from 'react';
import { 
  ChatBubbleLeftRightIcon,
  HashtagIcon,
  DocumentDuplicateIcon,
  PhotoIcon,
  LinkIcon,
  RocketLaunchIcon,
  FaceSmileIcon,
  DevicePhoneMobileIcon,
  ComputerDesktopIcon
} from '@heroicons/react/24/outline';
import { Card, CardContent, CardHeader, CardTitle } from './ui/Card';
import { Button } from './ui/Button';
import { cn } from '../lib/utils';

// Interfaces
interface LinkPreview {
  title_hint: string;
  description_hint: string;
  enable_preview: boolean;
}

interface Link {
  url: string;
  short: string;
  preview: LinkPreview;
  instant_view_hint: string;
  fallback: string;
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

interface TelegramPostContent {
  post: string;
  alt_versions: string[];
  extended_post: string;
  link: Link;
  hashtags: string[];
  emoji_suggestions: string[];
  image_prompts: ImagePrompt[];
}

interface TelegramPostViewProps {
  content: any;
}

export const TelegramPostView: React.FC<TelegramPostViewProps> = ({ content }) => {
  const [activeTab, setActiveTab] = useState<'post' | 'images' | 'preview'>('post');
  const [selectedVersion, setSelectedVersion] = useState(0);
  const [previewMode, setPreviewMode] = useState<'desktop' | 'mobile'>('mobile');

  // Parse content
  const telegramPost: TelegramPostContent = content.envelope?.content || content.content || content;
  const {
    post = '',
    alt_versions = [],
    extended_post = '',
    link = {
      url: '',
      short: '',
      preview: { title_hint: '', description_hint: '', enable_preview: true },
      instant_view_hint: '',
      fallback: ''
    },
    hashtags = [],
    emoji_suggestions = [],
    image_prompts = []
  } = telegramPost;

  const allVersions = [post, ...alt_versions];

  // Copy functions
  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
  };

  const copyPost = () => {
    copyToClipboard(allVersions[selectedVersion]);
  };

  const copyExtendedPost = () => {
    copyToClipboard(extended_post);
  };

  const getCharCount = (text: string) => {
    return text.length;
  };

  const getCharCountColor = (count: number) => {
    if (count > 1024) return 'text-red-600 dark:text-red-400';
    if (count > 900) return 'text-yellow-600 dark:text-yellow-400';
    return 'text-green-600 dark:text-green-400';
  };

  return (
    <div className="bg-white dark:bg-gray-900 rounded-3xl shadow-2xl max-w-7xl w-full max-h-[90vh] overflow-hidden flex flex-col">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-500 to-cyan-500 text-white p-6">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold flex items-center">
              <ChatBubbleLeftRightIcon className="h-8 w-8 mr-3" />
              Telegram Post
            </h2>
            <p className="text-blue-100 mt-1">
              {content.meta?.topic_title || 'Telegram Channel Post'}
            </p>
          </div>
          <div className="flex space-x-4 text-sm">
            <div className="text-center">
              <div className="text-2xl font-bold">{getCharCount(post)}</div>
              <div className="text-blue-100">Characters</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold">{allVersions.length}</div>
              <div className="text-blue-100">Versions</div>
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
        {(['post', 'images', 'preview'] as const).map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={cn(
              'flex-1 px-6 py-3 text-sm font-medium transition-all capitalize',
              activeTab === tab
                ? 'text-cyan-600 dark:text-cyan-400 border-b-2 border-cyan-600 dark:border-cyan-400 bg-white dark:bg-gray-800'
                : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-100'
            )}
          >
            {tab === 'post' && <ChatBubbleLeftRightIcon className="h-4 w-4 inline mr-2" />}
            {tab === 'images' && <PhotoIcon className="h-4 w-4 inline mr-2" />}
            {tab === 'preview' && <DevicePhoneMobileIcon className="h-4 w-4 inline mr-2" />}
            {tab}
          </button>
        ))}
      </div>

      {/* Content */}
      <div className="flex-1 overflow-y-auto p-6">
        {/* Post Tab */}
        {activeTab === 'post' && (
          <div className="space-y-6">
            {/* Main Post */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center justify-between">
                  <span className="flex items-center">
                    <ChatBubbleLeftRightIcon className="h-5 w-5 mr-2 text-cyan-600 dark:text-cyan-400" />
                    Channel Post
                  </span>
                  <Button
                    variant="primary"
                    size="sm"
                    onClick={copyPost}
                    leftIcon={<DocumentDuplicateIcon className="h-4 w-4" />}
                  >
                    Copy Post
                  </Button>
                </CardTitle>
              </CardHeader>
              <CardContent>
                {/* Version Selector */}
                {allVersions.length > 1 && (
                  <div className="mb-4">
                    <label className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2 block">
                      Post Version:
                    </label>
                    <div className="flex space-x-2">
                      {allVersions.map((_, index) => (
                        <button
                          key={index}
                          onClick={() => setSelectedVersion(index)}
                          className={cn(
                            'px-3 py-1 rounded-lg text-sm font-medium transition-all',
                            selectedVersion === index
                              ? 'bg-cyan-600 text-white'
                              : 'bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-300 dark:hover:bg-gray-600'
                          )}
                        >
                          {index === 0 ? 'Main' : `Alt ${index}`}
                        </button>
                      ))}
                    </div>
                  </div>
                )}

                {/* Post Text */}
                <div className="bg-gradient-to-br from-blue-50 to-cyan-50 dark:from-blue-900/20 dark:to-cyan-900/20 p-6 rounded-xl">
                  <p className="text-gray-800 dark:text-gray-200 whitespace-pre-wrap text-lg leading-relaxed font-[system-ui]">
                    {allVersions[selectedVersion]}
                  </p>
                  <div className="mt-4 flex items-center justify-between">
                    <span className={cn('text-sm font-medium', getCharCountColor(getCharCount(allVersions[selectedVersion])))}>
                      {getCharCount(allVersions[selectedVersion])}/1024 characters
                    </span>
                  </div>
                </div>

                {/* Hashtags & Emojis */}
                <div className="mt-4 space-y-3">
                  {hashtags.length > 0 && (
                    <div>
                      <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Hashtags:</p>
                      <div className="flex flex-wrap gap-2">
                        {hashtags.map((tag, index) => (
                          <span
                            key={index}
                            className="inline-flex items-center px-3 py-1 rounded-full text-sm bg-cyan-100 dark:bg-cyan-900/30 text-cyan-700 dark:text-cyan-300"
                          >
                            <HashtagIcon className="h-3 w-3 mr-1" />
                            {tag.replace('#', '')}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                  
                  {emoji_suggestions.length > 0 && (
                    <div>
                      <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Suggested Emojis:</p>
                      <div className="flex gap-3">
                        {emoji_suggestions.map((emoji, index) => (
                          <span
                            key={index}
                            className="text-2xl cursor-pointer hover:scale-125 transition-transform"
                            onClick={() => copyToClipboard(emoji)}
                            title="Click to copy"
                          >
                            {emoji}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>

            {/* Extended Post */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center justify-between">
                  <span className="flex items-center">
                    <DocumentDuplicateIcon className="h-5 w-5 mr-2 text-indigo-600 dark:text-indigo-400" />
                    Extended Version
                  </span>
                  <div className="flex items-center space-x-3">
                    <span className={cn('text-sm font-medium', getCharCountColor(getCharCount(extended_post)))}>
                      {getCharCount(extended_post)} chars
                    </span>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={copyExtendedPost}
                      leftIcon={<DocumentDuplicateIcon className="h-4 w-4" />}
                    >
                      Copy
                    </Button>
                  </div>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="bg-indigo-50 dark:bg-indigo-900/20 p-4 rounded-lg">
                  <p className="text-gray-700 dark:text-gray-300 whitespace-pre-wrap">
                    {extended_post}
                  </p>
                </div>
              </CardContent>
            </Card>

            {/* Link Configuration */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <LinkIcon className="h-5 w-5 mr-2 text-purple-600 dark:text-purple-400" />
                  Link Settings
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Full URL</p>
                    <p className="text-sm text-gray-600 dark:text-gray-400 font-mono bg-gray-100 dark:bg-gray-800 p-2 rounded break-all">
                      {link.url}
                    </p>
                  </div>
                  <div>
                    <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Short URL</p>
                    <p className="text-sm text-gray-600 dark:text-gray-400 font-mono bg-gray-100 dark:bg-gray-800 p-2 rounded">
                      {link.short}
                    </p>
                  </div>
                </div>

                <div className="border-t border-gray-200 dark:border-gray-700 pt-4">
                  <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">Link Preview</p>
                  <div className="bg-gray-50 dark:bg-gray-800 p-4 rounded-lg space-y-2">
                    <p className="font-semibold text-gray-900 dark:text-gray-100">
                      {link.preview.title_hint}
                    </p>
                    <p className="text-sm text-gray-600 dark:text-gray-400">
                      {link.preview.description_hint}
                    </p>
                    <div className="flex items-center space-x-4 text-xs">
                      <span className={cn(
                        'flex items-center',
                        link.preview.enable_preview 
                          ? 'text-green-600 dark:text-green-400' 
                          : 'text-gray-500 dark:text-gray-500'
                      )}>
                        {link.preview.enable_preview ? '✓' : '✗'} Preview enabled
                      </span>
                      <span className="text-gray-500 dark:text-gray-500">
                        Instant View: {link.instant_view_hint}
                      </span>
                    </div>
                  </div>
                  {link.fallback && (
                    <p className="text-sm text-gray-600 dark:text-gray-400 mt-2 italic">
                      Fallback: {link.fallback}
                    </p>
                  )}
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

        {/* Preview Tab */}
        {activeTab === 'preview' && (
          <div className="space-y-6">
            {/* Preview Mode Toggle */}
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
                Channel Preview
              </h3>
              <div className="flex space-x-2">
                <Button
                  variant={previewMode === 'desktop' ? 'primary' : 'ghost'}
                  size="sm"
                  onClick={() => setPreviewMode('desktop')}
                  leftIcon={<ComputerDesktopIcon className="h-4 w-4" />}
                >
                  Desktop
                </Button>
                <Button
                  variant={previewMode === 'mobile' ? 'primary' : 'ghost'}
                  size="sm"
                  onClick={() => setPreviewMode('mobile')}
                  leftIcon={<DevicePhoneMobileIcon className="h-4 w-4" />}
                >
                  Mobile
                </Button>
              </div>
            </div>

            {/* Preview Container */}
            <Card>
              <CardContent className="p-0">
                <div className={cn(
                  'mx-auto',
                  previewMode === 'desktop' ? 'max-w-2xl' : 'max-w-sm'
                )}>
                  {/* Telegram UI Mock */}
                  <div className="bg-gray-100 dark:bg-gray-800 rounded-2xl overflow-hidden">
                    {/* Header */}
                    <div className="bg-gradient-to-r from-blue-500 to-cyan-500 text-white p-4">
                      <div className="flex items-center space-x-3">
                        <div className="w-10 h-10 bg-white/20 rounded-full flex items-center justify-center">
                          <RocketLaunchIcon className="h-6 w-6" />
                        </div>
                        <div>
                          <p className="font-semibold">{content.meta?.brand?.handles?.telegram || '@channel'}</p>
                          <p className="text-xs text-blue-100">1.2K subscribers</p>
                        </div>
                      </div>
                    </div>

                    {/* Messages */}
                    <div className="p-4 space-y-4">
                      {/* Post Message */}
                      <div className="bg-white dark:bg-gray-700 rounded-2xl p-4 shadow-sm">
                        <p className="text-gray-800 dark:text-gray-200 whitespace-pre-wrap">
                          {allVersions[selectedVersion]}
                        </p>
                        
                        {/* Link Preview */}
                        {link.preview.enable_preview && (
                          <div className="mt-3 border-l-2 border-cyan-500 pl-3">
                            <p className="font-medium text-gray-900 dark:text-gray-100 text-sm">
                              {link.preview.title_hint}
                            </p>
                            <p className="text-gray-600 dark:text-gray-400 text-xs mt-1">
                              {link.preview.description_hint}
                            </p>
                            <p className="text-cyan-600 dark:text-cyan-400 text-xs mt-1">
                              {link.short}
                            </p>
                          </div>
                        )}

                        {/* Footer */}
                        <div className="flex items-center justify-between mt-3 pt-3 border-t border-gray-200 dark:border-gray-600">
                          <span className="text-xs text-gray-500 dark:text-gray-400">
                            12:34 PM
                          </span>
                          <div className="flex items-center space-x-3 text-xs text-gray-500 dark:text-gray-400">
                            <span>👁 1.2K</span>
                            <span>❤️ 89</span>
                            <span>💬 12</span>
                          </div>
                        </div>
                      </div>

                      {/* Extended Post (if different) */}
                      {extended_post && extended_post !== allVersions[selectedVersion] && (
                        <div className="bg-blue-50 dark:bg-blue-900/20 rounded-2xl p-4 border border-blue-200 dark:border-blue-700">
                          <p className="text-xs text-blue-700 dark:text-blue-300 mb-2 font-medium">
                            Extended Version
                          </p>
                          <p className="text-gray-700 dark:text-gray-300 text-sm whitespace-pre-wrap">
                            {extended_post}
                          </p>
                        </div>
                      )}
                    </div>
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
              <ChatBubbleLeftRightIcon className="h-4 w-4 mr-1" />
              {getCharCount(post)} chars
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
