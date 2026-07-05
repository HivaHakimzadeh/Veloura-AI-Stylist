import { MetricCard } from "../../components/MetricCard";
import { SectionCard } from "../../components/SectionCard";
import type { AnalyticsSummary, TrendingSummary } from "../../types/domain";

interface AnalyticsPanelProps {
  analytics: AnalyticsSummary | null;
  trending: TrendingSummary | null;
}

export function AnalyticsPanel({ analytics, trending }: AnalyticsPanelProps) {
  const topAesthetics = analytics?.top_aesthetics ?? [];
  const maxCount = topAesthetics.reduce((max, item) => Math.max(max, item.count), 0) || 1;

  return (
    <SectionCard title="Growth Dashboard" eyebrow="Analytics">
      <div className="grid gap-3 md:grid-cols-2 xl:grid-cols-5">
        <MetricCard label="Products" value={String(analytics?.total_products ?? 0)} index={0} />
        <MetricCard label="Outfits" value={String(analytics?.total_outfits ?? 0)} index={1} />
        <MetricCard label="Boards" value={String(analytics?.total_boards ?? 0)} index={2} />
        <MetricCard label="Impressions" value={String(analytics?.total_impressions ?? 0)} index={3} />
        <MetricCard
          label="Affiliate Earnings"
          value={`$${(analytics?.estimated_affiliate_earnings ?? 0).toFixed(2)}`}
          tone="accent"
          index={4}
        />
      </div>

      <div className="mt-5 grid gap-4 xl:grid-cols-3">
        <div className="rounded-[26px] border border-line bg-parchment/70 p-6 xl:col-span-2">
          <p className="text-[10px] uppercase tracking-[0.3em] text-rosewood/70">The Index</p>
          <p className="mt-1 font-display text-xl text-ink">Top aesthetics</p>
          <div className="mt-5 space-y-4">
            {topAesthetics.map((item, index) => (
              <div key={item.name}>
                <div className="mb-2 flex items-baseline gap-3 text-sm">
                  <span className="font-display text-xs text-taupe">0{index + 1}</span>
                  <span className="text-ink">{item.name}</span>
                  <span className="leader" aria-hidden />
                  <span className="font-display text-base text-rosewood">{item.count}</span>
                </div>
                <div className="h-1.5 overflow-hidden rounded-full bg-sand">
                  <div
                    className="h-full rounded-full bg-gradient-to-r from-rosewood to-gold transition-all duration-500"
                    style={{ width: `${Math.max((item.count / maxCount) * 100, 6)}%` }}
                  />
                </div>
              </div>
            ))}
            {!topAesthetics.length ? (
              <p className="text-sm text-espresso/50">No aesthetics tracked yet.</p>
            ) : null}
          </div>
        </div>

        <div className="rounded-[26px] border border-line bg-parchment/70 p-6">
          <p className="text-[10px] uppercase tracking-[0.3em] text-rosewood/70">On the radar</p>
          <p className="mt-1 font-display text-xl text-ink">Trending signals</p>
          <div className="mt-5 flex flex-wrap gap-2">
            {trending?.keywords.map((keyword) => (
              <span
                key={keyword}
                className="rounded-full border border-line bg-paper px-3 py-1 text-sm text-espresso/75 transition-colors hover:border-rosewood/40 hover:text-rosewood"
              >
                {keyword}
              </span>
            ))}
            {!trending?.keywords.length ? (
              <p className="text-sm text-espresso/50">No trending keywords yet.</p>
            ) : null}
          </div>
        </div>
      </div>
    </SectionCard>
  );
}
