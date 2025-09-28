import React, { useState } from 'react';
import { 
  PlayIcon, 
  LinkIcon, 
  HashtagIcon,
  ClockIcon,
  EyeIcon,
  DocumentDuplicateIcon,
  SparklesIcon,
  CameraIcon,
  CheckCircleIcon,
  ExclamationTriangleIcon,
  PaintBrushIcon
} from '@heroicons/react/24/outline';
import { Card, CardContent, CardHeader, CardTitle } from './ui/Card';
import { Button } from './ui/Button';
import { cn } from '../lib/utils';

interface StoryFrame {
  index: number;
  role: string;
  copy: string;
  sticker_ideas: string[];
  overlay_notes: string;
  layout: string;
  alt_text: string;
  duration_seconds: number;
}

interface StoryStickers {
  global: string[];
  link_strategy: {
    enabled: boolean;
    link_url: string;
    link_text: string;
    placement_hint: string;
  };
  time_sensitive_angle: string;
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

interface InstagramStoryContent {
  frames: StoryFrame[];
  stickers: StoryStickers;
  image_prompts: ImagePrompt[];
  overlay_hashtags: string[];
  compliance: {
    frames_total: number;
    has_link: boolean;
    checks: string[];
  };
}

interface InstagramStoryViewProps {
  content: {
    job_id: string;
    platform: string;
    format: string;
    envelope: {
      content: InstagramStoryContent;
    };
  };
  onCopy: () => void;
}

const InstagramStoryView: React.FC<InstagramStoryViewProps> = ({ content, onCopy }) => {
  // Normalize envelope.content which may be either {frames,...} or {meta, content:{frames,...}}
  const rawContent: any = content.envelope.content as any;
  const story: any = rawContent && rawContent.frames
    ? rawContent
    : rawContent && rawContent.content
      ? rawContent.content
      : null;

  // Add safety checks for required properties
  if (!story || !story.frames || !Array.isArray(story.frames)) {
    return (
      <Card className="max-w-4xl w-full">
        <CardContent className="p-6">
          <div className="text-center text-error-600 dark:text-error-400">
            <ExclamationTriangleIcon className="h-12 w-12 mx-auto mb-4" />
            <h2 className="text-xl font-bold mb-2">Error Loading Story Content</h2>
            <p className="text-gray-600 dark:text-gray-400">The story content is missing or malformed.</p>
          </div>
        </CardContent>
      </Card>
    );
  }

  const [selectedFrame, setSelectedFrame] = useState<number | null>(null);
  
  const getRoleColor = (role: string) => {
    switch (role) {
      case 'hook': return 'bg-error-100 dark:bg-error-900/20 text-error-800 dark:text-error-400 border-error-200 dark:border-error-700';
      case 'micro_insight': return 'bg-primary-100 dark:bg-primary-900/20 text-primary-800 dark:text-primary-400 border-primary-200 dark:border-primary-700';
      case 'cta': return 'bg-success-100 dark:bg-success-900/20 text-success-800 dark:text-success-400 border-success-200 dark:border-success-700';
      default: return 'bg-gray-100 dark:bg-gray-800 text-gray-800 dark:text-gray-300 border-gray-200 dark:border-gray-700';
    }
  };

  const getRoleIcon = (role: string) => {
    switch (role) {
      case 'hook': return <PlayIcon className="h-4 w-4" />;
      case 'micro_insight': return <EyeIcon className="h-4 w-4" />;
      case 'cta': return <LinkIcon className="h-4 w-4" />;
      default: return <DocumentDuplicateIcon className="h-4 w-4" />;
    }
  };

  return (
    <div className="bg-white dark:bg-gray-900 rounded-3xl shadow-2xl max-w-6xl w-full max-h-[90vh] overflow-hidden flex flex-col">
      {/* Header */}
      <div className="bg-gradient-to-r from-primary-500 to-secondary-500 text-white p-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="p-3 bg-white/20 backdrop-blur-sm rounded-xl">
              <PlayIcon className="h-8 w-8" />
            </div>
            <div>
              <h2 className="text-2xl font-bold">Instagram Story</h2>
              <p className="text-primary-100 text-sm">
                {story.frames.length} frames • {story.frames.reduce((acc: number, frame: any) => acc + (frame.duration_seconds || 0), 0)}s total duration
              </p>
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

      <div className="flex-1 overflow-y-auto p-6 bg-gray-50 dark:bg-gray-950">
        {/* Story Frames */}
        <div className="space-y-8">
          <Card className="animate-fade-in-up">
            <CardHeader>
              <CardTitle className="flex items-center">
                <PlayIcon className="h-5 w-5 mr-2 text-primary-600 dark:text-primary-400" />
                Story Frames
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {story.frames.map((frame: any, index: number) => (
                  <Card 
                    key={index} 
                    className={cn(
                      "hover:shadow-lg transition-all duration-300 cursor-pointer",
                      selectedFrame === index && "ring-2 ring-primary-500 dark:ring-primary-400"
                    )}
                    onClick={() => setSelectedFrame(selectedFrame === index ? null : index)}
                  >
                    <CardContent className="p-4">
                      {/* Frame Header */}
                      <div className="flex items-center justify-between mb-3">
                        <div className="flex items-center space-x-2">
                          <span className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-medium border ${getRoleColor(frame.role)}`}>
                            {getRoleIcon(frame.role)}
                            <span className="ml-1 capitalize">{frame.role}</span>
                          </span>
                          <span className="text-xs text-gray-500 dark:text-gray-400 font-medium">Frame {frame.index}</span>
                        </div>
                        <div className="flex items-center text-xs text-gray-500 dark:text-gray-400">
                          <ClockIcon className="h-3 w-3 mr-1" />
                          {frame.duration_seconds}s
                        </div>
                      </div>

                      {/* Frame Content */}
                      <div className="space-y-3">
                        <div>
                          <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Copy:</p>
                          <div className="bg-gradient-to-r from-primary-50 to-secondary-50 dark:from-primary-900/20 dark:to-secondary-900/20 p-3 rounded-lg border border-primary-200 dark:border-primary-700">
                            <p className="text-sm text-gray-900 dark:text-gray-100 font-medium leading-relaxed">{frame.copy}</p>
                          </div>
                        </div>

                        {/* Sticker Ideas */}
                        {Array.isArray(frame.sticker_ideas) && frame.sticker_ideas.length > 0 && (
                          <div className={cn("transition-all duration-300", selectedFrame === index ? "opacity-100" : "opacity-80")}>
                            <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2 flex items-center">
                              <SparklesIcon className="h-4 w-4 mr-1 text-secondary-600 dark:text-secondary-400" />
                              Sticker Ideas:
                            </p>
                            <div className="space-y-1">
                              {frame.sticker_ideas.map((sticker: string, idx: number) => (
                                <div key={idx} className="bg-secondary-50 dark:bg-secondary-900/20 border border-secondary-200 dark:border-secondary-700 rounded-lg p-2">
                                  <p className="text-xs text-secondary-800 dark:text-secondary-400">{sticker}</p>
                                </div>
                              ))}
                            </div>
                          </div>
                        )}

                        {/* Layout & Overlay Notes */}
                        <div className="grid grid-cols-2 gap-2 text-xs">
                          <div>
                            <p className="font-medium text-gray-700 dark:text-gray-300 mb-1">Layout:</p>
                            <p className="text-gray-600 dark:text-gray-400 bg-gray-50 dark:bg-gray-800 p-2 rounded border border-gray-200 dark:border-gray-700">{frame.layout}</p>
                          </div>
                          <div>
                            <p className="font-medium text-gray-700 dark:text-gray-300 mb-1">Overlay:</p>
                            <p className="text-gray-600 dark:text-gray-400 bg-gray-50 dark:bg-gray-800 p-2 rounded border border-gray-200 dark:border-gray-700">{frame.overlay_notes}</p>
                          </div>
                        </div>

                        {/* Alt Text */}
                        {selectedFrame === index && (
                          <div className="animate-fade-in">
                            <p className="text-xs font-medium text-gray-700 dark:text-gray-300 mb-1">Alt Text:</p>
                            <p className="text-xs text-gray-600 dark:text-gray-400 bg-gray-50 dark:bg-gray-800 p-2 rounded italic border border-gray-200 dark:border-gray-700">{frame.alt_text}</p>
                          </div>
                        )}
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Stickers & Interactive Elements */}
          <Card className="animate-fade-in-up animation-delay-100">
            <CardHeader>
              <CardTitle className="flex items-center">
                <HashtagIcon className="h-5 w-5 mr-2 text-secondary-600 dark:text-secondary-400" />
                Interactive Elements
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* Global Stickers */}
                <Card variant="filled">
                  <CardContent className="p-4">
                    <h4 className="font-medium text-gray-900 dark:text-gray-100 mb-3">Global Sticker Guidelines</h4>
                    <div className="space-y-2">
                      {(story.stickers?.global || []).map((guideline: string, index: number) => (
                        <div key={index} className="bg-primary-50 dark:bg-primary-900/20 border border-primary-200 dark:border-primary-700 rounded-lg p-3">
                          <p className="text-sm text-primary-800 dark:text-primary-400">{guideline}</p>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>

                {/* Link Strategy */}
                {story.stickers?.link_strategy?.enabled && (
                  <Card variant="filled">
                    <CardContent className="p-4">
                      <h4 className="font-medium text-gray-900 dark:text-gray-100 mb-3 flex items-center">
                        <LinkIcon className="h-4 w-4 mr-2 text-primary-600 dark:text-primary-400" />
                        Link Strategy
                      </h4>
                      <div className="space-y-3">
                        <div>
                          <p className="text-sm font-medium text-gray-700 dark:text-gray-300">Link URL:</p>
                          <div className="bg-gray-50 dark:bg-gray-800 p-2 rounded mt-1 border border-gray-200 dark:border-gray-700">
                            <p className="text-sm text-primary-600 dark:text-primary-400 break-all font-mono">{story.stickers?.link_strategy?.link_url}</p>
                          </div>
                        </div>
                        <div>
                          <p className="text-sm font-medium text-gray-700 dark:text-gray-300">Link Text:</p>
                          <p className="text-sm text-gray-600 dark:text-gray-400 bg-gray-50 dark:bg-gray-800 p-2 rounded mt-1 border border-gray-200 dark:border-gray-700">{story.stickers?.link_strategy?.link_text}</p>
                        </div>
                        <div>
                          <p className="text-sm font-medium text-gray-700 dark:text-gray-300">Placement:</p>
                          <p className="text-sm text-gray-600 dark:text-gray-400 bg-gray-50 dark:bg-gray-800 p-2 rounded mt-1 border border-gray-200 dark:border-gray-700">{story.stickers?.link_strategy?.placement_hint}</p>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                )}
              </div>

              {/* Time Sensitive Angle */}
              {story.stickers?.time_sensitive_angle && (
                <Card className="mt-4 bg-gradient-to-r from-warning-50 to-orange-50 dark:from-warning-900/20 dark:to-orange-900/20 border-warning-200 dark:border-warning-700">
                  <CardContent className="p-4">
                    <h4 className="font-medium text-warning-900 dark:text-warning-400 mb-2 flex items-center">
                      <ClockIcon className="h-4 w-4 mr-2" />
                      Time Sensitive Angle
                    </h4>
                    <p className="text-sm text-warning-800 dark:text-warning-300">{story.stickers?.time_sensitive_angle}</p>
                  </CardContent>
                </Card>
              )}
            </CardContent>
          </Card>

          {/* Overlay Hashtags */}
          {(story.overlay_hashtags && story.overlay_hashtags.length > 0) && (
            <Card className="animate-fade-in-up animation-delay-200">
              <CardHeader>
                <CardTitle className="flex items-center">
                  <HashtagIcon className="h-5 w-5 mr-2 text-primary-600 dark:text-primary-400" />
                  Overlay Hashtags
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex flex-wrap gap-2">
                  {story.overlay_hashtags.map((hashtag: string, index: number) => (
                    <span key={index} className="px-3 py-1 bg-primary-100 dark:bg-primary-900/20 text-primary-800 dark:text-primary-400 rounded-full text-sm font-medium border border-primary-200 dark:border-primary-700">
                      {hashtag}
                    </span>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}

          {/* Image Prompts */}
          <Card className="animate-fade-in-up animation-delay-300">
            <CardHeader>
              <CardTitle className="flex items-center">
                <CameraIcon className="h-5 w-5 mr-2 text-success-600 dark:text-success-400" />
                Visual Assets ({(story.image_prompts?.length || 0)})
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {(story.image_prompts || []).map((imagePrompt: any, index: number) => (
                  <Card key={index} variant="filled" className="hover:shadow-md transition-shadow">
                    <CardContent className="p-4">
                      <div className="flex items-center justify-between mb-3">
                        <h4 className="font-medium text-gray-900 dark:text-gray-100 flex items-center">
                          <PaintBrushIcon className="h-4 w-4 mr-2 text-success-600 dark:text-success-400" />
                          {imagePrompt.title}
                        </h4>
                        <span className="px-2 py-1 bg-success-100 dark:bg-success-900/20 text-success-800 dark:text-success-400 rounded text-xs font-medium">
                          {imagePrompt.role}
                        </span>
                      </div>
                  
                      <div className="space-y-3">
                        <div>
                          <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Prompt:</p>
                          <p className="text-sm text-gray-600 dark:text-gray-400 bg-gray-50 dark:bg-gray-800 p-3 rounded border border-gray-200 dark:border-gray-700">{imagePrompt.prompt}</p>
                        </div>
                        
                        <div>
                          <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Negative Prompt:</p>
                          <p className="text-sm text-error-600 dark:text-error-400 bg-error-50 dark:bg-error-900/20 p-3 rounded border border-error-200 dark:border-error-700">{imagePrompt.negative_prompt}</p>
                        </div>
                    
                        <div className="grid grid-cols-2 gap-2 text-xs">
                          <div>
                            <p className="font-medium text-gray-700 dark:text-gray-300 mb-1">Dimensions:</p>
                            <p className="text-gray-600 dark:text-gray-400 bg-gray-50 dark:bg-gray-800 p-2 rounded border border-gray-200 dark:border-gray-700">{imagePrompt.size_px}</p>
                          </div>
                          <div>
                            <p className="font-medium text-gray-700 dark:text-gray-300 mb-1">Ratio:</p>
                            <p className="text-gray-600 dark:text-gray-400 bg-gray-50 dark:bg-gray-800 p-2 rounded border border-gray-200 dark:border-gray-700">{imagePrompt.ratio}</p>
                          </div>
                        </div>
                        
                        <div>
                          <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Style Notes:</p>
                          <p className="text-sm text-gray-600 dark:text-gray-400 bg-warning-50 dark:bg-warning-900/20 p-2 rounded border border-warning-200 dark:border-warning-700">{imagePrompt.style_notes}</p>
                        </div>
                        
                        <div>
                          <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Alt Text:</p>
                          <p className="text-sm text-gray-600 dark:text-gray-400 bg-gray-50 dark:bg-gray-800 p-2 rounded italic border border-gray-200 dark:border-gray-700">{imagePrompt.alt_text}</p>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Compliance Information */}
          <Card className="animate-fade-in-up animation-delay-400">
            <CardHeader>
              <CardTitle className="flex items-center">
                <CheckCircleIcon className="h-5 w-5 mr-2 text-success-600 dark:text-success-400" />
                Compliance & Checks
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="bg-gray-50 dark:bg-gray-800/50 rounded-xl p-6 border border-gray-200 dark:border-gray-700">
                <div className="grid grid-cols-2 md:grid-cols-3 gap-4 mb-6">
                  <div className="text-center">
                    <p className="text-3xl font-bold text-success-600 dark:text-success-400">{story.compliance?.frames_total ?? story.frames.length}</p>
                    <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">Total Frames</p>
                  </div>
                  <div className="text-center">
                    <p className="text-3xl font-bold text-primary-600 dark:text-primary-400">
                      {story.frames.reduce((acc: number, frame: any) => acc + (frame.duration_seconds || 0), 0)}s
                    </p>
                    <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">Total Duration</p>
                  </div>
                  <div className="text-center">
                    <p className="text-3xl font-bold">
                      {story.compliance?.has_link ? (
                        <CheckCircleIcon className="h-8 w-8 inline text-success-600 dark:text-success-400" />
                      ) : (
                        <ExclamationTriangleIcon className="h-8 w-8 inline text-warning-600 dark:text-warning-400" />
                      )}
                    </p>
                    <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">Has Link</p>
                  </div>
                </div>
                
                {(story.compliance?.checks && story.compliance.checks.length > 0) && (
                  <div>
                    <p className="font-medium text-gray-700 dark:text-gray-300 mb-3">Compliance Checks:</p>
                    <div className="space-y-2">
                      {story.compliance.checks.map((check: string, index: number) => (
                        <div key={index} className="flex items-center text-sm bg-success-50 dark:bg-success-900/20 border border-success-200 dark:border-success-700 rounded-lg p-2">
                          <CheckCircleIcon className="h-4 w-4 text-success-600 dark:text-success-400 mr-2 flex-shrink-0" />
                          <span className="text-success-800 dark:text-success-300">{check}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default InstagramStoryView;
