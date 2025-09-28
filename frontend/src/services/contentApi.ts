/**
 * Content Generation API Service
 * Handles communication with the FastAPI content generation service
 */

export interface ContentGenerationRequest {
  topicId: string;
  topicName: string;
  topicDescription: string;
  audience: 'beginners' | 'intermediate' | 'advanced';
  tone: string;
  locale: 'en' | 'hi' | 'en-hi';
  primaryUrl: string;
  brand: {
    siteUrl: string;
    handles: {
      instagram?: string;
      x?: string;
      linkedin?: string;
      youtube?: string;
      github?: string;
    };
    utmBase: string;
  };
  targetPlatforms: string[];
  options: {
    include_images: boolean;
    max_length_levels: 'compact' | 'standard' | 'detailed';
    force: boolean;
    length_hint: number;
  };
}

export interface JobResponse {
  jobId: string;
  status: 'running' | 'done' | 'error';
  selected: Array<{
    platform: string;
    format: string;
  }>;
}

export interface JobStatusResponse {
  jobId: string;
  status: 'running' | 'done' | 'error';
  progress: {
    total: number;
    done: number;
  };
  errors?: Array<{
    taskId: string;
    platform: string;
    format: string;
    message: string;
  }>;
}

export interface ContentResult {
  platform: string;
  format: string;
  envelope: {
    meta: any;
    content: any;
  };
}

export interface ResultsResponse {
  jobId: string;
  status: 'done' | 'error';
  results: ContentResult[];
  errors: any[];
}

class ContentApiService {
  private baseUrl = '/content-api';

  /**
   * Generate content for multiple platforms
   */
  async generateAllContent(request: ContentGenerationRequest): Promise<JobResponse> {
    const response = await fetch(`${this.baseUrl}/content/generate-all`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      throw new Error(`Content generation failed: ${response.statusText}`);
    }

    return response.json();
  }

  /**
   * Get job status
   */
  async getJobStatus(jobId: string): Promise<JobStatusResponse> {
    const response = await fetch(`${this.baseUrl}/jobs/${jobId}`);

    if (!response.ok) {
      throw new Error(`Failed to get job status: ${response.statusText}`);
    }

    return response.json();
  }

  /**
   * Get job results
   */
  async getJobResults(jobId: string): Promise<ResultsResponse> {
    const response = await fetch(`${this.baseUrl}/results/${jobId}`);

    if (!response.ok) {
      throw new Error(`Failed to get job results: ${response.statusText}`);
    }

    return response.json();
  }

  /**
   * Generate content for a specific platform
   */
  async generatePlatformContent(
    platform: string,
    format: string,
    request: Omit<ContentGenerationRequest, 'targetPlatforms'>
  ): Promise<any> {
    const response = await fetch(`${this.baseUrl}/content/${platform}/${format}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      throw new Error(`Platform content generation failed: ${response.statusText}`);
    }

    return response.json();
  }

  /**
   * Health check
   */
  async healthCheck(): Promise<{ status: string }> {
    const response = await fetch(`${this.baseUrl}/health`);
    
    if (!response.ok) {
      throw new Error(`Health check failed: ${response.statusText}`);
    }

    return response.json();
  }
}

export const contentApiService = new ContentApiService();
