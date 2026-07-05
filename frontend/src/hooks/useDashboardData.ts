import { startTransition, useEffect, useMemo, useState } from "react";

import { api, isDemoModeEnabled } from "../api/client";
import type {
  AnalyticsSummary,
  GeneratedBoard,
  Outfit,
  PinterestBoard,
  Product,
  ScheduledPost,
  TrendingSummary
} from "../types/domain";

interface DashboardState {
  products: Product[];
  outfits: Outfit[];
  boards: GeneratedBoard[];
  scheduledPosts: ScheduledPost[];
  pinterestBoards: PinterestBoard[];
  analytics: AnalyticsSummary | null;
  trending: TrendingSummary | null;
  recommendedAesthetics: string[];
  demoMode: boolean;
}

const defaultState: DashboardState = {
  products: [],
  outfits: [],
  boards: [],
  scheduledPosts: [],
  pinterestBoards: [],
  analytics: null,
  trending: null,
  recommendedAesthetics: [],
  demoMode: false
};

export function useDashboardData() {
  const [state, setState] = useState<DashboardState>(defaultState);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const refresh = async () => {
    setLoading(true);
    setError(null);
    try {
      const [
        products,
        outfits,
        boards,
        scheduledPosts,
        analytics,
        trending,
        pinterestBoards,
        recommendedAesthetics
      ] = await Promise.all([
        api.listProducts(),
        api.listOutfits(),
        api.listBoards(),
        api.listScheduledPosts(),
        api.analytics(),
        api.trending(),
        api.listPinterestBoards(),
        api.recommendAesthetics()
      ]);
      startTransition(() => {
        setState((current) => ({
          ...current,
          products,
          outfits,
          boards,
          scheduledPosts,
          analytics,
          trending,
          pinterestBoards,
          recommendedAesthetics,
          demoMode: isDemoModeEnabled()
        }));
      });
    } catch (refreshError) {
      setError(refreshError instanceof Error ? refreshError.message : "Unable to load dashboard.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    void refresh();
  }, []);

  const boardLookup = useMemo(() => {
    return new Map(state.boards.map((board) => [board.id, board]));
  }, [state.boards]);

  return {
    ...state,
    boardLookup,
    loading,
    error,
    setBoards: (boards: GeneratedBoard[]) => setState((current) => ({ ...current, boards })),
    addBoard: (board: GeneratedBoard) =>
      setState((current) => ({ ...current, boards: [board, ...current.boards] })),
    addProduct: (product: Product) =>
      setState((current) => ({ ...current, products: [product, ...current.products] })),
    setOutfits: (outfits: Outfit[]) => setState((current) => ({ ...current, outfits })),
    addScheduledPost: (scheduledPost: ScheduledPost) =>
      setState((current) => ({
        ...current,
        scheduledPosts: [scheduledPost, ...current.scheduledPosts]
      })),
    addPinterestBoard: (board: PinterestBoard) =>
      setState((current) => ({ ...current, pinterestBoards: [board, ...current.pinterestBoards] })),
    refresh
  };
}
