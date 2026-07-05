import type {
  AnalyticsSummary,
  GeneratedBoard,
  Outfit,
  PinterestBoard,
  Product,
  ProductPayload,
  ScheduledPost,
  TrendingSummary
} from "../types/domain";

const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000/api/v1";
const API_ORIGIN = API_URL.replace(/\/api\/v1\/?$/, "");

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers ?? {})
    },
    ...init
  });

  if (!response.ok) {
    const detail = await response.text();
    throw new Error(detail || "Request failed");
  }

  if (response.status === 204) {
    return undefined as T;
  }

  return (await response.json()) as T;
}

export const api = {
  listProducts: () => request<Product[]>("/products/"),
  createProduct: (payload: ProductPayload) =>
    request<Product>("/products/", { method: "POST", body: JSON.stringify(payload) }),
  generateOutfits: (aesthetics: string[]) =>
    request<Outfit[]>("/outfits/generate", {
      method: "POST",
      body: JSON.stringify({ aesthetics, max_outfits: aesthetics.length })
    }),
  listOutfits: () => request<Outfit[]>("/outfits/"),
  listBoards: () => request<GeneratedBoard[]>("/boards/"),
  recommendAesthetics: () => request<string[]>("/outfits/recommendations"),
  generateBoard: (outfitId: number) =>
    request<GeneratedBoard>("/boards/generate", {
      method: "POST",
      body: JSON.stringify({ outfit_id: outfitId })
    }),
  listScheduledPosts: () => request<ScheduledPost[]>("/schedule/"),
  createScheduledPost: (payload: {
    generated_board_id: number;
    pinterest_board_id?: number | null;
    campaign_type: string;
    scheduled_for: string;
    caption: string;
    hashtags: string[];
  }) => request<ScheduledPost>("/schedule/", { method: "POST", body: JSON.stringify(payload) }),
  autofillCaption: (generatedBoardId: number) =>
    request<{ caption: string; hashtags: string[] }>(`/schedule/autofill-caption/${generatedBoardId}`, {
      method: "POST"
    }),
  analytics: () => request<AnalyticsSummary>("/analytics/"),
  trending: () => request<TrendingSummary>("/analytics/trending"),
  listPinterestBoards: () => request<PinterestBoard[]>("/pinterest/boards"),
  createPinterestBoard: (payload: { name: string; description: string }) =>
    request<PinterestBoard>("/pinterest/boards", { method: "POST", body: JSON.stringify(payload) })
};

export function resolveAssetUrl(path: string) {
  return path.startsWith("/static/") ? `${API_ORIGIN}${path}` : path;
}
