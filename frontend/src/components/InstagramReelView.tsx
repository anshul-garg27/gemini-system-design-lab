import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/Card';
import { Button } from './ui/Button';
import { 
  FilmIcon, 
  ClockIcon, 
  HashtagIcon, 
  PhotoIcon,
  MusicalNoteIcon,
  PlayIcon,
  ChatBubbleLeftIcon,
  ChartBarIcon,
  SparklesIcon,
  CheckCircleIcon,
  DocumentDuplicateIcon,
} from '@heroicons/react/24/outline';

interface InstagramReelViewProps {
  content: any;
}

const InstagramReelView: React.FC<InstagramReelViewProps> = ({ content }) => {
  const [activeTab, setActiveTab] = useState<'timeline' | 'caption' | 'visuals' | 'overview'>('timeline');
  const [selectedSegment, setSelectedSegment] = useState(0);

  // Extract data with fallbacks
  const reelData = content?.envelope?.content || content?.content || {};
  const meta = content?.envelope?.meta || content?.meta || {};
  
  const title = reelData.title || 'Instagram Reel';
  const hook = reelData.hook || '';
  const segments = reelData.content_segments || [];
  const caption = reelData.caption || '';
  const hashtags = reelData.hashtags || [];
  const imagePrompts = reelData.image_prompts || [];
  const cta = reelData.call_to_action || '';
  const musicSuggestion = reelData.music_suggestion || '';
  const topicTitle = meta.topic_title || '';

  // Calculate total duration
  const calculateTotalDuration = () => {
    if (!segments.length) return 0;
    const lastSegment = segments[segments.length - 1];
    const timeRange = lastSegment.time_range || '0-0s';
    const endTime = timeRange.split('-')[1];
    return parseInt(endTime.replace('s', '')) || 0;
  };

  const totalDuration = calculateTotalDuration();

  // Get segment color based on label
  const getSegmentColor = (label: string) => {
    const colors: { [key: string]: string } = {
      'hook': 'from-purple-500 to-pink-500',
      'problem': 'from-red-500 to-orange-500',
      'solution': 'from-green-500 to-teal-500',
      'cta': 'from-blue-500 to-purple-500',
    };
    return colors[label.toLowerCase()] || 'from-gray-500 to-gray-600';
  };

  // Copy to clipboard function
  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
  };

  const tabs = [
    { id: 'timeline', label: 'Timeline', icon: FilmIcon },
    { id: 'caption', label: 'Caption & Tags', icon: ChatBubbleLeftIcon },
    { id: 'visuals', label: 'Visuals', icon: PhotoIcon },
    { id: 'overview', label: 'Overview', icon: ChartBarIcon },
  ];

  return (
    <div className="h-screen bg-gray-50 dark:bg-gray-900 overflow-hidden">
      <div className="h-full max-w-7xl mx-auto p-6 space-y-6 overflow-y-auto">
        {/* Header */}
        <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6">
          <div className="flex items-center space-x-4">
            <div className="w-12 h-12 bg-gradient-to-r from-purple-500 to-pink-500 rounded-xl flex items-center justify-center shadow-lg">
              <FilmIcon className="h-6 w-6 text-white" />
            </div>
            <div className="flex-1">
              <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100">
                {title}
              </h1>
              {topicTitle && (
                <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                  Topic: {topicTitle}
                </p>
              )}
            </div>
            <div className="flex items-center space-x-2">
              <span className="px-3 py-1 bg-purple-100 dark:bg-purple-900/20 text-purple-700 dark:text-purple-300 rounded-full text-sm font-medium">
                Instagram Reel
              </span>
            </div>
          </div>
          
          {/* Hook Display */}
          {hook && (
            <div className="mt-6 p-4 bg-gradient-to-r from-purple-50 to-pink-50 dark:from-purple-900/10 dark:to-pink-900/10 rounded-lg border border-purple-200 dark:border-purple-700/30">
              <div className="flex items-start space-x-3">
                <SparklesIcon className="h-5 w-5 text-purple-600 dark:text-purple-400 flex-shrink-0 mt-1" />
                <p className="text-gray-800 dark:text-gray-200 font-medium">
                  {hook}
                </p>
              </div>
            </div>
          )}
        </div>

        {/* Tab Navigation */}
        <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-1">
          <div className="flex space-x-1">
            {tabs.map((tab) => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id as any)}
                  className={`flex-1 flex items-center justify-center space-x-2 px-4 py-3 rounded-lg transition-all duration-200 ${
                    activeTab === tab.id
                      ? 'bg-purple-500 text-white shadow-sm'
                      : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200 hover:bg-gray-50 dark:hover:bg-gray-700'
                  }`}
                >
                  <Icon className="h-4 w-4" />
                  <span className="text-sm font-medium">{tab.label}</span>
                </button>
              );
            })}
          </div>
        </div>

        {/* Timeline Tab */}
        {activeTab === 'timeline' && (
          <div className="h-[calc(100vh-300px)]">
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 h-full">
              {/* Segments List */}
              <div className="lg:col-span-1">
                <Card className="h-full flex flex-col">
                  <CardHeader className="flex-shrink-0">
                    <CardTitle className="flex items-center space-x-2">
                      <FilmIcon className="h-5 w-5 text-purple-600" />
                      <span>Segments ({segments.length})</span>
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="flex-1 overflow-y-auto space-y-3">
                    {segments.map((segment: any, index: number) => (
                      <div
                        key={index}
                        className={`p-3 rounded-lg border cursor-pointer transition-all duration-200 ${
                          selectedSegment === index 
                            ? 'border-purple-500 bg-purple-50 dark:bg-purple-900/20' 
                            : 'border-gray-200 dark:border-gray-700 hover:border-purple-300 dark:hover:border-purple-600'
                        }`}
                        onClick={() => setSelectedSegment(index)}
                      >
                        <div className="flex items-center space-x-3">
                          <div className={`w-2 h-12 bg-gradient-to-b ${getSegmentColor(segment.label)} rounded-full`} />
                          <div className="flex-1">
                            <div className="flex items-center justify-between">
                              <h4 className="font-semibold text-gray-900 dark:text-gray-100 text-sm">
                                {segment.label}
                              </h4>
                              <span className="text-xs text-gray-500 dark:text-gray-400">
                                {segment.time_range}
                              </span>
                            </div>
                            <p className="text-xs text-gray-600 dark:text-gray-400 mt-1 line-clamp-2">
                              {segment.narration}
                            </p>
                          </div>
                        </div>
                      </div>
                    ))}
                  </CardContent>
                </Card>
              </div>

              {/* Selected Segment Details */}
              <div className="lg:col-span-2">
                {segments[selectedSegment] && (
                  <Card className="h-full flex flex-col">
                    <CardHeader className="flex-shrink-0">
                      <CardTitle className="flex items-center justify-between">
                        <span className="flex items-center space-x-2">
                          <div className={`w-3 h-3 bg-gradient-to-r ${getSegmentColor(segments[selectedSegment].label)} rounded-full`} />
                          <span>{segments[selectedSegment].label}</span>
                        </span>
                        <span className="text-sm font-normal text-gray-500">
                          {segments[selectedSegment].time_range}
                        </span>
                      </CardTitle>
                    </CardHeader>
                    <CardContent className="flex-1 overflow-y-auto space-y-6">
                      {/* Narration */}
                      <div>
                        <h4 className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
                          Narration
                        </h4>
                        <p className="text-gray-800 dark:text-gray-200 bg-gray-50 dark:bg-gray-800/50 p-4 rounded-lg">
                          {segments[selectedSegment].narration}
                        </p>
                      </div>

                      {/* On-screen Text */}
                      <div>
                        <h4 className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
                          On-screen Text
                        </h4>
                        <p className="text-gray-800 dark:text-gray-200 bg-purple-50 dark:bg-purple-900/20 p-4 rounded-lg font-medium">
                          {segments[selectedSegment].on_screen_text}
                        </p>
                      </div>

                      {/* Visuals */}
                      <div>
                        <h4 className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
                          Visuals
                        </h4>
                        <p className="text-gray-800 dark:text-gray-200 bg-blue-50 dark:bg-blue-900/20 p-4 rounded-lg">
                          {segments[selectedSegment].visuals}
                        </p>
                      </div>

                      {/* B-roll */}
                      {segments[selectedSegment].b_roll && segments[selectedSegment].b_roll.length > 0 && (
                        <div>
                          <h4 className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
                            B-roll Suggestions
                          </h4>
                          <div className="flex flex-wrap gap-2">
                            {segments[selectedSegment].b_roll.map((item: string, i: number) => (
                              <span
                                key={i}
                                className="px-3 py-1 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-full text-sm"
                              >
                                {item}
                              </span>
                            ))}
                          </div>
                        </div>
                      )}

                      {/* Text Motion */}
                      {segments[selectedSegment].text_motion && (
                        <div>
                          <h4 className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
                            Text Motion
                          </h4>
                          <span className="inline-flex items-center px-3 py-1 bg-pink-100 dark:bg-pink-900/20 text-pink-700 dark:text-pink-300 rounded-full text-sm">
                            <PlayIcon className="h-4 w-4 mr-1" />
                            {segments[selectedSegment].text_motion}
                          </span>
                        </div>
                      )}
                    </CardContent>
                  </Card>
                )}
              </div>
            </div>
          </div>
        )}

        {/* Caption & Tags Tab */}
        {activeTab === 'caption' && (
          <div className="h-[calc(100vh-300px)] overflow-y-auto">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Caption */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center justify-between">
                  <span>Caption</span>
                  <Button
                    size="sm"
                    variant="ghost"
                    onClick={() => copyToClipboard(caption)}
                  >
                    <DocumentDuplicateIcon className="h-4 w-4" />
                  </Button>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="bg-gray-50 dark:bg-gray-800/50 p-4 rounded-lg">
                  <p className="text-gray-800 dark:text-gray-200 whitespace-pre-wrap text-sm">
                    {caption}
                  </p>
                </div>
                <div className="mt-4 flex items-center justify-between text-sm text-gray-500 dark:text-gray-400">
                  <span>{caption.length} characters</span>
                  <span className={caption.length > 2200 ? 'text-red-500' : 'text-green-500'}>
                    {caption.length > 2200 ? 'Too long' : 'Good length'}
                  </span>
                </div>
              </CardContent>
            </Card>

            {/* Hashtags */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center justify-between">
                  <span>Hashtags ({hashtags.length})</span>
                  <Button
                    size="sm"
                    variant="ghost"
                    onClick={() => copyToClipboard(hashtags.map((tag: string) => tag.startsWith('#') ? tag : `#${tag}`).join(' '))}
                  >
                    <DocumentDuplicateIcon className="h-4 w-4" />
                  </Button>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex flex-wrap gap-2">
                  {hashtags.map((tag: string, index: number) => (
                    <span
                      key={index}
                      className="px-3 py-1 bg-purple-100 dark:bg-purple-900/20 text-purple-700 dark:text-purple-300 rounded-full text-sm font-medium hover:bg-purple-200 dark:hover:bg-purple-900/30 transition-colors cursor-pointer"
                      onClick={() => copyToClipboard(tag.startsWith('#') ? tag : `#${tag}`)}
                    >
                      {tag.startsWith('#') ? tag : `#${tag}`}
                    </span>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Call to Action */}
            <Card>
              <CardHeader>
                <CardTitle>Call to Action</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="bg-gradient-to-r from-purple-50 to-pink-50 dark:from-purple-900/20 dark:to-pink-900/20 p-4 rounded-lg border border-purple-200 dark:border-purple-700/30">
                  <p className="text-gray-800 dark:text-gray-200 font-medium">
                    {cta}
                  </p>
                </div>
              </CardContent>
            </Card>

            {/* Music Suggestion */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <MusicalNoteIcon className="h-5 w-5 text-purple-600" />
                  <span>Music</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="bg-gray-50 dark:bg-gray-800/50 p-4 rounded-lg">
                  <p className="text-gray-800 dark:text-gray-200">
                    {musicSuggestion}
                  </p>
                </div>
              </CardContent>
            </Card>
            </div>
          </div>
        )}

        {/* Visuals Tab */}
        {activeTab === 'visuals' && (
          <div className="h-[calc(100vh-300px)] overflow-y-auto">
            <div className="space-y-6">
            {imagePrompts.map((prompt: any, index: number) => (
              <Card key={index}>
                <CardHeader>
                  <CardTitle className="flex items-center justify-between">
                    <span>{prompt.title}</span>
                    <span className="text-sm font-normal px-2 py-1 bg-purple-100 dark:bg-purple-900/20 text-purple-700 dark:text-purple-300 rounded">
                      {prompt.role}
                    </span>
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {/* Prompt */}
                    <div>
                      <h4 className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
                        Prompt
                      </h4>
                      <p className="text-sm text-gray-600 dark:text-gray-400 bg-gray-50 dark:bg-gray-800/50 p-3 rounded-lg">
                        {prompt.prompt}
                      </p>
                    </div>

                    {/* Negative Prompt */}
                    <div>
                      <h4 className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
                        Negative Prompt
                      </h4>
                      <p className="text-sm text-gray-600 dark:text-gray-400 bg-gray-50 dark:bg-gray-800/50 p-3 rounded-lg">
                        {prompt.negative_prompt}
                      </p>
                    </div>
                  </div>

                  {/* Metadata */}
                  <div className="flex flex-wrap gap-4 text-sm">
                    <div>
                      <span className="text-gray-500 dark:text-gray-400">Ratio:</span>
                      <span className="ml-1 font-medium text-gray-700 dark:text-gray-300">{prompt.ratio}</span>
                    </div>
                    <div>
                      <span className="text-gray-500 dark:text-gray-400">Size:</span>
                      <span className="ml-1 font-medium text-gray-700 dark:text-gray-300">{prompt.size_px}</span>
                    </div>
                    <div>
                      <span className="text-gray-500 dark:text-gray-400">Style:</span>
                      <span className="ml-1 font-medium text-gray-700 dark:text-gray-300">{prompt.style_notes}</span>
                    </div>
                  </div>

                  {/* Alt Text */}
                  <div>
                    <h4 className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
                      Alt Text
                    </h4>
                    <p className="text-sm text-gray-600 dark:text-gray-400 bg-blue-50 dark:bg-blue-900/20 p-3 rounded-lg">
                      {prompt.alt_text}
                    </p>
                  </div>
                </CardContent>
              </Card>
            ))}
            </div>
          </div>
        )}

        {/* Overview Tab */}
        {activeTab === 'overview' && (
          <div className="h-[calc(100vh-300px)] overflow-y-auto">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {/* Duration */}
            <Card>
              <CardContent className="p-6 text-center">
                <ClockIcon className="h-12 w-12 text-purple-600 mx-auto mb-3" />
                <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
                  Total Duration
                </h3>
                <p className="text-3xl font-bold text-purple-600 mt-2">
                  {totalDuration}s
                </p>
              </CardContent>
            </Card>

            {/* Segments */}
            <Card>
              <CardContent className="p-6 text-center">
                <FilmIcon className="h-12 w-12 text-pink-600 mx-auto mb-3" />
                <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
                  Content Segments
                </h3>
                <p className="text-3xl font-bold text-pink-600 mt-2">
                  {segments.length}
                </p>
              </CardContent>
            </Card>

            {/* Hashtags */}
            <Card>
              <CardContent className="p-6 text-center">
                <HashtagIcon className="h-12 w-12 text-blue-600 mx-auto mb-3" />
                <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
                  Hashtags
                </h3>
                <p className="text-3xl font-bold text-blue-600 mt-2">
                  {hashtags.length}
                </p>
              </CardContent>
            </Card>

            {/* Image Prompts */}
            <Card>
              <CardContent className="p-6 text-center">
                <PhotoIcon className="h-12 w-12 text-green-600 mx-auto mb-3" />
                <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
                  Visual Assets
                </h3>
                <p className="text-3xl font-bold text-green-600 mt-2">
                  {imagePrompts.length}
                </p>
              </CardContent>
            </Card>

            {/* Caption Length */}
            <Card>
              <CardContent className="p-6 text-center">
                <ChatBubbleLeftIcon className="h-12 w-12 text-orange-600 mx-auto mb-3" />
                <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
                  Caption Length
                </h3>
                <p className="text-3xl font-bold text-orange-600 mt-2">
                  {caption.length}
                </p>
                <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
                  characters
                </p>
              </CardContent>
            </Card>

            {/* Compliance */}
            <Card>
              <CardContent className="p-6 text-center">
                <CheckCircleIcon className="h-12 w-12 text-teal-600 mx-auto mb-3" />
                <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
                  Ready to Post
                </h3>
                <div className="mt-2">
                  <CheckCircleIcon className="h-8 w-8 text-green-500 mx-auto" />
                </div>
              </CardContent>
            </Card>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default InstagramReelView;