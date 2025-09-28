import React, { useState } from 'react';
import { 
  ChatBubbleLeftIcon,
  DocumentDuplicateIcon,
  UserGroupIcon,
  TagIcon,
  ClockIcon,
  QuestionMarkCircleIcon,
  ExclamationTriangleIcon,
  ChatBubbleBottomCenterTextIcon,
  CheckCircleIcon,
  ArrowUpIcon
} from '@heroicons/react/24/outline';
import { Card, CardContent, CardHeader, CardTitle } from './ui/Card';
import { Button } from './ui/Button';
import { cn } from '../lib/utils';

// Interfaces
interface LinkPlan {
  enabled: boolean;
  insert_after_paragraph: number;
  url: string;
}

interface Structure {
  paragraphs: string[];
  link_plan: LinkPlan;
}

interface Subreddit {
  name: string;
  why_relevant: string;
  posting_time_hint: string;
  flair_suggestions: string[];
  rules_checklist: string[];
}

interface FAQ {
  q: string;
  a: string;
}

interface CommentPreparation {
  top_level_seeds: string[];
  faqs: FAQ[];
}

interface RedditPostContent {
  title: string;
  body: string;
  structure: Structure;
  suggested_subreddits: Subreddit[];
  comment_preparation: CommentPreparation;
  image_prompts: any[];
  moderation_notes: string[];
}

interface RedditPostViewProps {
  content: any;
}

export const RedditPostView: React.FC<RedditPostViewProps> = ({ content }) => {
  const [activeTab, setActiveTab] = useState<'post' | 'subreddits' | 'comments' | 'guidelines'>('post');
  const [expandedSubreddit, setExpandedSubreddit] = useState<number | null>(null);

  // Parse content
  const redditPost: RedditPostContent = content.envelope?.content || content.content || content;
  const {
    title = '',
    body = '',
    structure = {
      paragraphs: [],
      link_plan: { enabled: false, insert_after_paragraph: 0, url: '' }
    },
    suggested_subreddits = [],
    comment_preparation = {
      top_level_seeds: [],
      faqs: []
    },
    image_prompts = [],
    moderation_notes = []
  } = redditPost;

  // Copy functions
  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
  };

  const copyPost = () => {
    const fullPost = `${title}\n\n${body}`;
    copyToClipboard(fullPost);
  };

  const copyTitle = () => {
    copyToClipboard(title);
  };

  const copyBody = () => {
    copyToClipboard(body);
  };

  const copyComment = (text: string) => {
    copyToClipboard(text);
  };

  const getCharCount = (text: string) => {
    return text.length;
  };

  const getWordCount = (text: string) => {
    return text.split(/\s+/).filter(word => word.length > 0).length;
  };

  // Split body into paragraphs for analysis
  const bodyParagraphs = body.split('\n\n').filter(p => p.trim());

  return (
    <div className="bg-white dark:bg-gray-900 rounded-3xl shadow-2xl max-w-7xl w-full max-h-[90vh] overflow-hidden flex flex-col">
      {/* Header */}
      <div className="bg-gradient-to-r from-orange-600 to-red-600 text-white p-6">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold flex items-center">
              <ArrowUpIcon className="h-8 w-8 mr-3" />
              Reddit Post
            </h2>
            <p className="text-orange-100 mt-1">
              {title || content.meta?.topic_title || 'Reddit Post Content'}
            </p>
          </div>
          <div className="flex space-x-4 text-sm">
            <div className="text-center">
              <div className="text-2xl font-bold">{getCharCount(title)}</div>
              <div className="text-orange-100">Title Chars</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold">{getWordCount(body)}</div>
              <div className="text-orange-100">Body Words</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold">{suggested_subreddits.length}</div>
              <div className="text-orange-100">Subreddits</div>
            </div>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex border-b border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800/50">
        {(['post', 'subreddits', 'comments', 'guidelines'] as const).map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={cn(
              'flex-1 px-6 py-3 text-sm font-medium transition-all capitalize',
              activeTab === tab
                ? 'text-orange-600 dark:text-orange-400 border-b-2 border-orange-600 dark:border-orange-400 bg-white dark:bg-gray-800'
                : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-100'
            )}
          >
            {tab === 'post' && <ChatBubbleLeftIcon className="h-4 w-4 inline mr-2" />}
            {tab === 'subreddits' && <UserGroupIcon className="h-4 w-4 inline mr-2" />}
            {tab === 'comments' && <ChatBubbleBottomCenterTextIcon className="h-4 w-4 inline mr-2" />}
            {tab === 'guidelines' && <ExclamationTriangleIcon className="h-4 w-4 inline mr-2" />}
            {tab}
          </button>
        ))}
      </div>

      {/* Content */}
      <div className="flex-1 overflow-y-auto p-6">
        {/* Post Tab */}
        {activeTab === 'post' && (
          <div className="space-y-6">
            {/* Title */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center justify-between">
                  <span className="flex items-center">
                    <ChatBubbleLeftIcon className="h-5 w-5 mr-2 text-orange-600 dark:text-orange-400" />
                    Post Title
                  </span>
                  <div className="flex items-center space-x-2">
                    <span className={cn(
                      'text-sm font-medium',
                      getCharCount(title) > 300 ? 'text-red-600 dark:text-red-400' : 'text-green-600 dark:text-green-400'
                    )}>
                      {getCharCount(title)}/300
                    </span>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={copyTitle}
                      leftIcon={<DocumentDuplicateIcon className="h-4 w-4" />}
                    >
                      Copy
                    </Button>
                  </div>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="bg-orange-50 dark:bg-orange-900/20 p-4 rounded-lg">
                  <h3 className="text-xl font-semibold text-gray-900 dark:text-gray-100">
                    {title}
                  </h3>
                </div>
              </CardContent>
            </Card>

            {/* Body */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center justify-between">
                  <span className="flex items-center">
                    <DocumentDuplicateIcon className="h-5 w-5 mr-2 text-orange-600 dark:text-orange-400" />
                    Post Body
                  </span>
                  <div className="flex items-center space-x-3">
                    <span className="text-sm text-gray-600 dark:text-gray-400">
                      {getWordCount(body)} words • {bodyParagraphs.length} paragraphs
                    </span>
                    <Button
                      variant="primary"
                      size="sm"
                      onClick={copyBody}
                      leftIcon={<DocumentDuplicateIcon className="h-4 w-4" />}
                    >
                      Copy Body
                    </Button>
                  </div>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {bodyParagraphs.map((paragraph, index) => (
                    <div key={index} className="relative">
                      {structure.link_plan.enabled && index === structure.link_plan.insert_after_paragraph && (
                        <div className="absolute -top-3 right-0 text-xs bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 px-2 py-1 rounded">
                          Link inserted after this paragraph
                        </div>
                      )}
                      <div className={cn(
                        'p-4 rounded-lg',
                        index === 0 ? 'bg-gray-50 dark:bg-gray-800' :
                        index === bodyParagraphs.length - 1 ? 'bg-blue-50 dark:bg-blue-900/20' :
                        'bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-700'
                      )}>
                        <p className="text-gray-700 dark:text-gray-300 whitespace-pre-wrap">
                          {paragraph}
                        </p>
                        {index < structure.paragraphs.length && (
                          <p className="text-xs text-gray-500 dark:text-gray-500 mt-2 italic">
                            {structure.paragraphs[index]}
                          </p>
                        )}
                      </div>
                    </div>
                  ))}
                </div>

                {/* Copy Full Post Button */}
                <div className="mt-6 pt-6 border-t border-gray-200 dark:border-gray-700 text-center">
                  <Button
                    variant="primary"
                    onClick={copyPost}
                    leftIcon={<DocumentDuplicateIcon className="h-5 w-5" />}
                  >
                    Copy Complete Post
                  </Button>
                </div>
              </CardContent>
            </Card>
          </div>
        )}

        {/* Subreddits Tab */}
        {activeTab === 'subreddits' && (
          <div className="space-y-4">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 flex items-center">
              <UserGroupIcon className="h-5 w-5 mr-2 text-orange-600 dark:text-orange-400" />
              Suggested Subreddits
            </h3>
            
            {suggested_subreddits.map((subreddit, index) => (
              <Card
                key={index}
                className={cn(
                  'cursor-pointer transition-all',
                  expandedSubreddit === index ? 'ring-2 ring-orange-500' : 'hover:shadow-lg'
                )}
                onClick={() => setExpandedSubreddit(expandedSubreddit === index ? null : index)}
              >
                <CardContent className="p-4">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <h4 className="text-lg font-semibold text-orange-600 dark:text-orange-400">
                        {subreddit.name}
                      </h4>
                      <p className="text-gray-700 dark:text-gray-300 mt-1">
                        {subreddit.why_relevant}
                      </p>
                      
                      {expandedSubreddit === index && (
                        <div className="mt-4 space-y-4">
                          {/* Posting Time */}
                          <div>
                            <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-1 flex items-center">
                              <ClockIcon className="h-4 w-4 mr-1" />
                              Best Posting Time
                            </p>
                            <p className="text-sm text-gray-600 dark:text-gray-400">
                              {subreddit.posting_time_hint}
                            </p>
                          </div>

                          {/* Flair Suggestions */}
                          {subreddit.flair_suggestions.length > 0 && (
                            <div>
                              <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2 flex items-center">
                                <TagIcon className="h-4 w-4 mr-1" />
                                Suggested Flairs
                              </p>
                              <div className="flex flex-wrap gap-2">
                                {subreddit.flair_suggestions.map((flair, flairIndex) => (
                                  <span
                                    key={flairIndex}
                                    className="px-3 py-1 bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-full text-sm"
                                  >
                                    {flair}
                                  </span>
                                ))}
                              </div>
                            </div>
                          )}

                          {/* Rules Checklist */}
                          {subreddit.rules_checklist.length > 0 && (
                            <div>
                              <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2 flex items-center">
                                <CheckCircleIcon className="h-4 w-4 mr-1" />
                                Rules to Check
                              </p>
                              <ul className="space-y-1">
                                {subreddit.rules_checklist.map((rule, ruleIndex) => (
                                  <li key={ruleIndex} className="flex items-center text-sm text-gray-600 dark:text-gray-400">
                                    <CheckCircleIcon className="h-3 w-3 text-green-500 mr-2" />
                                    {rule}
                                  </li>
                                ))}
                              </ul>
                            </div>
                          )}
                        </div>
                      )}
                    </div>
                    <ArrowUpIcon className={cn(
                      'h-5 w-5 text-gray-400 transition-transform',
                      expandedSubreddit === index ? 'rotate-180' : ''
                    )} />
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        )}

        {/* Comments Tab */}
        {activeTab === 'comments' && (
          <div className="space-y-6">
            {/* Top Level Comments */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <ChatBubbleBottomCenterTextIcon className="h-5 w-5 mr-2 text-blue-600 dark:text-blue-400" />
                  Discussion Starters
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {comment_preparation.top_level_seeds.map((seed, index) => (
                    <div key={index} className="bg-blue-50 dark:bg-blue-900/20 p-4 rounded-lg">
                      <p className="text-gray-700 dark:text-gray-300 mb-2">{seed}</p>
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => copyComment(seed)}
                        leftIcon={<DocumentDuplicateIcon className="h-3 w-3" />}
                      >
                        Copy
                      </Button>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* FAQs */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <QuestionMarkCircleIcon className="h-5 w-5 mr-2 text-purple-600 dark:text-purple-400" />
                  Anticipated FAQs
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {comment_preparation.faqs.map((faq, index) => (
                    <div key={index} className="border-l-4 border-purple-500 pl-4">
                      <p className="font-medium text-gray-900 dark:text-gray-100 mb-2">
                        Q: {faq.q}
                      </p>
                      <p className="text-gray-700 dark:text-gray-300 mb-2">
                        A: {faq.a}
                      </p>
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => copyComment(`Q: ${faq.q}\n\nA: ${faq.a}`)}
                        leftIcon={<DocumentDuplicateIcon className="h-3 w-3" />}
                      >
                        Copy Q&A
                      </Button>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>
        )}

        {/* Guidelines Tab */}
        {activeTab === 'guidelines' && (
          <div className="space-y-6">
            {/* Moderation Notes */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <ExclamationTriangleIcon className="h-5 w-5 mr-2 text-yellow-600 dark:text-yellow-400" />
                  Moderation Guidelines
                </CardTitle>
              </CardHeader>
              <CardContent>
                <ul className="space-y-2">
                  {moderation_notes.map((note, index) => (
                    <li key={index} className="flex items-start">
                      <ExclamationTriangleIcon className="h-5 w-5 text-yellow-500 mr-2 mt-0.5 flex-shrink-0" />
                      <span className="text-gray-700 dark:text-gray-300">{note}</span>
                    </li>
                  ))}
                </ul>
              </CardContent>
            </Card>

            {/* Post Structure Guidelines */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <DocumentDuplicateIcon className="h-5 w-5 mr-2 text-green-600 dark:text-green-400" />
                  Post Structure
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {structure.paragraphs.map((guideline, index) => (
                    <div key={index} className="flex items-start">
                      <span className="flex-shrink-0 w-8 h-8 bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-300 rounded-full flex items-center justify-center text-sm font-medium">
                        {index + 1}
                      </span>
                      <span className="ml-3 text-gray-700 dark:text-gray-300">{guideline}</span>
                    </div>
                  ))}
                </div>
                
                {structure.link_plan.enabled && (
                  <div className="mt-4 p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
                    <p className="text-sm text-blue-700 dark:text-blue-300">
                      <strong>Link Placement:</strong> Insert after paragraph {structure.link_plan.insert_after_paragraph + 1}
                    </p>
                    <p className="text-xs text-blue-600 dark:text-blue-400 mt-1 font-mono">
                      {structure.link_plan.url}
                    </p>
                  </div>
                )}
              </CardContent>
            </Card>

            {/* Best Practices */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <CheckCircleIcon className="h-5 w-5 mr-2 text-blue-600 dark:text-blue-400" />
                  Reddit Best Practices
                </CardTitle>
              </CardHeader>
              <CardContent>
                <ul className="space-y-2">
                  <li className="flex items-start">
                    <CheckCircleIcon className="h-5 w-5 text-green-500 mr-2 mt-0.5 flex-shrink-0" />
                    <span className="text-gray-700 dark:text-gray-300">
                      Engage authentically with the community
                    </span>
                  </li>
                  <li className="flex items-start">
                    <CheckCircleIcon className="h-5 w-5 text-green-500 mr-2 mt-0.5 flex-shrink-0" />
                    <span className="text-gray-700 dark:text-gray-300">
                      Follow subreddit-specific rules and culture
                    </span>
                  </li>
                  <li className="flex items-start">
                    <CheckCircleIcon className="h-5 w-5 text-green-500 mr-2 mt-0.5 flex-shrink-0" />
                    <span className="text-gray-700 dark:text-gray-300">
                      Respond to comments promptly and helpfully
                    </span>
                  </li>
                  <li className="flex items-start">
                    <CheckCircleIcon className="h-5 w-5 text-green-500 mr-2 mt-0.5 flex-shrink-0" />
                    <span className="text-gray-700 dark:text-gray-300">
                      Avoid excessive self-promotion
                    </span>
                  </li>
                </ul>
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
              <ChatBubbleLeftIcon className="h-4 w-4 mr-1" />
              {getWordCount(body)} words
            </span>
            <span className="flex items-center">
              <UserGroupIcon className="h-4 w-4 mr-1" />
              {suggested_subreddits.length} subreddits
            </span>
            <span className="flex items-center">
              <QuestionMarkCircleIcon className="h-4 w-4 mr-1" />
              {comment_preparation.faqs.length} FAQs
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};
