import { useMemo } from "react";

import { AppShell } from "../layouts/AppShell";
import { ProductForm } from "../features/products/ProductForm";
import { ProductGrid } from "../features/products/ProductGrid";
import { OutfitGallery } from "../features/outfits/OutfitGallery";
import { BoardGallery } from "../features/boards/BoardGallery";
import { SchedulePanel } from "../features/schedule/SchedulePanel";
import { AnalyticsPanel } from "../features/analytics/AnalyticsPanel";
import { useDashboardData } from "../hooks/useDashboardData";

const signatureAesthetics = ["Old Money", "Clean Girl", "Office Chic", "Summer Vacation"];

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
      <section className="glass-card relative overflow-hidden rounded-[28px] border border-line p-6 shadow-editorial md:p-9">
        {/* editorial texture: soft warm glow + issue number watermark */}
        <div
          className="pointer-events-none absolute -right-28 -top-28 h-80 w-80 rounded-full bg-blush/40 blur-3xl"
          aria-hidden
        />

        <div className="relative grid gap-8 lg:grid-cols-[1.55fr_0.85fr] lg:items-stretch">
          <div className="flex min-w-0 flex-col">
            <p className="flex items-center gap-3 text-[11px] font-medium uppercase tracking-[0.32em] text-rosewood/75">
              <span className="h-px w-8 bg-rosewood/40" aria-hidden />
              The Command Desk
            </p>
            <h2 className="mt-4 max-w-3xl break-words font-display text-[2rem] font-light leading-[1.06] tracking-tight text-ink sm:text-[2.5rem] md:text-[3.6rem]">
              Curate affiliate fashion, art-direct outfit boards, and publish on a{" "}
              <span className="italic text-rosewood">repeatable</span> Pinterest rhythm.
            </h2>
            <p className="mt-5 max-w-2xl text-[0.98rem] leading-relaxed text-espresso/65">
              Veloura blends AI product classification, aesthetic-based outfit generation, board rendering, and
              campaign scheduling into a single workflow built for fashion content operations.
            </p>

            <div className="mt-auto pt-7">
              <div className="flex flex-wrap items-center gap-x-6 gap-y-3">
                <p className="text-[10px] uppercase tracking-[0.3em] text-espresso/40">Signature aesthetics</p>
                <div className="flex flex-wrap gap-2">
                  {signatureAesthetics.map((tag) => (
                    <span
                      key={tag}
                      className="rounded-full border border-line bg-parchment/60 px-3 py-1 text-xs text-espresso/75"
                    >
                      {tag}
                    </span>
                  ))}
                </div>
              </div>
              {dashboard.demoMode || dashboard.error ? (
                <div className="mt-4 flex flex-wrap items-center gap-3">
                  {dashboard.demoMode ? (
                    <span className="inline-flex items-center gap-2 rounded-full border border-line bg-parchment/80 px-4 py-1.5 text-xs uppercase tracking-[0.18em] text-espresso/60">
                      <span className="h-1.5 w-1.5 rounded-full bg-gold" aria-hidden />
                      Demo mode · local sample data
                    </span>
                  ) : null}
                  {dashboard.error ? (
                    <span className="inline-flex rounded-full border border-rosewood/30 bg-rosewood/10 px-4 py-1.5 text-xs text-rosewood">
                      {dashboard.error}
                    </span>
                  ) : null}
                </div>
              ) : null}
            </div>
          </div>

          {/* The ledger — dark editorial panel replaces three floating stat boxes */}
          <div className="relative min-w-0 overflow-hidden rounded-[24px] bg-espresso p-7 text-parchment shadow-lift">
            <span
              className="pointer-events-none absolute -bottom-8 -right-4 select-none font-display text-[9rem] font-light leading-none text-parchment/[0.05]"
              aria-hidden
            >
              01
            </span>
            <div className="relative flex items-center justify-between">
              <p className="text-[10px] uppercase tracking-[0.34em] text-champagne/80">The Ledger</p>
              <p className="text-[10px] uppercase tracking-[0.24em] text-parchment/40">Today</p>
            </div>
            <div className="relative mt-6 space-y-5">
              {heroMetrics.map((item, index) => (
                <div key={item.label}>
                  {index > 0 ? <div className="mb-5 h-px w-full bg-parchment/12" aria-hidden /> : null}
                  <div className="flex items-end justify-between gap-4">
                    <span className="text-[11px] uppercase tracking-[0.2em] text-parchment/55">
                      {item.label}
                    </span>
                    <span
                      className={`font-display text-4xl font-light leading-none ${
                        index === 2 ? "text-champagne" : "text-parchment"
                      }`}
                    >
                      {item.value}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      <AnalyticsPanel analytics={dashboard.analytics} trending={dashboard.trending} />

      <ProductForm
        onCreated={(product) => {
          dashboard.addProduct(product);
          void dashboard.refresh();
        }}
      />
      <ProductGrid
        products={dashboard.products}
        onDeleted={() => {
          void dashboard.refresh();
        }}
      />

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
