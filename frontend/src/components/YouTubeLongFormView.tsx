import React, { useState } from 'react';
import { 
  HashtagIcon,
  DocumentDuplicateIcon,
  ClockIcon,
  SparklesIcon,
  MusicalNoteIcon,
  VideoCameraIcon,
  MegaphoneIcon,
  FilmIcon,
  BookOpenIcon,
  ChartBarIcon,
  LightBulbIcon,
  PencilSquareIcon,
  PhotoIcon,
  SpeakerWaveIcon
} from '@heroicons/react/24/outline';
import { Card, CardContent, CardHeader, CardTitle } from './ui/Card';
import { Button } from './ui/Button';
import { cn } from '../lib/utils';

// New comprehensive interfaces
interface MusicInfo {
  vibe: string[];
  bpm_range: string;
  ducking_notes?: string;
}

interface IntroSection {
  time_range: string;
  narration: string;
  on_screen_text: string;
  visuals: string;
  b_roll: string[];
  sfx: string[];
  music: MusicInfo;
}

interface OutlineSection {
  section: string;
  beats: string[];
}

interface Chapter {
  index: number;
  name: string;
  timestamp: string;
}

interface ScriptSegment {
  chapter_index: number;
  time_range: string;
  talking_points: string[];
  details: string;
  screen_recording_notes: string[];
  graphics: string[];
}

interface BRollPlan {
  time: string;
  ideas: string[];
}

interface GraphicsItem {
  name: string;
  purpose: string;
  appears_at: string;
}

interface VisualAids {
  b_roll_plan: BRollPlan[];
  graphics_list: GraphicsItem[];
  lower_thirds: string[];
  music: MusicInfo;
  sfx: string[];
}

interface EndScreen {
  duration_seconds: number;
  elements: string[];
  show_handles: boolean;
}

interface CTA {
  midroll: string;
  end: string;
  end_screen: EndScreen;
}

interface DescriptionChapter {
  time: string;
  title: string;
}

interface Resource {
  title: string;
  url: string;
}

interface Description {
  text: string;
  chapters: DescriptionChapter[];
  resources: Resource[];
  hashtags: string[];
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
  est_duration_minutes: number;
  title_char_count: number;
  chapters_count: number;
  description_word_count: number;
  tags_count: number;
  image_prompt_count: number;
  has_tracked_link: boolean;
  checks: string[];
}

interface YouTubeLongFormContent {
  title: string;
  thumbnail_text: string;
  intro: IntroSection;
  outline: OutlineSection[];
  chapters: Chapter[];
  script: ScriptSegment[];
  visual_aids: VisualAids;
  cta: CTA;
  description: Description;
  tags: string[];
  image_prompts: ImagePrompt[];
  compliance: Compliance;
}

interface YouTubeLongFormViewProps {
  content: {
    job_id: string;
    platform: string;
    format: string;
    envelope: {
      content: YouTubeLongFormContent;
    };
    meta?: {
      topic_title?: string;
      topic_id?: string;
    };
  };
  onCopy: () => void;
}

const YouTubeLongFormView: React.FC<YouTubeLongFormViewProps> = ({ content, onCopy }) => {
  const [activeTab, setActiveTab] = useState<'overview' | 'script' | 'production' | 'metadata'>('overview');
  const [expandedChapter, setExpandedChapter] = useState<number | null>(null);
  
  // Extract content with fallbacks
  const video = content.envelope?.content || {};
  const meta = content.meta || {};
  
  // Add fallbacks for required properties
  const title = video.title || 'Untitled Video';
  const thumbnail_text = video.thumbnail_text || '';
  const intro = video.intro || {};
  const outline = video.outline || [];
  const chapters = video.chapters || [];
  const script = video.script || [];
  const visual_aids = video.visual_aids || {};
  const cta = video.cta || {};
  const description = video.description || {};
  const tags = video.tags || [];
  const image_prompts = video.image_prompts || [];
  const compliance = video.compliance || {};

  const getChapterColor = (index: number) => {
    const colors = [
      'bg-primary-100 dark:bg-primary-900/20 text-primary-800 dark:text-primary-400 border-primary-200 dark:border-primary-700',
      'bg-success-100 dark:bg-success-900/20 text-success-800 dark:text-success-400 border-success-200 dark:border-success-700',
      'bg-secondary-100 dark:bg-secondary-900/20 text-secondary-800 dark:text-secondary-400 border-secondary-200 dark:border-secondary-700',
      'bg-warning-100 dark:bg-warning-900/20 text-warning-800 dark:text-warning-400 border-warning-200 dark:border-warning-700',
      'bg-error-100 dark:bg-error-900/20 text-error-800 dark:text-error-400 border-error-200 dark:border-error-700',
      'bg-indigo-100 dark:bg-indigo-900/20 text-indigo-800 dark:text-indigo-400 border-indigo-200 dark:border-indigo-700'
    ];
    return colors[index % colors.length];
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
  };

  return (
    <div className="bg-white dark:bg-gray-900 rounded-3xl shadow-2xl max-w-7xl w-full max-h-[90vh] overflow-hidden flex flex-col">
      {/* Header */}
      <div className="bg-gradient-to-r from-red-500 to-red-600 text-white p-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="p-3 bg-white/20 backdrop-blur-sm rounded-xl">
              <VideoCameraIcon className="h-8 w-8" />
            </div>
            <div>
              <h2 className="text-2xl font-bold">YouTube Long Form</h2>
              {meta.topic_title && (
                <p className="text-red-100 text-sm mt-1">{meta.topic_title}</p>
              )}
              <p className="text-red-200 text-xs mt-1">{compliance.est_duration_minutes || 0} min • {chapters.length} chapters</p>
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
            variant={activeTab === 'overview' ? 'primary' : 'ghost'}
            onClick={() => setActiveTab('overview')}
            className={cn("flex-1", activeTab === 'overview' && "shadow-sm")}
          >
            <BookOpenIcon className="h-4 w-4 mr-2" />
            Overview
          </Button>
          <Button
            variant={activeTab === 'script' ? 'primary' : 'ghost'}
            onClick={() => setActiveTab('script')}
            className={cn("flex-1", activeTab === 'script' && "shadow-sm")}
          >
            <PencilSquareIcon className="h-4 w-4 mr-2" />
            Script
          </Button>
          <Button
            variant={activeTab === 'production' ? 'primary' : 'ghost'}
            onClick={() => setActiveTab('production')}
            className={cn("flex-1", activeTab === 'production' && "shadow-sm")}
          >
            <FilmIcon className="h-4 w-4 mr-2" />
            Production
          </Button>
          <Button
            variant={activeTab === 'metadata' ? 'primary' : 'ghost'}
            onClick={() => setActiveTab('metadata')}
            className={cn("flex-1", activeTab === 'metadata' && "shadow-sm")}
          >
            <ChartBarIcon className="h-4 w-4 mr-2" />
            Metadata
          </Button>
        </div>
      </div>

      {/* Content Area */}
      <div className="flex-1 overflow-y-auto p-6 bg-gray-50 dark:bg-gray-950">
        {/* Overview Tab */}
        {activeTab === 'overview' && (
          <div className="space-y-6 animate-fade-in">
            {/* Title & Thumbnail */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <VideoCameraIcon className="h-5 w-5 mr-2 text-primary-600 dark:text-primary-400" />
                  Title & Thumbnail
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Title</p>
                  <p className="text-xl font-bold text-gray-900 dark:text-gray-100">
                    {title}
                  </p>
                  <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                    {compliance.title_char_count || title.length} characters
                  </p>
                </div>
                {thumbnail_text && (
                  <div>
                    <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Thumbnail Text</p>
                    <div className="bg-gradient-to-r from-red-50 to-pink-50 dark:from-red-900/20 dark:to-pink-900/20 p-4 rounded-xl border border-red-200 dark:border-red-700">
                      <p className="text-lg font-bold text-red-800 dark:text-red-200">
                        {thumbnail_text}
                      </p>
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>

            {/* Intro Section */}
            {intro.narration && (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <SparklesIcon className="h-5 w-5 mr-2 text-secondary-600 dark:text-secondary-400" />
                    Introduction ({intro.time_range || '0:00-0:15'})
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div>
                      <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Narration</p>
                      <p className="text-gray-700 dark:text-gray-300">{intro.narration}</p>
                    </div>
                    {intro.on_screen_text && (
                      <div>
                        <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">On-Screen Text</p>
                        <div className="bg-primary-50 dark:bg-primary-900/20 p-3 rounded-lg border border-primary-200 dark:border-primary-700">
                          <p className="text-primary-800 dark:text-primary-200 font-medium">{intro.on_screen_text}</p>
                        </div>
                      </div>
                    )}
                    {intro.visuals && (
                      <div>
                        <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Visuals</p>
                        <p className="text-gray-600 dark:text-gray-400 italic">{intro.visuals}</p>
                      </div>
                    )}
                  </div>
                </CardContent>
              </Card>
            )}

            {/* Content Outline */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <BookOpenIcon className="h-5 w-5 mr-2 text-primary-600 dark:text-primary-400" />
                  Content Outline
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {outline.map((section, index) => (
                    <Card key={index} variant="filled">
                      <CardContent className="p-4">
                        <h4 className="font-medium text-gray-900 dark:text-gray-100 mb-2">{section.section}</h4>
                        <ul className="space-y-1">
                          {section.beats.map((beat, beatIndex) => (
                            <li key={beatIndex} className="flex items-start text-sm text-gray-600 dark:text-gray-400">
                              <span className="text-primary-500 mr-2">•</span>
                              {beat}
                            </li>
                          ))}
                        </ul>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Chapters */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <ClockIcon className="h-5 w-5 mr-2 text-secondary-600 dark:text-secondary-400" />
                  Chapters & Timestamps
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  {chapters.map((chapter, index) => (
                    <div
                      key={index}
                      className={cn(
                        "flex items-center justify-between p-3 rounded-lg border",
                        getChapterColor(index)
                      )}
                    >
                      <div className="flex items-center space-x-3">
                        <span className="text-lg font-bold">#{chapter.index}</span>
                        <span className="font-medium">{chapter.name}</span>
                      </div>
                      <span className="text-sm font-mono">{chapter.timestamp}</span>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>
        )}

        {/* Script Tab */}
        {activeTab === 'script' && (
          <div className="space-y-6 animate-fade-in">
            {script.map((segment, index) => {
              const chapter = chapters.find(ch => ch.index === segment.chapter_index);
              return (
                <Card key={index}>
                  <CardHeader
                    className="cursor-pointer"
                    onClick={() => setExpandedChapter(expandedChapter === index ? null : index)}
                  >
                    <CardTitle className="flex items-center justify-between">
                      <span className="flex items-center">
                        <PencilSquareIcon className="h-5 w-5 mr-2 text-primary-600 dark:text-primary-400" />
                        {chapter?.name || `Chapter ${segment.chapter_index}`}
                      </span>
                      <span className="text-sm font-mono text-gray-500 dark:text-gray-400">
                        {segment.time_range}
                      </span>
                    </CardTitle>
                  </CardHeader>
                  {(expandedChapter === null || expandedChapter === index) && (
                    <CardContent className="space-y-4">
                      {/* Talking Points */}
                      <div>
                        <h4 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Talking Points</h4>
                        <ul className="space-y-1">
                          {segment.talking_points.map((point, pointIndex) => (
                            <li key={pointIndex} className="flex items-start text-sm">
                              <span className="text-primary-500 mr-2">•</span>
                              <span className="text-gray-700 dark:text-gray-300">{point}</span>
                            </li>
                          ))}
                        </ul>
                      </div>

                      {/* Details */}
                      <div>
                        <h4 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Script Details</h4>
                        <div className="bg-gray-50 dark:bg-gray-800 p-4 rounded-lg border border-gray-200 dark:border-gray-700">
                          <p className="text-gray-700 dark:text-gray-300 whitespace-pre-wrap">{segment.details}</p>
                        </div>
                      </div>

                      {/* Screen Recording Notes */}
                      {segment.screen_recording_notes.length > 0 && (
                        <div>
                          <h4 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Screen Recording Notes</h4>
                          <div className="bg-blue-50 dark:bg-blue-900/20 p-3 rounded-lg border border-blue-200 dark:border-blue-700">
                            <ul className="space-y-1">
                              {segment.screen_recording_notes.map((note, noteIndex) => (
                                <li key={noteIndex} className="text-sm text-blue-800 dark:text-blue-200">
                                  • {note}
                                </li>
                              ))}
                            </ul>
                          </div>
                        </div>
                      )}

                      {/* Graphics */}
                      {segment.graphics.length > 0 && (
                        <div>
                          <h4 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Graphics</h4>
                          <div className="flex flex-wrap gap-2">
                            {segment.graphics.map((graphic, graphicIndex) => (
                              <span
                                key={graphicIndex}
                                className="px-3 py-1 bg-secondary-100 dark:bg-secondary-900/20 text-secondary-800 dark:text-secondary-400 rounded-full text-sm font-medium"
                              >
                                {graphic}
                              </span>
                            ))}
                          </div>
                        </div>
                      )}
                    </CardContent>
                  )}
                </Card>
              );
            })}
          </div>
        )}

        {/* Production Tab */}
        {activeTab === 'production' && (
          <div className="space-y-6 animate-fade-in">
            {/* Visual Aids */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <PhotoIcon className="h-5 w-5 mr-2 text-primary-600 dark:text-primary-400" />
                  Visual Aids & B-Roll
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {/* B-Roll Plan */}
                {visual_aids.b_roll_plan && visual_aids.b_roll_plan.length > 0 && (
                  <div>
                    <h4 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">B-Roll Plan</h4>
                    <div className="space-y-3">
                      {visual_aids.b_roll_plan.map((plan, index) => (
                        <div key={index} className="bg-gray-50 dark:bg-gray-800 p-3 rounded-lg border border-gray-200 dark:border-gray-700">
                          <div className="flex items-center justify-between mb-2">
                            <span className="text-sm font-medium text-gray-700 dark:text-gray-300">Time: {plan.time}</span>
                          </div>
                          <ul className="space-y-1">
                            {plan.ideas.map((idea, ideaIndex) => (
                              <li key={ideaIndex} className="text-sm text-gray-600 dark:text-gray-400">
                                • {idea}
                              </li>
                            ))}
                          </ul>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Graphics List */}
                {visual_aids.graphics_list && visual_aids.graphics_list.length > 0 && (
                  <div>
                    <h4 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">Graphics</h4>
                    <div className="space-y-2">
                      {visual_aids.graphics_list.map((graphic, index) => (
                        <div key={index} className="flex items-center justify-between p-3 bg-primary-50 dark:bg-primary-900/20 rounded-lg border border-primary-200 dark:border-primary-700">
                          <div>
                            <p className="font-medium text-primary-800 dark:text-primary-200">{graphic.name}</p>
                            <p className="text-sm text-primary-600 dark:text-primary-400">{graphic.purpose}</p>
                          </div>
                          <span className="text-sm font-mono text-primary-600 dark:text-primary-400">{graphic.appears_at}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Lower Thirds */}
                {visual_aids.lower_thirds && visual_aids.lower_thirds.length > 0 && (
                  <div>
                    <h4 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">Lower Thirds</h4>
                    <div className="flex flex-wrap gap-2">
                      {visual_aids.lower_thirds.map((text, index) => (
                        <span key={index} className="px-3 py-1 bg-secondary-100 dark:bg-secondary-900/20 text-secondary-800 dark:text-secondary-400 rounded text-sm">
                          {text}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>

            {/* Music & Sound */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <MusicalNoteIcon className="h-5 w-5 mr-2 text-green-600 dark:text-green-400" />
                  Music & Sound Effects
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {/* Music */}
                {visual_aids.music && (
                  <div>
                    <h4 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Music</h4>
                    <div className="bg-green-50 dark:bg-green-900/20 p-4 rounded-lg border border-green-200 dark:border-green-700">
                      <p className="text-sm text-green-800 dark:text-green-200">
                        <strong>Vibe:</strong> {visual_aids.music.vibe?.join(', ') || 'Not specified'}
                      </p>
                      <p className="text-sm text-green-800 dark:text-green-200 mt-1">
                        <strong>BPM:</strong> {visual_aids.music.bpm_range || 'Not specified'}
                      </p>
                      {visual_aids.music.ducking_notes && (
                        <p className="text-sm text-green-700 dark:text-green-300 mt-1">
                          <strong>Ducking:</strong> {visual_aids.music.ducking_notes}
                        </p>
                      )}
                    </div>
                  </div>
                )}

                {/* Sound Effects */}
                {visual_aids.sfx && visual_aids.sfx.length > 0 && (
                  <div>
                    <h4 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Sound Effects</h4>
                    <div className="flex flex-wrap gap-2">
                      {visual_aids.sfx.map((sfx, index) => (
                        <span key={index} className="px-3 py-1 bg-green-100 dark:bg-green-900/20 text-green-800 dark:text-green-400 rounded-full text-sm">
                          <SpeakerWaveIcon className="h-3 w-3 inline mr-1" />
                          {sfx}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>

            {/* Image Prompts */}
            {image_prompts.length > 0 && (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <PhotoIcon className="h-5 w-5 mr-2 text-secondary-600 dark:text-secondary-400" />
                    Thumbnail Prompts ({image_prompts.length})
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {image_prompts.map((prompt, idx) => (
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

        {/* Metadata Tab */}
        {activeTab === 'metadata' && (
          <div className="space-y-6 animate-fade-in">
            {/* Description */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center justify-between">
                  <span className="flex items-center">
                    <BookOpenIcon className="h-5 w-5 mr-2 text-primary-600 dark:text-primary-400" />
                    Description
                  </span>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => copyToClipboard(description.text || '')}
                    leftIcon={<DocumentDuplicateIcon className="h-4 w-4" />}
                  >
                    Copy
                  </Button>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="bg-white dark:bg-gray-800 p-4 rounded-xl border border-gray-200 dark:border-gray-700">
                  <p className="text-gray-700 dark:text-gray-300 whitespace-pre-wrap text-sm">
                    {description.text || 'No description provided'}
                  </p>
                </div>
                {compliance.description_word_count && (
                  <p className="text-xs text-gray-500 dark:text-gray-400 mt-2">
                    {compliance.description_word_count} words
                  </p>
                )}
              </CardContent>
            </Card>

            {/* Call to Action */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <MegaphoneIcon className="h-5 w-5 mr-2 text-secondary-600 dark:text-secondary-400" />
                  Call to Action
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {cta.midroll && (
                  <div>
                    <h4 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Mid-roll CTA</h4>
                    <div className="bg-secondary-50 dark:bg-secondary-900/20 p-3 rounded-lg border border-secondary-200 dark:border-secondary-700">
                      <p className="text-secondary-800 dark:text-secondary-200">{cta.midroll}</p>
                    </div>
                  </div>
                )}
                {cta.end && (
                  <div>
                    <h4 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">End CTA</h4>
                    <div className="bg-secondary-50 dark:bg-secondary-900/20 p-3 rounded-lg border border-secondary-200 dark:border-secondary-700">
                      <p className="text-secondary-800 dark:text-secondary-200">{cta.end}</p>
                    </div>
                  </div>
                )}
                {cta.end_screen && (
                  <div>
                    <h4 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">End Screen</h4>
                    <div className="bg-gray-50 dark:bg-gray-800 p-3 rounded-lg border border-gray-200 dark:border-gray-700">
                      <p className="text-sm text-gray-700 dark:text-gray-300">
                        <strong>Duration:</strong> {cta.end_screen.duration_seconds}s
                      </p>
                      <p className="text-sm text-gray-700 dark:text-gray-300 mt-1">
                        <strong>Elements:</strong> {cta.end_screen.elements?.join(', ') || 'None'}
                      </p>
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>

            {/* Tags */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center justify-between">
                  <span className="flex items-center">
                    <HashtagIcon className="h-5 w-5 mr-2 text-primary-600 dark:text-primary-400" />
                    Tags ({tags.length})
                  </span>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => copyToClipboard(tags.join(', '))}
                    leftIcon={<DocumentDuplicateIcon className="h-4 w-4" />}
                  >
                    Copy All
                  </Button>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex flex-wrap gap-2">
                  {tags.map((tag, idx) => (
                    <span key={idx} className="px-3 py-1 bg-primary-100 dark:bg-primary-900/20 text-primary-800 dark:text-primary-400 rounded-full text-sm font-medium border border-primary-200 dark:border-primary-700">
                      {tag}
                    </span>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Compliance */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <LightBulbIcon className="h-5 w-5 mr-2 text-success-600 dark:text-success-400" />
                  Compliance & Checks
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-2 md:grid-cols-3 gap-4 mb-4">
                  <div className="text-center">
                    <p className="text-2xl font-bold text-primary-600 dark:text-primary-400">
                      {compliance.est_duration_minutes || 0}
                    </p>
                    <p className="text-xs text-gray-600 dark:text-gray-400">Minutes</p>
                  </div>
                  <div className="text-center">
                    <p className="text-2xl font-bold text-secondary-600 dark:text-secondary-400">
                      {compliance.chapters_count || chapters.length}
                    </p>
                    <p className="text-xs text-gray-600 dark:text-gray-400">Chapters</p>
                  </div>
                  <div className="text-center">
                    <p className="text-2xl font-bold text-success-600 dark:text-success-400">
                      {compliance.tags_count || tags.length}
                    </p>
                    <p className="text-xs text-gray-600 dark:text-gray-400">Tags</p>
                  </div>
                </div>
                {compliance.checks && compliance.checks.length > 0 && (
                  <div className="space-y-2 mt-4">
                    {compliance.checks.map((check, idx) => (
                      <div key={idx} className="flex items-start p-3 bg-success-50 dark:bg-success-900/20 rounded-lg border border-success-200 dark:border-success-700">
                        <span className="text-success-600 dark:text-success-400 mr-2">✓</span>
                        <p className="text-sm text-success-800 dark:text-success-300">{check}</p>
                      </div>
                    ))}
                  </div>
                )}
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
              <ClockIcon className="h-4 w-4 mr-1 text-gray-500 dark:text-gray-400" />
              <span className="text-gray-600 dark:text-gray-400">
                {compliance.est_duration_minutes || 0} min
              </span>
            </div>
            <div className="flex items-center">
              <FilmIcon className="h-4 w-4 mr-1 text-gray-500 dark:text-gray-400" />
              <span className="text-gray-600 dark:text-gray-400">
                {chapters.length} chapters
              </span>
            </div>
            <div className="flex items-center">
              <HashtagIcon className="h-4 w-4 mr-1 text-gray-500 dark:text-gray-400" />
              <span className="text-gray-600 dark:text-gray-400">
                {tags.length} tags
              </span>
            </div>
          </div>
          <div className="text-sm text-gray-600 dark:text-gray-400">
            YouTube Long Form • {compliance.has_tracked_link ? 'Tracked Link ✓' : 'No Tracking'}
          </div>
        </div>
      </div>
    </div>
  );
};

export default YouTubeLongFormView;