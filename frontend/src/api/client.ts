import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL ?? "http://localhost:8000",
  timeout: 8000
});

export interface PluginSummary {
  name: string;
  version: string;
  description: string;
  tags: string[];
  latest_run_at?: string | null;
}

export interface PluginManifest {
  name: string;
  version: string;
  description: string;
  authors: string[];
  entrypoint: string;
  created_at: string;
  updated_at: string;
  inputs: Array<{
    name: string;
    description: string;
    media_type: string;
    optional?: boolean;
  }>;
  outputs: Array<{
    name: string;
    description: string;
    media_type: string;
  }>;
  tags: string[];
  provenance: {
    container_image: string;
    container_digest?: string | null;
    repository_url?: string | null;
    reference?: string | null;
  };
  resources?: Record<string, string> | null;
}

export const fetchPlugins = async (): Promise<PluginSummary[]> => {
  const response = await api.get<PluginSummary[]>("/api/v1/plugins/");
  return response.data;
};

export const fetchPlugin = async (name: string): Promise<PluginManifest> => {
  const response = await api.get<PluginManifest>(`/api/v1/plugins/${name}`);
  return response.data;
};

export default api;
