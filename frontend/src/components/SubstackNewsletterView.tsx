import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { 
  EnvelopeIcon,
  DocumentTextIcon,
  DocumentDuplicateIcon,
  PhotoIcon,
  BookOpenIcon,
  LightBulbIcon,
  LinkIcon,
  MagnifyingGlassIcon,
  BeakerIcon,
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

interface Resource {
  title: string;
  url: string;
  note: string;
  tracked: boolean;
}

interface SubscribeCTA {
  text: string;
  link: string;
  placed_in_markdown: boolean;
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

interface SEO {
  meta_title: string;
  meta_description: string;
  keywords_used: string[];
  lsi_terms_used: string[];
}

interface SubstackNewsletterContent {
  subject: string;
  preheader: string;
  alt_subject_tests: string[];
  markdown: string;
  sections: Section[];
  key_takeaways: string[];
  resources: Resource[];
  subscribe_cta: SubscribeCTA;
  image_prompts: ImagePrompt[];
  seo: SEO;
}

interface SubstackNewsletterViewProps {
  content: any;
}

export const SubstackNewsletterView: React.FC<SubstackNewsletterViewProps> = ({ content }) => {
  const [activeTab, setActiveTab] = useState<'newsletter' | 'structure' | 'images' | 'analytics'>('newsletter');
  const [selectedSubject, setSelectedSubject] = useState(0);

  // Parse content
  const newsletter: SubstackNewsletterContent = content.envelope?.content || content.content || content;
  const {
    subject = '',
    preheader = '',
    alt_subject_tests = [],
    markdown = '',
    sections = [],
    key_takeaways = [],
    resources = [],
    subscribe_cta = { text: '', link: '', placed_in_markdown: false },
    image_prompts = [],
    seo = {
      meta_title: '',
      meta_description: '',
      keywords_used: [],
      lsi_terms_used: []
    }
  } = newsletter;

  const allSubjects = [subject, ...alt_subject_tests];

  // Copy functions
  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
  };

  const copyMarkdown = () => {
    copyToClipboard(markdown);
  };

  const copySubjectLine = () => {
    copyToClipboard(allSubjects[selectedSubject]);
  };

  return (
    <div className="bg-white dark:bg-gray-900 rounded-3xl shadow-2xl max-w-7xl w-full max-h-[90vh] overflow-hidden flex flex-col">
      {/* Header */}
      <div className="bg-gradient-to-r from-orange-500 to-orange-600 text-white p-6">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold flex items-center">
              <EnvelopeIcon className="h-8 w-8 mr-3" />
              Substack Newsletter
            </h2>
            <p className="text-orange-100 mt-1">
              {subject || content.meta?.topic_title || 'Newsletter Content'}
            </p>
          </div>
          <div className="flex space-x-4 text-sm">
            <div className="text-center">
              <div className="text-2xl font-bold">{sections.length}</div>
              <div className="text-orange-100">Sections</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold">{key_takeaways.length}</div>
              <div className="text-orange-100">Takeaways</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold">{resources.length}</div>
              <div className="text-orange-100">Resources</div>
            </div>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex border-b border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800/50">
        {(['newsletter', 'structure', 'images', 'analytics'] as const).map((tab) => (
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
            {tab === 'newsletter' && <EnvelopeIcon className="h-4 w-4 inline mr-2" />}
            {tab === 'structure' && <DocumentTextIcon className="h-4 w-4 inline mr-2" />}
            {tab === 'images' && <PhotoIcon className="h-4 w-4 inline mr-2" />}
            {tab === 'analytics' && <MagnifyingGlassIcon className="h-4 w-4 inline mr-2" />}
            {tab}
          </button>
        ))}
      </div>

      {/* Content */}
      <div className="flex-1 overflow-y-auto p-6">
        {/* Newsletter Tab */}
        {activeTab === 'newsletter' && (
          <div className="space-y-6">
            {/* Subject Lines */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center justify-between">
                  <span className="flex items-center">
                    <EnvelopeIcon className="h-5 w-5 mr-2 text-orange-600 dark:text-orange-400" />
                    Subject Lines
                  </span>
                  <Button
                    variant="primary"
                    size="sm"
                    onClick={copySubjectLine}
                    leftIcon={<DocumentDuplicateIcon className="h-4 w-4" />}
                  >
                    Copy Subject
                  </Button>
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Preheader Text</p>
                  <p className="text-gray-600 dark:text-gray-400 italic">{preheader}</p>
                </div>

                {/* Subject Line Selector */}
                <div>
                  <label className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2 block">
                    Subject Line Versions:
                  </label>
                  <div className="space-y-2">
                    {allSubjects.map((subj, index) => (
                      <div
                        key={index}
                        onClick={() => setSelectedSubject(index)}
                        className={cn(
                          'p-3 rounded-lg cursor-pointer transition-all',
                          selectedSubject === index
                            ? 'bg-orange-100 dark:bg-orange-900/30 border-2 border-orange-500'
                            : 'bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 hover:border-orange-300'
                        )}
                      >
                        <div className="flex items-start justify-between">
                          <p className="text-gray-800 dark:text-gray-200 font-medium">
                            {subj}
                          </p>
                          <span className="text-xs text-gray-500 dark:text-gray-400 ml-2">
                            {index === 0 ? 'Main' : `Test ${index}`}
                          </span>
                        </div>
                        <p className="text-xs text-gray-600 dark:text-gray-400 mt-1">
                          {subj.length} chars
                        </p>
                      </div>
                    ))}
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Newsletter Content */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center justify-between">
                  <span className="flex items-center">
                    <DocumentTextIcon className="h-5 w-5 mr-2 text-orange-600 dark:text-orange-400" />
                    Newsletter Content
                  </span>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={copyMarkdown}
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
                    prose-h1:text-3xl prose-h1:font-bold prose-h1:mb-4
                    prose-h2:text-2xl prose-h2:font-semibold prose-h2:mt-8 prose-h2:mb-4 prose-h2:text-orange-600 dark:prose-h2:text-orange-400
                    prose-p:text-gray-700 dark:prose-p:text-gray-300 prose-p:leading-relaxed
                    prose-a:text-orange-600 dark:prose-a:text-orange-400 prose-a:no-underline hover:prose-a:underline
                    prose-ul:my-4 prose-ul:list-disc prose-ul:pl-6
                    prose-li:text-gray-700 dark:prose-li:text-gray-300
                    prose-em:text-gray-600 dark:prose-em:text-gray-400"
                  >
                    <ReactMarkdown remarkPlugins={[remarkGfm]}>
                      {markdown}
                    </ReactMarkdown>
                  </article>
                </div>
              </CardContent>
            </Card>

            {/* Subscribe CTA */}
            {subscribe_cta.text && (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <LinkIcon className="h-5 w-5 mr-2 text-indigo-600 dark:text-indigo-400" />
                    Subscribe Call-to-Action
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="bg-indigo-50 dark:bg-indigo-900/20 p-4 rounded-lg">
                    <p className="text-gray-700 dark:text-gray-300 mb-2">{subscribe_cta.text}</p>
                    <a 
                      href={subscribe_cta.link}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-indigo-600 dark:text-indigo-400 hover:underline text-sm"
                    >
                      {subscribe_cta.link}
                    </a>
                    {subscribe_cta.placed_in_markdown && (
                      <p className="text-xs text-gray-500 dark:text-gray-500 mt-2">
                        ✓ Already included in markdown
                      </p>
                    )}
                  </div>
                </CardContent>
              </Card>
            )}
          </div>
        )}

        {/* Structure Tab */}
        {activeTab === 'structure' && (
          <div className="space-y-6">
            {/* Sections */}
            <div className="space-y-4">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 flex items-center">
                <BookOpenIcon className="h-5 w-5 mr-2 text-orange-600 dark:text-orange-400" />
                Content Sections
              </h3>
              {sections.map((section, index) => (
                <Card key={index} className="border-l-4 border-orange-500">
                  <CardHeader>
                    <CardTitle className="text-lg">{section.h2}</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-3">
                    <p className="text-gray-700 dark:text-gray-300">{section.summary}</p>
                    {section.key_points.length > 0 && (
                      <div>
                        <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Key Points:</p>
                        <ul className="space-y-1">
                          {section.key_points.map((point, pointIndex) => (
                            <li key={pointIndex} className="flex items-start">
                              <CheckCircleIcon className="h-4 w-4 text-green-500 mr-2 mt-0.5 flex-shrink-0" />
                              <span className="text-sm text-gray-600 dark:text-gray-400">{point}</span>
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </CardContent>
                </Card>
              ))}
            </div>

            {/* Key Takeaways */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <LightBulbIcon className="h-5 w-5 mr-2 text-yellow-600 dark:text-yellow-400" />
                  Key Takeaways
                </CardTitle>
              </CardHeader>
              <CardContent>
                <ul className="space-y-2">
                  {key_takeaways.map((takeaway, index) => (
                    <li key={index} className="flex items-start">
                      <span className="text-yellow-600 dark:text-yellow-400 mr-2">•</span>
                      <span className="text-gray-700 dark:text-gray-300">{takeaway}</span>
                    </li>
                  ))}
                </ul>
              </CardContent>
            </Card>

            {/* Resources */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <LinkIcon className="h-5 w-5 mr-2 text-purple-600 dark:text-purple-400" />
                  Resources
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {resources.map((resource, index) => (
                    <div key={index} className="p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <a 
                            href={resource.url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="font-medium text-purple-600 dark:text-purple-400 hover:underline"
                          >
                            {resource.title}
                          </a>
                          <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                            {resource.note}
                          </p>
                        </div>
                        {resource.tracked && (
                          <span className="text-xs bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-300 px-2 py-1 rounded">
                            Tracked
                          </span>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
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
            {/* SEO Metadata */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <MagnifyingGlassIcon className="h-5 w-5 mr-2 text-green-600 dark:text-green-400" />
                  SEO Metadata
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Meta Title</p>
                  <p className="text-gray-700 dark:text-gray-300 font-mono text-sm bg-gray-100 dark:bg-gray-800 p-2 rounded">
                    {seo.meta_title}
                  </p>
                </div>
                <div>
                  <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Meta Description</p>
                  <p className="text-gray-700 dark:text-gray-300 font-mono text-sm bg-gray-100 dark:bg-gray-800 p-2 rounded">
                    {seo.meta_description}
                  </p>
                </div>
              </CardContent>
            </Card>

            {/* Keywords Analysis */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <BeakerIcon className="h-5 w-5 mr-2 text-purple-600 dark:text-purple-400" />
                  Keywords Analysis
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div>
                    <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Primary Keywords Used</p>
                    <div className="flex flex-wrap gap-2">
                      {seo.keywords_used.map((keyword, index) => (
                        <span
                          key={index}
                          className="px-3 py-1 bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-300 rounded-full text-sm"
                        >
                          {keyword}
                        </span>
                      ))}
                    </div>
                  </div>
                  <div>
                    <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">LSI Terms Used</p>
                    <div className="flex flex-wrap gap-2">
                      {seo.lsi_terms_used.map((term, index) => (
                        <span
                          key={index}
                          className="px-3 py-1 bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-300 rounded-full text-sm"
                        >
                          {term}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Newsletter Metrics */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <CheckCircleIcon className="h-5 w-5 mr-2 text-blue-600 dark:text-blue-400" />
                  Newsletter Metrics
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <div className="bg-blue-50 dark:bg-blue-900/20 p-4 rounded-lg text-center">
                    <p className="text-2xl font-bold text-gray-900 dark:text-gray-100">
                      {sections.length}
                    </p>
                    <p className="text-sm text-gray-600 dark:text-gray-400">Sections</p>
                  </div>
                  <div className="bg-green-50 dark:bg-green-900/20 p-4 rounded-lg text-center">
                    <p className="text-2xl font-bold text-gray-900 dark:text-gray-100">
                      {key_takeaways.length}
                    </p>
                    <p className="text-sm text-gray-600 dark:text-gray-400">Takeaways</p>
                  </div>
                  <div className="bg-purple-50 dark:bg-purple-900/20 p-4 rounded-lg text-center">
                    <p className="text-2xl font-bold text-gray-900 dark:text-gray-100">
                      {resources.length}
                    </p>
                    <p className="text-sm text-gray-600 dark:text-gray-400">Resources</p>
                  </div>
                  <div className="bg-orange-50 dark:bg-orange-900/20 p-4 rounded-lg text-center">
                    <p className="text-2xl font-bold text-gray-900 dark:text-gray-100">
                      {allSubjects.length}
                    </p>
                    <p className="text-sm text-gray-600 dark:text-gray-400">Subjects</p>
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
              <BookOpenIcon className="h-4 w-4 mr-1" />
              {sections.length} sections
            </span>
            <span className="flex items-center">
              <LightBulbIcon className="h-4 w-4 mr-1" />
              {key_takeaways.length} takeaways
            </span>
            <span className="flex items-center">
              <LinkIcon className="h-4 w-4 mr-1" />
              {resources.length} resources
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};
