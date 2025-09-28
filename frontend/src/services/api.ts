const API_BASE_URL = '/api';

export interface Topic {
  id: number;
  title: string;
  description: string;
  category: string;
  subcategory: string;
  company: string;
  technologies: string[];
  complexity_level: string;
  tags: string[];
  related_topics: number[];
  metrics: {
    scale: string;
    performance: string;
    reliability: string;
    latency: string;
  };
  implementation_details: {
    architecture: string;
    scaling: string;
    storage: string;
    caching: string;
    monitoring: string;
  };
  learning_objectives: string[];
  difficulty: number;
  estimated_read_time: string;
  prerequisites: string[];
  created_date: string;
  updated_date: string;
  processing_status?: string;
  error_message?: string;
}

export interface ProcessingStatus {
  is_processing: boolean;
  total_topics: number;
  processed_topics: number;
  current_batch: number;
  total_batches: number;
  current_topic: string;
  skipped_topics: number;
  skipped_titles: string[];
  errors: string[];
  event_log: string[];
}

export interface Stats {
  total_topics: number;
  status_breakdown: {
    completed: number;
    pending: number;
    failed: number;
  };
  category_breakdown: Record<string, number>;
  complexity_breakdown: Record<string, number>;
  daily_stats: Array<[string, number]>;
  company_breakdown: Record<string, number>;
}

class ApiService {
  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const url = `${API_BASE_URL}${endpoint}`;
    const response = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ error: 'Network error' }));
      throw new Error(error.error || `HTTP ${response.status}`);
    }

    return response.json();
  }

  private parseTopicJsonFields(topic: any): Topic {
    // Helper function to safely parse JSON strings
    const safeJsonParse = (jsonString: any, fallback: any = []) => {
      if (typeof jsonString === 'string') {
        try {
          return JSON.parse(jsonString);
        } catch {
          return fallback;
        }
      }
      return jsonString || fallback;
    };

    return {
      ...topic,
      technologies: safeJsonParse(topic.technologies, []),
      tags: safeJsonParse(topic.tags, []),
      related_topics: safeJsonParse(topic.related_topics, []),
      metrics: safeJsonParse(topic.metrics, {}),
      implementation_details: safeJsonParse(topic.implementation_details, {}),
      learning_objectives: safeJsonParse(topic.learning_objectives, []),
      prerequisites: safeJsonParse(topic.prerequisites, []),
    };
  }

  // Topics
  async getTopics(limit = 20, offset = 0, search = '', filters: {
    category?: string;
    subcategory?: string;
    status?: string;
    complexity?: string;
    company?: string;
    sortBy?: string;
    sortOrder?: string;
  } = {}): Promise<{ topics: Topic[]; total_count: number; limit: number; offset: number }> {
    const params = new URLSearchParams({
      limit: limit.toString(),
      offset: offset.toString(),
    });

    if (search) params.append('search', search);
    if (filters.category) params.append('category', filters.category);
    if (filters.subcategory) params.append('subcategory', filters.subcategory);
    if (filters.status) params.append('status', filters.status);
    if (filters.complexity) params.append('complexity', filters.complexity);
    if (filters.company) params.append('company', filters.company);
    if (filters.sortBy) params.append('sort_by', filters.sortBy);
    if (filters.sortOrder) params.append('sort_order', filters.sortOrder);

    const response = await this.request<{ topics: any[]; total_count: number; limit: number; offset: number }>(`/topics?${params.toString()}`);
    
    return {
      ...response,
      topics: response.topics.map(topic => this.parseTopicJsonFields(topic))
    };
  }

  async getAllTopics(): Promise<Topic[]> {
    // Fetch all topics by setting a very high limit
    const response = await this.request<any[]>('/topics?limit=10000&offset=0');
    return response.map(topic => this.parseTopicJsonFields(topic));
  }

  async getTopic(id: number): Promise<Topic> {
    const topic = await this.request<any>(`/topics/${id}`);
    return this.parseTopicJsonFields(topic);
  }

  async createTopics(topics: string[], batchSize = 3): Promise<{ message: string; total_topics: number }> {
    return this.request<{ message: string; total_topics: number }>('/topics', {
      method: 'POST',
      body: JSON.stringify({ topics, batch_size: batchSize }),
    });
  }

  async deleteTopic(id: number): Promise<{ message: string }> {
    return this.request<{ message: string }>(`/topics/${id}`, {
      method: 'DELETE',
    });
  }

  async retryTopic(id: number): Promise<{ message: string }> {
    return this.request<{ message: string }>(`/topics/${id}/retry`, {
      method: 'POST',
    });
  }

  // Status
  async getStatus(): Promise<ProcessingStatus> {
    return this.request<ProcessingStatus>('/status');
  }

  // Stats
  async getStats(): Promise<Stats> {
    return this.request<Stats>('/stats');
  }

  // Cleanup
  async cleanupFailedTopics(): Promise<{ success: boolean; message: string; cleaned_count: number }> {
    return this.request<{ success: boolean; message: string; cleaned_count: number }>('/cleanup-failed', {
      method: 'POST',
    });
  }

  // Processing Status
  async getProcessingStatus(): Promise<ProcessingStatus> {
    return this.request<ProcessingStatus>('/status');
  }

  // Topic Status Summary
  async getTopicStatusSummary(): Promise<{ success: boolean; summary: Record<string, number> }> {
    return this.request<{ success: boolean; summary: Record<string, number> }>('/topic-status-summary');
  }

  // Content Generation APIs
  async generateContent(request: {
    topicId: string;
    topicName: string;
    topicDescription: string;
    audience: string;
    tone: string;
    locale: string;
    primaryUrl: string;
    brand: {
      siteUrl: string;
      handles: Record<string, string>;
      utmBase: string;
    };
    targetPlatforms: string[];
    options: {
      include_images: boolean;
      max_length_levels: string;
      force: boolean;
      length_hint: number;
    };
  }): Promise<{ jobId: string; status: string; selected: Array<{ platform: string; format: string }> }> {
    return this.request('/content/generate-all', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  async getJobStatus(jobId: string): Promise<{
    job_id: string;
    status: string;
    created_at: string;
    progress?: { done: number; total: number };
  }> {
    return this.request(`/jobs/${jobId}`);
  }

  async getJobResults(jobId: string): Promise<{
    job_id: string;
    results: Array<{
      platform: string;
      format: string;
      envelope: { content: any };
    }>;
  }> {
    return this.request(`/results/${jobId}`);
  }

  async getResultsByTopic(topicId: string): Promise<{
    results: Array<{
      job_id: string;
      platform: string;
      format: string;
      topic_id: number;
      envelope: { content: any };
    }>;
  }> {
    return this.request(`/results/topic/${topicId}`);
  }
}

export const apiService = new ApiService();
