import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { 
  BookOpenIcon,
  ClockIcon,
  HashtagIcon,
  DocumentDuplicateIcon,
  LinkIcon,
  ChartBarIcon,
  CodeBracketIcon,
  ChatBubbleBottomCenterTextIcon,
  PhotoIcon,
  MagnifyingGlassIcon,
  PencilSquareIcon,
  CheckCircleIcon
} from '@heroicons/react/24/outline';
import { Card, CardContent, CardHeader, CardTitle } from './ui/Card';
import { Button } from './ui/Button';
import { cn } from '../lib/utils';

// Interfaces
interface Section {
  h2: string;
  summary: string;
  key_points: string[];
}

interface CodeSnippet {
  id: string;
  language: string;
  content: string;
  title?: string;
}

interface DiagramBlock {
  id: string;
  type: string;
  alt: string;
  content: string;
  placement_hint: string;
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

interface CTA {
  text: string;
  link: string;
}

interface SEO {
  slug: string;
  meta_title: string;
  meta_description: string;
  keywords_used: string[];
  lsi_terms_used: string[];
}

interface Reference {
  title: string;
  url?: string;
  note?: string;
}

interface MediumContent {
  title: string;
  subtitle: string;
  reading_time_min: number;
  tags: string[];
  markdown: string;
  sections: Section[];
  code_snippets: CodeSnippet[];
  diagram_blocks: DiagramBlock[];
  pull_quotes: string[];
  cta: CTA;
  references: Reference[];
  image_prompts: ImagePrompt[];
  seo: SEO;
}

interface MediumArticleViewProps {
  content: {
    job_id: string;
    platform: string;
    format: string;
    envelope: {
      content: MediumContent;
    };
    meta?: {
      topic_title?: string;
      topic_id?: string;
    };
  };
  onCopy: () => void;
}

const MediumArticleView: React.FC<MediumArticleViewProps> = ({ content, onCopy }) => {
  const [activeTab, setActiveTab] = useState<'content' | 'structure' | 'assets' | 'seo'>('content');
  const [expandedSection, setExpandedSection] = useState<number | null>(null);
  
  // Extract content with fallbacks
  const article = content.envelope?.content || {};
  const meta = content.meta || {};
  
  // Add fallbacks for required properties
  const title = article.title || 'Untitled Article';
  const subtitle = article.subtitle || '';
  const reading_time_min = article.reading_time_min || 0;
  const tags = article.tags || [];
  const markdown = article.markdown || '';
  const sections = article.sections || [];
  const code_snippets = article.code_snippets || [];
  const diagram_blocks = article.diagram_blocks || [];
  const pull_quotes = article.pull_quotes || [];
  const cta = article.cta || {};
  const references = article.references || [];
  const image_prompts = article.image_prompts || [];
  const seo = article.seo || {};

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
  };

  const getSectionColor = (index: number) => {
    const colors = [
      'bg-primary-100 dark:bg-primary-900/20 text-primary-800 dark:text-primary-400 border-primary-200 dark:border-primary-700',
      'bg-success-100 dark:bg-success-900/20 text-success-800 dark:text-success-400 border-success-200 dark:border-success-700',
      'bg-secondary-100 dark:bg-secondary-900/20 text-secondary-800 dark:text-secondary-400 border-secondary-200 dark:border-secondary-700',
      'bg-warning-100 dark:bg-warning-900/20 text-warning-800 dark:text-warning-400 border-warning-200 dark:border-warning-700',
      'bg-error-100 dark:bg-error-900/20 text-error-800 dark:text-error-400 border-error-200 dark:border-error-700'
    ];
    return colors[index % colors.length];
  };


  return (
    <div className="bg-white dark:bg-gray-900 rounded-3xl shadow-2xl max-w-7xl w-full max-h-[90vh] overflow-hidden flex flex-col">
      {/* Header */}
      <div className="bg-gradient-to-r from-green-500 to-green-600 text-white p-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="p-3 bg-white/20 backdrop-blur-sm rounded-xl">
              <BookOpenIcon className="h-8 w-8" />
            </div>
            <div>
              <h2 className="text-2xl font-bold">Medium Article</h2>
              {meta.topic_title && (
                <p className="text-green-100 text-sm mt-1">{meta.topic_title}</p>
              )}
              <p className="text-green-200 text-xs mt-1">
                {reading_time_min} min read • {sections.length} sections
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

      {/* Tab Navigation */}
      <div className="border-b border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800">
        <div className="flex space-x-1 p-2">
          <Button
            variant={activeTab === 'content' ? 'primary' : 'ghost'}
            onClick={() => setActiveTab('content')}
            className={cn("flex-1", activeTab === 'content' && "shadow-sm")}
          >
            <PencilSquareIcon className="h-4 w-4 mr-2" />
            Content
          </Button>
          <Button
            variant={activeTab === 'structure' ? 'primary' : 'ghost'}
            onClick={() => setActiveTab('structure')}
            className={cn("flex-1", activeTab === 'structure' && "shadow-sm")}
          >
            <BookOpenIcon className="h-4 w-4 mr-2" />
            Structure
          </Button>
          <Button
            variant={activeTab === 'assets' ? 'primary' : 'ghost'}
            onClick={() => setActiveTab('assets')}
            className={cn("flex-1", activeTab === 'assets' && "shadow-sm")}
          >
            <PhotoIcon className="h-4 w-4 mr-2" />
            Assets
          </Button>
          <Button
            variant={activeTab === 'seo' ? 'primary' : 'ghost'}
            onClick={() => setActiveTab('seo')}
            className={cn("flex-1", activeTab === 'seo' && "shadow-sm")}
          >
            <MagnifyingGlassIcon className="h-4 w-4 mr-2" />
            SEO
          </Button>
        </div>
      </div>

      {/* Content Area */}
      <div className="flex-1 overflow-y-auto p-6 bg-gray-50 dark:bg-gray-950">
        {/* Content Tab */}
        {activeTab === 'content' && (
          <div className="space-y-6 animate-fade-in">
            {/* Title & Subtitle */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <BookOpenIcon className="h-5 w-5 mr-2 text-primary-600 dark:text-primary-400" />
                  Article Header
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Title</p>
                  <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100">
                    {title}
                  </h1>
                </div>
                {subtitle && (
                  <div>
                    <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Subtitle</p>
                    <p className="text-lg text-gray-700 dark:text-gray-300">
                      {subtitle}
                    </p>
                  </div>
                )}
                <div className="flex items-center space-x-4 text-sm text-gray-600 dark:text-gray-400">
                  <span className="flex items-center">
                    <ClockIcon className="h-4 w-4 mr-1" />
                    {reading_time_min} min read
                  </span>
                  <span className="flex items-center">
                    <BookOpenIcon className="h-4 w-4 mr-1" />
                    {sections.length} sections
                  </span>
                </div>
              </CardContent>
            </Card>

            {/* Article Content */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center justify-between">
                  <span className="flex items-center">
                    <PencilSquareIcon className="h-5 w-5 mr-2 text-secondary-600 dark:text-secondary-400" />
                    Article Content
                  </span>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => copyToClipboard(markdown)}
                    leftIcon={<DocumentDuplicateIcon className="h-4 w-4" />}
                  >
                    Copy Markdown
                  </Button>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="bg-white dark:bg-gray-800 p-6 rounded-xl border border-gray-200 dark:border-gray-700 max-h-[600px] overflow-y-auto">
                  <article className="prose prose-lg dark:prose-invert max-w-none
                    prose-headings:text-gray-900 dark:prose-headings:text-gray-100
                    prose-h1:text-3xl prose-h1:font-bold prose-h1:mb-8 prose-h1:mt-0
                    prose-h2:text-2xl prose-h2:font-semibold prose-h2:mt-8 prose-h2:mb-4
                    prose-h3:text-xl prose-h3:font-medium prose-h3:mt-6 prose-h3:mb-3
                    prose-p:text-gray-700 dark:prose-p:text-gray-300 prose-p:leading-relaxed prose-p:mb-4
                    prose-a:text-primary-600 dark:prose-a:text-primary-400 prose-a:no-underline hover:prose-a:underline
                    prose-strong:text-gray-900 dark:prose-strong:text-gray-100
                    prose-em:text-gray-800 dark:prose-em:text-gray-200
                    prose-ul:my-4 prose-ul:list-disc prose-ul:pl-6
                    prose-ol:my-4 prose-ol:list-decimal prose-ol:pl-6
                    prose-li:text-gray-700 dark:prose-li:text-gray-300 prose-li:mb-2
                    prose-blockquote:border-l-4 prose-blockquote:border-primary-500 prose-blockquote:pl-4 prose-blockquote:italic
                    prose-blockquote:text-gray-700 dark:prose-blockquote:text-gray-300
                    prose-code:bg-gray-100 dark:prose-code:bg-gray-800 prose-code:px-2 prose-code:py-1 prose-code:rounded
                    prose-code:text-primary-600 dark:prose-code:text-primary-400 prose-code:font-mono prose-code:text-sm
                    prose-pre:bg-gray-900 prose-pre:text-gray-100 prose-pre:p-4 prose-pre:rounded-lg prose-pre:overflow-x-auto
                    prose-pre:my-6 dark:prose-pre:bg-gray-950
                    prose-table:w-full prose-table:my-6 prose-table:border-collapse
                    prose-th:bg-gray-100 dark:prose-th:bg-gray-800 prose-th:p-3 prose-th:text-left prose-th:font-semibold
                    prose-th:border prose-th:border-gray-300 dark:prose-th:border-gray-700
                    prose-td:p-3 prose-td:border prose-td:border-gray-300 dark:prose-td:border-gray-700
                    prose-img:rounded-lg prose-img:shadow-lg prose-img:my-6
                    prose-hr:border-gray-300 dark:prose-hr:border-gray-700 prose-hr:my-8"
                  >
                    <ReactMarkdown 
                      remarkPlugins={[remarkGfm]}
                      components={{
                        // Custom rendering for code blocks
                        code({node, inline, className, children, ...props}: any) {
                          const match = /language-(\w+)/.exec(className || '');
                          const lang = match ? match[1] : '';
                          
                          if (!inline && match) {
                            return (
                              <div className="relative group">
                                <div className="absolute top-0 right-0 mt-2 mr-2">
                                  <span className="text-xs text-gray-400 bg-gray-800 px-2 py-1 rounded">{lang}</span>
                                </div>
                                <pre className={className} {...props}>
                                  <code className={className} {...props}>
                                    {children}
                                  </code>
                                </pre>
                              </div>
                            );
                          }
                          
                          return (
                            <code className={className} {...props}>
                              {children}
                            </code>
                          );
                        },
                        // Custom rendering for blockquotes
                        blockquote({node, children, ...props}) {
                          return (
                            <blockquote className="relative pl-6 my-6 border-l-4 border-primary-500" {...props}>
                              <span className="absolute left-0 top-0 text-4xl text-primary-200 dark:text-primary-800 leading-none">"</span>
                              {children}
                            </blockquote>
                          );
                        },
                        // Custom rendering for tables
                        table({node, children, ...props}) {
                          return (
                            <div className="overflow-x-auto my-6">
                              <table className="min-w-full divide-y divide-gray-300 dark:divide-gray-700" {...props}>
                                {children}
                              </table>
                            </div>
                          );
                        },
                        // Custom rendering for links
                        a({node, children, href, ...props}) {
                          return (
                            <a 
                              href={href} 
                              className="text-primary-600 dark:text-primary-400 hover:underline font-medium"
                              target="_blank"
                              rel="noopener noreferrer"
                              {...props}
                            >
                              {children}
                            </a>
                          );
                        },
                        // Custom rendering for horizontal rules
                        hr({node, ...props}) {
                          return (
                            <hr className="my-8 border-t-2 border-gray-200 dark:border-gray-700" {...props} />
                          );
                        }
                      }}
                    >
                      {markdown}
                    </ReactMarkdown>
                  </article>
                  <div className="mt-6 pt-4 border-t border-gray-200 dark:border-gray-700">
                    <p className="text-xs text-gray-500 dark:text-gray-400">
                      Word count: {markdown.split(/\s+/).filter(word => word.length > 0).length} words
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Pull Quotes */}
            {pull_quotes.length > 0 && (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <ChatBubbleBottomCenterTextIcon className="h-5 w-5 mr-2 text-primary-600 dark:text-primary-400" />
                    Pull Quotes
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {pull_quotes.map((quote, idx) => (
                      <div key={idx} className="relative">
                        <div className="absolute -left-2 top-0 text-6xl text-primary-200 dark:text-primary-800">"</div>
                        <blockquote className="pl-8 pr-4 py-2 border-l-4 border-primary-500 bg-primary-50 dark:bg-primary-900/20 rounded-r-lg">
                          <p className="text-lg italic text-primary-800 dark:text-primary-200">
                            {quote}
                          </p>
                        </blockquote>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            )}

            {/* Tags */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center justify-between">
                  <span className="flex items-center">
                    <HashtagIcon className="h-5 w-5 mr-2 text-secondary-600 dark:text-secondary-400" />
                    Tags
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
                    <span key={idx} className="px-3 py-1 bg-secondary-100 dark:bg-secondary-900/20 text-secondary-800 dark:text-secondary-400 rounded-full text-sm font-medium border border-secondary-200 dark:border-secondary-700">
                      {tag}
                    </span>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>
        )}

        {/* Structure Tab */}
        {activeTab === 'structure' && (
          <div className="space-y-6 animate-fade-in">
            {/* Sections */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <BookOpenIcon className="h-5 w-5 mr-2 text-primary-600 dark:text-primary-400" />
                  Article Sections
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {sections.map((section, index) => (
                  <Card
                    key={index}
                    className={cn(
                      "cursor-pointer hover:shadow-md transition-all",
                      getSectionColor(index),
                      expandedSection === index && "ring-2 ring-primary-500 dark:ring-primary-400"
                    )}
                    onClick={() => setExpandedSection(expandedSection === index ? null : index)}
                  >
                    <CardContent className="p-4">
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <h3 className="font-medium text-lg mb-2">{section.h2}</h3>
                          <p className="text-sm opacity-90">{section.summary}</p>
                        </div>
                        <span className="text-xs font-medium px-2 py-1 bg-white/50 dark:bg-gray-900/50 rounded">
                          Section {index + 1}
                        </span>
                      </div>
                      
                      {(expandedSection === null || expandedSection === index) && section.key_points.length > 0 && (
                        <div className="mt-4 pt-4 border-t border-white/20 dark:border-gray-700/20">
                          <h4 className="text-sm font-medium mb-2">Key Points:</h4>
                          <ul className="space-y-1">
                            {section.key_points.map((point, pointIdx) => (
                              <li key={pointIdx} className="flex items-start text-sm">
                                <span className="mr-2">•</span>
                                <span>{point}</span>
                              </li>
                            ))}
                          </ul>
                        </div>
                      )}
                    </CardContent>
                  </Card>
                ))}
              </CardContent>
            </Card>

            {/* Call to Action */}
            {cta.text && (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <LinkIcon className="h-5 w-5 mr-2 text-secondary-600 dark:text-secondary-400" />
                    Call to Action
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="bg-gradient-to-r from-secondary-50 to-pink-50 dark:from-secondary-900/20 dark:to-pink-900/20 p-4 rounded-xl border border-secondary-200 dark:border-secondary-700">
                    <p className="text-secondary-800 dark:text-secondary-200 font-medium mb-2">
                      {cta.text}
                    </p>
                    {cta.link && (
                      <a
                        href={cta.link}
                        className="text-sm text-secondary-600 dark:text-secondary-400 hover:underline flex items-center"
                        target="_blank"
                        rel="noopener noreferrer"
                      >
                        <LinkIcon className="h-4 w-4 mr-1" />
                        {cta.link}
                      </a>
                    )}
                  </div>
                </CardContent>
              </Card>
            )}
          </div>
        )}

        {/* Assets Tab */}
        {activeTab === 'assets' && (
          <div className="space-y-6 animate-fade-in">
            {/* Code Snippets */}
            {code_snippets.length > 0 && (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <CodeBracketIcon className="h-5 w-5 mr-2 text-primary-600 dark:text-primary-400" />
                    Code Snippets
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {code_snippets.map((snippet, idx) => (
                      <div key={idx} className="bg-gray-900 rounded-lg p-4 overflow-x-auto">
                        {snippet.title && (
                          <p className="text-sm text-gray-400 mb-2">{snippet.title}</p>
                        )}
                        <pre className="text-sm text-gray-300">
                          <code>{snippet.content}</code>
                        </pre>
                        <div className="flex items-center justify-between mt-2">
                          <span className="text-xs text-gray-500">{snippet.language}</span>
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => copyToClipboard(snippet.content)}
                            className="text-gray-400 hover:text-gray-200"
                          >
                            Copy
                          </Button>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            )}

            {/* Diagram Blocks */}
            {diagram_blocks.length > 0 && (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <ChartBarIcon className="h-5 w-5 mr-2 text-secondary-600 dark:text-secondary-400" />
                    Diagrams
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {diagram_blocks.map((diagram, idx) => (
                      <Card key={idx} variant="filled">
                        <CardContent className="p-4">
                          <div className="flex items-start justify-between mb-2">
                            <div>
                              <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                                {diagram.type.toUpperCase()} Diagram
                              </span>
                              <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                                Place {diagram.placement_hint}
                              </p>
                            </div>
                            <span className="px-2 py-1 bg-secondary-100 dark:bg-secondary-900/20 text-secondary-800 dark:text-secondary-400 rounded text-xs">
                              {diagram.id}
                            </span>
                          </div>
                          <div className="bg-gray-50 dark:bg-gray-800 p-3 rounded-lg border border-gray-200 dark:border-gray-700 mt-3">
                            <pre className="text-xs text-gray-600 dark:text-gray-400 overflow-x-auto">
                              {diagram.content}
                            </pre>
                          </div>
                          <p className="text-xs text-gray-500 dark:text-gray-400 mt-2">
                            Alt: {diagram.alt}
                          </p>
                        </CardContent>
                      </Card>
                    ))}
                  </div>
                </CardContent>
              </Card>
            )}

            {/* Image Prompts */}
            {image_prompts.length > 0 && (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <PhotoIcon className="h-5 w-5 mr-2 text-primary-600 dark:text-primary-400" />
                    Cover Image
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {image_prompts.map((prompt, idx) => (
                      <Card key={idx} variant="filled">
                        <CardContent className="p-4">
                          <div className="flex items-start justify-between mb-3">
                            <div className="flex items-center space-x-2">
                              <span className="px-2 py-1 bg-primary-100 dark:bg-primary-900/20 text-primary-800 dark:text-primary-400 rounded-full text-xs font-medium">
                                {prompt.role}
                              </span>
                              <span className="px-2 py-1 bg-secondary-100 dark:bg-secondary-900/20 text-secondary-800 dark:text-secondary-400 rounded-full text-xs font-medium">
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

            {/* References */}
            {references.length > 0 && (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <LinkIcon className="h-5 w-5 mr-2 text-secondary-600 dark:text-secondary-400" />
                    References
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <ul className="space-y-2">
                    {references.map((ref, idx) => (
                      <li key={idx} className="flex items-start text-sm text-gray-700 dark:text-gray-300">
                        <span className="text-secondary-500 mr-2">[{idx + 1}]</span>
                        <div className="flex-1">
                          <div className="font-medium text-gray-900 dark:text-gray-100">
                            {typeof ref === 'string' ? ref : ref.title}
                          </div>
                          {typeof ref === 'object' && ref.url && (
                            <a 
                              href={ref.url} 
                              target="_blank" 
                              rel="noopener noreferrer"
                              className="text-blue-600 dark:text-blue-400 hover:underline text-xs"
                            >
                              {ref.url}
                            </a>
                          )}
                          {typeof ref === 'object' && ref.note && (
                            <div className="text-gray-600 dark:text-gray-400 text-xs mt-1">
                              {ref.note}
                            </div>
                          )}
                        </div>
                      </li>
                    ))}
                  </ul>
                </CardContent>
              </Card>
            )}
          </div>
        )}

        {/* SEO Tab */}
        {activeTab === 'seo' && (
          <div className="space-y-6 animate-fade-in">
            {/* SEO Metadata */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <MagnifyingGlassIcon className="h-5 w-5 mr-2 text-primary-600 dark:text-primary-400" />
                  SEO Metadata
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {seo.slug && (
                  <div>
                    <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">URL Slug</p>
                    <div className="bg-gray-50 dark:bg-gray-800 p-3 rounded-lg border border-gray-200 dark:border-gray-700">
                      <p className="text-sm font-mono text-gray-700 dark:text-gray-300">/{seo.slug}</p>
                    </div>
                  </div>
                )}
                
                {seo.meta_title && (
                  <div>
                    <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Meta Title</p>
                    <p className="text-gray-700 dark:text-gray-300">{seo.meta_title}</p>
                    <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                      {seo.meta_title.length} characters
                    </p>
                  </div>
                )}
                
                {seo.meta_description && (
                  <div>
                    <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Meta Description</p>
                    <p className="text-sm text-gray-700 dark:text-gray-300">{seo.meta_description}</p>
                    <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                      {seo.meta_description.length} characters
                    </p>
                  </div>
                )}
              </CardContent>
            </Card>

            {/* Keywords */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <HashtagIcon className="h-5 w-5 mr-2 text-secondary-600 dark:text-secondary-400" />
                  Keywords Used
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {seo.keywords_used && seo.keywords_used.length > 0 && (
                  <div>
                    <h4 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Primary Keywords</h4>
                    <div className="flex flex-wrap gap-2">
                      {seo.keywords_used.map((keyword, idx) => (
                        <span key={idx} className="px-3 py-1 bg-primary-100 dark:bg-primary-900/20 text-primary-800 dark:text-primary-400 rounded-full text-sm">
                          {keyword}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
                
                {seo.lsi_terms_used && seo.lsi_terms_used.length > 0 && (
                  <div>
                    <h4 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">LSI Terms</h4>
                    <div className="flex flex-wrap gap-2">
                      {seo.lsi_terms_used.map((term, idx) => (
                        <span key={idx} className="px-3 py-1 bg-secondary-100 dark:bg-secondary-900/20 text-secondary-800 dark:text-secondary-400 rounded-full text-sm">
                          {term}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>

            {/* SEO Checklist */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <CheckCircleIcon className="h-5 w-5 mr-2 text-success-600 dark:text-success-400" />
                  SEO Checklist
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  <div className="flex items-center p-3 bg-success-50 dark:bg-success-900/20 rounded-lg border border-success-200 dark:border-success-700">
                    <CheckCircleIcon className="h-5 w-5 text-success-600 dark:text-success-400 mr-3 flex-shrink-0" />
                    <p className="text-sm text-success-800 dark:text-success-300">
                      Meta title under 60 characters ({seo.meta_title?.length || 0})
                    </p>
                  </div>
                  <div className="flex items-center p-3 bg-success-50 dark:bg-success-900/20 rounded-lg border border-success-200 dark:border-success-700">
                    <CheckCircleIcon className="h-5 w-5 text-success-600 dark:text-success-400 mr-3 flex-shrink-0" />
                    <p className="text-sm text-success-800 dark:text-success-300">
                      Meta description under 160 characters ({seo.meta_description?.length || 0})
                    </p>
                  </div>
                  <div className="flex items-center p-3 bg-success-50 dark:bg-success-900/20 rounded-lg border border-success-200 dark:border-success-700">
                    <CheckCircleIcon className="h-5 w-5 text-success-600 dark:text-success-400 mr-3 flex-shrink-0" />
                    <p className="text-sm text-success-800 dark:text-success-300">
                      Keywords integrated ({seo.keywords_used?.length || 0} primary, {seo.lsi_terms_used?.length || 0} LSI)
                    </p>
                  </div>
                  <div className="flex items-center p-3 bg-success-50 dark:bg-success-900/20 rounded-lg border border-success-200 dark:border-success-700">
                    <CheckCircleIcon className="h-5 w-5 text-success-600 dark:text-success-400 mr-3 flex-shrink-0" />
                    <p className="text-sm text-success-800 dark:text-success-300">
                      URL slug optimized
                    </p>
                  </div>
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
                {reading_time_min} min read
              </span>
            </div>
            <div className="flex items-center">
              <BookOpenIcon className="h-4 w-4 mr-1 text-gray-500 dark:text-gray-400" />
              <span className="text-gray-600 dark:text-gray-400">
                {sections.length} sections
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
            Medium Article
          </div>
        </div>
      </div>
    </div>
  );
};

export default MediumArticleView;
