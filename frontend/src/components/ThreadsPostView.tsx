import React, { useState } from 'react';
import { 
  ChatBubbleLeftIcon,
  HashtagIcon,
  DocumentDuplicateIcon,
  LinkIcon,
  PhotoIcon,
  CheckCircleIcon,
  AtSymbolIcon,
  ChartBarIcon,
  ArrowPathIcon
} from '@heroicons/react/24/outline';
import { Card, CardContent, CardHeader, CardTitle } from './ui/Card';
import { Button } from './ui/Button';
import { cn } from '../lib/utils';

// Interfaces
interface Reply {
  index: number;
  text: string;
  character_count: number;
  hashtags?: string[];
  mentions?: string[];
}

interface LinkPlan {
  enabled: boolean;
  placement: string;
  url: string;
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
  main_post_chars_count: number;
  replies_total: number;
  hashtags_count: number;
  image_prompt_count: number;
  has_tracked_link: boolean;
  per_post_hashtags_ok: boolean;
  per_post_mentions_ok: boolean;
  checks: string[];
}

interface ThreadsPostContent {
  post: string;
  alt_versions: string[];
  reply_chain: Reply[];
  hashtags: string[];
  mentions_suggestions: string[];
  link_plan: LinkPlan;
  image_prompts: ImagePrompt[];
  compliance: Compliance;
}

interface ThreadsPostViewProps {
  content: any;
}

export const ThreadsPostView: React.FC<ThreadsPostViewProps> = ({ content }) => {
  const [activeTab, setActiveTab] = useState<'thread' | 'images' | 'analytics'>('thread');
  const [selectedVersion, setSelectedVersion] = useState(0);
  const [expandedReply, setExpandedReply] = useState<number | null>(null);

  // Parse content
  const threadsPost: ThreadsPostContent = content.envelope?.content || content.content || content;
  const {
    post = '',
    alt_versions = [],
    reply_chain = [],
    hashtags = [],
    mentions_suggestions = [],
    link_plan = { enabled: false, placement: '', url: '' },
    image_prompts = [],
    compliance = {
      main_post_chars_count: 0,
      replies_total: 0,
      hashtags_count: 0,
      image_prompt_count: 0,
      has_tracked_link: false,
      per_post_hashtags_ok: false,
      per_post_mentions_ok: false,
      checks: []
    }
  } = threadsPost;

  const allVersions = [post, ...alt_versions];

  // Copy functions
  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
  };

  const copyPost = () => {
    const selectedPost = allVersions[selectedVersion];
    const postWithLink = link_plan.enabled && link_plan.placement === 'main_post' 
      ? `${selectedPost}\n\n${link_plan.url}` 
      : selectedPost;
    copyToClipboard(postWithLink);
  };

  const copyFullThread = () => {
    let fullThread = allVersions[selectedVersion];
    
    if (link_plan.enabled && link_plan.placement === 'main_post') {
      fullThread += `\n\n${link_plan.url}`;
    }
    
    reply_chain.forEach((reply, index) => {
      fullThread += `\n\n---\n\n${reply.text}`;
      if (link_plan.enabled && link_plan.placement === `reply_${index + 1}`) {
        fullThread += `\n\n${link_plan.url}`;
      }
    });
    
    copyToClipboard(fullThread);
  };

  const copyReply = (reply: Reply) => {
    let replyText = reply.text;
    if (link_plan.enabled && link_plan.placement === `reply_${reply.index}`) {
      replyText += `\n\n${link_plan.url}`;
    }
    copyToClipboard(replyText);
  };

  const getCharCountColor = (count: number) => {
    if (count > 500) return 'text-red-600 dark:text-red-400';
    if (count > 450) return 'text-yellow-600 dark:text-yellow-400';
    return 'text-green-600 dark:text-green-400';
  };

  const getCharCountProgress = (count: number) => {
    return Math.min((count / 500) * 100, 100);
  };

  return (
    <div className="bg-white dark:bg-gray-900 rounded-3xl shadow-2xl max-w-7xl w-full max-h-[90vh] overflow-hidden flex flex-col">
      {/* Header */}
      <div className="bg-gradient-to-r from-purple-600 to-pink-600 text-white p-6">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold flex items-center">
              <ChatBubbleLeftIcon className="h-8 w-8 mr-3" />
              Threads Post
            </h2>
            <p className="text-purple-100 mt-1">
              {content.meta?.topic_title || 'Threads Post Content'}
            </p>
          </div>
          <div className="flex space-x-4 text-sm">
            <div className="text-center">
              <div className="text-2xl font-bold">{1 + reply_chain.length}</div>
              <div className="text-purple-100">Posts</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold">{compliance.main_post_chars_count}</div>
              <div className="text-purple-100">Characters</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold">{hashtags.length}</div>
              <div className="text-purple-100">Hashtags</div>
            </div>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex border-b border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800/50">
        {(['thread', 'images', 'analytics'] as const).map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={cn(
              'flex-1 px-6 py-3 text-sm font-medium transition-all capitalize',
              activeTab === tab
                ? 'text-purple-600 dark:text-purple-400 border-b-2 border-purple-600 dark:border-purple-400 bg-white dark:bg-gray-800'
                : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-100'
            )}
          >
            {tab === 'thread' && <ChatBubbleLeftIcon className="h-4 w-4 inline mr-2" />}
            {tab === 'images' && <PhotoIcon className="h-4 w-4 inline mr-2" />}
            {tab === 'analytics' && <ChartBarIcon className="h-4 w-4 inline mr-2" />}
            {tab}
          </button>
        ))}
      </div>

      {/* Content */}
      <div className="flex-1 overflow-y-auto p-6">
        {/* Thread Tab */}
        {activeTab === 'thread' && (
          <div className="space-y-6">
            {/* Main Post */}
            <Card className="border-2 border-purple-200 dark:border-purple-800">
              <CardHeader>
                <CardTitle className="flex items-center justify-between">
                  <span className="flex items-center">
                    <ChatBubbleLeftIcon className="h-5 w-5 mr-2 text-purple-600 dark:text-purple-400" />
                    Main Post
                  </span>
                  <div className="flex items-center space-x-2">
                    <span className={cn('text-sm font-medium', getCharCountColor(compliance.main_post_chars_count))}>
                      {compliance.main_post_chars_count}/500
                    </span>
                    <Button
                      variant="primary"
                      size="sm"
                      onClick={copyPost}
                      leftIcon={<DocumentDuplicateIcon className="h-4 w-4" />}
                    >
                      Copy Post
                    </Button>
                  </div>
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
                              ? 'bg-purple-600 text-white'
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
                <div className="bg-gradient-to-br from-purple-50 to-pink-50 dark:from-purple-900/20 dark:to-pink-900/20 p-6 rounded-xl">
                  <p className="text-gray-800 dark:text-gray-200 whitespace-pre-wrap text-lg leading-relaxed mb-4">
                    {allVersions[selectedVersion]}
                  </p>
                  
                  {link_plan.enabled && link_plan.placement === 'main_post' && (
                    <div className="mt-4 p-3 bg-white dark:bg-gray-800 rounded-lg border border-purple-200 dark:border-purple-700">
                      <div className="flex items-center text-sm">
                        <LinkIcon className="h-4 w-4 text-purple-600 dark:text-purple-400 mr-2" />
                        <a href={link_plan.url} target="_blank" rel="noopener noreferrer" 
                           className="text-purple-600 dark:text-purple-400 hover:underline truncate">
                          {link_plan.url}
                        </a>
                      </div>
                    </div>
                  )}

                  {/* Character Count Progress */}
                  <div className="mt-4">
                    <div className="h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                      <div
                        className={cn(
                          'h-full transition-all',
                          compliance.main_post_chars_count > 500 ? 'bg-red-500' :
                          compliance.main_post_chars_count > 450 ? 'bg-yellow-500' : 'bg-green-500'
                        )}
                        style={{ width: `${getCharCountProgress(compliance.main_post_chars_count)}%` }}
                      />
                    </div>
                  </div>
                </div>

                {/* Hashtags & Mentions */}
                <div className="mt-4 space-y-2">
                  {hashtags.length > 0 && (
                    <div className="flex flex-wrap gap-2">
                      {hashtags.map((tag, index) => (
                        <span
                          key={index}
                          className="inline-flex items-center px-3 py-1 rounded-full text-sm bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-300"
                        >
                          <HashtagIcon className="h-3 w-3 mr-1" />
                          {tag.replace('#', '')}
                        </span>
                      ))}
                    </div>
                  )}
                  
                  {mentions_suggestions.length > 0 && (
                    <div className="flex flex-wrap gap-2">
                      {mentions_suggestions.map((mention, index) => (
                        <span
                          key={index}
                          className="inline-flex items-center px-3 py-1 rounded-full text-sm bg-pink-100 dark:bg-pink-900/30 text-pink-700 dark:text-pink-300"
                        >
                          <AtSymbolIcon className="h-3 w-3 mr-1" />
                          {mention.replace('@', '')}
                        </span>
                      ))}
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>

            {/* Reply Chain */}
            {reply_chain.length > 0 && (
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 flex items-center">
                    <ArrowPathIcon className="h-5 w-5 mr-2 text-purple-600 dark:text-purple-400" />
                    Reply Chain
                  </h3>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={copyFullThread}
                    leftIcon={<DocumentDuplicateIcon className="h-4 w-4" />}
                  >
                    Copy Full Thread
                  </Button>
                </div>

                {reply_chain.map((reply, index) => (
                  <Card
                    key={index}
                    className={cn(
                      'border-l-4 cursor-pointer transition-all',
                      'border-purple-400 dark:border-purple-600',
                      expandedReply === index ? 'ring-2 ring-purple-500 ring-offset-2' : ''
                    )}
                    onClick={() => setExpandedReply(expandedReply === index ? null : index)}
                  >
                    <CardContent className="p-4">
                      <div className="flex items-start justify-between mb-2">
                        <span className="text-sm font-medium text-gray-600 dark:text-gray-400">
                          Reply {reply.index}
                        </span>
                        <div className="flex items-center space-x-2">
                          <span className={cn('text-sm font-medium', getCharCountColor(reply.character_count))}>
                            {reply.character_count}/500
                          </span>
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={(e) => {
                              e.stopPropagation();
                              copyReply(reply);
                            }}
                            leftIcon={<DocumentDuplicateIcon className="h-3 w-3" />}
                          >
                            Copy
                          </Button>
                        </div>
                      </div>
                      
                      <p className="text-gray-700 dark:text-gray-300 whitespace-pre-wrap">
                        {reply.text}
                      </p>

                      {link_plan.enabled && link_plan.placement === `reply_${reply.index}` && (
                        <div className="mt-3 p-2 bg-purple-50 dark:bg-purple-900/20 rounded-lg">
                          <div className="flex items-center text-sm">
                            <LinkIcon className="h-3 w-3 text-purple-600 dark:text-purple-400 mr-1" />
                            <span className="text-purple-600 dark:text-purple-400 text-xs truncate">
                              {link_plan.url}
                            </span>
                          </div>
                        </div>
                      )}

                      {expandedReply === index && (
                        <div className="mt-3 pt-3 border-t border-gray-200 dark:border-gray-700">
                          {reply.hashtags && reply.hashtags.length > 0 && (
                            <div className="flex flex-wrap gap-1 mb-2">
                              {reply.hashtags.map((tag, tagIndex) => (
                                <span
                                  key={tagIndex}
                                  className="text-xs text-purple-600 dark:text-purple-400"
                                >
                                  #{tag.replace('#', '')}
                                </span>
                              ))}
                            </div>
                          )}
                          <div className="h-1 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                            <div
                              className={cn(
                                'h-full transition-all',
                                reply.character_count > 500 ? 'bg-red-500' :
                                reply.character_count > 450 ? 'bg-yellow-500' : 'bg-green-500'
                              )}
                              style={{ width: `${getCharCountProgress(reply.character_count)}%` }}
                            />
                          </div>
                        </div>
                      )}
                    </CardContent>
                  </Card>
                ))}
              </div>
            )}
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
                      <PhotoIcon className="h-5 w-5 mr-2 text-pink-600 dark:text-pink-400" />
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
                      <div className="bg-gradient-to-br from-purple-50 to-pink-50 dark:from-purple-900/20 dark:to-pink-900/20 p-4 rounded-lg">
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
                  <ChartBarIcon className="h-5 w-5 mr-2 text-purple-600 dark:text-purple-400" />
                  Content Metrics
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <div className="bg-gradient-to-br from-purple-50 to-pink-50 dark:from-purple-900/20 dark:to-pink-900/20 p-4 rounded-lg">
                    <p className="text-2xl font-bold text-gray-900 dark:text-gray-100">
                      {compliance.main_post_chars_count}
                    </p>
                    <p className="text-sm text-gray-600 dark:text-gray-400">Main Post Chars</p>
                  </div>
                  <div className="bg-gradient-to-br from-purple-50 to-pink-50 dark:from-purple-900/20 dark:to-pink-900/20 p-4 rounded-lg">
                    <p className="text-2xl font-bold text-gray-900 dark:text-gray-100">
                      {compliance.replies_total}
                    </p>
                    <p className="text-sm text-gray-600 dark:text-gray-400">Reply Chain</p>
                  </div>
                  <div className="bg-gradient-to-br from-purple-50 to-pink-50 dark:from-purple-900/20 dark:to-pink-900/20 p-4 rounded-lg">
                    <p className="text-2xl font-bold text-gray-900 dark:text-gray-100">
                      {compliance.hashtags_count}
                    </p>
                    <p className="text-sm text-gray-600 dark:text-gray-400">Hashtags</p>
                  </div>
                  <div className="bg-gradient-to-br from-purple-50 to-pink-50 dark:from-purple-900/20 dark:to-pink-900/20 p-4 rounded-lg">
                    <p className="text-2xl font-bold text-gray-900 dark:text-gray-100">
                      {compliance.image_prompt_count}
                    </p>
                    <p className="text-sm text-gray-600 dark:text-gray-400">Images</p>
                  </div>
                </div>

                {/* Status Indicators */}
                <div className="mt-6 grid grid-cols-2 md:grid-cols-3 gap-4">
                  <div className="flex items-center space-x-2">
                    <CheckCircleIcon className={cn(
                      'h-5 w-5',
                      compliance.has_tracked_link ? 'text-green-500' : 'text-gray-400'
                    )} />
                    <span className="text-sm text-gray-700 dark:text-gray-300">Tracked Link</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <CheckCircleIcon className={cn(
                      'h-5 w-5',
                      compliance.per_post_hashtags_ok ? 'text-green-500' : 'text-gray-400'
                    )} />
                    <span className="text-sm text-gray-700 dark:text-gray-300">Hashtags OK</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <CheckCircleIcon className={cn(
                      'h-5 w-5',
                      compliance.per_post_mentions_ok ? 'text-green-500' : 'text-gray-400'
                    )} />
                    <span className="text-sm text-gray-700 dark:text-gray-300">Mentions OK</span>
                  </div>
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

            {/* Character Analysis */}
            {allVersions.length > 1 && (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <ChartBarIcon className="h-5 w-5 mr-2 text-pink-600 dark:text-pink-400" />
                    Version Length Comparison
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    {allVersions.map((version, index) => {
                      const charCount = version.length;
                      return (
                        <div key={index} className="flex items-center">
                          <span className="text-sm text-gray-600 dark:text-gray-400 w-16">
                            {index === 0 ? 'Main' : `Alt ${index}`}
                          </span>
                          <div className="flex-1 mx-3">
                            <div className="h-6 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden relative">
                              <div
                                className={cn(
                                  'h-full transition-all',
                                  charCount > 500 ? 'bg-red-500' :
                                  charCount > 450 ? 'bg-yellow-500' : 'bg-green-500'
                                )}
                                style={{ width: `${getCharCountProgress(charCount)}%` }}
                              />
                              <span className="absolute inset-0 flex items-center justify-center text-xs font-medium text-gray-700 dark:text-gray-300">
                                {charCount} chars
                              </span>
                            </div>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </CardContent>
              </Card>
            )}
          </div>
        )}
      </div>

      {/* Footer */}
      <div className="border-t border-gray-200 dark:border-gray-700 p-4 bg-gradient-to-r from-purple-50 to-pink-50 dark:from-purple-900/20 dark:to-pink-900/20">
        <div className="flex items-center justify-between text-sm text-gray-600 dark:text-gray-400">
          <span>
            Generated with {content.meta?.model_version || 'AI'} • 
            Prompt v{content.meta?.prompt_version || '1.0'}
          </span>
          <div className="flex items-center space-x-4">
            <span className="flex items-center">
              <ChatBubbleLeftIcon className="h-4 w-4 mr-1" />
              {1 + reply_chain.length} posts
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
