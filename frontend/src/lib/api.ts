/** API client for communicating with FastAPI backend. */

import axios, { AxiosError } from 'axios';

// Get API URL - use relative path in production, localhost in development
const getApiUrl = (): string => {
  // If NEXT_PUBLIC_API_URL is explicitly set, use it (should be base URL without /api)
  if (process.env.NEXT_PUBLIC_API_URL) {
    // Remove trailing /api if present to avoid double /api/api/
    let url = process.env.NEXT_PUBLIC_API_URL;
    if (url.endsWith('/api')) {
      url = url.slice(0, -4);
    }
    return url;
  }
  
  // In browser (client-side)
  if (typeof window !== 'undefined') {
    // If hostname is localhost, use localhost backend
    if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
      return 'http://localhost:8000';
    }
    // Otherwise, we're in production - use relative path (same domain)
    return '';
  }
  
  // Server-side: check NODE_ENV
  if (process.env.NODE_ENV === 'production') {
    return ''; // Relative path in production
  }
  
  // Server-side development
  return 'http://localhost:8000';
};

export interface GenerationSettings {
    model: string;
    maxIterations: number;
    viralityThreshold: number;
}

export interface GenerateRequest {
    topic: string;
    platform: 'twitter' | 'linkedin';
    settings: GenerationSettings;
}

export interface ResearchAngle {
    title: string;
    why_viral: string;
    summary: string;
    sources: string[];
}

export interface GenerateResponse {
    final_content: string;
    virality_score: number;
    iterations: number;
    elapsed_time: number;
    drafts: string[];
    scores: number[];
    research_angles: ResearchAngle[];
    feedbacks: string[];
    status: string;
}

export interface HealthResponse {
    status: string;
    message: string;
}

export interface ModelsResponse {
    models: string[];
}

class APIClient {
    private getBaseURL(): string {
        return getApiUrl();
    }

    async healthCheck(): Promise<HealthResponse> {
        try {
            const response = await axios.get<HealthResponse>(`${this.getBaseURL()}/api/health`);
            return response.data;
        } catch (error) {
            throw this.handleError(error);
        }
    }

    async getModels(): Promise<string[]> {
        try {
            const response = await axios.get<ModelsResponse>(`${this.getBaseURL()}/api/models`);
            return response.data.models;
        } catch (error) {
            throw this.handleError(error);
        }
    }

    async generateContent(request: GenerateRequest): Promise<GenerateResponse> {
        try {
            const response = await axios.post<GenerateResponse>(
                `${this.getBaseURL()}/api/generate`,
                request,
                {
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    timeout: 120000, // 2 minute timeout
                }
            );
            return response.data;
        } catch (error) {
            throw this.handleError(error);
        }
    }

    private handleError(error: unknown): Error {
        if (axios.isAxiosError(error)) {
            const axiosError = error as AxiosError<{ detail: string }>;
            if (axiosError.response) {
                return new Error(
                    axiosError.response.data?.detail ||
                    `API Error: ${axiosError.response.status}`
                );
            } else if (axiosError.request) {
                return new Error('No response from server. Please check if the backend is running.');
            }
        }
        return error instanceof Error ? error : new Error('Unknown error occurred');
    }
}

export const apiClient = new APIClient();
