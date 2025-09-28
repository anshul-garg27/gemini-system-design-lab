import React, { useState } from 'react';
import { 
  PlayIcon,
  HashtagIcon,
  DocumentDuplicateIcon,
  ClockIcon,
  SparklesIcon,
  MusicalNoteIcon,
  SpeakerWaveIcon,
  VideoCameraIcon,
  ChartBarIcon,
  CheckCircleIcon,
  FilmIcon,
  MicrophoneIcon,
  PaintBrushIcon
} from '@heroicons/react/24/outline';
import { Card, CardContent, CardHeader, CardTitle } from './ui/Card';
import { Button } from './ui/Button';
import { cn } from '../lib/utils';

interface Beat {
  label: string;
  time_range: string;
  narration: string;
  on_screen_text: string;
  visuals: string;
  sfx?: string[];
  b_roll?: string[];
}

interface OverlayTextCue {
  time: string;
  text: string;
}

interface BRollPlan {
  time: string;
  ideas: string[];
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

interface YouTubeShortContent {
  title: string;
  beats: Beat[];
  script: string;
  overlay_text_cues: OverlayTextCue[];
  b_roll_plan: BRollPlan[];
  music: {
    vibe: string[];
    bpm_range: string;
    search_terms: string[];
    ducking_notes: string;
  };
  sfx: string[];
  end_screen: {
    cta_line: string;
    elements: string[];
    show_handles: boolean;
  };
  description: {
    text: string;
    word_count: number;
    timestamps: Array<{ time: string; label: string }>;
  };
  tags: string[];
  image_prompts: ImagePrompt[];
  compliance: {
    duration_seconds: number;
    title_char_count: number;
    tags_count: number;
    image_prompt_count: number;
    has_link_in_description: boolean;
    checks: string[];
  };
}

interface YouTubeShortViewProps {
  content: {
    job_id: string;
    platform: string;
    format: string;
    envelope: {
      content: YouTubeShortContent;
    };
    meta?: {
      topic_title?: string;
      primary_keywords?: string[];
      secondary_keywords?: string[];
    };
  };
  onCopy: () => void;
}

const YouTubeShortView: React.FC<YouTubeShortViewProps> = ({ content, onCopy }) => {
  const [activeTab, setActiveTab] = useState<'script' | 'production' | 'metadata'>('script');
  const [expandedBeat, setExpandedBeat] = useState<number | null>(null);
  
  // Extract content
  const short = content.envelope.content;
  const meta = content.meta || {};

  const getBeatColor = (label: string) => {
    switch (label.toLowerCase()) {
      case 'hook': return 'bg-primary-100 dark:bg-primary-900/20 text-primary-800 dark:text-primary-400 border-primary-200 dark:border-primary-700';
      case 'value-1':
      case 'value-2':
      case 'value-3': return 'bg-success-100 dark:bg-success-900/20 text-success-800 dark:text-success-400 border-success-200 dark:border-success-700';
      case 'subscribe': return 'bg-secondary-100 dark:bg-secondary-900/20 text-secondary-800 dark:text-secondary-400 border-secondary-200 dark:border-secondary-700';
      case 'endscreen': return 'bg-warning-100 dark:bg-warning-900/20 text-warning-800 dark:text-warning-400 border-warning-200 dark:border-warning-700';
      default: return 'bg-gray-100 dark:bg-gray-800 text-gray-800 dark:text-gray-300 border-gray-200 dark:border-gray-700';
    }
  };

  return (
    <div className="bg-white dark:bg-gray-900 rounded-3xl shadow-2xl max-w-6xl w-full max-h-[90vh] overflow-hidden flex flex-col">
      {/* Header */}
      <div className="bg-gradient-to-r from-red-500 to-pink-600 text-white p-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="p-3 bg-white/20 backdrop-blur-sm rounded-xl">
              <PlayIcon className="h-8 w-8" />
            </div>
            <div>
              <h2 className="text-2xl font-bold">YouTube Short</h2>
              {meta.topic_title && (
                <p className="text-red-100 text-sm mt-1">{meta.topic_title}</p>
              )}
              <p className="text-red-200 text-xs mt-1">{short.compliance.duration_seconds}s • {short.beats.length} beats</p>
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
            variant={activeTab === 'script' ? 'primary' : 'ghost'}
            onClick={() => setActiveTab('script')}
            className={cn(
              "flex-1",
              activeTab === 'script' && "shadow-sm"
            )}
          >
            <MicrophoneIcon className="h-4 w-4 mr-2" />
            Script & Beats
          </Button>
          <Button
            variant={activeTab === 'production' ? 'primary' : 'ghost'}
            onClick={() => setActiveTab('production')}
            className={cn(
              "flex-1",
              activeTab === 'production' && "shadow-sm"
            )}
          >
            <VideoCameraIcon className="h-4 w-4 mr-2" />
            Production
          </Button>
          <Button
            variant={activeTab === 'metadata' ? 'primary' : 'ghost'}
            onClick={() => setActiveTab('metadata')}
            className={cn(
              "flex-1",
              activeTab === 'metadata' && "shadow-sm"
            )}
          >
            <HashtagIcon className="h-4 w-4 mr-2" />
            Metadata
          </Button>
        </div>
      </div>

      {/* Content Area */}
      <div className="flex-1 overflow-y-auto p-6 bg-gray-50 dark:bg-gray-950">
        {/* Script & Beats Tab */}
        {activeTab === 'script' && (
          <div className="space-y-6 animate-fade-in">
            {/* Title */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <SparklesIcon className="h-5 w-5 mr-2 text-primary-600 dark:text-primary-400" />
                  Title
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-xl font-semibold text-gray-900 dark:text-gray-100">
                  {short.title}
                </p>
                <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
                  {short.compliance.title_char_count} characters
                </p>
              </CardContent>
            </Card>

            {/* Beats Timeline */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <FilmIcon className="h-5 w-5 mr-2 text-secondary-600 dark:text-secondary-400" />
                  Video Beats
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {short.beats.map((beat, index) => (
                  <Card
                    key={index}
                    className={cn(
                      "cursor-pointer hover:shadow-md transition-all",
                      expandedBeat === index && "ring-2 ring-primary-500 dark:ring-primary-400"
                    )}
                    onClick={() => setExpandedBeat(expandedBeat === index ? null : index)}
                  >
                    <CardContent className="p-4">
                      <div className="flex items-center justify-between mb-3">
                        <div className="flex items-center space-x-3">
                          <span className={cn(
                            "px-3 py-1 rounded-full text-xs font-medium border",
                            getBeatColor(beat.label)
                          )}>
                            {beat.label}
                          </span>
                          <span className="text-sm text-gray-600 dark:text-gray-400">
                            <ClockIcon className="h-4 w-4 inline mr-1" />
                            {beat.time_range}
                          </span>
                        </div>
                        <span className="text-lg font-bold text-primary-600 dark:text-primary-400">
                          {beat.on_screen_text}
                        </span>
                      </div>

                      <div className="space-y-3">
                        {/* Narration */}
                        <div>
                          <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Narration</p>
                          <p className="text-gray-700 dark:text-gray-300 bg-gray-50 dark:bg-gray-800 p-3 rounded-lg">
                            {beat.narration}
                          </p>
                        </div>

                        {/* Expanded Details */}
                        {expandedBeat === index && (
                          <div className="space-y-3 animate-fade-in">
                            {/* Visuals */}
                            <div>
                              <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Visuals</p>
                              <p className="text-gray-600 dark:text-gray-400 bg-blue-50 dark:bg-blue-900/20 p-2 rounded border border-blue-200 dark:border-blue-700">
                                {beat.visuals}
                              </p>
                            </div>

                            {/* B-Roll */}
                            {beat.b_roll && beat.b_roll.length > 0 && (
                              <div>
                                <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">B-Roll</p>
                                <div className="flex flex-wrap gap-2">
                                  {beat.b_roll.map((item, idx) => (
                                    <span key={idx} className="px-2 py-1 bg-purple-100 dark:bg-purple-900/20 text-purple-800 dark:text-purple-400 rounded text-sm">
                                      {item}
                                    </span>
                                  ))}
                                </div>
                              </div>
                            )}

                            {/* SFX */}
                            {beat.sfx && beat.sfx.length > 0 && (
                              <div>
                                <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Sound Effects</p>
                                <div className="flex flex-wrap gap-2">
                                  {beat.sfx.map((item, idx) => (
                                    <span key={idx} className="px-2 py-1 bg-orange-100 dark:bg-orange-900/20 text-orange-800 dark:text-orange-400 rounded text-sm">
                                      <SpeakerWaveIcon className="h-3 w-3 inline mr-1" />
                                      {item}
                                    </span>
                                  ))}
                                </div>
                              </div>
                            )}
                          </div>
                        )}
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </CardContent>
            </Card>

            {/* Full Script */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <MicrophoneIcon className="h-5 w-5 mr-2 text-primary-600 dark:text-primary-400" />
                  Full Script
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="bg-gradient-to-r from-gray-50 to-gray-100 dark:from-gray-800 dark:to-gray-900 p-6 rounded-xl">
                  <pre className="text-gray-700 dark:text-gray-300 whitespace-pre-wrap font-mono text-sm leading-relaxed">
                    {short.script}
                  </pre>
                </div>
              </CardContent>
            </Card>
          </div>
        )}

        {/* Production Tab */}
        {activeTab === 'production' && (
          <div className="space-y-6 animate-fade-in">
            {/* Overlay Text Cues */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <SparklesIcon className="h-5 w-5 mr-2 text-secondary-600 dark:text-secondary-400" />
                  Overlay Text Cues
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  {short.overlay_text_cues.map((cue, index) => (
                    <div key={index} className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
                      <span className="text-sm text-gray-600 dark:text-gray-400 font-mono">
                        <ClockIcon className="h-4 w-4 inline mr-1" />
                        {cue.time}
                      </span>
                      <span className="text-lg font-semibold text-gray-900 dark:text-gray-100">
                        {cue.text}
                      </span>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* B-Roll Plan */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <VideoCameraIcon className="h-5 w-5 mr-2 text-primary-600 dark:text-primary-400" />
                  B-Roll Plan
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                {short.b_roll_plan.map((plan, index) => (
                  <Card key={index} variant="filled">
                    <CardContent className="p-4">
                      <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                        <ClockIcon className="h-4 w-4 inline mr-1" />
                        {plan.time}
                      </p>
                      <div className="flex flex-wrap gap-2">
                        {plan.ideas.map((idea, idx) => (
                          <span key={idx} className="px-3 py-1 bg-purple-100 dark:bg-purple-900/20 text-purple-800 dark:text-purple-400 rounded-full text-sm">
                            {idea}
                          </span>
                        ))}
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </CardContent>
            </Card>

            {/* Music & SFX */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <MusicalNoteIcon className="h-5 w-5 mr-2 text-success-600 dark:text-success-400" />
                    Music
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div>
                    <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Vibe</p>
                    <div className="flex flex-wrap gap-2">
                      {short.music.vibe.map((vibe, idx) => (
                        <span key={idx} className="px-3 py-1 bg-green-100 dark:bg-green-900/20 text-green-800 dark:text-green-400 rounded-full text-sm">
                          {vibe}
                        </span>
                      ))}
                    </div>
                  </div>
                  <div>
                    <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">BPM Range</p>
                    <p className="text-lg font-semibold text-gray-900 dark:text-gray-100">{short.music.bpm_range}</p>
                  </div>
                  <div>
                    <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Search Terms</p>
                    <div className="space-y-1">
                      {short.music.search_terms.map((term, idx) => (
                        <p key={idx} className="text-sm text-gray-600 dark:text-gray-400">• {term}</p>
                      ))}
                    </div>
                  </div>
                  <div className="bg-yellow-50 dark:bg-yellow-900/20 p-3 rounded-lg border border-yellow-200 dark:border-yellow-700">
                    <p className="text-sm text-yellow-800 dark:text-yellow-400">{short.music.ducking_notes}</p>
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <SpeakerWaveIcon className="h-5 w-5 mr-2 text-warning-600 dark:text-warning-400" />
                    Sound Effects
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="flex flex-wrap gap-2">
                    {short.sfx.map((effect, idx) => (
                      <span key={idx} className="px-3 py-1 bg-orange-100 dark:bg-orange-900/20 text-orange-800 dark:text-orange-400 rounded-full text-sm font-medium">
                        {effect}
                      </span>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* End Screen */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <VideoCameraIcon className="h-5 w-5 mr-2 text-secondary-600 dark:text-secondary-400" />
                  End Screen
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">CTA Line</p>
                  <p className="text-gray-700 dark:text-gray-300 bg-gradient-to-r from-secondary-50 to-pink-50 dark:from-secondary-900/20 dark:to-pink-900/20 p-4 rounded-lg border border-secondary-200 dark:border-secondary-700">
                    {short.end_screen.cta_line}
                  </p>
                </div>
                <div>
                  <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Elements</p>
                  <div className="flex flex-wrap gap-2">
                    {short.end_screen.elements.map((element, idx) => (
                      <span key={idx} className="px-3 py-1 bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 rounded-full text-sm">
                        {element}
                      </span>
                    ))}
                  </div>
                </div>
                {short.end_screen.show_handles && (
                  <div className="bg-blue-50 dark:bg-blue-900/20 p-3 rounded-lg border border-blue-200 dark:border-blue-700">
                    <p className="text-sm text-blue-800 dark:text-blue-400">✓ Show social handles</p>
                  </div>
                )}
              </CardContent>
            </Card>

            {/* Image Prompts */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <PaintBrushIcon className="h-5 w-5 mr-2 text-primary-600 dark:text-primary-400" />
                  Cover Images
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {short.image_prompts.map((imagePrompt, index) => (
                  <Card key={index} variant="filled">
                    <CardContent className="p-4 space-y-3">
                      <div className="flex items-center justify-between">
                        <h4 className="font-medium text-gray-900 dark:text-gray-100">{imagePrompt.title}</h4>
                        <span className="px-2 py-1 bg-primary-100 dark:bg-primary-900/20 text-primary-800 dark:text-primary-400 rounded text-xs font-medium">
                          {imagePrompt.role}
                        </span>
                      </div>
                      
                      <div>
                        <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Prompt</p>
                        <p className="text-sm text-gray-600 dark:text-gray-400 bg-gray-50 dark:bg-gray-800 p-3 rounded">{imagePrompt.prompt}</p>
                      </div>
                      
                      <div className="grid grid-cols-2 gap-2">
                        <div>
                          <p className="text-xs font-medium text-gray-600 dark:text-gray-400">Dimensions</p>
                          <p className="text-sm font-semibold text-gray-900 dark:text-gray-100">{imagePrompt.size_px}</p>
                        </div>
                        <div>
                          <p className="text-xs font-medium text-gray-600 dark:text-gray-400">Ratio</p>
                          <p className="text-sm font-semibold text-gray-900 dark:text-gray-100">{imagePrompt.ratio}</p>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </CardContent>
            </Card>
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
                    <SparklesIcon className="h-5 w-5 mr-2 text-primary-600 dark:text-primary-400" />
                    Description
                  </span>
                  <span className="text-sm text-gray-500 dark:text-gray-400">
                    {short.description.word_count} words
                  </span>
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="bg-white dark:bg-gray-800 p-4 rounded-xl border border-gray-200 dark:border-gray-700">
                  <p className="text-gray-700 dark:text-gray-300 whitespace-pre-wrap">{short.description.text}</p>
                </div>
                
                {/* Timestamps */}
                <div>
                  <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Timestamps</p>
                  <div className="space-y-1">
                    {short.description.timestamps.map((timestamp, idx) => (
                      <div key={idx} className="flex items-center space-x-2 text-sm">
                        <span className="font-mono text-primary-600 dark:text-primary-400">{timestamp.time}</span>
                        <span className="text-gray-600 dark:text-gray-400">-</span>
                        <span className="text-gray-700 dark:text-gray-300">{timestamp.label}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Tags */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center justify-between">
                  <span className="flex items-center">
                    <HashtagIcon className="h-5 w-5 mr-2 text-secondary-600 dark:text-secondary-400" />
                    Tags ({short.tags.length})
                  </span>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => navigator.clipboard.writeText(short.tags.join(', '))}
                    leftIcon={<DocumentDuplicateIcon className="h-4 w-4" />}
                  >
                    Copy All
                  </Button>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex flex-wrap gap-2">
                  {short.tags.map((tag, idx) => (
                    <span key={idx} className="px-3 py-1 bg-secondary-100 dark:bg-secondary-900/20 text-secondary-800 dark:text-secondary-400 rounded-full text-sm font-medium border border-secondary-200 dark:border-secondary-700">
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
                  <CheckCircleIcon className="h-5 w-5 mr-2 text-success-600 dark:text-success-400" />
                  Compliance Checks
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
                  <Card variant="filled">
                    <CardContent className="p-3 text-center">
                      <p className="text-2xl font-bold text-primary-600 dark:text-primary-400">{short.compliance.duration_seconds}s</p>
                      <p className="text-xs text-gray-600 dark:text-gray-400">Duration</p>
                    </CardContent>
                  </Card>
                  <Card variant="filled">
                    <CardContent className="p-3 text-center">
                      <p className="text-2xl font-bold text-secondary-600 dark:text-secondary-400">{short.compliance.title_char_count}</p>
                      <p className="text-xs text-gray-600 dark:text-gray-400">Title Chars</p>
                    </CardContent>
                  </Card>
                  <Card variant="filled">
                    <CardContent className="p-3 text-center">
                      <p className="text-2xl font-bold text-success-600 dark:text-success-400">{short.compliance.tags_count}</p>
                      <p className="text-xs text-gray-600 dark:text-gray-400">Tags</p>
                    </CardContent>
                  </Card>
                  <Card variant="filled">
                    <CardContent className="p-3 text-center">
                      <p className="text-2xl font-bold text-warning-600 dark:text-warning-400">
                        {short.compliance.has_link_in_description ? '✓' : '✗'}
                      </p>
                      <p className="text-xs text-gray-600 dark:text-gray-400">Has Link</p>
                    </CardContent>
                  </Card>
                </div>

                <div className="space-y-2">
                  {short.compliance.checks.map((check, idx) => (
                    <div key={idx} className="flex items-center p-3 bg-success-50 dark:bg-success-900/20 rounded-lg border border-success-200 dark:border-success-700">
                      <CheckCircleIcon className="h-4 w-4 text-success-600 dark:text-success-400 mr-2 flex-shrink-0" />
                      <span className="text-sm text-success-800 dark:text-success-300">{check}</span>
                    </div>
                  ))}
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
              <ClockIcon className="h-4 w-4 mr-1 text-gray-500 dark:text-gray-400" />
              <span className="text-gray-600 dark:text-gray-400">
                {short.compliance.duration_seconds}s video
              </span>
            </div>
            <div className="flex items-center">
              <FilmIcon className="h-4 w-4 mr-1 text-gray-500 dark:text-gray-400" />
              <span className="text-gray-600 dark:text-gray-400">
                {short.beats.length} beats
              </span>
            </div>
            <div className="flex items-center">
              <ChartBarIcon className="h-4 w-4 mr-1 text-gray-500 dark:text-gray-400" />
              <span className="text-gray-600 dark:text-gray-400">
                {short.description.word_count} word description
              </span>
            </div>
          </div>
          <div className="flex items-center text-success-600 dark:text-success-400">
            <CheckCircleIcon className="h-4 w-4 mr-1" />
            <span className="text-sm font-medium">
              {short.compliance.checks.length} checks passed
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default YouTubeShortView;
