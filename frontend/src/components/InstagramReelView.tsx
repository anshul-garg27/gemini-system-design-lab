import React, { useState, useEffect, useRef } from 'react';
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
  DevicePhoneMobileIcon,
  ArrowDownTrayIcon,
  FireIcon,
  BoltIcon,
  EyeIcon,
  HeartIcon,
  ShareIcon,
  BeakerIcon,
} from '@heroicons/react/24/outline';

interface InstagramReelViewProps {
  content: any;
}

const InstagramReelView: React.FC<InstagramReelViewProps> = ({ content }) => {
  const [activeTab, setActiveTab] = useState<'timeline' | 'caption' | 'visuals' | 'overview' | 'preview' | 'analytics' | 'export' | 'engagement' | 'accessibility' | 'production'>('timeline');
  const [selectedSegment, setSelectedSegment] = useState(0);
  const [currentTime, setCurrentTime] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const animationRef = useRef<number | undefined>(undefined);

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

  // Timeline animation
  useEffect(() => {
    if (isPlaying) {
      const animate = () => {
        setCurrentTime((prev) => {
          if (prev >= totalDuration) {
            setIsPlaying(false);
            return 0;
          }
          return prev + 0.1;
        });
        animationRef.current = requestAnimationFrame(animate);
      };
      animationRef.current = requestAnimationFrame(animate);
    }
    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, [isPlaying, totalDuration]);

  // Auto-select segment based on current time
  useEffect(() => {
    segments.forEach((segment: any, index: number) => {
      const timeRange = segment.time_range || '0-0s';
      const [start, end] = timeRange.split('-').map((t: string) => parseInt(t.replace('s', '')));
      if (currentTime >= start && currentTime < end) {
        setSelectedSegment(index);
      }
    });
  }, [currentTime, segments]);

  // Calculate engagement score
  const calculateEngagementScore = () => {
    let score = 0;
    // Hook strength (0-20 points)
    if (hook.length > 50 && hook.length < 120) score += 20;
    else if (hook.length > 30) score += 10;
    
    // Hashtag optimization (0-20 points)
    if (hashtags.length >= 20 && hashtags.length <= 30) score += 20;
    else if (hashtags.length >= 10) score += 10;
    
    // Duration optimization (0-20 points)
    if (totalDuration >= 30 && totalDuration <= 60) score += 20;
    else if (totalDuration <= 90) score += 10;
    
    // Caption quality (0-20 points)
    if (caption.length >= 500 && caption.length <= 2200) score += 20;
    else if (caption.length >= 200) score += 10;
    
    // Visual assets (0-20 points)
    if (imagePrompts.length >= 3) score += 20;
    else if (imagePrompts.length >= 1) score += 10;
    
    return score;
  };

  const engagementScore = calculateEngagementScore();

  // SEO Score calculation
  const calculateSEOScore = () => {
    let score = 0;
    const keywordTiers = meta.keyword_tiers || {};
    
    // Primary keywords in title (0-25 points)
    const primaryKeywords = meta.primary_keywords || [];
    const titleLower = title.toLowerCase();
    const keywordsInTitle = primaryKeywords.filter((kw: string) => 
      titleLower.includes(kw.toLowerCase())
    ).length;
    score += Math.min(25, keywordsInTitle * 12);
    
    // Hashtag diversity (0-25 points)
    const hasNiche = keywordTiers.niche?.length > 0;
    const hasMicroNiche = keywordTiers.micro_niche?.length > 0;
    const hasIntent = keywordTiers.intent?.length > 0;
    if (hasNiche && hasMicroNiche && hasIntent) score += 25;
    else if (hasNiche && hasMicroNiche) score += 15;
    
    // Caption keyword density (0-25 points)
    const captionWords = caption.toLowerCase().split(/\s+/);
    const keywordMatches = captionWords.filter((word: string) => 
      primaryKeywords.some((kw: string) => word.includes(kw.toLowerCase()))
    ).length;
    const density = keywordMatches / captionWords.length;
    if (density > 0.02 && density < 0.05) score += 25;
    else if (density > 0.01) score += 15;
    
    // CTA presence (0-25 points)
    if (cta) score += 25;
    
    return Math.min(100, score);
  };

  const seoScore = calculateSEOScore();

  // Get score color
  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-500';
    if (score >= 60) return 'text-yellow-500';
    if (score >= 40) return 'text-orange-500';
    return 'text-red-500';
  };

  // Export functions
  const exportAsJSON = () => {
    const dataStr = JSON.stringify(content, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `instagram-reel-${Date.now()}.json`;
    link.click();
  };

  const exportAsScript = () => {
    let scriptText = `INSTAGRAM REEL SCRIPT\n\n`;
    scriptText += `Title: ${title}\n`;
    scriptText += `Duration: ${totalDuration}s\n`;
    scriptText += `Hook: ${hook}\n\n`;
    scriptText += `SEGMENTS:\n\n`;
    segments.forEach((seg: any) => {
      scriptText += `[${seg.time_range}] ${seg.label.toUpperCase()}\n`;
      scriptText += `Narration: ${seg.narration}\n`;
      scriptText += `On-screen: ${seg.on_screen_text}\n`;
      scriptText += `Visuals: ${seg.visuals}\n\n`;
    });
    scriptText += `\nCAPTION:\n${caption}\n\n`;
    scriptText += `HASHTAGS:\n${hashtags.join(' ')}\n\n`;
    scriptText += `CTA: ${cta}\n`;
    scriptText += `MUSIC: ${musicSuggestion}\n`;
    
    const dataBlob = new Blob([scriptText], { type: 'text/plain' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `instagram-reel-script-${Date.now()}.txt`;
    link.click();
  };

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
    { id: 'preview', label: 'Phone Preview', icon: DevicePhoneMobileIcon },
    { id: 'production', label: 'Production', icon: BoltIcon },
    { id: 'engagement', label: 'Engagement', icon: FireIcon },
    { id: 'caption', label: 'Caption & Tags', icon: ChatBubbleLeftIcon },
    { id: 'visuals', label: 'Visuals', icon: PhotoIcon },
    { id: 'accessibility', label: 'Accessibility', icon: CheckCircleIcon },
    { id: 'analytics', label: 'Analytics', icon: ChartBarIcon },
    { id: 'export', label: 'Export', icon: ArrowDownTrayIcon },
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

        {/* Production Tab */}
        {activeTab === 'production' && (
          <div className="h-[calc(100vh-300px)] overflow-y-auto">
            <div className="space-y-6">
              {/* Transitions */}
              {reelData.transitions && reelData.transitions.length > 0 && (
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center space-x-2">
                      <BoltIcon className="h-5 w-5 text-purple-600" />
                      <span>Transitions ({reelData.transitions.length})</span>
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-3">
                      {reelData.transitions.map((transition: any, index: number) => (
                        <div key={index} className="p-4 bg-gradient-to-r from-purple-50 to-pink-50 dark:from-purple-900/20 dark:to-pink-900/20 rounded-lg border border-purple-200 dark:border-purple-700/30">
                          <div className="flex items-center justify-between mb-2">
                            <div className="flex items-center space-x-2">
                              <span className="text-sm font-semibold text-gray-700 dark:text-gray-300">
                                {transition.from_segment} → {transition.to_segment}
                              </span>
                              <span className="px-2 py-1 bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-300 rounded text-xs">
                                {transition.type}
                              </span>
                            </div>
                            <span className="text-sm text-gray-500">{transition.timing}</span>
                          </div>
                          <p className="text-sm text-gray-600 dark:text-gray-400">
                            Effect: <span className="font-medium">{transition.effect}</span>
                          </p>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              )}

              {/* Text Animations */}
              {reelData.text_animations && reelData.text_animations.length > 0 && (
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center space-x-2">
                      <SparklesIcon className="h-5 w-5 text-yellow-600" />
                      <span>Text Animations ({reelData.text_animations.length})</span>
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-3">
                      {reelData.text_animations.map((anim: any, index: number) => (
                        <div key={index} className="p-4 bg-gray-50 dark:bg-gray-800/50 rounded-lg border border-gray-200 dark:border-gray-700">
                          <div className="flex items-start justify-between mb-2">
                            <div className="flex-1">
                              <p className="font-semibold text-gray-900 dark:text-gray-100 mb-1">
                                "{anim.text}"
                              </p>
                              <p className="text-xs text-gray-500">{anim.time_range}</p>
                            </div>
                            <span className="px-2 py-1 bg-blue-100 dark:bg-blue-900/20 text-blue-700 dark:text-blue-300 rounded text-xs">
                              {anim.size_px}px
                            </span>
                          </div>
                          <div className="grid grid-cols-2 md:grid-cols-4 gap-2 mt-3 text-xs">
                            <div>
                              <span className="text-gray-500">Animation In:</span>
                              <p className="font-medium text-gray-700 dark:text-gray-300">{anim.animation_in}</p>
                            </div>
                            <div>
                              <span className="text-gray-500">Animation Out:</span>
                              <p className="font-medium text-gray-700 dark:text-gray-300">{anim.animation_out}</p>
                            </div>
                            <div>
                              <span className="text-gray-500">Position:</span>
                              <p className="font-medium text-gray-700 dark:text-gray-300">{anim.position}</p>
                            </div>
                            <div>
                              <span className="text-gray-500">Appears/Disappears:</span>
                              <p className="font-medium text-gray-700 dark:text-gray-300">{anim.appears_at} / {anim.disappears_at}</p>
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              )}

              {/* Pacing & First Frame */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* Pacing */}
                {reelData.pacing && (
                  <Card>
                    <CardHeader>
                      <CardTitle className="flex items-center space-x-2">
                        <ClockIcon className="h-5 w-5 text-blue-600" />
                        <span>Pacing & Editing</span>
                      </CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="space-y-3">
                        <div className="flex justify-between items-center p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
                          <span className="text-sm text-gray-600 dark:text-gray-400">Edit Frequency</span>
                          <span className="font-bold text-blue-600">{reelData.pacing.edit_frequency_seconds}s</span>
                        </div>
                        <div className="flex justify-between items-center p-3 bg-orange-50 dark:bg-orange-900/20 rounded-lg">
                          <span className="text-sm text-gray-600 dark:text-gray-400">Pattern Interrupt</span>
                          <span className="font-bold text-orange-600">{reelData.pacing.pattern_interrupt_at}s</span>
                        </div>
                        <div className="flex justify-between items-center p-3 bg-purple-50 dark:bg-purple-900/20 rounded-lg">
                          <span className="text-sm text-gray-600 dark:text-gray-400">Total Scenes</span>
                          <span className="font-bold text-purple-600">{reelData.pacing.scene_count}</span>
                        </div>
                        <div className="flex justify-between items-center p-3 bg-green-50 dark:bg-green-900/20 rounded-lg">
                          <span className="text-sm text-gray-600 dark:text-gray-400">Total Cuts</span>
                          <span className="font-bold text-green-600">{reelData.pacing.total_cuts}</span>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                )}

                {/* First Frame */}
                {reelData.first_frame && (
                  <Card>
                    <CardHeader>
                      <CardTitle className="flex items-center space-x-2">
                        <PhotoIcon className="h-5 w-5 text-pink-600" />
                        <span>First Frame (Thumbnail)</span>
                      </CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="space-y-3">
                        <p className="text-sm text-gray-700 dark:text-gray-300">
                          {reelData.first_frame.description}
                        </p>
                        <div className="grid grid-cols-2 gap-3">
                          <div className="p-3 bg-gray-50 dark:bg-gray-800/50 rounded-lg">
                            <p className="text-xs text-gray-500 mb-1">Text Size</p>
                            <p className="font-bold text-purple-600">{reelData.first_frame.text_size_px}px</p>
                          </div>
                          <div className="p-3 bg-gray-50 dark:bg-gray-800/50 rounded-lg">
                            <p className="text-xs text-gray-500 mb-1">Thumbnail Readable</p>
                            <p className="font-bold text-green-600">
                              {reelData.first_frame.text_readable_at_thumbnail ? '✓ Yes' : '✗ No'}
                            </p>
                          </div>
                        </div>
                        <div className="p-3 bg-gradient-to-r from-purple-50 to-pink-50 dark:from-purple-900/20 dark:to-pink-900/20 rounded-lg">
                          <p className="text-xs text-gray-500 mb-1">Includes</p>
                          <p className="text-sm font-medium text-gray-700 dark:text-gray-300">
                            {reelData.first_frame.includes}
                          </p>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                )}
              </div>

              {/* Music Sync Points */}
              {reelData.trending_audio?.sync_points && (
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center space-x-2">
                      <MusicalNoteIcon className="h-5 w-5 text-green-600" />
                      <span>Music Sync Points</span>
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      <div className="grid grid-cols-1 md:grid-cols-3 gap-3 mb-4">
                        <div className="p-3 bg-green-50 dark:bg-green-900/20 rounded-lg">
                          <p className="text-xs text-gray-500">Drop Moment</p>
                          <p className="font-bold text-green-600">{reelData.trending_audio.drop_moment}</p>
                        </div>
                        <div className="p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg col-span-2">
                          <p className="text-xs text-gray-500">Energy Curve</p>
                          <p className="font-medium text-blue-600 text-sm">{reelData.trending_audio.energy_curve}</p>
                        </div>
                      </div>
                      <div className="space-y-2">
                        {reelData.trending_audio.sync_points.map((sync: any, index: number) => (
                          <div key={index} className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-800/50 rounded-lg">
                            <div className="flex items-center space-x-3">
                              <span className="text-lg font-bold text-purple-600">{sync.beat}s</span>
                              <span className="text-sm text-gray-700 dark:text-gray-300">{sync.action}</span>
                            </div>
                            <MusicalNoteIcon className="h-4 w-4 text-gray-400" />
                          </div>
                        ))}
                      </div>
                    </div>
                  </CardContent>
                </Card>
              )}

              {/* Loop Potential */}
              {reelData.loop_potential && reelData.loop_potential.enabled && (
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center space-x-2">
                      <FireIcon className="h-5 w-5 text-orange-600" />
                      <span>Loop Potential (Algorithm Boost)</span>
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-3">
                      <div className="flex items-center space-x-2 p-3 bg-green-50 dark:bg-green-900/20 rounded-lg">
                        <CheckCircleIcon className="h-5 w-5 text-green-600" />
                        <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                          Loop Enabled - Last frame connects to first
                        </span>
                      </div>
                      <div className="p-4 bg-gray-50 dark:bg-gray-800/50 rounded-lg">
                        <p className="text-xs text-gray-500 mb-2">Rewatch Trigger</p>
                        <p className="text-sm text-gray-700 dark:text-gray-300">{reelData.loop_potential.rewatch_trigger}</p>
                      </div>
                      <div className="p-4 bg-gray-50 dark:bg-gray-800/50 rounded-lg">
                        <p className="text-xs text-gray-500 mb-2">Callback Element</p>
                        <p className="text-sm text-gray-700 dark:text-gray-300">{reelData.loop_potential.callback_element}</p>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              )}
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

                  {/* Accessibility Info */}
                  {prompt.accessibility && (
                    <div className="p-4 bg-green-50 dark:bg-green-900/20 rounded-lg border border-green-200 dark:border-green-700/30">
                      <h4 className="text-sm font-semibold text-green-700 dark:text-green-400 mb-3 flex items-center space-x-2">
                        <CheckCircleIcon className="h-4 w-4" />
                        <span>Accessibility</span>
                      </h4>
                      <div className="space-y-2 text-sm">
                        <div>
                          <span className="text-gray-600 dark:text-gray-400">Alt Text:</span>
                          <p className="text-gray-700 dark:text-gray-300 mt-1">{prompt.accessibility.alt_text}</p>
                        </div>
                        <div className="grid grid-cols-2 gap-2 mt-2">
                          <div>
                            <span className="text-gray-600 dark:text-gray-400">Contrast:</span>
                            <p className="font-medium text-green-600">{prompt.accessibility.color_contrast_ratio}</p>
                          </div>
                          <div>
                            <span className="text-gray-600 dark:text-gray-400">Font:</span>
                            <p className="font-medium text-green-600">{prompt.accessibility.font_accessibility}</p>
                          </div>
                        </div>
                      </div>
                    </div>
                  )}

                  {/* Alt Text (legacy) */}
                  {prompt.alt_text && !prompt.accessibility && (
                    <div>
                      <h4 className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
                        Alt Text
                      </h4>
                      <p className="text-sm text-gray-600 dark:text-gray-400 bg-blue-50 dark:bg-blue-900/20 p-3 rounded-lg">
                        {prompt.alt_text}
                      </p>
                    </div>
                  )}
                </CardContent>
              </Card>
            ))}
            </div>
          </div>
        )}

        {/* Accessibility Tab */}
        {activeTab === 'accessibility' && (
          <div className="h-[calc(100vh-300px)] overflow-y-auto">
            <div className="space-y-6">
              {/* Meta Accessibility Status */}
              {meta.accessibility && (
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center space-x-2">
                      <CheckCircleIcon className="h-5 w-5 text-green-600" />
                      <span>Accessibility Compliance (WCAG AA)</span>
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                      <div className={`p-4 rounded-lg ${meta.accessibility.captions_included ? 'bg-green-50 dark:bg-green-900/20' : 'bg-red-50 dark:bg-red-900/20'}`}>
                        <CheckCircleIcon className={`h-6 w-6 mb-2 ${meta.accessibility.captions_included ? 'text-green-600' : 'text-red-600'}`} />
                        <p className="text-sm font-medium text-gray-700 dark:text-gray-300">Captions</p>
                        <p className={`text-xs ${meta.accessibility.captions_included ? 'text-green-600' : 'text-red-600'}`}>
                          {meta.accessibility.captions_included ? 'Included' : 'Missing'}
                        </p>
                      </div>
                      <div className={`p-4 rounded-lg ${meta.accessibility.alt_text_all_images ? 'bg-green-50 dark:bg-green-900/20' : 'bg-red-50 dark:bg-red-900/20'}`}>
                        <CheckCircleIcon className={`h-6 w-6 mb-2 ${meta.accessibility.alt_text_all_images ? 'text-green-600' : 'text-red-600'}`} />
                        <p className="text-sm font-medium text-gray-700 dark:text-gray-300">Alt Text</p>
                        <p className={`text-xs ${meta.accessibility.alt_text_all_images ? 'text-green-600' : 'text-red-600'}`}>
                          {meta.accessibility.alt_text_all_images ? 'All Images' : 'Missing'}
                        </p>
                      </div>
                      <div className={`p-4 rounded-lg ${meta.accessibility.color_contrast_checked ? 'bg-green-50 dark:bg-green-900/20' : 'bg-red-50 dark:bg-red-900/20'}`}>
                        <CheckCircleIcon className={`h-6 w-6 mb-2 ${meta.accessibility.color_contrast_checked ? 'text-green-600' : 'text-red-600'}`} />
                        <p className="text-sm font-medium text-gray-700 dark:text-gray-300">Contrast</p>
                        <p className={`text-xs ${meta.accessibility.color_contrast_checked ? 'text-green-600' : 'text-red-600'}`}>
                          {meta.accessibility.color_contrast_checked ? 'Checked (4.5:1+)' : 'Not Checked'}
                        </p>
                      </div>
                      <div className={`p-4 rounded-lg ${meta.accessibility.dyslexic_friendly_fonts ? 'bg-green-50 dark:bg-green-900/20' : 'bg-red-50 dark:bg-red-900/20'}`}>
                        <CheckCircleIcon className={`h-6 w-6 mb-2 ${meta.accessibility.dyslexic_friendly_fonts ? 'text-green-600' : 'text-red-600'}`} />
                        <p className="text-sm font-medium text-gray-700 dark:text-gray-300">Fonts</p>
                        <p className={`text-xs ${meta.accessibility.dyslexic_friendly_fonts ? 'text-green-600' : 'text-red-600'}`}>
                          {meta.accessibility.dyslexic_friendly_fonts ? 'Dyslexic-friendly' : 'Not Optimized'}
                        </p>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              )}

              {/* Auto Captions */}
              {reelData.accessibility?.auto_captions && reelData.accessibility.auto_captions.length > 0 && (
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center space-x-2">
                      <ChatBubbleLeftIcon className="h-5 w-5 text-blue-600" />
                      <span>Auto Captions ({reelData.accessibility.auto_captions.length})</span>
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-2">
                      {reelData.accessibility.auto_captions.map((caption: any, index: number) => (
                        <div key={index} className="p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg border-l-4 border-blue-500">
                          <div className="flex items-center justify-between mb-1">
                            <span className="text-xs font-semibold text-blue-700 dark:text-blue-400">{caption.time}</span>
                          </div>
                          <p className="text-sm text-gray-700 dark:text-gray-300">{caption.text}</p>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              )}

              {/* Audio Descriptions */}
              {reelData.accessibility?.audio_descriptions && reelData.accessibility.audio_descriptions.length > 0 && (
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center space-x-2">
                      <MusicalNoteIcon className="h-5 w-5 text-purple-600" />
                      <span>Audio Descriptions</span>
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <ul className="space-y-2">
                      {reelData.accessibility.audio_descriptions.map((desc: string, index: number) => (
                        <li key={index} className="p-3 bg-purple-50 dark:bg-purple-900/20 rounded-lg text-sm text-gray-700 dark:text-gray-300">
                          {desc}
                        </li>
                      ))}
                    </ul>
                  </CardContent>
                </Card>
              )}
            </div>
          </div>
        )}

        {/* Engagement Tab */}
        {activeTab === 'engagement' && (
          <div className="h-[calc(100vh-300px)] overflow-y-auto">
            <div className="space-y-6">
              {/* Engagement Tactics */}
              {reelData.engagement_tactics && (
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center space-x-2">
                      <FireIcon className="h-5 w-5 text-red-600" />
                      <span>Engagement Tactics</span>
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      {/* Comment Bait */}
                      <div className="p-4 bg-gradient-to-r from-blue-50 to-cyan-50 dark:from-blue-900/20 dark:to-cyan-900/20 rounded-lg border border-blue-200 dark:border-blue-700/30">
                        <div className="flex items-center space-x-2 mb-2">
                          <ChatBubbleLeftIcon className="h-5 w-5 text-blue-600" />
                          <h4 className="font-semibold text-gray-900 dark:text-gray-100">Comment Bait</h4>
                        </div>
                        <p className="text-gray-700 dark:text-gray-300">
                          {reelData.engagement_tactics.comment_bait}
                        </p>
                      </div>

                      {/* Save Trigger */}
                      <div className="p-4 bg-gradient-to-r from-purple-50 to-pink-50 dark:from-purple-900/20 dark:to-pink-900/20 rounded-lg border border-purple-200 dark:border-purple-700/30">
                        <div className="flex items-center space-x-2 mb-2">
                          <ArrowDownTrayIcon className="h-5 w-5 text-purple-600" />
                          <h4 className="font-semibold text-gray-900 dark:text-gray-100">Save Trigger</h4>
                        </div>
                        <p className="text-gray-700 dark:text-gray-300">
                          {reelData.engagement_tactics.save_trigger}
                        </p>
                      </div>

                      {/* Share Trigger */}
                      <div className="p-4 bg-gradient-to-r from-green-50 to-teal-50 dark:from-green-900/20 dark:to-teal-900/20 rounded-lg border border-green-200 dark:border-green-700/30">
                        <div className="flex items-center space-x-2 mb-2">
                          <ShareIcon className="h-5 w-5 text-green-600" />
                          <h4 className="font-semibold text-gray-900 dark:text-gray-100">Share Trigger</h4>
                        </div>
                        <p className="text-gray-700 dark:text-gray-300">
                          {reelData.engagement_tactics.share_trigger}
                        </p>
                      </div>

                      {/* Pattern Interrupt */}
                      <div className="p-4 bg-gradient-to-r from-orange-50 to-red-50 dark:from-orange-900/20 dark:to-red-900/20 rounded-lg border border-orange-200 dark:border-orange-700/30">
                        <div className="flex items-center space-x-2 mb-2">
                          <BoltIcon className="h-5 w-5 text-orange-600" />
                          <h4 className="font-semibold text-gray-900 dark:text-gray-100">Pattern Interrupt</h4>
                        </div>
                        <p className="text-gray-700 dark:text-gray-300">
                          {reelData.engagement_tactics.pattern_interrupt}
                        </p>
                      </div>

                      {/* Loop Element */}
                      <div className="p-4 bg-gradient-to-r from-yellow-50 to-amber-50 dark:from-yellow-900/20 dark:to-amber-900/20 rounded-lg border border-yellow-200 dark:border-yellow-700/30">
                        <div className="flex items-center space-x-2 mb-2">
                          <FireIcon className="h-5 w-5 text-yellow-600" />
                          <h4 className="font-semibold text-gray-900 dark:text-gray-100">Loop Element</h4>
                        </div>
                        <p className="text-gray-700 dark:text-gray-300">
                          {reelData.engagement_tactics.loop_element}
                        </p>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              )}

              {/* Structured Caption Breakdown */}
              {reelData.caption_structured && (
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center space-x-2">
                      <ChatBubbleLeftIcon className="h-5 w-5 text-indigo-600" />
                      <span>Caption Structure (SEO Optimized)</span>
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      {/* Hook (First 125 chars) */}
                      <div className="p-4 bg-yellow-50 dark:bg-yellow-900/20 rounded-lg border-l-4 border-yellow-500">
                        <h4 className="text-xs font-semibold text-yellow-700 dark:text-yellow-400 uppercase mb-2">
                          Hook (First 125 chars - Visible before "...more")
                        </h4>
                        <p className="text-gray-800 dark:text-gray-200 font-medium">
                          {reelData.caption_structured.hook_125chars}
                        </p>
                        <p className="text-xs text-gray-500 mt-2">
                          {reelData.caption_structured.hook_125chars?.length || 0} characters
                        </p>
                      </div>

                      {/* Problem Statement */}
                      <div className="p-4 bg-red-50 dark:bg-red-900/20 rounded-lg border-l-4 border-red-500">
                        <h4 className="text-xs font-semibold text-red-700 dark:text-red-400 uppercase mb-2">
                          Problem Statement
                        </h4>
                        <p className="text-gray-700 dark:text-gray-300 text-sm">
                          {reelData.caption_structured.problem_statement}
                        </p>
                      </div>

                      {/* Solution Tease */}
                      <div className="p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg border-l-4 border-blue-500">
                        <h4 className="text-xs font-semibold text-blue-700 dark:text-blue-400 uppercase mb-2">
                          Solution Tease
                        </h4>
                        <p className="text-gray-700 dark:text-gray-300 text-sm">
                          {reelData.caption_structured.solution_tease}
                        </p>
                      </div>

                      {/* Value Props */}
                      <div className="p-4 bg-green-50 dark:bg-green-900/20 rounded-lg border-l-4 border-green-500">
                        <h4 className="text-xs font-semibold text-green-700 dark:text-green-400 uppercase mb-2">
                          Value Propositions
                        </h4>
                        <ul className="space-y-2">
                          {reelData.caption_structured.value_props?.map((prop: string, index: number) => (
                            <li key={index} className="text-gray-700 dark:text-gray-300 text-sm">
                              {prop}
                            </li>
                          ))}
                        </ul>
                      </div>

                      {/* Keywords Woven */}
                      <div className="p-4 bg-purple-50 dark:bg-purple-900/20 rounded-lg border-l-4 border-purple-500">
                        <h4 className="text-xs font-semibold text-purple-700 dark:text-purple-400 uppercase mb-2">
                          Keywords Integration (SEO)
                        </h4>
                        <p className="text-gray-700 dark:text-gray-300 text-sm">
                          {reelData.caption_structured.keywords_woven}
                        </p>
                      </div>

                      {/* CTA */}
                      <div className="p-4 bg-indigo-50 dark:bg-indigo-900/20 rounded-lg border-l-4 border-indigo-500">
                        <h4 className="text-xs font-semibold text-indigo-700 dark:text-indigo-400 uppercase mb-2">
                          Call to Action
                        </h4>
                        <p className="text-gray-700 dark:text-gray-300 text-sm font-medium">
                          {reelData.caption_structured.cta}
                        </p>
                        {reelData.caption_structured.link && (
                          <p className="text-xs text-blue-600 dark:text-blue-400 mt-2 break-all">
                            Link: {reelData.caption_structured.link}
                          </p>
                        )}
                      </div>
                    </div>
                  </CardContent>
                </Card>
              )}
            </div>
          </div>
        )}

        {/* Phone Preview Tab */}
        {activeTab === 'preview' && (
          <div className="h-[calc(100vh-300px)] overflow-y-auto">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Phone Mockup */}
              <div className="flex items-center justify-center">
                <div className="relative">
                  {/* Phone Frame */}
                  <div className="w-[375px] h-[667px] bg-black rounded-[50px] p-3 shadow-2xl">
                    {/* Screen */}
                    <div className="w-full h-full bg-gradient-to-b from-gray-900 to-gray-800 rounded-[40px] overflow-hidden relative">
                      {/* Instagram UI */}
                      <div className="absolute top-0 left-0 right-0 z-10 p-4 bg-gradient-to-b from-black/60 to-transparent">
                        <div className="flex items-center justify-between">
                          <div className="flex items-center space-x-2">
                            <div className="w-8 h-8 bg-purple-500 rounded-full flex items-center justify-center">
                              <span className="text-white text-xs font-bold">SD</span>
                            </div>
                            <span className="text-white text-sm font-semibold">@systemdesign</span>
                          </div>
                          <MusicalNoteIcon className="h-5 w-5 text-white" />
                        </div>
                      </div>

                      {/* Content Area */}
                      <div className="h-full flex items-center justify-center p-8 text-center">
                        {segments[selectedSegment] ? (
                          <div className="space-y-6">
                            <h2 className="text-white text-2xl font-bold leading-tight">
                              {segments[selectedSegment].on_screen_text}
                            </h2>
                            <div className="flex items-center justify-center space-x-2 text-purple-300 text-sm">
                              <ClockIcon className="h-4 w-4" />
                              <span>{segments[selectedSegment].time_range}</span>
                            </div>
                          </div>
                        ) : (
                          <h2 className="text-white text-3xl font-bold leading-tight px-4">
                            {title}
                          </h2>
                        )}
                      </div>

                      {/* Bottom Actions */}
                      <div className="absolute bottom-0 right-0 p-4 space-y-6">
                        <div className="flex flex-col items-center space-y-1">
                          <HeartIcon className="h-7 w-7 text-white" />
                          <span className="text-white text-xs">2.4K</span>
                        </div>
                        <div className="flex flex-col items-center space-y-1">
                          <ChatBubbleLeftIcon className="h-7 w-7 text-white" />
                          <span className="text-white text-xs">156</span>
                        </div>
                        <div className="flex flex-col items-center space-y-1">
                          <ShareIcon className="h-7 w-7 text-white" />
                          <span className="text-white text-xs">89</span>
                        </div>
                      </div>

                      {/* Caption Preview */}
                      <div className="absolute bottom-0 left-0 right-16 p-4 bg-gradient-to-t from-black/80 to-transparent">
                        <p className="text-white text-xs line-clamp-2">
                          {caption.substring(0, 100)}...
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Timeline Scrubber & Controls */}
              <div className="space-y-6">
                {/* Playback Controls */}
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center justify-between">
                      <span>Playback Preview</span>
                      <span className="text-sm font-normal text-purple-600">
                        {currentTime.toFixed(1)}s / {totalDuration}s
                      </span>
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    {/* Timeline Scrubber */}
                    <div className="relative h-16 bg-gray-100 dark:bg-gray-800 rounded-lg overflow-hidden">
                      {/* Segments Background */}
                      {segments.map((segment: any, index: number) => {
                        const timeRange = segment.time_range || '0-0s';
                        const [start, end] = timeRange.split('-').map((t: string) => parseInt(t.replace('s', '')));
                        const startPercent = (start / totalDuration) * 100;
                        const widthPercent = ((end - start) / totalDuration) * 100;
                        return (
                          <div
                            key={index}
                            className={`absolute top-0 h-full bg-gradient-to-r ${getSegmentColor(segment.label)} opacity-20`}
                            style={{
                              left: `${startPercent}%`,
                              width: `${widthPercent}%`,
                            }}
                          />
                        );
                      })}
                      
                      {/* Progress Bar */}
                      <div
                        className="absolute top-0 h-full bg-purple-500 opacity-40"
                        style={{ width: `${(currentTime / totalDuration) * 100}%` }}
                      />
                      
                      {/* Playhead */}
                      <div
                        className="absolute top-0 w-1 h-full bg-purple-600 shadow-lg"
                        style={{ left: `${(currentTime / totalDuration) * 100}%` }}
                      />
                      
                      {/* Segment Labels */}
                      <div className="absolute inset-0 flex items-center px-2">
                        {segments.map((segment: any, index: number) => {
                          const timeRange = segment.time_range || '0-0s';
                          const [start] = timeRange.split('-').map((t: string) => parseInt(t.replace('s', '')));
                          const startPercent = (start / totalDuration) * 100;
                          return (
                            <div
                              key={index}
                              className="absolute text-xs font-semibold text-gray-700 dark:text-gray-300"
                              style={{ left: `${startPercent}%` }}
                            >
                              {segment.label}
                            </div>
                          );
                        })}
                      </div>
                    </div>

                    {/* Play/Pause Button */}
                    <div className="flex items-center justify-center space-x-4">
                      <Button
                        onClick={() => {
                          setCurrentTime(0);
                          setIsPlaying(false);
                        }}
                        variant="outline"
                        size="sm"
                      >
                        Reset
                      </Button>
                      <Button
                        onClick={() => setIsPlaying(!isPlaying)}
                        className="px-8"
                      >
                        {isPlaying ? 'Pause' : 'Play'}
                      </Button>
                    </div>
                  </CardContent>
                </Card>

                {/* Current Segment Info */}
                <Card>
                  <CardHeader>
                    <CardTitle>Current Segment</CardTitle>
                  </CardHeader>
                  <CardContent>
                    {segments[selectedSegment] && (
                      <div className="space-y-3">
                        <div className="flex items-center space-x-2">
                          <div className={`w-3 h-3 bg-gradient-to-r ${getSegmentColor(segments[selectedSegment].label)} rounded-full`} />
                          <span className="font-semibold text-gray-900 dark:text-gray-100">
                            {segments[selectedSegment].label}
                          </span>
                          <span className="text-sm text-gray-500">
                            {segments[selectedSegment].time_range}
                          </span>
                        </div>
                        <p className="text-sm text-gray-600 dark:text-gray-400">
                          {segments[selectedSegment].narration}
                        </p>
                      </div>
                    )}
                  </CardContent>
                </Card>

                {/* Visual Plan */}
                {reelData.visual_plan && (
                  <Card>
                    <CardHeader>
                      <CardTitle className="flex items-center space-x-2">
                        <PhotoIcon className="h-5 w-5 text-purple-600" />
                        <span>Visual Plan</span>
                      </CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-3">
                      <div>
                        <span className="text-sm font-semibold text-gray-700 dark:text-gray-300">Color Palette:</span>
                        <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                          {reelData.visual_plan.color_palette}
                        </p>
                      </div>
                      <div>
                        <span className="text-sm font-semibold text-gray-700 dark:text-gray-300">Motion Graphics:</span>
                        <div className="flex flex-wrap gap-2 mt-1">
                          {reelData.visual_plan.motion_graphics?.map((mg: string, i: number) => (
                            <span key={i} className="px-2 py-1 bg-blue-100 dark:bg-blue-900/20 text-blue-700 dark:text-blue-300 rounded text-xs">
                              {mg}
                            </span>
                          ))}
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                )}
              </div>
            </div>
          </div>
        )}

        {/* Analytics Tab */}
        {activeTab === 'analytics' && (
          <div className="h-[calc(100vh-300px)] overflow-y-auto">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {/* Engagement Score */}
              <Card className="col-span-1 md:col-span-2 lg:col-span-3">
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <ChartBarIcon className="h-5 w-5 text-purple-600" />
                    <span>Content Performance Prediction</span>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {/* Engagement Score */}
                    <div className="text-center p-6 bg-gradient-to-br from-purple-50 to-pink-50 dark:from-purple-900/20 dark:to-pink-900/20 rounded-xl">
                      <FireIcon className="h-12 w-12 text-purple-600 mx-auto mb-3" />
                      <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-2">
                        Engagement Score
                      </h3>
                      <p className={`text-5xl font-bold ${getScoreColor(engagementScore)} mb-2`}>
                        {engagementScore}
                      </p>
                      <p className="text-sm text-gray-600 dark:text-gray-400">out of 100</p>
                      <div className="mt-4 w-full bg-gray-200 dark:bg-gray-700 rounded-full h-3">
                        <div
                          className="bg-gradient-to-r from-purple-500 to-pink-500 h-3 rounded-full transition-all duration-500"
                          style={{ width: `${engagementScore}%` }}
                        />
                      </div>
                    </div>

                    {/* SEO Score */}
                    <div className="text-center p-6 bg-gradient-to-br from-blue-50 to-teal-50 dark:from-blue-900/20 dark:to-teal-900/20 rounded-xl">
                      <BoltIcon className="h-12 w-12 text-blue-600 mx-auto mb-3" />
                      <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-2">
                        SEO Score
                      </h3>
                      <p className={`text-5xl font-bold ${getScoreColor(seoScore)} mb-2`}>
                        {seoScore}
                      </p>
                      <p className="text-sm text-gray-600 dark:text-gray-400">out of 100</p>
                      <div className="mt-4 w-full bg-gray-200 dark:bg-gray-700 rounded-full h-3">
                        <div
                          className="bg-gradient-to-r from-blue-500 to-teal-500 h-3 rounded-full transition-all duration-500"
                          style={{ width: `${seoScore}%` }}
                        />
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Estimated Reach */}
              <Card>
                <CardContent className="p-6 text-center">
                  <EyeIcon className="h-12 w-12 text-blue-600 mx-auto mb-3" />
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
                    Est. Reach
                  </h3>
                  <p className="text-3xl font-bold text-blue-600 mt-2">
                    {Math.round(engagementScore * 150 + 2000).toLocaleString()}
                  </p>
                  <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
                    accounts
                  </p>
                </CardContent>
              </Card>

              {/* Estimated Likes */}
              <Card>
                <CardContent className="p-6 text-center">
                  <HeartIcon className="h-12 w-12 text-pink-600 mx-auto mb-3" />
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
                    Est. Likes
                  </h3>
                  <p className="text-3xl font-bold text-pink-600 mt-2">
                    {Math.round((engagementScore * 150 + 2000) * 0.08).toLocaleString()}
                  </p>
                  <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
                    8% engagement rate
                  </p>
                </CardContent>
              </Card>

              {/* Estimated Shares */}
              <Card>
                <CardContent className="p-6 text-center">
                  <ShareIcon className="h-12 w-12 text-green-600 mx-auto mb-3" />
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
                    Est. Shares
                  </h3>
                  <p className="text-3xl font-bold text-green-600 mt-2">
                    {Math.round((engagementScore * 150 + 2000) * 0.02).toLocaleString()}
                  </p>
                  <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
                    2% share rate
                  </p>
                </CardContent>
              </Card>

              {/* Hook Strength */}
              <Card className="col-span-1 md:col-span-2 lg:col-span-3">
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <SparklesIcon className="h-5 w-5 text-yellow-600" />
                    <span>Hook Analysis</span>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div className="p-4 bg-yellow-50 dark:bg-yellow-900/20 rounded-lg">
                      <p className="text-gray-800 dark:text-gray-200 font-medium">
                        "{hook}"
                      </p>
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                      <div className="p-4 bg-gray-50 dark:bg-gray-800/50 rounded-lg">
                        <h4 className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-1">
                          Length
                        </h4>
                        <p className={`text-2xl font-bold ${hook.length > 50 && hook.length < 120 ? 'text-green-500' : 'text-yellow-500'}`}>
                          {hook.length}
                        </p>
                        <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                          {hook.length > 50 && hook.length < 120 ? 'Optimal' : 'Could be better'}
                        </p>
                      </div>
                      <div className="p-4 bg-gray-50 dark:bg-gray-800/50 rounded-lg">
                        <h4 className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-1">
                          Question Mark
                        </h4>
                        <p className={`text-2xl font-bold ${hook.includes('?') ? 'text-green-500' : 'text-gray-400'}`}>
                          {hook.includes('?') ? '✓' : '✗'}
                        </p>
                        <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                          {hook.includes('?') ? 'Engages curiosity' : 'Consider adding'}
                        </p>
                      </div>
                      <div className="p-4 bg-gray-50 dark:bg-gray-800/50 rounded-lg">
                        <h4 className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-1">
                          Power Words
                        </h4>
                        <p className="text-2xl font-bold text-purple-500">
                          {['stop', 'how', 'why', 'secret', 'proven', 'ultimate', 'killing', 'crush'].filter(word => 
                            hook.toLowerCase().includes(word)
                          ).length}
                        </p>
                        <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                          Found in hook
                        </p>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Hashtag Strategy */}
              <Card className="col-span-1 md:col-span-2 lg:col-span-3">
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <HashtagIcon className="h-5 w-5 text-blue-600" />
                    <span>Hashtag Strategy Breakdown</span>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                    {meta.keyword_tiers && Object.entries(meta.keyword_tiers).map(([tier, tags]: [string, any]) => (
                      <div key={tier} className="p-4 bg-gray-50 dark:bg-gray-800/50 rounded-lg">
                        <h4 className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2 capitalize">
                          {tier.replace('_', ' ')}
                        </h4>
                        <p className="text-3xl font-bold text-purple-600 mb-2">
                          {tags?.length || 0}
                        </p>
                        <div className="flex flex-wrap gap-1">
                          {tags?.slice(0, 3).map((tag: string, i: number) => (
                            <span key={i} className="text-xs px-2 py-1 bg-purple-100 dark:bg-purple-900/20 text-purple-700 dark:text-purple-300 rounded">
                              #{tag}
                            </span>
                          ))}
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        )}

        {/* Export Tab */}
        {activeTab === 'export' && (
          <div className="h-[calc(100vh-300px)] overflow-y-auto">
            <div className="max-w-4xl mx-auto space-y-6">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <ArrowDownTrayIcon className="h-5 w-5 text-purple-600" />
                    <span>Export Options</span>
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-6">
                  {/* Export Formats */}
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {/* JSON Export */}
                    <div className="p-6 border-2 border-gray-200 dark:border-gray-700 rounded-xl hover:border-purple-500 dark:hover:border-purple-500 transition-colors">
                      <DocumentDuplicateIcon className="h-10 w-10 text-purple-600 mb-3" />
                      <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-2">
                        JSON Export
                      </h3>
                      <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
                        Download complete data structure for programmatic use
                      </p>
                      <Button onClick={exportAsJSON} className="w-full">
                        <ArrowDownTrayIcon className="h-4 w-4 mr-2" />
                        Download JSON
                      </Button>
                    </div>

                    {/* Script Export */}
                    <div className="p-6 border-2 border-gray-200 dark:border-gray-700 rounded-xl hover:border-purple-500 dark:hover:border-purple-500 transition-colors">
                      <FilmIcon className="h-10 w-10 text-blue-600 mb-3" />
                      <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-2">
                        Production Script
                      </h3>
                      <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
                        Download formatted script for video production team
                      </p>
                      <Button onClick={exportAsScript} variant="outline" className="w-full">
                        <ArrowDownTrayIcon className="h-4 w-4 mr-2" />
                        Download Script
                      </Button>
                    </div>
                  </div>

                  {/* Quick Copy Options */}
                  <div className="space-y-3">
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
                      Quick Copy
                    </h3>
                    <div className="grid grid-cols-1 gap-3">
                      {/* Copy Full Caption */}
                      <div className="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-800/50 rounded-lg">
                        <div>
                          <h4 className="font-medium text-gray-900 dark:text-gray-100">Full Caption</h4>
                          <p className="text-sm text-gray-600 dark:text-gray-400">
                            Caption + Hashtags + CTA
                          </p>
                        </div>
                        <Button
                          size="sm"
                          onClick={() => copyToClipboard(`${caption}\n\n${hashtags.map((t: string) => t.startsWith('#') ? t : `#${t}`).join(' ')}`)}
                        >
                          <DocumentDuplicateIcon className="h-4 w-4 mr-2" />
                          Copy
                        </Button>
                      </div>

                      {/* Copy All Hashtags */}
                      <div className="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-800/50 rounded-lg">
                        <div>
                          <h4 className="font-medium text-gray-900 dark:text-gray-100">All Hashtags</h4>
                          <p className="text-sm text-gray-600 dark:text-gray-400">
                            {hashtags.length} hashtags ready to paste
                          </p>
                        </div>
                        <Button
                          size="sm"
                          variant="outline"
                          onClick={() => copyToClipboard(hashtags.map((t: string) => t.startsWith('#') ? t : `#${t}`).join(' '))}
                        >
                          <DocumentDuplicateIcon className="h-4 w-4 mr-2" />
                          Copy
                        </Button>
                      </div>

                      {/* Copy Image Prompts */}
                      <div className="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-800/50 rounded-lg">
                        <div>
                          <h4 className="font-medium text-gray-900 dark:text-gray-100">Image Prompts</h4>
                          <p className="text-sm text-gray-600 dark:text-gray-400">
                            All {imagePrompts.length} prompts for AI image generation
                          </p>
                        </div>
                        <Button
                          size="sm"
                          variant="outline"
                          onClick={() => {
                            const promptsText = imagePrompts.map((p: any, i: number) => 
                              `Image ${i + 1} (${p.role}):\n${p.prompt}\n\nNegative: ${p.negative_prompt}\n`
                            ).join('\n---\n\n');
                            copyToClipboard(promptsText);
                          }}
                        >
                          <DocumentDuplicateIcon className="h-4 w-4 mr-2" />
                          Copy
                        </Button>
                      </div>
                    </div>
                  </div>

                  {/* Integration Options */}
                  <div className="space-y-3">
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
                      Integration Ready
                    </h3>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                      <div className="p-4 bg-gradient-to-br from-blue-50 to-blue-100 dark:from-blue-900/20 dark:to-blue-800/20 rounded-lg text-center">
                        <BeakerIcon className="h-8 w-8 text-blue-600 mx-auto mb-2" />
                        <p className="text-sm font-medium text-gray-900 dark:text-gray-100">
                          Notion
                        </p>
                        <p className="text-xs text-gray-600 dark:text-gray-400 mt-1">
                          Coming Soon
                        </p>
                      </div>
                      <div className="p-4 bg-gradient-to-br from-purple-50 to-purple-100 dark:from-purple-900/20 dark:to-purple-800/20 rounded-lg text-center">
                        <BeakerIcon className="h-8 w-8 text-purple-600 mx-auto mb-2" />
                        <p className="text-sm font-medium text-gray-900 dark:text-gray-100">
                          Airtable
                        </p>
                        <p className="text-xs text-gray-600 dark:text-gray-400 mt-1">
                          Coming Soon
                        </p>
                      </div>
                      <div className="p-4 bg-gradient-to-br from-pink-50 to-pink-100 dark:from-pink-900/20 dark:to-pink-800/20 rounded-lg text-center">
                        <BeakerIcon className="h-8 w-8 text-pink-600 mx-auto mb-2" />
                        <p className="text-sm font-medium text-gray-900 dark:text-gray-100">
                          Trello
                        </p>
                        <p className="text-xs text-gray-600 dark:text-gray-400 mt-1">
                          Coming Soon
                        </p>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
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