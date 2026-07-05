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
import { demoApi } from "../lib/demoApi";

const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000/api/v1";
const API_ORIGIN = API_URL.replace(/\/api\/v1\/?$/, "");
let demoModeEnabled = false;

class ApiUnavailableError extends Error {
  constructor(message = "Backend unavailable.") {
    super(message);
    this.name = "ApiUnavailableError";
  }
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  let response: Response;
  try {
    response = await fetch(`${API_URL}${path}`, {
      headers: {
        "Content-Type": "application/json",
        ...(init?.headers ?? {})
      },
      ...init
    });
  } catch (_error) {
    throw new ApiUnavailableError();
  }

  if (!response.ok) {
    const detail = await response.text();
    const contentType = response.headers.get("content-type") ?? "";
    if (response.status >= 500 || (response.status === 404 && contentType.includes("text/html"))) {
      throw new ApiUnavailableError();
    }
    throw new Error(detail || "Request failed");
  }

  if (response.status === 204) {
    return undefined as T;
  }

  return (await response.json()) as T;
}

async function withFallback<T>(remote: () => Promise<T>, fallback: () => T | Promise<T>): Promise<T> {
  try {
    const result = await remote();
    demoModeEnabled = false;
    return result;
  } catch (error) {
    if (error instanceof ApiUnavailableError) {
      demoModeEnabled = true;
      return await fallback();
    }
    throw error;
  }
}

export const api = {
  listProducts: () => withFallback(() => request<Product[]>("/products/"), () => demoApi.listProducts()),
  createProduct: (payload: ProductPayload) =>
    withFallback(
      () => request<Product>("/products/", { method: "POST", body: JSON.stringify(payload) }),
      () => demoApi.createProduct(payload)
    ),
  generateOutfits: (aesthetics: string[]) =>
    withFallback(
      () =>
        request<Outfit[]>("/outfits/generate", {
          method: "POST",
          body: JSON.stringify({ aesthetics, max_outfits: aesthetics.length })
        }),
      () => demoApi.generateOutfits(aesthetics)
    ),
  listOutfits: () => withFallback(() => request<Outfit[]>("/outfits/"), () => demoApi.listOutfits()),
  listBoards: () => withFallback(() => request<GeneratedBoard[]>("/boards/"), () => demoApi.listBoards()),
  recommendAesthetics: () =>
    withFallback(() => request<string[]>("/outfits/recommendations"), () => demoApi.recommendAesthetics()),
  generateBoard: (outfitId: number) =>
    withFallback(
      () =>
        request<GeneratedBoard>("/boards/generate", {
          method: "POST",
          body: JSON.stringify({ outfit_id: outfitId })
        }),
      () => demoApi.generateBoard(outfitId)
    ),
  listScheduledPosts: () =>
    withFallback(() => request<ScheduledPost[]>("/schedule/"), () => demoApi.listScheduledPosts()),
  createScheduledPost: (payload: {
    generated_board_id: number;
    pinterest_board_id?: number | null;
    campaign_type: string;
    scheduled_for: string;
    caption: string;
    hashtags: string[];
  }) =>
    withFallback(
      () => request<ScheduledPost>("/schedule/", { method: "POST", body: JSON.stringify(payload) }),
      () => demoApi.createScheduledPost(payload)
    ),
  autofillCaption: (generatedBoardId: number) =>
    withFallback(
      () =>
        request<{ caption: string; hashtags: string[] }>(`/schedule/autofill-caption/${generatedBoardId}`, {
          method: "POST"
        }),
      () => demoApi.autofillCaption(generatedBoardId)
    ),
  analytics: () => withFallback(() => request<AnalyticsSummary>("/analytics/"), () => demoApi.analytics()),
  trending: () => withFallback(() => request<TrendingSummary>("/analytics/trending"), () => demoApi.trending()),
  listPinterestBoards: () =>
    withFallback(() => request<PinterestBoard[]>("/pinterest/boards"), () => demoApi.listPinterestBoards()),
  createPinterestBoard: (payload: { name: string; description: string }) =>
    withFallback(
      () => request<PinterestBoard>("/pinterest/boards", { method: "POST", body: JSON.stringify(payload) }),
      () => demoApi.createPinterestBoard(payload)
    )
};

export function resolveAssetUrl(path: string) {
  return path.startsWith("/static/") ? `${API_ORIGIN}${path}` : path;
}

export function isDemoModeEnabled() {
  return demoModeEnabled;
}
