import React, { useState, useEffect } from 'react';
import { toast } from 'react-hot-toast';
import { 
  EyeIcon, 
  PlayIcon,
  DocumentTextIcon,
  ClockIcon,
  CheckCircleIcon,
  ExclamationTriangleIcon,
  SparklesIcon
} from '@heroicons/react/24/outline';
import type { Topic } from '../services/api';
import { apiService } from '../services/api';
import InstagramStoryView from './InstagramStoryView';
import InstagramPostView from './InstagramPostView';
import InstagramCarouselView from './InstagramCarouselView';
import InstagramReelView from './InstagramReelView';
import YouTubeShortView from './YouTubeShortView';
import YouTubeLongFormView from './YouTubeLongFormView';
import XTwitterThreadView from './XTwitterThreadView';
import MediumArticleView from './MediumArticleView';
import { FacebookPostView } from './FacebookPostView';
import { ThreadsPostView } from './ThreadsPostView';
import { LinkedInCarouselView } from './LinkedInCarouselView';
import { LinkedInPostView } from './LinkedInPostView';
import { GhostPostView } from './GhostPostView';
import { TelegramPostView } from './TelegramPostView';
import { SubstackNewsletterView } from './SubstackNewsletterView';
import { RedditPostView } from './RedditPostView';
import DevtoArticleView from './DevtoArticleView';
import ErrorBoundary from './ErrorBoundary';
import { Card, CardContent, CardHeader, CardTitle } from './ui/Card';
import { Button } from './ui/Button';
import { LoadingSpinner, ProgressBar } from './ui/LoadingStates';

// Define interfaces for content generation

interface JobStatus {
  job_id: string;
  status: 'running' | 'done' | 'error';
  created_at: string;
  errors?: string[];
}

interface JobResult {
  job_id: string;
  platform: string;
  format: string;
  topic_id?: number;
  envelope: {
    content: any;
  };
}


interface JobStatusResponse {
  job_id: string;
  status: string;
  created_at: string;
  progress?: {
    done: number;
    total: number;
  };
}

const ContentGenerator: React.FC = () => {
  const [selectedTopics, setSelectedTopics] = useState<Topic[]>([]);
  const [availableTopics, setAvailableTopics] = useState<Topic[]>([]);
  const [selectedPlatforms, setSelectedPlatforms] = useState<string[]>([]);
  const [isGenerating, setIsGenerating] = useState(false);
  const [activeJobs, setActiveJobs] = useState<JobStatus[]>([]);
  const [previousResults, setPreviousResults] = useState<JobResult[]>([]);
  const [showResults, setShowResults] = useState<{jobId: string, platform: string, format: string} | null>(null);
  const [selectedContentType, setSelectedContentType] = useState<string>('all');

  // Available platforms
  const platforms = [
    { value: 'instagram:reel', label: 'Instagram Reel' },
    { value: 'instagram:carousel', label: 'Instagram Carousel' },
    { value: 'instagram:story', label: 'Instagram Story' },
    { value: 'instagram:post', label: 'Instagram Post' },
    { value: 'linkedin:post', label: 'LinkedIn Post' },
    { value: 'linkedin:carousel', label: 'LinkedIn Carousel' },
    { value: 'x_twitter:thread', label: 'X/Twitter Thread' },
    { value: 'youtube:short', label: 'YouTube Short' },
    { value: 'youtube:long_form', label: 'YouTube Long Form' },
    { value: 'threads:post', label: 'Threads Post' },
    { value: 'facebook:post', label: 'Facebook Post' },
    { value: 'medium:article', label: 'Medium Article' },
    { value: 'substack:newsletter', label: 'Substack Newsletter' },
    { value: 'reddit:post', label: 'Reddit Post' },
    { value: 'hacker_news:item', label: 'Hacker News Item' },
    { value: 'devto:article', label: 'Dev.to Article' },
    { value: 'hashnode:article', label: 'Hashnode Article' },
    { value: 'github_pages:content', label: 'GitHub Pages' },
    { value: 'notion:page', label: 'Notion Page' },
    { value: 'personal_blog:post', label: 'Personal Blog' },
    { value: 'ghost:post', label: 'Ghost Post' },
    { value: 'telegram:post', label: 'Telegram Post' }
  ];

  // Load available topics and handle URL parameters
  useEffect(() => {
    // Check for URL parameters to pre-select a topic by ID
    const urlParams = new URLSearchParams(window.location.search);
    const topicId = urlParams.get('topicId');
    
    if (topicId) {
      // If coming from URL with topicId, only load that specific topic
      loadTopicById(parseInt(topicId));
    } else {
      // Only load all topics if no specific topic is requested
      loadAvailableTopics();
    }
  }, []);

  // Load previous results when component mounts
  useEffect(() => {
    loadPreviousResults();
  }, []);

  const loadAvailableTopics = async () => {
    try {
      const response = await apiService.getTopics();
      setAvailableTopics(response.topics || response);
    } catch (error) {
      console.error('Error loading topics:', error);
      toast.error('Failed to load topics');
    }
  };

  const loadTopicById = async (topicId: number) => {
    try {
      const topic = await apiService.getTopic(topicId);
      if (topic) {
        setSelectedTopics([topic]);
        // When loading a specific topic, don't show other available topics
        setAvailableTopics([topic]);
        
        // Load previous content for this topic
        await loadPreviousResults(topicId);
        
        toast.success(`Loaded topic: ${topic.title}`);
      } else {
        toast.error('Topic not found');
      }
    } catch (error) {
      console.error('Error loading topic:', error);
      toast.error('Failed to load topic');
    }
  };

  const loadPreviousResults = async (topicId?: number) => {
    try {
      if (topicId) {
        // Load real previous results for specific topic
        const response = await apiService.getResultsByTopic(topicId.toString());
        setPreviousResults(response.results);
      } else {
        // If no topic ID, don't load any results
        setPreviousResults([]);
      }
    } catch (error) {
      console.error('Error loading previous results:', error);
      // Fallback to empty results on error
      setPreviousResults([]);
    }
  };

  // Helper function to format platform:format combinations
  const formatPlatformType = (platform: string, format: string) => {
    const platformMap: { [key: string]: string } = {
      'instagram:carousel': 'Instagram Carousel',
      'instagram:reel': 'Instagram Reel', 
      'instagram:post': 'Instagram Post',
      'instagram:story': 'Instagram Story',
      'linkedin:post': 'LinkedIn Post',
      'linkedin:carousel': 'LinkedIn Carousel',
      'x_twitter:thread': 'Twitter Thread',
      'youtube:short': 'YouTube Short',
      'youtube:long_form': 'YouTube Video',
      'threads:post': 'Threads Post',
      'facebook:post': 'Facebook Post',
      'medium:article': 'Medium Article',
      'substack:newsletter': 'Substack Newsletter',
      'reddit:post': 'Reddit Post',
      'hacker_news:item': 'Hacker News Post',
      'devto:article': 'Dev.to Article',
      'hashnode:article': 'Hashnode Article',
      'github_pages:content': 'GitHub Pages',
      'notion:page': 'Notion Page',
      'personal_blog:post': 'Blog Post',
      'ghost:post': 'Ghost Post',
      'telegram:post': 'Telegram Post'
    };
    
    const key = `${platform}:${format}`;
    return platformMap[key] || `${platform.charAt(0).toUpperCase() + platform.slice(1)} ${format.charAt(0).toUpperCase() + format.slice(1)}`;
  };

  // Get unique content types for filtering
  const getContentTypes = () => {
    const types = new Set<string>();
    previousResults.forEach(result => {
      types.add(`${result.platform}:${result.format}`);
    });
    return Array.from(types).sort();
  };

  // Helper function to normalize content structure
  const normalizeContent = (result: JobResult) => {
    let content = result.envelope.content;
    // Unwrap nested { meta, content } shape if present
    if (content && typeof content === 'object' && 'content' in content && 'meta' in content) {
      // @ts-ignore - dynamic shape from API
      content = (content as any).content;
    }
    // If content is an array, take the first element
    if (Array.isArray(content)) {
      content = content[0] || {};
    }
    return { ...result, envelope: { ...result.envelope, content } };
  };

  // Helper function to safely render content that might be an object or string
  const safeRenderContent = (content: any): string => {
    if (typeof content === 'string') {
      return content;
    }
    if (Array.isArray(content)) {
      return content.map((c) => safeRenderContent(c)).join(' ');
    }
    if (typeof content === 'object' && content !== null) {
      // If it's an object, try to extract meaningful text
      if (content.content) return safeRenderContent(content.content);
      if (content.text) return safeRenderContent(content.text);
      if (content.caption) return safeRenderContent(content.caption);
      // If no meaningful text found, return empty string
      return '';
    }
    return String(content || '');
  };

  // Copy content to clipboard
  const copyToClipboard = async (result: JobResult) => {
    const content = result.envelope.content;
    let textToCopy = '';
    
    // Handle Instagram Story content
    if (result.platform === 'instagram' && result.format === 'story') {
      // Support both direct and nested shapes
      const story = (content && content.frames) ? content : (content && (content as any).content ? (content as any).content : null);
      if (story && story.frames) {
        textToCopy += `Instagram Story - ${story.frames.length} Frames\n`;
        textToCopy += `Total Duration: ${story.frames.reduce((acc: number, frame: any) => acc + (frame.duration_seconds || 0), 0)}s\n\n`;
        
        story.frames.forEach((frame: any) => {
          textToCopy += `Frame ${frame.index} (${frame.role}):\n`;
          textToCopy += `Copy: ${frame.copy}\n`;
          textToCopy += `Duration: ${frame.duration_seconds}s\n`;
          textToCopy += `Layout: ${frame.layout}\n`;
          textToCopy += `Overlay: ${frame.overlay_notes}\n`;
          if (frame.sticker_ideas && frame.sticker_ideas.length > 0) {
            textToCopy += `Stickers: ${frame.sticker_ideas.join(', ')}\n`;
          }
          textToCopy += `Alt Text: ${frame.alt_text}\n\n`;
        });
        
        if (story.stickers?.link_strategy?.enabled) {
          textToCopy += `Link: ${story.stickers.link_strategy.link_url}\n`;
          textToCopy += `Link Text: ${story.stickers.link_strategy.link_text}\n\n`;
        }
        
        if (story.overlay_hashtags) {
          textToCopy += `Hashtags: ${story.overlay_hashtags.join(' ')}\n\n`;
        }
      } else {
        textToCopy += 'Story content is missing.';
      }
    } else {
      // Handle other content types
      if (content.title) textToCopy += `Title: ${safeRenderContent(content.title)}\n\n`;
      if (content.caption) textToCopy += `Caption: ${safeRenderContent(content.caption)}\n\n`;
      if (content.content) textToCopy += `Content: ${safeRenderContent(content.content)}\n\n`;
      if (Array.isArray(content.hashtags)) textToCopy += `Hashtags: ${content.hashtags.join(' ')}\n\n`;
      if (content.visual_description) textToCopy += `Visual: ${safeRenderContent(content.visual_description)}\n\n`;
      if (content.call_to_action) textToCopy += `CTA: ${safeRenderContent(content.call_to_action)}`;
    }
    
    // Handle dev.to article content copy
    if (result.platform === 'devto' && result.format === 'article') {
      const article = content as any;
      const frontMatter = article.front_matter || {};
      const sections = [
        `Title: ${frontMatter.title || article.title || 'Untitled'}`,
        frontMatter.published === false ? 'Status: Draft' : 'Status: Published',
        `Tags: ${(frontMatter.tags || []).join(', ')}`,
        frontMatter.canonical_url ? `Canonical: ${frontMatter.canonical_url}` : '',
        frontMatter.cover_image ? `Cover Image: ${frontMatter.cover_image}` : '',
        '',
        '--- Markdown ---',
        article.markdown || ''
      ];
      textToCopy = sections.filter(Boolean).join('\n');
    }

    try {
      await navigator.clipboard.writeText(textToCopy);
      toast.success('Content copied to clipboard!');
    } catch (err) {
      toast.error('Failed to copy content');
    }
  };

  // Filter results by content type and normalize content structure
  const filteredResults = (selectedContentType === 'all' 
    ? previousResults 
    : previousResults.filter(result => `${result.platform}:${result.format}` === selectedContentType)
  ).map(normalizeContent);

  const handleTopicSelect = (topic: Topic) => {
    setSelectedTopics(prev => {
      if (prev.find(t => t.id === topic.id)) {
        return prev.filter(t => t.id !== topic.id);
      }
      return [...prev, topic];
    });
  };

  const handlePlatformToggle = (platform: string) => {
    setSelectedPlatforms(prev => {
      if (prev.includes(platform)) {
        return prev.filter(p => p !== platform);
      }
      return [...prev, platform];
    });
  };

  const generateContent = async () => {
    if (selectedTopics.length === 0) {
      toast.error('Please select at least one topic');
      return;
    }

    if (selectedPlatforms.length === 0) {
      toast.error('Please select at least one platform');
      return;
    }

    setIsGenerating(true);

    try {
      // Generate content for each selected topic
      for (const topic of selectedTopics) {
        const request = {
          topicId: topic.id.toString(),
          topicName: topic.title,
          topicDescription: topic.description,
          audience: 'intermediate',
          tone: 'clear, confident, non-cringe',
          locale: 'en',
          primaryUrl: `https://example.com/topic/${topic.id}`,
          brand: {
            siteUrl: 'https://example.com',
            handles: {
              instagram: '@yourhandle',
              x: '@yourhandle',
              linkedin: 'yourhandle',
              youtube: 'yourhandle',
              github: 'yourhandle'
            },
            utmBase: `utm_source={platform}&utm_medium=social&utm_campaign=${topic.id}`
          },
          targetPlatforms: selectedPlatforms,
          options: {
            include_images: true,
            max_length_levels: 'standard',
            force: false,
            length_hint: 0
          }
        };

        // Call real API for content generation
        const response = await apiService.generateContent(request);
        
        setActiveJobs(prev => [...prev, {
          job_id: response.jobId,
          status: response.status as 'running' | 'done' | 'error',
          created_at: new Date().toISOString()
        }]);

        // Start polling for job status
        pollJobStatus(response.jobId);

        toast.success(`Started content generation for "${topic.title}"`);
      }
    } catch (error) {
      console.error('Content generation error:', error);
      toast.error(`Failed to start content generation: ${error}`);
    } finally {
      setIsGenerating(false);
    }
  };

  const pollJobStatus = async (jobId: string) => {
    const pollInterval = setInterval(async () => {
      try {
        const status = await apiService.getJobStatus(jobId);
        
        // Update job status in activeJobs
        setActiveJobs(prev => prev.map(job => 
          job.job_id === jobId 
            ? { ...job, status: status.status as 'running' | 'done' | 'error' }
            : job
        ));

        // If job is done, stop polling and load results
        if (status.status === 'done') {
          clearInterval(pollInterval);
          await loadJobResults(jobId);
        } else if (status.status === 'error') {
          clearInterval(pollInterval);
          toast.error(`Content generation failed for job ${jobId.slice(0, 8)}`);
        }
      } catch (error) {
        console.error('Error polling job status:', error);
        clearInterval(pollInterval);
      }
    }, 2000); // Poll every 2 seconds
  };

  const loadJobResults = async (jobId: string) => {
    try {
      const results = await apiService.getJobResults(jobId);
      
      // Add results to previousResults
      const newResults = results.results.map(result => ({
        job_id: jobId,
        platform: result.platform,
        format: result.format,
        topic_id: selectedTopics[0]?.id, // Associate with current topic
        envelope: result.envelope
      }));

      setPreviousResults(prev => [...prev, ...newResults]);
      toast.success(`Content generation completed for job ${jobId.slice(0, 8)}`);
    } catch (error) {
      console.error('Error loading job results:', error);
      toast.error(`Failed to load results for job ${jobId.slice(0, 8)}`);
    }
  };


  const getJobProgress = (jobStatus: JobStatusResponse) => {
    if (!jobStatus.progress) return 0;
    return Math.round((jobStatus.progress.done / Math.max(jobStatus.progress.total, 1)) * 100);
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'running': return <ClockIcon className="h-5 w-5 text-primary-500 dark:text-primary-400 animate-spin" />;
      case 'done': return <CheckCircleIcon className="h-5 w-5 text-success-500 dark:text-success-400" />;
      case 'error': return <ExclamationTriangleIcon className="h-5 w-5 text-error-500 dark:text-error-400" />;
      default: return <ClockIcon className="h-5 w-5 text-gray-500 dark:text-gray-400" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'running': return 'bg-primary-100 dark:bg-primary-900/20 text-primary-800 dark:text-primary-400';
      case 'done': return 'bg-success-100 dark:bg-success-900/20 text-success-800 dark:text-success-400';
      case 'error': return 'bg-error-100 dark:bg-error-900/20 text-error-800 dark:text-error-400';
      default: return 'bg-gray-100 dark:bg-gray-800 text-gray-800 dark:text-gray-300';
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 via-white to-secondary-50 dark:from-gray-950 dark:via-gray-900 dark:to-black">
      {/* Animated Background */}
      <div className="fixed inset-0 -z-10">
        <div className="absolute top-0 right-0 w-[700px] h-[700px] bg-secondary-400/20 dark:bg-secondary-500/10 rounded-full blur-3xl animate-pulse" />
        <div className="absolute bottom-0 left-0 w-[700px] h-[700px] bg-primary-400/20 dark:bg-primary-500/10 rounded-full blur-3xl animate-pulse animation-delay-2000" />
      </div>

      <div className="px-6 py-8">
        {/* Header */}
        <div className="text-center mb-8 animate-fade-in-down">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-r from-primary-500 to-secondary-500 rounded-full mb-4 shadow-lg animate-float">
            <SparklesIcon className="h-8 w-8 text-white" />
          </div>
          <h1 className="text-4xl font-bold gradient-text-primary mb-2">
            Multi-Platform Content Generator
          </h1>
          <p className="text-lg text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
            Generate content for multiple platforms from your system design topics
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Topic Selection */}
          <Card className="relative overflow-hidden animate-fade-in-up">
            <div className="absolute top-0 left-0 w-48 h-48 bg-gradient-to-br from-primary-400/20 to-secondary-400/20 dark:from-primary-500/10 dark:to-secondary-500/10 rounded-full blur-3xl" />
            <CardHeader>
              <CardTitle className="flex items-center">
                <div className="p-2 bg-gradient-to-r from-primary-500 to-secondary-500 rounded-lg mr-3">
                  <DocumentTextIcon className="h-6 w-6 text-white" />
                </div>
                <span>Select Topics</span>
              </CardTitle>
            </CardHeader>
            <CardContent>

              <div className="space-y-4 max-h-96 overflow-y-auto">
                {/* Show selected topics first if coming from URL */}
                {selectedTopics.length > 0 && selectedTopics.some(t => t.company === 'Selected Topic') ? (
                  selectedTopics.map((topic) => (
                    <div
                      key={topic.id}
                      className="p-4 rounded-xl border-2 border-primary-500 bg-primary-50 dark:bg-primary-900/20"
                    >
                      <div className="flex items-center justify-between mb-2">
                        <h3 className="font-semibold text-gray-900 dark:text-gray-100">{topic.title}</h3>
                        <span className="px-2 py-1 bg-primary-100 dark:bg-primary-900/20 text-primary-800 dark:text-primary-400 rounded-full text-xs font-medium">
                          Pre-selected
                        </span>
                      </div>
                      <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">{topic.description}</p>
                      <div className="flex items-center justify-between text-sm text-gray-600 dark:text-gray-400">
                        <span className="capitalize">{topic.company}</span>
                        <span className="px-2 py-1 bg-primary-100 dark:bg-primary-900/20 text-primary-800 dark:text-primary-400 rounded-full text-xs">
                          {topic.complexity_level}
                        </span>
                      </div>
                    </div>
                  ))
                ) : (
                  /* Show available topics for selection */
                  availableTopics.map((topic) => (
                    <div
                      key={topic.id}
                      onClick={() => handleTopicSelect(topic)}
                      className={`p-4 rounded-xl border-2 cursor-pointer transition-all duration-200 ${
                        selectedTopics.find(t => t.id === topic.id)
                          ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/20'
                          : 'border-gray-200 dark:border-gray-700 hover:border-primary-300 dark:hover:border-primary-600 hover:bg-primary-50/50 dark:hover:bg-primary-900/10'
                      }`}
                    >
                      <h3 className="font-semibold text-gray-900 dark:text-gray-100 mb-2">{topic.title}</h3>
                      <div className="flex items-center justify-between text-sm text-gray-600 dark:text-gray-400">
                        <span className="capitalize">{topic.company}</span>
                        <span className="px-2 py-1 bg-primary-100 dark:bg-primary-900/20 text-primary-800 dark:text-primary-400 rounded-full text-xs">
                          {topic.complexity_level}
                        </span>
                      </div>
                    </div>
                  ))
                )}
              </div>

              {selectedTopics.length > 0 && (
                <div className="mt-4 p-3 bg-primary-50 dark:bg-primary-900/20 rounded-xl">
                  <p className="text-sm font-medium text-primary-700 dark:text-primary-400">
                    {selectedTopics.length} topic{selectedTopics.length !== 1 ? 's' : ''} selected
                  </p>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Platform Selection */}
          <Card className="relative overflow-hidden animate-fade-in-up animation-delay-100">
            <div className="absolute top-0 right-0 w-48 h-48 bg-gradient-to-br from-secondary-400/20 to-primary-400/20 dark:from-secondary-500/10 dark:to-primary-500/10 rounded-full blur-3xl" />
            <CardHeader>
              <CardTitle className="flex items-center">
                <div className="p-2 bg-gradient-to-r from-secondary-500 to-primary-500 rounded-lg mr-3">
                  <SparklesIcon className="h-6 w-6 text-white" />
                </div>
                <span>Select Platforms</span>
              </CardTitle>
            </CardHeader>
            <CardContent>

              <div className="grid grid-cols-2 gap-3 max-h-96 overflow-y-auto">
                {platforms.map((platform) => (
                  <label
                    key={platform.value}
                    className={`flex items-center p-3 rounded-xl border-2 cursor-pointer transition-all duration-200 ${
                      selectedPlatforms.includes(platform.value)
                        ? 'border-secondary-500 bg-secondary-50 dark:bg-secondary-900/20'
                        : 'border-gray-200 dark:border-gray-700 hover:border-secondary-300 dark:hover:border-secondary-600 hover:bg-secondary-50/50 dark:hover:bg-secondary-900/10'
                    }`}
                  >
                    <input
                      type="checkbox"
                      checked={selectedPlatforms.includes(platform.value)}
                      onChange={() => handlePlatformToggle(platform.value)}
                      className="sr-only"
                    />
                    <span className="text-sm font-medium text-gray-900 dark:text-gray-100">{platform.label}</span>
                  </label>
                ))}
              </div>

              {selectedPlatforms.length > 0 && (
                <div className="mt-4 p-3 bg-secondary-50 dark:bg-secondary-900/20 rounded-xl">
                  <p className="text-sm font-medium text-secondary-700 dark:text-secondary-400">
                    {selectedPlatforms.length} platform{selectedPlatforms.length !== 1 ? 's' : ''} selected
                  </p>
                </div>
              )}
            </CardContent>
          </Card>
        </div>

        {/* Generate Button */}
        <div className="text-center mt-8 animate-fade-in-up animation-delay-200">
          <Button
            onClick={generateContent}
            disabled={isGenerating || selectedTopics.length === 0 || selectedPlatforms.length === 0}
            variant="primary"
            size="lg"
            leftIcon={isGenerating ? <LoadingSpinner className="h-5 w-5" /> : <PlayIcon className="h-5 w-5" />}
            className="mx-auto"
          >
            {isGenerating ? 'Generating Content...' : 'Generate Content'}
          </Button>
        </div>

        {/* Active Jobs */}
        {activeJobs.length > 0 && (
          <div className="mt-12 animate-fade-in-up">
            <Card className="relative overflow-hidden">
              <div className="absolute bottom-0 right-0 w-64 h-64 bg-gradient-to-br from-success-400/20 to-primary-400/20 dark:from-success-500/10 dark:to-primary-500/10 rounded-full blur-3xl" />
              <CardHeader>
                <CardTitle className="flex items-center">
                  <div className="p-2 bg-gradient-to-r from-success-500 to-primary-500 rounded-lg mr-3">
                    <ClockIcon className="h-6 w-6 text-white" />
                  </div>
                  <span>Active Jobs</span>
                </CardTitle>
              </CardHeader>
              <CardContent>

                <div className="space-y-4">
                  {activeJobs.map((jobStatus) => (
                    <div key={jobStatus.job_id} className="bg-white dark:bg-gray-800/50 rounded-xl p-4 border border-gray-200 dark:border-gray-700">
                      <div className="flex items-center justify-between mb-3">
                        <div className="flex items-center space-x-3">
                          {getStatusIcon(jobStatus.status)}
                          <span className="font-medium text-gray-900 dark:text-gray-100">Job {jobStatus.job_id.slice(0, 8)}</span>
                          <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(jobStatus.status)}`}>
                            {jobStatus.status}
                          </span>
                        </div>
                        {jobStatus.status === 'done' && (
                          <Button
                            onClick={async () => {
                              try {
                                const response = await apiService.getJobResults(jobStatus.job_id);
                                if (response.results && response.results.length > 0) {
                                  const firstResult = response.results[0];
                                  setShowResults({
                                    jobId: jobStatus.job_id,
                                    platform: firstResult.platform,
                                    format: firstResult.format
                                  });
                                }
                              } catch (error) {
                                console.error('Error fetching job results:', error);
                              }
                            }}
                            variant="primary"
                            size="sm"
                            leftIcon={<EyeIcon className="h-4 w-4" />}
                          >
                            View Results
                          </Button>
                        )}
                      </div>

                      {jobStatus.status === 'running' && (
                        <div className="space-y-2">
                          <div className="flex justify-between text-sm text-gray-600 dark:text-gray-400">
                            <span>Progress</span>
                            <span>{getJobProgress(jobStatus)}%</span>
                          </div>
                          <ProgressBar progress={getJobProgress(jobStatus)} className="w-full" />
                        </div>
                      )}

                      {jobStatus.errors && jobStatus.errors.length > 0 && (
                        <div className="mt-3 p-3 bg-red-50 rounded-lg">
                          <h4 className="text-sm font-medium text-red-700 mb-2">Errors:</h4>
                          {jobStatus.errors.map((error: string, index: number) => (
                            <p key={index} className="text-sm text-red-600">
                              {error}
                            </p>
                          ))}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>
        )}

        {/* Results Modal */}
        {showResults && (() => {
          const specificResult = previousResults.find(r => 
            r.job_id === showResults.jobId && 
            r.platform === showResults.platform && 
            r.format === showResults.format
          );
          const normalizedResult = specificResult ? normalizeContent(specificResult) : null;
          return normalizedResult ? (
            <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
              {normalizedResult.platform === 'instagram' && normalizedResult.format === 'post' ? (
                <div className="relative">
                  <button
                    onClick={() => setShowResults(null)}
                    className="absolute -top-4 -right-4 z-10 bg-white rounded-full p-2 shadow-lg hover:bg-gray-100 transition-colors"
                  >
                    <svg className="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                  <ErrorBoundary>
                    <InstagramPostView content={normalizedResult} onCopy={() => copyToClipboard(normalizedResult)} />
                  </ErrorBoundary>
                </div>
              ) : normalizedResult.platform === 'instagram' && normalizedResult.format === 'story' ? (
                <div className="relative">
                  <button
                    onClick={() => setShowResults(null)}
                    className="absolute -top-4 -right-4 z-10 bg-white rounded-full p-2 shadow-lg hover:bg-gray-100 transition-colors"
                  >
                    <svg className="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                  <ErrorBoundary>
                    <InstagramStoryView content={normalizedResult} onCopy={() => copyToClipboard(normalizedResult)} />
                  </ErrorBoundary>
                </div>
              ) : normalizedResult.platform === 'instagram' && normalizedResult.format === 'post' ? (
                <div className="relative">
                  <button
                    onClick={() => setShowResults(null)}
                    className="absolute -top-4 -right-4 z-10 bg-white rounded-full p-2 shadow-lg hover:bg-gray-100 transition-colors"
                  >
                    <svg className="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                  <ErrorBoundary>
                    <InstagramPostView content={normalizedResult} onCopy={() => copyToClipboard(normalizedResult)} />
                  </ErrorBoundary>
                </div>
              ) : normalizedResult.platform === 'instagram' && normalizedResult.format === 'carousel' ? (
                <div className="relative">
                  <button
                    onClick={() => setShowResults(null)}
                    className="absolute -top-4 -right-4 z-10 bg-white rounded-full p-2 shadow-lg hover:bg-gray-100 transition-colors"
                  >
                    <svg className="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                  <ErrorBoundary>
                    <InstagramCarouselView content={normalizedResult} onCopy={() => copyToClipboard(normalizedResult)} />
                  </ErrorBoundary>
                </div>
              ) : normalizedResult.platform === 'instagram' && normalizedResult.format === 'reel' ? (
                <div className="relative">
                  <button
                    onClick={() => setShowResults(null)}
                    className="absolute -top-4 -right-4 z-10 bg-white rounded-full p-2 shadow-lg hover:bg-gray-100 transition-colors"
                  >
                    <svg className="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                  <ErrorBoundary>
                    <InstagramReelView content={normalizedResult} />
                  </ErrorBoundary>
                </div>
              ) : normalizedResult.platform === 'youtube' && normalizedResult.format === 'short' ? (
                <div className="relative">
                  <button
                    onClick={() => setShowResults(null)}
                    className="absolute -top-4 -right-4 z-10 bg-white rounded-full p-2 shadow-lg hover:bg-gray-100 transition-colors"
                  >
                    <svg className="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                  <ErrorBoundary>
                    <YouTubeShortView content={normalizedResult} onCopy={() => copyToClipboard(normalizedResult)} />
                  </ErrorBoundary>
                </div>
              ) : normalizedResult.platform === 'youtube' && normalizedResult.format === 'long_form' ? (
                <div className="relative">
                  <button
                    onClick={() => setShowResults(null)}
                    className="absolute -top-4 -right-4 z-10 bg-white rounded-full p-2 shadow-lg hover:bg-gray-100 transition-colors"
                  >
                    <svg className="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                  <ErrorBoundary>
                    <YouTubeLongFormView content={normalizedResult} onCopy={() => copyToClipboard(normalizedResult)} />
                  </ErrorBoundary>
                </div>
              ) : normalizedResult.platform === 'x_twitter' && normalizedResult.format === 'thread' ? (
                <div className="relative">
                  <button
                    onClick={() => setShowResults(null)}
                    className="absolute -top-4 -right-4 z-10 bg-white rounded-full p-2 shadow-lg hover:bg-gray-100 transition-colors"
                  >
                    <svg className="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                  <ErrorBoundary>
                    <XTwitterThreadView content={normalizedResult} onCopy={() => copyToClipboard(normalizedResult)} />
                  </ErrorBoundary>
                </div>
              ) : normalizedResult.platform === 'medium' && normalizedResult.format === 'article' ? (
                <div className="relative">
                  <button
                    onClick={() => setShowResults(null)}
                    className="absolute -top-4 -right-4 z-10 bg-white rounded-full p-2 shadow-lg hover:bg-gray-100 transition-colors"
                  >
                    <svg className="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                  <ErrorBoundary>
                    <MediumArticleView content={normalizedResult} onCopy={() => copyToClipboard(normalizedResult)} />
                  </ErrorBoundary>
                </div>
              ) : normalizedResult.platform === 'facebook' && normalizedResult.format === 'post' ? (
                <div className="relative">
                  <button
                    onClick={() => setShowResults(null)}
                    className="absolute -top-4 -right-4 z-10 bg-white rounded-full p-2 shadow-lg hover:bg-gray-100 transition-colors"
                  >
                    <svg className="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                  <ErrorBoundary>
                    <FacebookPostView content={normalizedResult} />
                  </ErrorBoundary>
                </div>
              ) : normalizedResult.platform === 'threads' && normalizedResult.format === 'post' ? (
                <div className="relative">
                  <button
                    onClick={() => setShowResults(null)}
                    className="absolute -top-4 -right-4 z-10 bg-white rounded-full p-2 shadow-lg hover:bg-gray-100 transition-colors"
                  >
                    <svg className="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                  <ErrorBoundary>
                    <ThreadsPostView content={normalizedResult} />
                  </ErrorBoundary>
                </div>
              ) : normalizedResult.platform === 'linkedin' && normalizedResult.format === 'carousel' ? (
                <div className="relative">
                  <button
                    onClick={() => setShowResults(null)}
                    className="absolute -top-4 -right-4 z-10 bg-white rounded-full p-2 shadow-lg hover:bg-gray-100 transition-colors"
                  >
                    <svg className="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                  <ErrorBoundary>
                    <LinkedInCarouselView content={normalizedResult} />
                  </ErrorBoundary>
                </div>
              ) : normalizedResult.platform === 'linkedin' && normalizedResult.format === 'post' ? (
                <div className="relative">
                  <button
                    onClick={() => setShowResults(null)}
                    className="absolute -top-4 -right-4 z-10 bg-white rounded-full p-2 shadow-lg hover:bg-gray-100 transition-colors"
                  >
                    <svg className="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                  <ErrorBoundary>
                    <LinkedInPostView content={normalizedResult} />
                  </ErrorBoundary>
                </div>
              ) : normalizedResult.platform === 'ghost' && normalizedResult.format === 'post' ? (
                <div className="relative">
                  <button
                    onClick={() => setShowResults(null)}
                    className="absolute -top-4 -right-4 z-10 bg-white rounded-full p-2 shadow-lg hover:bg-gray-100 transition-colors"
                  >
                    <svg className="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                  <ErrorBoundary>
                    <GhostPostView content={normalizedResult} />
                  </ErrorBoundary>
                </div>
              ) : normalizedResult.platform === 'telegram' && normalizedResult.format === 'post' ? (
                <div className="relative">
                  <button
                    onClick={() => setShowResults(null)}
                    className="absolute -top-4 -right-4 z-10 bg-white rounded-full p-2 shadow-lg hover:bg-gray-100 transition-colors"
                  >
                    <svg className="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                  <ErrorBoundary>
                    <TelegramPostView content={normalizedResult} />
                  </ErrorBoundary>
                </div>
              ) : normalizedResult.platform === 'substack' && normalizedResult.format === 'newsletter' ? (
                <div className="relative">
                  <button
                    onClick={() => setShowResults(null)}
                    className="absolute -top-4 -right-4 z-10 bg-white rounded-full p-2 shadow-lg hover:bg-gray-100 transition-colors"
                  >
                    <svg className="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                  <ErrorBoundary>
                    <SubstackNewsletterView content={normalizedResult} />
                  </ErrorBoundary>
                </div>
              ) : normalizedResult.platform === 'reddit' && normalizedResult.format === 'post' ? (
                <div className="relative">
                  <button
                    onClick={() => setShowResults(null)}
                    className="absolute -top-4 -right-4 z-10 bg-white rounded-full p-2 shadow-lg hover:bg-gray-100 transition-colors"
                  >
                    <svg className="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                  <ErrorBoundary>
                    <RedditPostView content={normalizedResult} />
                  </ErrorBoundary>
                </div>
              ) : normalizedResult.platform === 'devto' && normalizedResult.format === 'article' ? (
                <div className="relative">
                  <button
                    onClick={() => setShowResults(null)}
                    className="absolute -top-4 -right-4 z-10 bg-white rounded-full p-2 shadow-lg hover:bg-gray-100 transition-colors"
                  >
                    <svg className="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                  <ErrorBoundary>
                    <DevtoArticleView content={normalizedResult} onCopy={() => copyToClipboard(normalizedResult)} />
                  </ErrorBoundary>
                </div>
              ) : (
                <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-96 overflow-y-auto">
                  <ErrorBoundary>
                  <div className="p-6">
                    <div className="flex justify-between items-start mb-4">
                      <span className="inline-block px-2 py-1 bg-blue-100 text-blue-800 rounded text-xs font-medium">
                        {formatPlatformType(normalizedResult.platform, normalizedResult.format)}
                      </span>
                      <button
                        onClick={() => setShowResults(null)}
                        className="text-gray-400 hover:text-gray-600 transition-colors"
                      >
                        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                        </svg>
                      </button>
                    </div>
                    <div className="space-y-4">
                      {normalizedResult.envelope.content.title && (
                        <div>
                          <p><strong>Title:</strong></p>
                          <p className="text-sm bg-gray-100 p-2 rounded mt-1">{safeRenderContent(normalizedResult.envelope.content.title)}</p>
                        </div>
                      )}
                      {normalizedResult.envelope.content.caption && (
                        <div>
                          <p><strong>Caption:</strong></p>
                          <p className="text-xs bg-gray-100 p-2 rounded mt-1 whitespace-pre-wrap">{safeRenderContent(normalizedResult.envelope.content.caption)}</p>
                        </div>
                      )}
                      {normalizedResult.envelope.content.content && (
                        <div>
                          <p><strong>Content:</strong></p>
                          <p className="text-xs bg-gray-100 p-2 rounded mt-1 whitespace-pre-wrap">{safeRenderContent(normalizedResult.envelope.content.content)}</p>
                        </div>
                      )}
                      {Array.isArray(normalizedResult.envelope.content.slides) && (
                        <div>
                          <p><strong>Slides:</strong></p>
                          {normalizedResult.envelope.content.slides.map((slide: any, idx: number) => (
                            <div key={idx} className="text-xs bg-gray-100 p-2 rounded mt-1 mb-2">
                              <p><strong>Slide {slide.slide_number}:</strong> {safeRenderContent(slide.headline)}</p>
                              <p>{safeRenderContent(slide.content)}</p>
                              {slide.visual_description && (
                                <p className="text-gray-500 italic mt-1">Visual: {safeRenderContent(slide.visual_description)}</p>
                              )}
                            </div>
                          ))}
                        </div>
                      )}
                      {Array.isArray(normalizedResult.envelope.content.tweets) && (
                        <div>
                          <p><strong>Thread:</strong></p>
                          {normalizedResult.envelope.content.tweets.map((tweet: any, idx: number) => (
                            <div key={idx} className="text-xs bg-gray-100 p-2 rounded mt-1 mb-2">
                              <p><strong>Tweet {tweet.tweet_number}:</strong></p>
                              <p>{safeRenderContent(tweet.content)}</p>
                            </div>
                          ))}
                        </div>
                      )}
                      {Array.isArray(normalizedResult.envelope.content.hashtags) && (
                        <div>
                          <p><strong>Hashtags:</strong></p>
                          <div className="flex flex-wrap gap-2 mt-1">
                            {normalizedResult.envelope.content.hashtags.map((tag: string, idx: number) => (
                              <span key={idx} className="px-2 py-1 bg-blue-100 text-blue-800 rounded text-xs">
                                {tag}
                              </span>
                            ))}
                          </div>
                        </div>
                      )}
                      {normalizedResult.envelope.content.visual_description && (
                        <div>
                          <p><strong>Visual Description:</strong></p>
                          <p className="text-xs bg-gray-100 p-2 rounded mt-1 whitespace-pre-wrap">{safeRenderContent(normalizedResult.envelope.content.visual_description)}</p>
                        </div>
                      )}
                      {normalizedResult.envelope.content.call_to_action && (
                        <div>
                          <p><strong>Call to Action:</strong></p>
                          <p className="text-xs bg-gray-100 p-2 rounded mt-1">{safeRenderContent(normalizedResult.envelope.content.call_to_action)}</p>
                        </div>
                      )}
                    </div>
                  </div>
                  </ErrorBoundary>
                </div>
              )}
            </div>
          ) : null;
        })()}

        {/* Previous Results Section */}
        {previousResults.length > 0 && (
          <Card className="relative overflow-hidden mt-12 animate-fade-in-up">
            <div className="absolute top-0 left-0 w-96 h-96 bg-gradient-to-br from-success-400/20 to-secondary-400/20 dark:from-success-500/10 dark:to-secondary-500/10 rounded-full blur-3xl" />
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle className="flex items-center">
                  <div className="p-2 bg-gradient-to-r from-success-500 to-secondary-500 rounded-lg mr-3">
                    <EyeIcon className="h-6 w-6 text-white" />
                  </div>
                  <span>Previous Content</span>
                </CardTitle>
                {selectedTopics.length > 0 && selectedTopics[0].company === 'Selected Topic' && (
                  <div className="text-sm text-gray-600 dark:text-gray-400">
                    Showing content for: <span className="font-semibold text-gray-900 dark:text-gray-100">{selectedTopics[0].title}</span>
                  </div>
                )}
              </div>
            </CardHeader>
            <CardContent>

              {/* Content Type Filter Tabs */}
              {getContentTypes().length > 1 && (
                <div className="mb-6">
                  <div className="flex flex-wrap gap-2">
                    <button
                      onClick={() => setSelectedContentType('all')}
                      className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                        selectedContentType === 'all'
                          ? 'bg-primary-500 text-white'
                          : 'bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-700'
                      }`}
                    >
                      All ({previousResults.length})
                    </button>
                    {getContentTypes().map(type => {
                      const [platform, format] = type.split(':');
                      const count = previousResults.filter(r => `${r.platform}:${r.format}` === type).length;
                      return (
                        <button
                          key={type}
                          onClick={() => setSelectedContentType(type)}
                          className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                            selectedContentType === type
                              ? 'bg-primary-500 text-white'
                              : 'bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-700'
                          }`}
                        >
                          {formatPlatformType(platform, format)} ({count})
                        </button>
                      );
                    })}
                  </div>
                </div>
              )}

              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {filteredResults.map((result, index) => (
                  <Card key={index} className="hover:shadow-lg transition-all duration-300">
                    <CardContent className="p-4">
                      <div className="flex items-center justify-between mb-3">
                        <span className="px-3 py-1 bg-primary-100 dark:bg-primary-900/20 text-primary-800 dark:text-primary-400 rounded-full text-sm font-medium">
                          {formatPlatformType(result.platform, result.format)}
                        </span>
                        <span className="text-xs text-gray-500 dark:text-gray-400">
                          {result.job_id.substring(0, 8)}...
                        </span>
                      </div>
                    
                    <div className="space-y-2 text-sm text-gray-600">
                      {result.envelope.content.title && (
                        <div>
                          <p className="font-semibold text-gray-900 dark:text-gray-100">{safeRenderContent(result.envelope.content.title)}</p>
                        </div>
                      )}
                      {result.envelope.content.caption && (
                        <div>
                          <p className="text-xs text-gray-700 dark:text-gray-300 line-clamp-3">{safeRenderContent(result.envelope.content.caption)}</p>
                        </div>
                      )}
                      {result.envelope.content.content && (
                        <div>
                          <p className="text-xs text-gray-700 dark:text-gray-300 line-clamp-3">{safeRenderContent(result.envelope.content.content)}</p>
                        </div>
                      )}
                      {Array.isArray(result.envelope.content.hashtags) && (
                        <div className="flex flex-wrap gap-1 mt-2">
                          {result.envelope.content.hashtags.slice(0, 3).map((tag: string, idx: number) => (
                            <span key={idx} className="px-2 py-1 bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400 rounded text-xs">
                              {tag}
                            </span>
                          ))}
                          {result.envelope.content.hashtags.length > 3 && (
                            <span className="px-2 py-1 bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400 rounded text-xs">
                              +{result.envelope.content.hashtags.length - 3} more
                            </span>
                          )}
                        </div>
                      )}
                    </div>
                    
                      <Button
                        onClick={() => setShowResults(
                          showResults?.jobId === result.job_id && 
                          showResults?.platform === result.platform && 
                          showResults?.format === result.format
                            ? null 
                            : {jobId: result.job_id, platform: result.platform, format: result.format}
                        )}
                        variant="outline"
                        size="sm"
                        className="mt-3 w-full"
                      >
                        {showResults?.jobId === result.job_id && 
                         showResults?.platform === result.platform && 
                         showResults?.format === result.format
                          ? 'Hide Details' : 'View Details'}
                      </Button>
                    
                    {showResults?.jobId === result.job_id && 
                     showResults?.platform === result.platform && 
                     showResults?.format === result.format && (
                      <div className="mt-3 p-3 bg-gray-50 rounded-lg">
                        <div className="space-y-2 text-sm text-gray-600">
                          {Array.isArray(result.envelope.content.slides) && (
                            <div>
                              <p className="font-medium text-gray-900 mb-2">Slides:</p>
                              {result.envelope.content.slides.map((slide: any, idx: number) => (
                                <div key={idx} className="text-xs bg-white p-2 rounded mb-2">
                                  <p className="font-medium">Slide {slide.slide_number}: {safeRenderContent(slide.headline)}</p>
                                  <p className="text-gray-600">{safeRenderContent(slide.content)}</p>
                                </div>
                              ))}
                            </div>
                          )}
                          {Array.isArray(result.envelope.content.tweets) && (
                            <div>
                              <p className="font-medium text-gray-900 mb-2">Thread:</p>
                              {result.envelope.content.tweets.map((tweet: any, idx: number) => (
                                <div key={idx} className="text-xs bg-white p-2 rounded mb-2">
                                  <p className="font-medium">Tweet {tweet.tweet_number}:</p>
                                  <p className="text-gray-600">{safeRenderContent(tweet.content)}</p>
                                </div>
                              ))}
                            </div>
                          )}
                          {result.envelope.content.description && (
                            <div>
                              <p className="font-medium text-gray-900">Description:</p>
                              <p className="text-xs bg-white p-2 rounded mt-1">{safeRenderContent(result.envelope.content.description)}</p>
                            </div>
                          )}
                        </div>
                      </div>
                    )}
                    </CardContent>
                  </Card>
                ))}
              </div>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
};

export default ContentGenerator;
