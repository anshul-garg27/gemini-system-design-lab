import React, { useState } from 'react';
import { 
  ChatBubbleLeftRightIcon,
  HashtagIcon,
  DocumentDuplicateIcon,
  SparklesIcon,
  ChartBarIcon,
  CheckCircleIcon,
  AtSymbolIcon,
  MegaphoneIcon,
  ArrowPathIcon
} from '@heroicons/react/24/outline';
import { Card, CardContent, CardHeader, CardTitle } from './ui/Card';
import { Button } from './ui/Button';
import { cn } from '../lib/utils';

interface Tweet {
  index: number;
  t?: string;  // tweet text (new schema)
  text?: string;  // tweet text (old schema fallback)
  hashtags: string[];
  mentions: string[];
  media_roles: string[];
  chars_count?: number;  // character count (new schema)
  character_count?: number;  // character count (old schema fallback)
}

interface EngagementTweet {
  t: string;  // tweet text
  poll: {
    enabled: boolean;
    options: string[];
    duration_minutes: number;
  };
}

interface TweetMediaPlan {
  tweet_index: number;
  attach_roles: string[];
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
  tweets_total: number;
  chars_counts: number[];
  hashtags_per_tweet_ok: boolean;
  has_midthread_link: boolean;
  image_prompt_count: number;
  checks: string[];
}

interface XTwitterThreadContent {
  tweets: Tweet[];
  engagement_tweet: EngagementTweet;
  hashtags: string[];
  mention_suggestions: string[];
  tweet_media_plan: TweetMediaPlan[];
  image_prompts: ImagePrompt[];
  compliance: Compliance;
}

interface XTwitterThreadViewProps {
  content: {
    job_id: string;
    platform: string;
    format: string;
    envelope: {
      content: XTwitterThreadContent;
    };
    meta?: {
      topic_title?: string;
      topic_id?: string;
    };
  };
  onCopy: () => void;
}

const XTwitterThreadView: React.FC<XTwitterThreadViewProps> = ({ content, onCopy }) => {
  const [activeTab, setActiveTab] = useState<'thread' | 'analytics' | 'tips'>('thread');
  const [selectedTweet, setSelectedTweet] = useState<number | null>(null);
  
  // Extract content with fallbacks
  const thread = content.envelope?.content || {};
  const meta = content.meta || {};
  
  // Add fallbacks for required properties
  const tweets = thread.tweets || [];
  const compliance = thread.compliance || {
    tweets_total: tweets.length,
    chars_counts: tweets.map(t => t.chars_count || 0),
    hashtags_per_tweet_ok: true,
    has_midthread_link: false,
    image_prompt_count: 0,
    checks: []
  };
  const engagement_tweet = thread.engagement_tweet || {
    t: "What are your thoughts on this topic?",
    poll: { enabled: false, options: [], duration_minutes: 1440 }
  };
  const hashtags = thread.hashtags || [];
  const mention_suggestions = thread.mention_suggestions || [];


  const copyTweet = (tweet: Tweet) => {
    navigator.clipboard.writeText(tweet.t || tweet.text || '');
  };

  const copyAllTweets = () => {
    const allTweets = tweets.map(tweet => tweet.t || tweet.text || '').join('\n\n');
    navigator.clipboard.writeText(allTweets);
  };

  return (
    <div className="bg-white dark:bg-gray-900 rounded-3xl shadow-2xl max-w-6xl w-full max-h-[90vh] overflow-hidden flex flex-col">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-500 to-blue-600 text-white p-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="p-3 bg-white/20 backdrop-blur-sm rounded-xl">
              <ChatBubbleLeftRightIcon className="h-8 w-8" />
            </div>
            <div>
              <h2 className="text-2xl font-bold">X/Twitter Thread</h2>
              {meta.topic_title && (
                <p className="text-blue-100 text-sm mt-1">{meta.topic_title}</p>
              )}
              <p className="text-blue-200 text-xs mt-1">{compliance.tweets_total} tweets</p>
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
            variant={activeTab === 'thread' ? 'primary' : 'ghost'}
            onClick={() => setActiveTab('thread')}
            className={cn(
              "flex-1",
              activeTab === 'thread' && "shadow-sm"
            )}
          >
            <ChatBubbleLeftRightIcon className="h-4 w-4 mr-2" />
            Thread
          </Button>
          <Button
            variant={activeTab === 'analytics' ? 'primary' : 'ghost'}
            onClick={() => setActiveTab('analytics')}
            className={cn(
              "flex-1",
              activeTab === 'analytics' && "shadow-sm"
            )}
          >
            <ChartBarIcon className="h-4 w-4 mr-2" />
            Analytics
          </Button>
          <Button
            variant={activeTab === 'tips' ? 'primary' : 'ghost'}
            onClick={() => setActiveTab('tips')}
            className={cn(
              "flex-1",
              activeTab === 'tips' && "shadow-sm"
            )}
          >
            <SparklesIcon className="h-4 w-4 mr-2" />
            Tips
          </Button>
        </div>
      </div>

      {/* Content Area */}
      <div className="flex-1 overflow-y-auto p-6 bg-gray-50 dark:bg-gray-950">
        {/* Thread Tab */}
        {activeTab === 'thread' && (
          <div className="space-y-6 animate-fade-in">

            {/* Tweet Thread */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center justify-between">
                  <span className="flex items-center">
                    <ChatBubbleLeftRightIcon className="h-5 w-5 mr-2 text-secondary-600 dark:text-secondary-400" />
                    Tweet Thread ({compliance.tweets_total} tweets)
                  </span>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={copyAllTweets}
                    leftIcon={<DocumentDuplicateIcon className="h-4 w-4" />}
                  >
                    Copy All
                  </Button>
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {tweets.map((tweet, index) => (
                  <Card
                    key={index}
                    className={cn(
                      "cursor-pointer hover:shadow-md transition-all border-l-4",
                      selectedTweet === index ? "border-l-primary-500 ring-2 ring-primary-500 dark:ring-primary-400" : "border-l-gray-300 dark:border-l-gray-600",
                      index === 0 && "border-l-success-500", // Hook tweet
                      index === tweets.length - 1 && "border-l-secondary-500" // CTA tweet
                    )}
                    onClick={() => setSelectedTweet(selectedTweet === index ? null : index)}
                  >
                    <CardContent className="p-4">
                      <div className="flex items-start justify-between mb-3">
                        <div className="flex items-center space-x-2">
                          <span className="px-2 py-1 bg-primary-100 dark:bg-primary-900/20 text-primary-800 dark:text-primary-400 rounded-full text-xs font-medium">
                            {tweet.index}/{compliance.tweets_total}
                          </span>
                          {index === 0 && (
                            <span className="px-2 py-1 bg-success-100 dark:bg-success-900/20 text-success-800 dark:text-success-400 rounded-full text-xs font-medium">
                              Hook
                            </span>
                          )}
                          {index === thread.tweets.length - 1 && (
                            <span className="px-2 py-1 bg-secondary-100 dark:bg-secondary-900/20 text-secondary-800 dark:text-secondary-400 rounded-full text-xs font-medium">
                              CTA
                            </span>
                          )}
                        </div>
                        <div className="flex items-center space-x-2">
                          <span className={cn(
                            "text-xs px-2 py-1 rounded",
                            (tweet.chars_count || tweet.character_count || 0) > 280 ? "bg-error-100 dark:bg-error-900/20 text-error-800 dark:text-error-400" :
                            (tweet.chars_count || tweet.character_count || 0) > 240 ? "bg-warning-100 dark:bg-warning-900/20 text-warning-800 dark:text-warning-400" :
                            "bg-success-100 dark:bg-success-900/20 text-success-800 dark:text-success-400"
                          )}>
                            {tweet.chars_count || tweet.character_count || 0}/280
                          </span>
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={(e) => {
                              e.stopPropagation();
                              copyTweet(tweet);
                            }}
                          >
                            <DocumentDuplicateIcon className="h-4 w-4" />
                          </Button>
                        </div>
                      </div>

                      {/* Tweet Text */}
                      <div className="bg-gradient-to-r from-gray-50 to-blue-50 dark:from-gray-800 dark:to-blue-900/20 p-4 rounded-xl border border-gray-200 dark:border-gray-700 mb-3">
                        <p className="text-gray-800 dark:text-gray-200 whitespace-pre-wrap leading-relaxed">
                          {tweet.t || tweet.text || ''}
                        </p>
                      </div>

                      {/* Hashtags and Mentions */}
                      {((tweet.hashtags && tweet.hashtags.length > 0) || (tweet.mentions && tweet.mentions.length > 0)) && (
                        <div className="flex flex-wrap gap-2 mt-3">
                          {(tweet.hashtags || []).map((hashtag, idx) => (
                            <span key={`hashtag-${idx}`} className="px-2 py-1 bg-primary-100 dark:bg-primary-900/20 text-primary-800 dark:text-primary-400 rounded text-xs font-medium">
                              <HashtagIcon className="h-3 w-3 inline mr-1" />
                              {hashtag.startsWith('#') ? hashtag : `#${hashtag}`}
                            </span>
                          ))}
                          {(tweet.mentions || []).map((mention, idx) => (
                            <span key={`mention-${idx}`} className="px-2 py-1 bg-secondary-100 dark:bg-secondary-900/20 text-secondary-800 dark:text-secondary-400 rounded text-xs font-medium">
                              <AtSymbolIcon className="h-3 w-3 inline mr-1" />
                              {mention}
                            </span>
                          ))}
                        </div>
                      )}

                      {selectedTweet !== index && (
                        <p className="text-xs text-gray-500 dark:text-gray-500 mt-2 text-center">
                          Click to view details
                        </p>
                      )}
                    </CardContent>
                  </Card>
                ))}
              </CardContent>
            </Card>

            {/* Engagement Tweet */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <MegaphoneIcon className="h-5 w-5 mr-2 text-secondary-600 dark:text-secondary-400" />
                  Engagement Tweet
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="bg-gradient-to-r from-secondary-50 to-pink-50 dark:from-secondary-900/20 dark:to-pink-900/20 p-4 rounded-xl border border-secondary-200 dark:border-secondary-700">
                  <div className="flex items-center justify-between mb-2">
                    <span className="px-2 py-1 bg-secondary-100 dark:bg-secondary-900/20 text-secondary-800 dark:text-secondary-400 rounded-full text-xs font-medium">
                      {engagement_tweet.poll.enabled ? "Poll" : "Question"}
                    </span>
                    {engagement_tweet.poll.enabled && (
                      <span className="text-sm text-gray-600 dark:text-gray-400">
                        {engagement_tweet.poll.duration_minutes}min
                      </span>
                    )}
                  </div>
                  <p className="text-secondary-800 dark:text-secondary-400 font-medium">
                    {engagement_tweet.t}
                  </p>
                  {engagement_tweet.poll.enabled && engagement_tweet.poll.options.length > 0 && (
                    <div className="mt-3 space-y-2">
                      {engagement_tweet.poll.options.map((option, idx) => (
                        <div key={idx} className="px-3 py-2 bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700">
                          <span className="text-sm text-gray-700 dark:text-gray-300">{option}</span>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>

            {/* Mention Suggestions */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <AtSymbolIcon className="h-5 w-5 mr-2 text-primary-600 dark:text-primary-400" />
                  Mention Suggestions
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex flex-wrap gap-2">
                  {mention_suggestions.map((mention, idx) => (
                    <span key={idx} className="px-3 py-1 bg-primary-100 dark:bg-primary-900/20 text-primary-800 dark:text-primary-400 rounded-full text-sm font-medium border border-primary-200 dark:border-primary-700">
                      {mention}
                    </span>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Image Prompts */}
            {thread.image_prompts && thread.image_prompts.length > 0 && (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <SparklesIcon className="h-5 w-5 mr-2 text-secondary-600 dark:text-secondary-400" />
                    Image Prompts ({thread.image_prompts.length})
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {thread.image_prompts.map((prompt, idx) => (
                      <Card key={idx} variant="filled">
                        <CardContent className="p-4">
                          <div className="flex items-start justify-between mb-3">
                            <div className="flex items-center space-x-2">
                              <span className="px-2 py-1 bg-secondary-100 dark:bg-secondary-900/20 text-secondary-800 dark:text-secondary-400 rounded-full text-xs font-medium">
                                {prompt.role}
                              </span>
                              <span className="px-2 py-1 bg-primary-100 dark:bg-primary-900/20 text-primary-800 dark:text-primary-400 rounded-full text-xs font-medium">
                                {prompt.ratio}
                              </span>
                              <span className="px-2 py-1 bg-success-100 dark:bg-success-900/20 text-success-800 dark:text-success-400 rounded-full text-xs font-medium">
                                {prompt.size_px}
                              </span>
                            </div>
                          </div>
                          
                          <div className="space-y-3">
                            <div>
                              <h4 className="font-medium text-gray-900 dark:text-gray-100 mb-1">{prompt.title}</h4>
                              <p className="text-sm text-gray-600 dark:text-gray-400">{prompt.alt_text}</p>
                            </div>
                            
                            <div>
                              <h5 className="text-sm font-medium text-gray-800 dark:text-gray-200 mb-1">Prompt:</h5>
                              <p className="text-sm text-gray-700 dark:text-gray-300 bg-gray-50 dark:bg-gray-800 p-3 rounded-lg border">
                                {prompt.prompt}
                              </p>
                            </div>
                            
                            <div>
                              <h5 className="text-sm font-medium text-gray-800 dark:text-gray-200 mb-1">Negative Prompt:</h5>
                              <p className="text-sm text-gray-700 dark:text-gray-300 bg-gray-50 dark:bg-gray-800 p-3 rounded-lg border">
                                {prompt.negative_prompt}
                              </p>
                            </div>
                            
                            {prompt.style_notes && (
                              <div>
                                <h5 className="text-sm font-medium text-gray-800 dark:text-gray-200 mb-1">Style Notes:</h5>
                                <p className="text-sm text-gray-600 dark:text-gray-400">{prompt.style_notes}</p>
                              </div>
                            )}
                          </div>
                        </CardContent>
                      </Card>
                    ))}
                  </div>
                </CardContent>
              </Card>
            )}
          </div>
        )}

        {/* Analytics Tab */}
        {activeTab === 'analytics' && (
          <div className="space-y-6 animate-fade-in">
            {/* Engagement Metrics */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <ChartBarIcon className="h-5 w-5 mr-2 text-primary-600 dark:text-primary-400" />
                  Thread Analytics
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <Card variant="filled">
                    <CardContent className="p-4 text-center">
                      <p className="text-2xl font-bold text-primary-600 dark:text-primary-400">{compliance.tweets_total}</p>
                      <p className="text-xs text-gray-600 dark:text-gray-400 mt-1">Total Tweets</p>
                    </CardContent>
                  </Card>
                  <Card variant="filled">
                    <CardContent className="p-4 text-center">
                      <p className="text-2xl font-bold text-secondary-600 dark:text-secondary-400">
                        {compliance.chars_counts.length > 0 ? Math.round(compliance.chars_counts.reduce((acc, count) => acc + count, 0) / compliance.chars_counts.length) : 0}
                      </p>
                      <p className="text-xs text-gray-600 dark:text-gray-400 mt-1">Avg Characters</p>
                    </CardContent>
                  </Card>
                  <Card variant="filled">
                    <CardContent className="p-4 text-center">
                      <p className="text-2xl font-bold text-success-600 dark:text-success-400">
                        {hashtags.length}
                      </p>
                      <p className="text-xs text-gray-600 dark:text-gray-400 mt-1">Total Hashtags</p>
                    </CardContent>
                  </Card>
                  <Card variant="filled">
                    <CardContent className="p-4 text-center">
                      <span className={cn(
                        "text-2xl font-bold px-3 py-1 rounded-full text-xs font-medium border",
                        compliance.hashtags_per_tweet_ok ? "bg-success-100 dark:bg-success-900/20 text-success-800 dark:text-success-400 border-success-200 dark:border-success-700" : "bg-error-100 dark:bg-error-900/20 text-error-800 dark:text-error-400 border-error-200 dark:border-error-700"
                      )}>
                        {compliance.hashtags_per_tweet_ok ? "✓" : "✗"}
                      </span>
                      <p className="text-xs text-gray-600 dark:text-gray-400 mt-1">Hashtag Limit</p>
                    </CardContent>
                  </Card>
                </div>
              </CardContent>
            </Card>

            {/* Character Count Analysis */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <SparklesIcon className="h-5 w-5 mr-2 text-secondary-600 dark:text-secondary-400" />
                  Character Count Analysis
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {tweets.map((tweet, index) => (
                    <div key={index} className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
                      <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                        Tweet {tweet.index}
                      </span>
                      <div className="flex items-center space-x-3">
                        <div className="w-32 bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                          <div
                            className={cn(
                              "h-2 rounded-full transition-all",
                              (tweet.chars_count || tweet.character_count || 0) > 280 ? "bg-error-500" :
                              (tweet.chars_count || tweet.character_count || 0) > 240 ? "bg-warning-500" :
                              "bg-success-500"
                            )}
                            style={{ width: `${Math.min(((tweet.chars_count || tweet.character_count || 0) / 280) * 100, 100)}%` }}
                          />
                        </div>
                        <span className={cn(
                          "text-sm font-medium",
                          (tweet.chars_count || tweet.character_count || 0) > 280 ? "text-error-600 dark:text-error-400" :
                          (tweet.chars_count || tweet.character_count || 0) > 240 ? "text-warning-600 dark:text-warning-400" :
                          "text-success-600 dark:text-success-400"
                        )}>
                          {tweet.chars_count || tweet.character_count || 0}/280
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Hashtag Distribution */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <HashtagIcon className="h-5 w-5 mr-2 text-primary-600 dark:text-primary-400" />
                  Hashtag Distribution
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex flex-wrap gap-2">
                  {hashtags.map((hashtag, idx) => (
                    <span key={idx} className="px-3 py-1 bg-primary-100 dark:bg-primary-900/20 text-primary-800 dark:text-primary-400 rounded-full text-sm font-medium">
                      {hashtag.startsWith('#') ? hashtag : `#${hashtag}`}
                    </span>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Image Prompts Summary */}
            {thread.image_prompts && thread.image_prompts.length > 0 && (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <SparklesIcon className="h-5 w-5 mr-2 text-secondary-600 dark:text-secondary-400" />
                    Image Prompts Summary
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {thread.image_prompts.map((prompt, idx) => (
                      <Card key={idx} variant="filled">
                        <CardContent className="p-4">
                          <div className="flex items-center justify-between mb-2">
                            <span className="px-2 py-1 bg-secondary-100 dark:bg-secondary-900/20 text-secondary-800 dark:text-secondary-400 rounded-full text-xs font-medium">
                              {prompt.role}
                            </span>
                            <span className="text-xs text-gray-500 dark:text-gray-400">
                              {prompt.ratio} • {prompt.size_px}
                            </span>
                          </div>
                          <h4 className="font-medium text-gray-900 dark:text-gray-100 mb-2">{prompt.title}</h4>
                          <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">{prompt.alt_text}</p>
                          <div className="text-xs text-gray-500 dark:text-gray-400 bg-gray-50 dark:bg-gray-800 p-2 rounded border">
                            <strong>Prompt:</strong> {prompt.prompt.substring(0, 100)}...
                          </div>
                        </CardContent>
                      </Card>
                    ))}
                  </div>
                </CardContent>
              </Card>
            )}
          </div>
        )}

        {/* Tips Tab */}
        {activeTab === 'tips' && (
          <div className="space-y-6 animate-fade-in">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <CheckCircleIcon className="h-5 w-5 mr-2 text-success-600 dark:text-success-400" />
                  Compliance Checks
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {compliance.checks.map((check, index) => (
                    <div key={index} className="flex items-start p-4 bg-success-50 dark:bg-success-900/20 rounded-lg border border-success-200 dark:border-success-700">
                      <CheckCircleIcon className="h-5 w-5 text-success-600 dark:text-success-400 mr-3 flex-shrink-0 mt-0.5" />
                      <p className="text-success-800 dark:text-success-300 text-sm">
                        {check}
                      </p>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Best Practices */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <ArrowPathIcon className="h-5 w-5 mr-2 text-secondary-600 dark:text-secondary-400" />
                  Thread Best Practices
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <Card variant="filled">
                    <CardContent className="p-4">
                      <h4 className="font-medium text-gray-900 dark:text-gray-100 mb-2">Timing</h4>
                      <p className="text-sm text-gray-600 dark:text-gray-400">Post when your audience is most active (typically 9-10 AM or 7-9 PM)</p>
                    </CardContent>
                  </Card>
                  <Card variant="filled">
                    <CardContent className="p-4">
                      <h4 className="font-medium text-gray-900 dark:text-gray-100 mb-2">Engagement</h4>
                      <p className="text-sm text-gray-600 dark:text-gray-400">Respond to comments quickly to boost engagement and reach</p>
                    </CardContent>
                  </Card>
                  <Card variant="filled">
                    <CardContent className="p-4">
                      <h4 className="font-medium text-gray-900 dark:text-gray-100 mb-2">Hashtags</h4>
                      <p className="text-sm text-gray-600 dark:text-gray-400">Use 2-3 relevant hashtags per tweet, mix trending and niche tags</p>
                    </CardContent>
                  </Card>
                  <Card variant="filled">
                    <CardContent className="p-4">
                      <h4 className="font-medium text-gray-900 dark:text-gray-100 mb-2">Hook</h4>
                      <p className="text-sm text-gray-600 dark:text-gray-400">Start with a compelling hook that promises value or creates curiosity</p>
                    </CardContent>
                  </Card>
                </div>
              </CardContent>
            </Card>
          </div>
        )}
      </div>

      {/* Footer */}
      <div className="border-t border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900 p-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-6 text-sm">
            <div className="flex items-center">
              <ChatBubbleLeftRightIcon className="h-4 w-4 mr-1 text-gray-500 dark:text-gray-400" />
              <span className="text-gray-600 dark:text-gray-400">
                {compliance.tweets_total} tweets
              </span>
            </div>
            <div className="flex items-center">
              <ChartBarIcon className="h-4 w-4 mr-1 text-gray-500 dark:text-gray-400" />
              <span className="text-gray-600 dark:text-gray-400">
                {compliance.chars_counts.length > 0 ? Math.round(compliance.chars_counts.reduce((acc, count) => acc + count, 0) / compliance.chars_counts.length) : 0} avg chars
              </span>
            </div>
            <div className="flex items-center">
              <HashtagIcon className="h-4 w-4 mr-1 text-gray-500 dark:text-gray-400" />
              <span className="text-gray-600 dark:text-gray-400">
                {hashtags.length} hashtags
              </span>
            </div>
          </div>
          <div className="flex items-center">
            <span className={cn(
              "px-3 py-1 rounded-full text-sm font-medium border",
              compliance.has_midthread_link ? "bg-success-100 dark:bg-success-900/20 text-success-800 dark:text-success-400 border-success-200 dark:border-success-700" : "bg-warning-100 dark:bg-warning-900/20 text-warning-800 dark:text-warning-400 border-warning-200 dark:border-warning-700"
            )}>
              {compliance.has_midthread_link ? "Has Link" : "No Link"}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default XTwitterThreadView;
