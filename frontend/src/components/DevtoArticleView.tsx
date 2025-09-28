import React, { useMemo, useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import {
  BookOpenIcon,
  ClockIcon,
  HashtagIcon,
  DocumentDuplicateIcon,
  LinkIcon,
  CodeBracketIcon,
  ChartBarIcon,
  PhotoIcon,
  MagnifyingGlassIcon,
  ArrowTopRightOnSquareIcon,
  QueueListIcon,
  BeakerIcon,
  SparklesIcon,
  CheckCircleIcon
} from '@heroicons/react/24/outline';
import { Card, CardContent, CardHeader, CardTitle } from './ui/Card';
import { Button } from './ui/Button';
import { cn } from '../lib/utils';

interface DevtoFrontMatter {
  title?: string;
  published?: boolean;
  tags?: string[];
  cover_image?: string;
  canonical_url?: string;
  description?: string;
}

interface DevtoCodeSnippet {
  language?: string;
  label?: string;
  content: string;
  runnable?: boolean;
}

interface DevtoDiagramBlock {
  id?: string;
  type?: string;
  alt?: string;
  content?: string;
  placement_hint?: string;
}

interface DevtoImagePrompt {
  role?: string;
  title?: string;
  prompt: string;
  negative_prompt?: string;
  style_notes?: string;
  ratio?: string;
  ratio_px?: {
    ratio?: string;
    size_px?: string;
  };
  size_px?: string;
}

interface DevtoResource {
  title?: string;
  url?: string;
  note?: string;
}

interface DevtoCompliance {
  word_count?: number;
  reading_time_min?: number;
  code_snippets_count?: number;
  diagram_blocks_count?: number;
  resources_count?: number;
  has_front_matter?: boolean;
  has_seo?: boolean;
  checks?: string[];
}

interface DevtoSEO {
  meta_description?: string;
  canonical_url?: string;
  tags?: string[];
  published?: boolean;
}

interface DevtoImagePlan {
  roles?: string[];
  ratios_px?: {
    ratio: string;
    size_px: string;
  }[];
}

interface DevtoArticle {
  front_matter?: DevtoFrontMatter;
  markdown?: string;
  reading_time_min?: number;
  code_snippets?: DevtoCodeSnippet[];
  diagram_blocks?: DevtoDiagramBlock[];
  resources?: DevtoResource[];
  image_prompts?: DevtoImagePrompt[];
  compliance?: DevtoCompliance;
  seo?: DevtoSEO;
  image_plan?: DevtoImagePlan;
}

interface DevtoMeta {
  topic_title?: string;
  topic_id?: string;
  canonical?: string;
  primary_keywords?: string[];
  secondary_keywords?: string[];
  lsi_terms?: string[];
}

interface DevtoEnvelope {
  content: DevtoArticle;
}

interface DevtoArticleViewProps {
  content: {
    envelope: DevtoEnvelope;
    meta?: DevtoMeta;
  };
  onCopy: () => void;
}

const DevtoArticleView: React.FC<DevtoArticleViewProps> = ({ content, onCopy }) => {
  const [activeTab, setActiveTab] = useState<'content' | 'structure' | 'assets' | 'seo'>('content');
  const [showRawMarkdown, setShowRawMarkdown] = useState(false);
  const envelope = content.envelope || { content: {} as DevtoArticle };
  const article = envelope.content || ({} as DevtoArticle);
  const meta = content.meta || {};
  const frontMatter = article.front_matter || {};
  const markdown = article.markdown || '';
  const readingTime = article.reading_time_min || 0;
  const codeSnippets = article.code_snippets || [];
  const diagramBlocks = article.diagram_blocks || [];
  const resources = article.resources || [];
  const seo = article.seo || {};
  const imagePrompts = article.image_prompts || [];
  const compliance = article.compliance || {};

  const copyToClipboard = (value: string) => {
    if (!value) return;
    navigator.clipboard.writeText(value);
  };

  const formattedResources = useMemo(() => {
    return resources.map((resource: DevtoResource) => ({
      title: resource.title || 'Untitled Resource',
      url: resource.url || '',
      note: resource.note || ''
    }));
  }, [resources]);

  const renderDiagram = (diagram: DevtoDiagramBlock, index: number) => {
    const content = diagram.content || '';
    if (!content.includes('```mermaid')) {
      return (
        <div className="relative bg-gray-900 text-gray-100 rounded-xl p-4 border border-gray-800">
          <div className="absolute top-3 right-3 text-xs uppercase tracking-wide text-gray-400 flex items-center space-x-1">
            <SparklesIcon className="h-4 w-4" />
            <span>Diagram</span>
          </div>
          <pre className="whitespace-pre-wrap text-sm font-mono leading-relaxed">{content}</pre>
        </div>
      );
    }
    const cleaned = content
      .replace(/```mermaid\n?/gi, '')
      .replace(/```$/gm, '')
      .trim();

    return (
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <span className="text-sm font-medium text-gray-600 dark:text-gray-300 flex items-center">
            <QueueListIcon className="h-4 w-4 mr-2" />
            Mermaid Diagram
          </span>
          <Button
            variant="ghost"
            size="sm"
            onClick={() => copyToClipboard(cleaned)}
            leftIcon={<DocumentDuplicateIcon className="h-4 w-4" />}
          >
            Copy Diagram
          </Button>
        </div>
        <pre className="bg-gray-900 text-gray-100 rounded-xl p-4 border border-gray-800 overflow-x-auto text-sm leading-relaxed">
          <code>{cleaned}</code>
        </pre>
      </div>
    );
  };

  return (
    <div className="bg-white dark:bg-gray-900 rounded-3xl shadow-2xl max-w-6xl w-full max-h-[90vh] overflow-hidden flex flex-col">
      {/* Header */}
      <div className="bg-gradient-to-r from-gray-900 via-gray-800 to-gray-900 text-white p-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="p-3 bg-white/10 backdrop-blur-sm rounded-xl">
              <BookOpenIcon className="h-8 w-8" />
            </div>
            <div>
              <h2 className="text-2xl font-bold">Dev.to Article</h2>
              {meta.topic_title && (
                <p className="text-gray-200 text-sm mt-1">{meta.topic_title}</p>
              )}
              <p className="text-gray-300 text-xs mt-1">
                {readingTime} min read • {codeSnippets.length} code snippets
              </p>
            </div>
          </div>
          <div className="flex items-center space-x-3">
            {frontMatter?.canonical_url && (
              <Button
                asChild
                variant="ghost"
                className="bg-white/10 hover:bg-white/20 text-white border-white/30"
              >
                <a href={frontMatter.canonical_url} target="_blank" rel="noopener noreferrer" className="flex items-center">
                  <LinkIcon className="h-4 w-4 mr-2" />
                  View Canonical
                </a>
              </Button>
            )}
            <Button
              onClick={onCopy}
              variant="ghost"
              className="bg-white/10 hover:bg-white/20 text-white border-white/30"
              leftIcon={<DocumentDuplicateIcon className="h-4 w-4" />}
            >
              Copy All
            </Button>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="border-b border-gray-200 dark:border-gray-800 bg-gray-50 dark:bg-gray-950">
        <div className="flex space-x-1 p-2">
          <Button
            variant={activeTab === 'content' ? 'primary' : 'ghost'}
            onClick={() => setActiveTab('content')}
            className={cn('flex-1', activeTab === 'content' && 'shadow-sm')}
          >
            <BookOpenIcon className="h-4 w-4 mr-2" />
            Content
          </Button>
          <Button
            variant={activeTab === 'structure' ? 'primary' : 'ghost'}
            onClick={() => setActiveTab('structure')}
            className={cn('flex-1', activeTab === 'structure' && 'shadow-sm')}
          >
            <QueueListIcon className="h-4 w-4 mr-2" />
            Structure
          </Button>
          <Button
            variant={activeTab === 'assets' ? 'primary' : 'ghost'}
            onClick={() => setActiveTab('assets')}
            className={cn('flex-1', activeTab === 'assets' && 'shadow-sm')}
          >
            <PhotoIcon className="h-4 w-4 mr-2" />
            Assets
          </Button>
          <Button
            variant={activeTab === 'seo' ? 'primary' : 'ghost'}
            onClick={() => setActiveTab('seo')}
            className={cn('flex-1', activeTab === 'seo' && 'shadow-sm')}
          >
            <MagnifyingGlassIcon className="h-4 w-4 mr-2" />
            SEO & Compliance
          </Button>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto p-6 bg-gray-50 dark:bg-gray-950">
        {/* Content Tab */}
        {activeTab === 'content' && (
          <div className="space-y-6 animate-fade-in">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center justify-between">
                  <span className="flex items-center">
                    <BookOpenIcon className="h-5 w-5 mr-2 text-primary-600 dark:text-primary-400" />
                    Front Matter
                  </span>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => copyToClipboard(JSON.stringify(frontMatter, null, 2))}
                    leftIcon={<DocumentDuplicateIcon className="h-4 w-4" />}
                  >
                    Copy Front Matter
                  </Button>
                </CardTitle>
              </CardHeader>
              <CardContent className="grid md:grid-cols-2 gap-4">
                <div>
                  <p className="text-sm font-medium text-gray-600 dark:text-gray-300">Title</p>
                  <h1 className="text-xl font-bold text-gray-900 dark:text-gray-100 mt-1">
                    {frontMatter.title || 'Untitled'}
                  </h1>
                </div>
                <div className="space-y-2">
                  <div className="flex items-center text-sm text-gray-600 dark:text-gray-400">
                    <ClockIcon className="h-4 w-4 mr-2" />
                    {readingTime} min read
                  </div>
                  <div className="flex items-center text-sm text-gray-600 dark:text-gray-400">
                    <HashtagIcon className="h-4 w-4 mr-2" />
                    {Array.isArray(frontMatter.tags) ? frontMatter.tags.length : 0} tags
                  </div>
                  <div className="flex items-center text-sm text-gray-600 dark:text-gray-400">
                    <CheckCircleIcon className="h-4 w-4 mr-2" />
                    {frontMatter.published ? 'Published' : 'Draft'}
                  </div>
                </div>
                {frontMatter.cover_image && (
                  <div className="col-span-full">
                    <div className="relative rounded-xl overflow-hidden border border-gray-200 dark:border-gray-800">
                      <img
                        src={frontMatter.cover_image}
                        alt={frontMatter.title || 'Cover image'}
                        className="w-full h-48 object-cover"
                      />
                      <Button
                        variant="ghost"
                        size="sm"
                        className="absolute top-3 right-3 bg-white/80 hover:bg-white"
                        onClick={() => copyToClipboard(frontMatter.cover_image)}
                        leftIcon={<DocumentDuplicateIcon className="h-4 w-4" />}
                      >
                        Copy URL
                      </Button>
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="flex items-center justify-between">
                  <span className="flex items-center">
                    <DocumentDuplicateIcon className="h-5 w-5 mr-2 text-secondary-600 dark:text-secondary-400" />
                    Article Markdown
                  </span>
                  <div className="flex items-center space-x-2">
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => copyToClipboard(markdown)}
                      leftIcon={<DocumentDuplicateIcon className="h-4 w-4" />}
                    >
                      Copy Markdown
                    </Button>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => setShowRawMarkdown(prev => !prev)}
                    >
                      {showRawMarkdown ? 'Hide Raw' : 'Show Raw'}
                    </Button>
                  </div>
                </CardTitle>
              </CardHeader>
              <CardContent>
                {showRawMarkdown ? (
                  <pre className="bg-gray-900 text-gray-100 p-4 rounded-xl border border-gray-800 overflow-x-auto text-sm leading-relaxed">
                    <code>{markdown}</code>
                  </pre>
                ) : (
                  <div className="bg-white dark:bg-gray-900 p-6 rounded-xl border border-gray-200 dark:border-gray-800 max-h-[500px] overflow-y-auto">
                    <article className="prose prose-lg dark:prose-invert max-w-none">
                      <ReactMarkdown remarkPlugins={[remarkGfm]}>
                        {markdown}
                      </ReactMarkdown>
                    </article>
                  </div>
                )}
              </CardContent>
            </Card>
          </div>
        )}

        {/* Structure Tab */}
        {activeTab === 'structure' && (
          <div className="space-y-6 animate-fade-in">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <CodeBracketIcon className="h-5 w-5 mr-2 text-primary-600 dark:text-primary-400" />
                  Code Snippets ({codeSnippets.length})
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {codeSnippets.length === 0 ? (
                  <p className="text-sm text-gray-500">No code snippets provided.</p>
                ) : (
                  codeSnippets.map((snippet: DevtoCodeSnippet, index: number) => (
                    <Card key={index} className="bg-gray-900 text-gray-100 border border-gray-800">
                      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium flex items-center text-white">
                          <CodeBracketIcon className="h-4 w-4 mr-2" />
                          {snippet.label || snippet.language || `Snippet ${index + 1}`}
                        </CardTitle>
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => copyToClipboard(snippet.content)}
                          leftIcon={<DocumentDuplicateIcon className="h-4 w-4" />}
                        >
                          Copy Code
                        </Button>
                      </CardHeader>
                      <CardContent>
                        <pre className="overflow-x-auto text-sm font-mono leading-relaxed">
                          <code>{snippet.content}</code>
                        </pre>
                      </CardContent>
                    </Card>
                  ))
                )}
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <QueueListIcon className="h-5 w-5 mr-2 text-secondary-600 dark:text-secondary-400" />
                  Diagram Blocks ({diagramBlocks.length})
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {diagramBlocks.length === 0 ? (
                  <p className="text-sm text-gray-500">No diagrams provided.</p>
                ) : (
                  diagramBlocks.map((diagram: DevtoDiagramBlock, index: number) => (
                    <Card key={diagram.id || index} className="border border-gray-200 dark:border-gray-800">
                      <CardHeader>
                        <CardTitle className="text-sm font-medium flex items-center justify-between">
                          <span>{diagram.alt || `Diagram ${index + 1}`}</span>
                          <span className="text-xs text-gray-500">
                            {diagram.type?.toUpperCase() || 'MERMAID'} • {diagram.placement_hint || 'Inline'}
                          </span>
                        </CardTitle>
                      </CardHeader>
                      <CardContent className="space-y-4">
                        {renderDiagram(diagram, index)}
                      </CardContent>
                    </Card>
                  ))
                )}
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <BeakerIcon className="h-5 w-5 mr-2 text-tertiary-600 dark:text-tertiary-400" />
                  Resources ({formattedResources.length})
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {formattedResources.length === 0 ? (
                  <p className="text-sm text-gray-500">No additional resources provided.</p>
                ) : (
                  formattedResources.map((resource, index) => (
                    <Card key={index} className="border border-gray-200 dark:border-gray-800">
                      <CardContent className="flex flex-col md:flex-row md:items-center md:justify-between space-y-3 md:space-y-0">
                        <div>
                          <p className="text-sm font-semibold text-gray-900 dark:text-gray-200">
                            {resource.title}
                          </p>
                          {resource.note && (
                            <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">{resource.note}</p>
                          )}
                        </div>
                        <div className="flex items-center space-x-2">
                          {resource.url ? (
                            <Button
                              asChild
                              variant="ghost"
                              size="sm"
                              className="text-primary-600"
                            >
                              <a href={resource.url} target="_blank" rel="noopener noreferrer" className="flex items-center">
                                <ArrowTopRightOnSquareIcon className="h-4 w-4 mr-1" />
                                Visit
                              </a>
                            </Button>
                          ) : (
                            <span className="text-xs text-gray-500">No URL</span>
                          )}
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => copyToClipboard(resource.url || resource.title)}
                            leftIcon={<DocumentDuplicateIcon className="h-4 w-4" />}
                          >
                            Copy
                          </Button>
                        </div>
                      </CardContent>
                    </Card>
                  ))
                )}
              </CardContent>
            </Card>
          </div>
        )}

        {/* Assets Tab */}
        {activeTab === 'assets' && (
          <div className="space-y-6 animate-fade-in">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <PhotoIcon className="h-5 w-5 mr-2 text-primary-600 dark:text-primary-400" />
                  Image Prompts ({imagePrompts.length})
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {imagePrompts.length === 0 ? (
                  <p className="text-sm text-gray-500">No image prompts provided.</p>
                ) : (
                  imagePrompts.map((prompt: DevtoImagePrompt, index: number) => (
                    <Card key={index} className="border border-gray-200 dark:border-gray-800">
                      <CardHeader>
                        <CardTitle className="text-sm font-medium flex items-center justify-between">
                          <span>{prompt.title || `Image Prompt ${index + 1}`}</span>
                          <span className="text-xs text-gray-500">
                            {prompt.role?.toUpperCase() || 'PROMPT'} • {prompt.ratio || prompt.ratio_px?.ratio || ''}
                          </span>
                        </CardTitle>
                      </CardHeader>
                      <CardContent className="space-y-3 text-sm">
                        <div>
                          <p className="text-xs uppercase text-gray-500 mb-1">Prompt</p>
                          <p className="bg-gray-50 dark:bg-gray-900 p-3 rounded-lg border border-gray-200 dark:border-gray-800 whitespace-pre-wrap">
                            {prompt.prompt}
                          </p>
                        </div>
                        {prompt.negative_prompt && (
                          <div>
                            <p className="text-xs uppercase text-gray-500 mb-1">Negative Prompt</p>
                            <p className="bg-gray-50 dark:bg-gray-900 p-3 rounded-lg border border-gray-200 dark:border-gray-800 whitespace-pre-wrap">
                              {prompt.negative_prompt}
                            </p>
                          </div>
                        )}
                        {prompt.style_notes && (
                          <div>
                            <p className="text-xs uppercase text-gray-500 mb-1">Style Notes</p>
                            <p className="bg-gray-50 dark:bg-gray-900 p-3 rounded-lg border border-gray-200 dark:border-gray-800 whitespace-pre-wrap">
                              {prompt.style_notes}
                            </p>
                          </div>
                        )}
                        <div className="flex items-center justify-between pt-2">
                          <span className="text-xs text-gray-500">
                            {prompt.size_px || prompt.ratio_px?.size_px || 'Custom size'}
                          </span>
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
                  ))
                )}
              </CardContent>
            </Card>

            {Array.isArray(article.image_plan?.roles) && (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <PhotoIcon className="h-5 w-5 mr-2 text-secondary-600 dark:text-secondary-400" />
                    Image Plan
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-3 text-sm text-gray-600 dark:text-gray-300">
                  <div className="flex flex-wrap gap-2">
                    {article.image_plan.roles.map((role: string, index: number) => (
                      <span key={index} className="px-3 py-1 bg-gray-100 dark:bg-gray-900 text-gray-700 dark:text-gray-300 rounded-full text-xs">
                        {role}
                      </span>
                    ))}
                  </div>
                  <div className="grid md:grid-cols-2 gap-3">
                    {(article.image_plan.ratios_px || []).map((ratio: any, index: number) => (
                      <div key={index} className="bg-gray-100 dark:bg-gray-900 p-3 rounded-lg border border-gray-200 dark:border-gray-800 text-xs">
                        <p className="font-medium text-gray-700 dark:text-gray-300">{ratio.ratio}</p>
                        <p className="text-gray-500 dark:text-gray-400">{ratio.size_px}</p>
                      </div>
                    ))}
                  </div>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => copyToClipboard(JSON.stringify(article.image_plan, null, 2))}
                    leftIcon={<DocumentDuplicateIcon className="h-4 w-4" />}
                  >
                    Copy Plan JSON
                  </Button>
                </CardContent>
              </Card>
            )}
          </div>
        )}

        {/* SEO & Compliance Tab */}
        {activeTab === 'seo' && (
          <div className="space-y-6 animate-fade-in">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <MagnifyingGlassIcon className="h-5 w-5 mr-2 text-primary-600 dark:text-primary-400" />
                  SEO Metadata
                </CardTitle>
              </CardHeader>
              <CardContent className="grid md:grid-cols-2 gap-4 text-sm text-gray-600 dark:text-gray-300">
                <div className="space-y-2">
                  <p className="text-xs uppercase text-gray-500">Meta Description</p>
                  <p className="bg-gray-100 dark:bg-gray-900 p-3 rounded-lg border border-gray-200 dark:border-gray-800 whitespace-pre-wrap">
                    {seo.meta_description || frontMatter.description || 'No meta description provided.'}
                  </p>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => copyToClipboard(seo.meta_description || frontMatter.description || '')}
                    leftIcon={<DocumentDuplicateIcon className="h-4 w-4" />}
                  >
                    Copy Description
                  </Button>
                </div>
                <div className="space-y-2">
                  <p className="text-xs uppercase text-gray-500">Canonical URL</p>
                  <p className="bg-gray-100 dark:bg-gray-900 p-3 rounded-lg border border-gray-200 dark:border-gray-800 break-all">
                    {seo.canonical_url || frontMatter.canonical_url || meta.canonical}
                  </p>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => copyToClipboard(seo.canonical_url || frontMatter.canonical_url || meta.canonical || '')}
                    leftIcon={<DocumentDuplicateIcon className="h-4 w-4" />}
                  >
                    Copy Canonical
                  </Button>
                </div>
                <div className="space-y-2">
                  <p className="text-xs uppercase text-gray-500">Tags</p>
                  <div className="flex flex-wrap gap-2">
                    {(frontMatter.tags || []).map((tag: string, index: number) => (
                      <span key={index} className="px-3 py-1 bg-primary-100 dark:bg-primary-900/20 text-primary-700 dark:text-primary-300 rounded-full text-xs">
                        #{tag}
                      </span>
                    ))}
                  </div>
                  {Array.isArray(frontMatter.tags) && frontMatter.tags.length > 0 && (
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => copyToClipboard(frontMatter.tags.join(', '))}
                      leftIcon={<DocumentDuplicateIcon className="h-4 w-4" />}
                    >
                      Copy Tags
                    </Button>
                  )}
                </div>
                <div className="space-y-2">
                  <p className="text-xs uppercase text-gray-500">Keyword Coverage</p>
                  <div className="bg-gray-100 dark:bg-gray-900 p-3 rounded-lg border border-gray-200 dark:border-gray-800">
                    <p className="text-sm font-semibold text-gray-700 dark:text-gray-200 mb-2 flex items-center">
                      <ChartBarIcon className="h-4 w-4 mr-2" />
                      Primary Keywords
                    </p>
                    <div className="flex flex-wrap gap-2">
                      {(meta.primary_keywords || []).map((keyword: string, index: number) => (
                        <span key={index} className="px-2 py-1 bg-white dark:bg-gray-800 rounded border border-gray-200 dark:border-gray-700 text-xs">
                          {keyword}
                        </span>
                      ))}
                    </div>
                  </div>
                  <div className="bg-gray-100 dark:bg-gray-900 p-3 rounded-lg border border-gray-200 dark:border-gray-800">
                    <p className="text-sm font-semibold text-gray-700 dark:text-gray-200 mb-2">
                      Secondary Keywords
                    </p>
                    <div className="flex flex-wrap gap-2">
                      {(meta.secondary_keywords || []).map((keyword: string, index: number) => (
                        <span key={index} className="px-2 py-1 bg-white dark:bg-gray-800 rounded border border-gray-200 dark:border-gray-700 text-xs">
                          {keyword}
                        </span>
                      ))}
                    </div>
                  </div>
                  <div className="bg-gray-100 dark:bg-gray-900 p-3 rounded-lg border border-gray-200 dark:border-gray-800">
                    <p className="text-sm font-semibold text-gray-700 dark:text-gray-200 mb-2">
                      LSI Terms
                    </p>
                    <div className="flex flex-wrap gap-2">
                      {(meta.lsi_terms || []).map((keyword: string, index: number) => (
                        <span key={index} className="px-2 py-1 bg-white dark:bg-gray-800 rounded border border-gray-200 dark:border-gray-700 text-xs">
                          {keyword}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <SparklesIcon className="h-5 w-5 mr-2 text-success-600 dark:text-success-400" />
                  Compliance Summary
                </CardTitle>
              </CardHeader>
              <CardContent className="grid md:grid-cols-2 gap-4 text-sm text-gray-600 dark:text-gray-300">
                <div className="bg-primary-50 dark:bg-primary-900/20 rounded-xl p-4 border border-primary-100 dark:border-primary-800">
                  <p className="text-xs uppercase font-semibold text-primary-600 dark:text-primary-300">Metrics</p>
                  <div className="mt-2 space-y-2 text-primary-800 dark:text-primary-200">
                    <p>Word count: {compliance.word_count || markdown.split(/\s+/).filter(Boolean).length}</p>
                    <p>Reading time: {compliance.reading_time_min || readingTime} min</p>
                    <p>Code snippets: {compliance.code_snippets_count || codeSnippets.length}</p>
                    <p>Diagrams: {compliance.diagram_blocks_count || diagramBlocks.length}</p>
                    <p>Resources: {compliance.resources_count || formattedResources.length}</p>
                    <p>Tags: {(frontMatter.tags || []).length}</p>
                  </div>
                </div>
                <div className="bg-secondary-50 dark:bg-secondary-900/20 rounded-xl p-4 border border-secondary-100 dark:border-secondary-800">
                  <p className="text-xs uppercase font-semibold text-secondary-600 dark:text-secondary-300">Required Checks</p>
                  <ul className="mt-2 space-y-2 text-secondary-800 dark:text-secondary-200 list-disc list-inside">
                    {(compliance.checks || [
                      '800–2000 words',
                      'Front matter includes title, tags, canonical URL',
                      'Published flag set appropriately',
                      'At least one code snippet or diagram',
                      'Resources section present',
                      'SEO meta description provided'
                    ]).map((check: string, index: number) => (
                      <li key={index}>{check}</li>
                    ))}
                  </ul>
                </div>
              </CardContent>
            </Card>
          </div>
        )}
      </div>
    </div>
  );
};

export default DevtoArticleView;
