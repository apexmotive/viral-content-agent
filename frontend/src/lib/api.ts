/** API client for communicating with FastAPI backend. */

import axios, { AxiosError } from 'axios';

// Use relative path in production (same domain), localhost in development
// In production on Vercel, API routes are on the same domain
// In development, use localhost backend
const getApiUrl = () => {
  // If NEXT_PUBLIC_API_URL is explicitly set, use it
  if (process.env.NEXT_PUBLIC_API_URL) {
    return process.env.NEXT_PUBLIC_API_URL;
  }
  // In browser (production), use relative path
  if (typeof window !== 'undefined') {
    return '';
  }
  // In server-side (development), use localhost
  return 'http://localhost:8000';
};

const API_URL = getApiUrl();

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
    private baseURL: string;

    constructor() {
        this.baseURL = API_URL;
    }

    async healthCheck(): Promise<HealthResponse> {
        try {
            const response = await axios.get<HealthResponse>(`${this.baseURL}/api/health`);
            return response.data;
        } catch (error) {
            throw this.handleError(error);
        }
    }

    async getModels(): Promise<string[]> {
        try {
            const response = await axios.get<ModelsResponse>(`${this.baseURL}/api/models`);
            return response.data.models;
        } catch (error) {
            throw this.handleError(error);
        }
    }

    async generateContent(request: GenerateRequest): Promise<GenerateResponse> {
        try {
            const response = await axios.post<GenerateResponse>(
                `${this.baseURL}/api/generate`,
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
