import type {
  AnalyticsSummary,
  CampaignType,
  GeneratedBoard,
  Outfit,
  OutfitItem,
  PinterestBoard,
  Product,
  ProductImportPreview,
  ProductCategory,
  ProductPayload,
  ScheduledPost,
  TrendingSummary
} from "../types/domain";

interface DemoState {
  products: Product[];
  outfits: Outfit[];
  boards: GeneratedBoard[];
  scheduledPosts: ScheduledPost[];
  pinterestBoards: PinterestBoard[];
  counters: Record<string, number>;
}

const STORAGE_KEY = "veloura-demo-state-v1";

function nowIso() {
  return new Date().toISOString();
}

function compactText(value: string, maxLength: number) {
  return value.length > maxLength ? `${value.slice(0, maxLength - 1)}…` : value;
}

function svgDataUri(title: string, subtitle: string, accent = "#9c5f50", background = "#f6eee4") {
  const safeTitle = compactText(title, 36);
  const safeSubtitle = compactText(subtitle, 28);
  const svg = `
    <svg xmlns="http://www.w3.org/2000/svg" width="1000" height="1500" viewBox="0 0 1000 1500">
      <rect width="1000" height="1500" rx="48" fill="${background}" />
      <rect x="52" y="52" width="896" height="1396" rx="40" fill="#fffaf5" stroke="${accent}" stroke-width="4" />
      <circle cx="170" cy="170" r="72" fill="${accent}" opacity="0.15" />
      <circle cx="820" cy="1280" r="96" fill="${accent}" opacity="0.12" />
      <text x="86" y="120" font-family="Georgia, serif" font-size="36" fill="${accent}">Veloura</text>
      <text x="86" y="190" font-family="Georgia, serif" font-size="48" fill="#2e2018">${safeTitle}</text>
      <text x="86" y="238" font-family="Arial, sans-serif" font-size="24" fill="#7a6758">${safeSubtitle}</text>
      <rect x="86" y="320" width="360" height="460" rx="32" fill="#eadbcf" />
      <rect x="554" y="320" width="360" height="460" rx="32" fill="#e6d6ca" />
      <rect x="86" y="860" width="360" height="460" rx="32" fill="#efe3d7" />
      <rect x="554" y="860" width="360" height="460" rx="32" fill="#f3e9df" />
      <text x="266" y="560" text-anchor="middle" font-family="Arial, sans-serif" font-size="28" fill="#7b5b3d">Curated Piece</text>
      <text x="734" y="560" text-anchor="middle" font-family="Arial, sans-serif" font-size="28" fill="#7b5b3d">Pinned Look</text>
      <text x="266" y="1100" text-anchor="middle" font-family="Arial, sans-serif" font-size="28" fill="#7b5b3d">Amazon Find</text>
      <text x="734" y="1100" text-anchor="middle" font-family="Arial, sans-serif" font-size="28" fill="#7b5b3d">Veloura Mood</text>
    </svg>
  `;
  return `data:image/svg+xml;charset=UTF-8,${encodeURIComponent(svg)}`;
}

function makeSeedProduct(
  id: number,
  title: string,
  category: ProductCategory,
  color: string,
  brand: string,
  aesthetic: string,
  season: string,
  styleTags: string[],
  occasionTags: string[],
  price: number
): Product {
  const stamp = nowIso();
  return {
    id,
    user_id: 1,
    title,
    category,
    price,
    image_url: svgDataUri(title, `${brand} • $${price.toFixed(2)}`),
    affiliate_link: "https://www.amazon.com/",
    color,
    style_tags: styleTags,
    brand,
    occasion_tags: occasionTags,
    color_palette: [color, "Ivory", "Camel"],
    aesthetic,
    season,
    ai_summary: `${title} is tagged for ${aesthetic.toLowerCase()} styling with a ${color.toLowerCase()} palette.`,
    created_at: stamp,
    updated_at: stamp
  };
}

function createInitialState(): DemoState {
  const products = [
    makeSeedProduct(1, "Linen Blazer", "tops", "Beige", "Veloura House", "Old Money", "Summer", ["tailored", "classic"], ["office"], 89.99),
    makeSeedProduct(2, "Pleated Wide-Leg Trousers", "bottoms", "Cream", "Veloura House", "Office Chic", "All Season", ["structured", "polished"], ["office"], 64.99),
    makeSeedProduct(3, "Leather Slingback Heels", "shoes", "Black", "Maison North", "Date Night", "All Season", ["sleek", "elevated"], ["date night"], 72.0),
    makeSeedProduct(4, "Structured Mini Tote", "bags", "Brown", "Maison North", "Clean Girl", "All Season", ["minimal", "refined"], ["everyday"], 58.5),
    makeSeedProduct(5, "Gold Statement Hoops", "jewelry", "Gold", "Aurelia Studio", "Clean Girl", "All Season", ["minimal", "polished"], ["everyday"], 24.0),
    makeSeedProduct(6, "Ribbed Knit Midi Dress", "dresses", "White", "Veloura House", "Summer Vacation", "Summer", ["breezy", "minimal"], ["vacation"], 76.0),
    makeSeedProduct(7, "Oversized Sunglasses", "accessories", "Tortoise", "Aurelia Studio", "Old Money", "Summer", ["classic", "resort"], ["vacation"], 28.0)
  ];

  const pinterestBoardStamp = nowIso();
  return {
    products,
    outfits: [],
    boards: [],
    scheduledPosts: [],
    pinterestBoards: [
      {
        id: 1,
        user_id: 1,
        name: "Veloura Aesthetic Edits",
        remote_id: "demo-board-1",
        description: "High-performing fashion collages and affiliate outfit inspiration.",
        created_at: pinterestBoardStamp,
        updated_at: pinterestBoardStamp
      }
    ],
    counters: {
      product: 7,
      outfit: 0,
      outfitItem: 0,
      board: 0,
      scheduledPost: 0,
      pinterestBoard: 1
    }
  };
}

function canUseStorage() {
  return typeof window !== "undefined" && typeof window.localStorage !== "undefined";
}

function readState(): DemoState {
  if (!canUseStorage()) {
    return createInitialState();
  }
  const raw = window.localStorage.getItem(STORAGE_KEY);
  if (!raw) {
    const initial = createInitialState();
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(initial));
    return initial;
  }
  return JSON.parse(raw) as DemoState;
}

function writeState(state: DemoState) {
  if (canUseStorage()) {
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
  }
}

function nextId(state: DemoState, key: keyof DemoState["counters"]) {
  state.counters[key] += 1;
  return state.counters[key];
}

function inferCategory(title: string): ProductCategory {
  const text = title.toLowerCase();
  if (/(dress|gown)/.test(text)) return "dresses";
  if (/(heel|loafer|sneaker|boot|shoe|sandal)/.test(text)) return "shoes";
  if (/(bag|tote|clutch|crossbody|purse)/.test(text)) return "bags";
  if (/(earring|ring|necklace|bracelet|hoop)/.test(text)) return "jewelry";
  if (/(belt|hat|scarf|sunglasses|watch)/.test(text)) return "accessories";
  if (/(pant|trouser|jean|short|skirt)/.test(text)) return "bottoms";
  return "tops";
}

function inferAesthetic(styleTags: string[], title: string) {
  const text = `${styleTags.join(" ")} ${title}`.toLowerCase();
  if (/(tailored|classic|linen|camel)/.test(text)) return "Old Money";
  if (/(work|office|structured|polished|blazer)/.test(text)) return "Office Chic";
  if (/(glam|sleek|silk|heel)/.test(text)) return "Date Night";
  if (/(beach|breezy|resort|vacation)/.test(text)) return "Summer Vacation";
  return "Clean Girl";
}

function inferSeason(title: string, styleTags: string[]) {
  const text = `${title} ${styleTags.join(" ")}`.toLowerCase();
  if (/(linen|breezy|resort|sandals|vacation)/.test(text)) return "Summer";
  if (/(knit|boot|coat|wool)/.test(text)) return "Fall";
  return "All Season";
}

function inferOccasion(occasionTags: string[]) {
  const text = occasionTags.join(" ").toLowerCase();
  if (text.includes("office")) return "Office";
  if (text.includes("date")) return "Date Night";
  if (text.includes("vacation")) return "Vacation";
  return "Everyday";
}

function findProductsForOutfit(products: Product[]) {
  const byCategory = {
    tops: products.find((item) => item.category === "tops"),
    bottoms: products.find((item) => item.category === "bottoms"),
    dresses: products.find((item) => item.category === "dresses"),
    shoes: products.find((item) => item.category === "shoes"),
    bags: products.find((item) => item.category === "bags"),
    jewelry: products.find((item) => item.category === "jewelry"),
    accessories: products.find((item) => item.category === "accessories")
  };

  const selected: Array<{ slot: string; product: Product }> = [];
  if (byCategory.dresses) {
    selected.push({ slot: "dress", product: byCategory.dresses });
  } else if (byCategory.tops && byCategory.bottoms) {
    selected.push({ slot: "top", product: byCategory.tops });
    selected.push({ slot: "bottom", product: byCategory.bottoms });
  }

  if (byCategory.shoes) selected.push({ slot: "shoes", product: byCategory.shoes });
  if (byCategory.bags) selected.push({ slot: "bag", product: byCategory.bags });
  if (byCategory.jewelry) selected.push({ slot: "jewelry", product: byCategory.jewelry });
  if (byCategory.accessories) selected.push({ slot: "accessory", product: byCategory.accessories });

  return selected;
}

function outfitItems(state: DemoState, products: Array<{ slot: string; product: Product }>): OutfitItem[] {
  return products.map(({ slot, product }) => ({
    id: nextId(state, "outfitItem"),
    slot,
    product
  }));
}

function buildAnalytics(state: DemoState): AnalyticsSummary {
  const topAestheticsMap = state.products.reduce<Record<string, number>>((accumulator, product) => {
    accumulator[product.aesthetic] = (accumulator[product.aesthetic] ?? 0) + 1;
    return accumulator;
  }, {});

  const keywordMap = state.products.flatMap((product) => product.style_tags).reduce<Record<string, number>>((accumulator, keyword) => {
    accumulator[keyword] = (accumulator[keyword] ?? 0) + 1;
    return accumulator;
  }, {});

  return {
    total_products: state.products.length,
    total_outfits: state.outfits.length,
    total_boards: state.boards.length,
    scheduled_posts: state.scheduledPosts.filter((post) => post.status === "scheduled").length,
    published_posts: state.scheduledPosts.filter((post) => post.status === "published").length,
    total_impressions: state.scheduledPosts.length * 840,
    total_clicks: state.scheduledPosts.length * 63,
    total_saves: state.scheduledPosts.length * 28,
    estimated_affiliate_earnings: Number(
      state.scheduledPosts.reduce((sum, post) => sum + post.affiliate_earnings, 0).toFixed(2)
    ),
    top_aesthetics: Object.entries(topAestheticsMap)
      .sort((left, right) => right[1] - left[1])
      .slice(0, 5)
      .map(([name, count]) => ({ name, count })),
    trending_keywords: Object.entries(keywordMap)
      .sort((left, right) => right[1] - left[1])
      .slice(0, 8)
      .map(([keyword]) => keyword)
  };
}

function buildTrending(state: DemoState): TrendingSummary {
  const aesthetics = Array.from(new Set(state.products.map((item) => item.aesthetic))).slice(0, 5);
  const keywords = Array.from(new Set(state.products.flatMap((item) => item.style_tags))).slice(0, 10);
  const occasions = Array.from(new Set(state.products.flatMap((item) => item.occasion_tags))).slice(0, 5);
  return { aesthetics, keywords, occasions };
}

export const demoApi = {
  listProducts() {
    return readState().products;
  },

  deleteProduct(productId: number) {
    const state = readState();
    state.products = state.products.filter((product) => product.id !== productId);
    writeState(state);
  },

  importProductFromUrl(payload: { url: string; affiliate_link?: string }): ProductImportPreview {
    let slug = "";
    try {
      const parsed = new URL(payload.url);
      slug =
        parsed.pathname
          .split("/")
          .filter(Boolean)
          .pop()
          ?.replace(/[-_]+/g, " ")
          .replace(/\.[a-z0-9]+$/i, "")
          .trim() ?? "";
    } catch (_error) {
      slug = "";
    }
    const title = slug
      ? slug.replace(/\b\w/g, (character) => character.toUpperCase())
      : "Imported Fashion Product";
    const category = inferCategory(title);
    return {
      title,
      brand: "Imported Brand",
      price: 79.99,
      image_url: svgDataUri(title, "Imported preview"),
      affiliate_link: payload.affiliate_link || payload.url,
      color: "Neutral",
      style_tags: ["versatile"],
      occasion_tags: ["everyday"],
      category
    };
  },

  createProduct(payload: ProductPayload) {
    const state = readState();
    const timestamp = nowIso();
    const category = payload.category ?? inferCategory(payload.title);
    const aesthetic = inferAesthetic(payload.style_tags, payload.title);
    const season = inferSeason(payload.title, payload.style_tags);
    const product: Product = {
      id: nextId(state, "product"),
      user_id: 1,
      title: payload.title,
      category,
      price: payload.price,
      image_url: payload.image_url || svgDataUri(payload.title, payload.brand),
      affiliate_link: payload.affiliate_link,
      color: payload.color,
      style_tags: payload.style_tags,
      brand: payload.brand,
      occasion_tags: payload.occasion_tags,
      color_palette: [payload.color, "Ivory", "Camel"],
      aesthetic,
      season,
      ai_summary: `${payload.title} is ready for ${aesthetic.toLowerCase()} styling in the Veloura demo mode.`,
      created_at: timestamp,
      updated_at: timestamp
    };
    state.products.unshift(product);
    writeState(state);
    return product;
  },

  listOutfits() {
    return readState().outfits;
  },

  listBoards() {
    return readState().boards;
  },

  listScheduledPosts() {
    return readState().scheduledPosts;
  },

  listPinterestBoards() {
    return readState().pinterestBoards;
  },

  recommendAesthetics() {
    return Array.from(new Set(readState().products.map((product) => product.aesthetic))).slice(0, 6);
  },

  generateOutfits(aesthetics: string[]) {
    const state = readState();
    const selection = findProductsForOutfit(state.products);
    const generated = aesthetics.map((aesthetic) => {
      const timestamp = nowIso();
      const items = outfitItems(state, selection);
      const outfit: Outfit = {
        id: nextId(state, "outfit"),
        user_id: 1,
        title: `${aesthetic} Edit`,
        description: `A ${aesthetic.toLowerCase()} outfit generated in demo mode with affiliate-ready styling and Pinterest-friendly copy.`,
        keywords: [aesthetic.toLowerCase(), "amazon fashion", "outfit ideas", "veloura"],
        pinterest_seo_title: `${aesthetic} Outfit Ideas with Amazon Fashion Finds`,
        pinterest_description: `Save this ${aesthetic.toLowerCase()} outfit for your next fashion mood board.`,
        suggested_board_name: `${aesthetic} Mood`,
        aesthetic,
        season: selection[0]?.product.season ?? "All Season",
        occasion: selection[0]?.product.occasion_tags[0] ?? "Everyday",
        status: "generated",
        items,
        created_at: timestamp,
        updated_at: timestamp
      };
      return outfit;
    });
    state.outfits = [...generated, ...state.outfits];
    writeState(state);
    return generated;
  },

  generateBoard(outfitId: number) {
    const state = readState();
    const outfit = state.outfits.find((item) => item.id === outfitId);
    if (!outfit) {
      throw new Error("Outfit not found.");
    }
    const timestamp = nowIso();
    const board: GeneratedBoard = {
      id: nextId(state, "board"),
      outfit_id: outfitId,
      title: `${outfit.title} Board`,
      image_url: svgDataUri(outfit.title, outfit.aesthetic, "#7b5b3d", "#f7f1ea"),
      storage_key: `demo-board-${outfitId}`,
      status: "generated",
      width: 1000,
      height: 1500,
      created_at: timestamp,
      updated_at: timestamp
    };
    state.boards.unshift(board);
    writeState(state);
    return board;
  },

  createScheduledPost(payload: {
    generated_board_id: number;
    pinterest_board_id?: number | null;
    campaign_type: string;
    scheduled_for: string;
    caption: string;
    hashtags: string[];
  }) {
    const state = readState();
    const board = state.boards.find((item) => item.id === payload.generated_board_id);
    if (!board) {
      throw new Error("Generated board not found.");
    }
    const timestamp = nowIso();
    const campaignType = payload.campaign_type as CampaignType;
    const scheduledPost: ScheduledPost = {
      id: nextId(state, "scheduledPost"),
      generated_board_id: payload.generated_board_id,
      pinterest_board_id: payload.pinterest_board_id ?? null,
      campaign_type: campaignType,
      scheduled_for: payload.scheduled_for,
      status: "scheduled",
      caption: payload.caption,
      hashtags: payload.hashtags,
      affiliate_earnings: Number((14.5 + state.scheduledPosts.length * 3.2).toFixed(2)),
      created_at: timestamp,
      updated_at: timestamp
    };
    state.scheduledPosts.unshift(scheduledPost);
    writeState(state);
    return scheduledPost;
  },

  autofillCaption(generatedBoardId: number) {
    const state = readState();
    const board = state.boards.find((item) => item.id === generatedBoardId);
    const outfit = state.outfits.find((item) => item.id === board?.outfit_id);
    if (!board || !outfit) {
      throw new Error("Board not found.");
    }
    return {
      caption: `${outfit.title} is curated for a ${outfit.aesthetic.toLowerCase()} Pinterest moment. Save this affiliate-ready edit for your next outfit refresh.`,
      hashtags: ["#Veloura", "#AmazonFashion", "#OutfitInspo", `#${outfit.aesthetic.replace(/\s+/g, "")}`]
    };
  },

  createPinterestBoard(payload: { name: string; description: string }) {
    const state = readState();
    const timestamp = nowIso();
    const board: PinterestBoard = {
      id: nextId(state, "pinterestBoard"),
      user_id: 1,
      name: payload.name,
      remote_id: `demo-pinterest-board-${Date.now()}`,
      description: payload.description,
      created_at: timestamp,
      updated_at: timestamp
    };
    state.pinterestBoards.unshift(board);
    writeState(state);
    return board;
  },

  analytics() {
    return buildAnalytics(readState());
  },

  trending() {
    return buildTrending(readState());
  }
};
