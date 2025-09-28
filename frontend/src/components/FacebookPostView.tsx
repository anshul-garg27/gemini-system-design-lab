import React, { useState } from 'react';
import { 
  ShareIcon,
  UserGroupIcon,
  HashtagIcon,
  DocumentDuplicateIcon,
  LinkIcon,
  ChartBarIcon,
  ChatBubbleLeftRightIcon,
  PhotoIcon,
  CheckCircleIcon,
  GlobeAltIcon,
  HeartIcon,
  ChatBubbleBottomCenterTextIcon
} from '@heroicons/react/24/outline';
import { Card, CardContent, CardHeader, CardTitle } from './ui/Card';
import { Button } from './ui/Button';
import { cn } from '../lib/utils';

// Interfaces
interface GroupToShare {
  name: string;
  type: string;
  url: string;
  why_relevant: string;
  share_blurb: string;
  rules_checklist: string[];
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

interface LinkPreview {
  title: string;
  description: string;
  og_image_role: string;
}

interface LongBody {
  text: string;
  word_count: number;
  emotional_angle: string;
}

interface Compliance {
  post_lines_count: number;
  long_body_word_count: number;
  hashtags_count: number;
  groups_count: number;
  image_prompt_count: number;
  has_tracked_link: boolean;
  checks: string[];
}

interface FacebookPostContent {
  headline: string;
  post: string;
  alt_versions: string[];
  long_body: LongBody;
  link_preview: LinkPreview;
  groups_pitch: string;
  groups_to_share: GroupToShare[];
  hashtags: string[];
  mention_suggestions: string[];
  image_prompts: ImagePrompt[];
  compliance: Compliance;
}

interface FacebookPostViewProps {
  content: any;
}

export const FacebookPostView: React.FC<FacebookPostViewProps> = ({ content }) => {
  const [activeTab, setActiveTab] = useState<'post' | 'groups' | 'images' | 'analytics'>('post');
  const [selectedVersion, setSelectedVersion] = useState(0);
  const [expandedGroup, setExpandedGroup] = useState<number | null>(null);

  // Parse content
  const facebookPost: FacebookPostContent = content.envelope?.content || content.content || content;
  const {
    headline = '',
    post = '',
    alt_versions = [],
    long_body = { text: '', word_count: 0, emotional_angle: '' },
    link_preview = { title: '', description: '', og_image_role: '' },
    groups_pitch = '',
    groups_to_share = [],
    hashtags = [],
    mention_suggestions = [],
    image_prompts = [],
    compliance = {
      post_lines_count: 0,
      long_body_word_count: 0,
      hashtags_count: 0,
      groups_count: 0,
      image_prompt_count: 0,
      has_tracked_link: false,
      checks: []
    }
  } = facebookPost;

  const allVersions = [post, ...alt_versions];

  // Copy functions
  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
  };

  const copyPost = () => {
    const fullPost = `${headline}\n\n${allVersions[selectedVersion]}\n\n${hashtags.map(tag => `#${tag.replace('#', '')}`).join(' ')}`;
    copyToClipboard(fullPost);
  };

  const copyGroupBlurb = (blurb: string) => {
    copyToClipboard(blurb);
  };

  const getGroupTypeIcon = (type: string) => {
    switch (type.toLowerCase()) {
      case 'group':
        return <UserGroupIcon className="h-4 w-4" />;
      case 'page':
        return <GlobeAltIcon className="h-4 w-4" />;
      case 'community':
        return <HeartIcon className="h-4 w-4" />;
      default:
        return <ChatBubbleLeftRightIcon className="h-4 w-4" />;
    }
  };

  const getGroupRelevanceColor = (index: number) => {
    const colors = [
      'border-blue-500 bg-blue-50 dark:bg-blue-900/20',
      'border-purple-500 bg-purple-50 dark:bg-purple-900/20',
      'border-green-500 bg-green-50 dark:bg-green-900/20',
      'border-yellow-500 bg-yellow-50 dark:bg-yellow-900/20',
      'border-pink-500 bg-pink-50 dark:bg-pink-900/20'
    ];
    return colors[index % colors.length];
  };

  return (
    <div className="bg-white dark:bg-gray-900 rounded-3xl shadow-2xl max-w-7xl w-full max-h-[90vh] overflow-hidden flex flex-col">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-600 to-blue-700 text-white p-6">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold flex items-center">
              <ShareIcon className="h-8 w-8 mr-3" />
              Facebook Post
            </h2>
            <p className="text-blue-100 mt-1">
              {content.meta?.topic_title || 'Facebook Post Content'}
            </p>
          </div>
          <div className="flex space-x-4 text-sm">
            <div className="text-center">
              <div className="text-2xl font-bold">{groups_to_share.length}</div>
              <div className="text-blue-100">Groups</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold">{hashtags.length}</div>
              <div className="text-blue-100">Hashtags</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold">{allVersions.length}</div>
              <div className="text-blue-100">Versions</div>
            </div>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex border-b border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800/50">
        {(['post', 'groups', 'images', 'analytics'] as const).map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={cn(
              'flex-1 px-6 py-3 text-sm font-medium transition-all capitalize',
              activeTab === tab
                ? 'text-blue-600 dark:text-blue-400 border-b-2 border-blue-600 dark:border-blue-400 bg-white dark:bg-gray-800'
                : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-100'
            )}
          >
            {tab === 'post' && <ShareIcon className="h-4 w-4 inline mr-2" />}
            {tab === 'groups' && <UserGroupIcon className="h-4 w-4 inline mr-2" />}
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
            {/* Main Post */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center justify-between">
                  <span className="flex items-center">
                    <ShareIcon className="h-5 w-5 mr-2 text-blue-600 dark:text-blue-400" />
                    Post Content
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
              <CardContent>
                {/* Headline */}
                <div className="mb-6">
                  <h3 className="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-2">
                    {headline}
                  </h3>
                </div>

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
                              ? 'bg-blue-600 text-white'
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
                <div className="bg-gray-50 dark:bg-gray-800 p-6 rounded-xl">
                  <p className="text-gray-800 dark:text-gray-200 whitespace-pre-wrap text-lg leading-relaxed">
                    {allVersions[selectedVersion]}
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
                  {mention_suggestions.length > 0 && (
                    <div className="mt-3 text-sm text-gray-600 dark:text-gray-400">
                      Mentions: {mention_suggestions.join(', ')}
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>

            {/* Long Form Content */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <DocumentDuplicateIcon className="h-5 w-5 mr-2 text-purple-600 dark:text-purple-400" />
                  Long Form Content
                  <span className="ml-2 text-sm font-normal text-gray-500 dark:text-gray-400">
                    ({long_body.word_count} words • {long_body.emotional_angle})
                  </span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="bg-gray-50 dark:bg-gray-800 p-6 rounded-xl max-h-96 overflow-y-auto">
                  <p className="text-gray-700 dark:text-gray-300 whitespace-pre-wrap leading-relaxed">
                    {long_body.text}
                  </p>
                </div>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => copyToClipboard(long_body.text)}
                  leftIcon={<DocumentDuplicateIcon className="h-4 w-4" />}
                  className="mt-4"
                >
                  Copy Long Form
                </Button>
              </CardContent>
            </Card>

            {/* Link Preview */}
            {link_preview.title && (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <LinkIcon className="h-5 w-5 mr-2 text-green-600 dark:text-green-400" />
                    Link Preview
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="bg-gray-50 dark:bg-gray-800 p-4 rounded-xl border border-gray-200 dark:border-gray-700">
                    <div className="flex items-start space-x-4">
                      <div className="flex-shrink-0 w-32 h-32 bg-gradient-to-br from-gray-200 to-gray-300 dark:from-gray-700 dark:to-gray-600 rounded-lg flex items-center justify-center">
                        <PhotoIcon className="h-12 w-12 text-gray-400 dark:text-gray-500" />
                        <span className="sr-only">{link_preview.og_image_role}</span>
                      </div>
                      <div className="flex-1">
                        <h4 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-2">
                          {link_preview.title}
                        </h4>
                        <p className="text-gray-600 dark:text-gray-400 text-sm">
                          {link_preview.description}
                        </p>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            )}
          </div>
        )}

        {/* Groups Tab */}
        {activeTab === 'groups' && (
          <div className="space-y-6">
            {/* Groups Pitch */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <ChatBubbleBottomCenterTextIcon className="h-5 w-5 mr-2 text-indigo-600 dark:text-indigo-400" />
                  Groups Strategy
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-gray-700 dark:text-gray-300">
                  {groups_pitch}
                </p>
              </CardContent>
            </Card>

            {/* Groups List */}
            <div className="space-y-4">
              {groups_to_share.map((group, index) => (
                <Card
                  key={index}
                  className={cn(
                    'border-2 transition-all cursor-pointer',
                    getGroupRelevanceColor(index),
                    expandedGroup === index ? 'ring-2 ring-offset-2 ring-blue-500' : ''
                  )}
                  onClick={() => setExpandedGroup(expandedGroup === index ? null : index)}
                >
                  <CardContent className="p-4">
                    <div className="flex items-start justify-between">
                      <div className="flex items-start space-x-3 flex-1">
                        <div className="flex-shrink-0 mt-1">
                          {getGroupTypeIcon(group.type)}
                        </div>
                        <div className="flex-1">
                          <h4 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
                            {group.name}
                          </h4>
                          <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                            {group.why_relevant}
                          </p>
                          
                          {expandedGroup === index && (
                            <div className="mt-4 space-y-3">
                              <div className="bg-white dark:bg-gray-800 p-3 rounded-lg">
                                <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                                  Share Blurb:
                                </p>
                                <p className="text-gray-600 dark:text-gray-400 text-sm">
                                  {group.share_blurb}
                                </p>
                                <Button
                                  variant="ghost"
                                  size="sm"
                                  onClick={(e) => {
                                    e.stopPropagation();
                                    copyGroupBlurb(group.share_blurb);
                                  }}
                                  leftIcon={<DocumentDuplicateIcon className="h-3 w-3" />}
                                  className="mt-2"
                                >
                                  Copy Blurb
                                </Button>
                              </div>
                              
                              {group.rules_checklist.length > 0 && (
                                <div>
                                  <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                                    Posting Checklist:
                                  </p>
                                  <div className="space-y-1">
                                    {group.rules_checklist.map((rule, ruleIndex) => (
                                      <div key={ruleIndex} className="flex items-center text-sm">
                                        <CheckCircleIcon className="h-4 w-4 text-green-500 mr-2 flex-shrink-0" />
                                        <span className="text-gray-600 dark:text-gray-400">{rule}</span>
                                      </div>
                                    ))}
                                  </div>
                                </div>
                              )}
                            </div>
                          )}
                        </div>
                      </div>
                      <div className="ml-4">
                        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300">
                          {group.type}
                        </span>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
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
            {/* Compliance Checks */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <CheckCircleIcon className="h-5 w-5 mr-2 text-green-600 dark:text-green-400" />
                  Content Compliance
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                  <div className="bg-gray-50 dark:bg-gray-800 p-4 rounded-lg">
                    <p className="text-2xl font-bold text-gray-900 dark:text-gray-100">
                      {compliance.post_lines_count}
                    </p>
                    <p className="text-sm text-gray-600 dark:text-gray-400">Post Lines</p>
                  </div>
                  <div className="bg-gray-50 dark:bg-gray-800 p-4 rounded-lg">
                    <p className="text-2xl font-bold text-gray-900 dark:text-gray-100">
                      {compliance.long_body_word_count}
                    </p>
                    <p className="text-sm text-gray-600 dark:text-gray-400">Long Body Words</p>
                  </div>
                  <div className="bg-gray-50 dark:bg-gray-800 p-4 rounded-lg">
                    <p className="text-2xl font-bold text-gray-900 dark:text-gray-100">
                      {compliance.hashtags_count}
                    </p>
                    <p className="text-sm text-gray-600 dark:text-gray-400">Hashtags</p>
                  </div>
                  <div className="bg-gray-50 dark:bg-gray-800 p-4 rounded-lg">
                    <p className="text-2xl font-bold text-gray-900 dark:text-gray-100">
                      {compliance.groups_count}
                    </p>
                    <p className="text-sm text-gray-600 dark:text-gray-400">Groups</p>
                  </div>
                  <div className="bg-gray-50 dark:bg-gray-800 p-4 rounded-lg">
                    <p className="text-2xl font-bold text-gray-900 dark:text-gray-100">
                      {compliance.image_prompt_count}
                    </p>
                    <p className="text-sm text-gray-600 dark:text-gray-400">Images</p>
                  </div>
                  <div className="bg-gray-50 dark:bg-gray-800 p-4 rounded-lg">
                    <p className="text-2xl font-bold text-gray-900 dark:text-gray-100">
                      {compliance.has_tracked_link ? '✓' : '✗'}
                    </p>
                    <p className="text-sm text-gray-600 dark:text-gray-400">Tracked Link</p>
                  </div>
                </div>

                {/* Compliance Checks */}
                <div className="mt-6">
                  <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">
                    Compliance Checks:
                  </p>
                  <div className="space-y-2">
                    {compliance.checks.map((check, index) => (
                      <div key={index} className="flex items-start">
                        <CheckCircleIcon className="h-5 w-5 text-green-500 mr-2 flex-shrink-0 mt-0.5" />
                        <span className="text-sm text-gray-600 dark:text-gray-400">{check}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Content Metrics */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <ChartBarIcon className="h-5 w-5 mr-2 text-blue-600 dark:text-blue-400" />
                  Content Metrics
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div>
                    <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                      Post Length Distribution
                    </p>
                    <div className="space-y-2">
                      {allVersions.map((version, index) => (
                        <div key={index} className="flex items-center">
                          <span className="text-xs text-gray-500 dark:text-gray-400 w-16">
                            {index === 0 ? 'Main' : `Alt ${index}`}
                          </span>
                          <div className="flex-1 mx-2">
                            <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                              <div
                                className="h-full bg-blue-600 dark:bg-blue-500"
                                style={{ width: `${Math.min((version.length / 280) * 100, 100)}%` }}
                              />
                            </div>
                          </div>
                          <span className="text-xs text-gray-500 dark:text-gray-400 w-12 text-right">
                            {version.length}
                          </span>
                        </div>
                      ))}
                    </div>
                  </div>

                  <div>
                    <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                      Hashtag Distribution
                    </p>
                    <div className="flex flex-wrap gap-2">
                      {hashtags.map((tag, index) => (
                        <span
                          key={index}
                          className="inline-flex items-center px-3 py-1 rounded-full text-xs bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300"
                        >
                          #{tag.replace('#', '')}
                        </span>
                      ))}
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
              <UserGroupIcon className="h-4 w-4 mr-1" />
              {groups_to_share.length} groups
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
