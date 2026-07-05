import { useMemo } from "react";

import { MetricCard } from "../components/MetricCard";
import { AppShell } from "../layouts/AppShell";
import { ProductForm } from "../features/products/ProductForm";
import { ProductGrid } from "../features/products/ProductGrid";
import { OutfitGallery } from "../features/outfits/OutfitGallery";
import { BoardGallery } from "../features/boards/BoardGallery";
import { SchedulePanel } from "../features/schedule/SchedulePanel";
import { AnalyticsPanel } from "../features/analytics/AnalyticsPanel";
import { useDashboardData } from "../hooks/useDashboardData";

export function DashboardPage() {
  const dashboard = useDashboardData();

  const heroMetrics = useMemo(
    () => [
      { label: "Catalog Size", value: String(dashboard.products.length) },
      { label: "Generated Looks", value: String(dashboard.outfits.length) },
      { label: "Queued Pins", value: String(dashboard.scheduledPosts.length) }
    ],
    [dashboard.products.length, dashboard.outfits.length, dashboard.scheduledPosts.length]
  );

  return (
    <AppShell>
      <section className="glass-card rounded-[36px] border border-white/70 p-8 shadow-card">
        <div className="grid gap-6 xl:grid-cols-[1.4fr_0.6fr]">
          <div>
            <p className="text-xs uppercase tracking-[0.35em] text-rosewood/70">SaaS Command Center</p>
            <h2 className="mt-3 max-w-3xl font-display text-5xl leading-tight text-espresso">
              Curate affiliate fashion, generate polished outfit boards, and publish on a repeatable Pinterest rhythm.
            </h2>
            <p className="mt-4 max-w-2xl text-base text-espresso/70">
              Veloura blends AI product classification, aesthetic-based outfit generation, board rendering, and campaign
              scheduling into a single workflow built for fashion content operations.
            </p>
            {dashboard.error ? <p className="mt-3 text-sm text-rosewood">{dashboard.error}</p> : null}
          </div>
          <div className="grid gap-4">
            {heroMetrics.map((item, index) => (
              <MetricCard key={item.label} label={item.label} value={item.value} tone={index === 2 ? "accent" : "default"} />
            ))}
          </div>
        </div>
      </section>

      <AnalyticsPanel analytics={dashboard.analytics} trending={dashboard.trending} />

      <div className="grid gap-6 xl:grid-cols-[1fr_1.2fr]">
        <ProductForm
          onCreated={(product) => {
            dashboard.addProduct(product);
            void dashboard.refresh();
          }}
        />
        <ProductGrid products={dashboard.products} />
      </div>

      <OutfitGallery
        outfits={dashboard.outfits}
        recommendedAesthetics={dashboard.recommendedAesthetics}
        onGenerated={(outfits) => {
          dashboard.setOutfits(outfits);
          void dashboard.refresh();
        }}
      />

      <BoardGallery
        outfits={dashboard.outfits}
        boards={dashboard.boards}
        onCreated={(board) => {
          dashboard.addBoard(board);
        }}
      />

      <SchedulePanel
        boards={dashboard.boards}
        pinterestBoards={dashboard.pinterestBoards}
        scheduledPosts={dashboard.scheduledPosts}
        onScheduled={(scheduledPost) => {
          dashboard.addScheduledPost(scheduledPost);
          void dashboard.refresh();
        }}
        onPinterestBoardCreated={(board) => {
          dashboard.addPinterestBoard(board);
        }}
      />
    </AppShell>
  );
}

