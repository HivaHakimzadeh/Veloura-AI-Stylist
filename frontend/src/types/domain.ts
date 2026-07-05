export type ProductCategory =
  | "tops"
  | "bottoms"
  | "dresses"
  | "shoes"
  | "bags"
  | "jewelry"
  | "accessories";

export type CampaignType = "daily" | "weekly" | "seasonal";
export type ScheduleStatus = "draft" | "scheduled" | "published" | "failed";

export interface Product {
  id: number;
  user_id: number;
  title: string;
  category: ProductCategory;
  price: number;
  image_url: string;
  affiliate_link: string;
  color: string;
  style_tags: string[];
  brand: string;
  occasion_tags: string[];
  color_palette: string[];
  aesthetic: string;
  season: string;
  ai_summary: string;
  created_at: string;
  updated_at: string;
}

export interface ProductPayload {
  title: string;
  category?: ProductCategory;
  price: number;
  image_url: string;
  affiliate_link: string;
  color: string;
  style_tags: string[];
  brand: string;
  occasion_tags: string[];
  run_ai_tagging: boolean;
}

export interface ProductImportPreview {
  title: string;
  brand: string;
  price: number;
  image_url: string;
  affiliate_link: string;
  color: string;
  style_tags: string[];
  occasion_tags: string[];
  category?: ProductCategory;
}

export interface OutfitItem {
  id: number;
  slot: string;
  product: Product;
}

export interface Outfit {
  id: number;
  user_id: number;
  title: string;
  description: string;
  keywords: string[];
  pinterest_seo_title: string;
  pinterest_description: string;
  suggested_board_name: string;
  aesthetic: string;
  season: string;
  occasion: string;
  status: string;
  items: OutfitItem[];
  created_at: string;
  updated_at: string;
}

export interface GeneratedBoard {
  id: number;
  outfit_id: number;
  title: string;
  image_url: string;
  storage_key: string;
  status: string;
  width: number;
  height: number;
  created_at: string;
  updated_at: string;
}

export interface ScheduledPost {
  id: number;
  generated_board_id: number;
  pinterest_board_id: number | null;
  campaign_type: CampaignType;
  scheduled_for: string;
  status: ScheduleStatus;
  caption: string;
  hashtags: string[];
  affiliate_earnings: number;
  created_at: string;
  updated_at: string;
}

export interface PinterestBoard {
  id: number;
  user_id: number;
  name: string;
  remote_id: string;
  description: string;
  created_at: string;
  updated_at: string;
}

export interface AnalyticsSummary {
  total_products: number;
  total_outfits: number;
  total_boards: number;
  scheduled_posts: number;
  published_posts: number;
  total_impressions: number;
  total_clicks: number;
  total_saves: number;
  estimated_affiliate_earnings: number;
  top_aesthetics: Array<{ name: string; count: number }>;
  trending_keywords: string[];
}

export interface TrendingSummary {
  aesthetics: string[];
  keywords: string[];
  occasions: string[];
}
