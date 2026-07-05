import { MetricCard } from "../../components/MetricCard";
import { SectionCard } from "../../components/SectionCard";
import type { AnalyticsSummary, TrendingSummary } from "../../types/domain";

interface AnalyticsPanelProps {
  analytics: AnalyticsSummary | null;
  trending: TrendingSummary | null;
}

export function AnalyticsPanel({ analytics, trending }: AnalyticsPanelProps) {
  return (
    <SectionCard title="Growth Dashboard" eyebrow="Analytics">
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-5">
        <MetricCard label="Products" value={String(analytics?.total_products ?? 0)} />
        <MetricCard label="Outfits" value={String(analytics?.total_outfits ?? 0)} />
        <MetricCard label="Boards" value={String(analytics?.total_boards ?? 0)} />
        <MetricCard label="Impressions" value={String(analytics?.total_impressions ?? 0)} />
        <MetricCard
          label="Affiliate Earnings"
          value={`$${(analytics?.estimated_affiliate_earnings ?? 0).toFixed(2)}`}
          tone="accent"
        />
      </div>
      <div className="mt-6 grid gap-4 xl:grid-cols-3">
        <div className="rounded-[28px] border border-white/60 bg-white/65 p-5 xl:col-span-2">
          <p className="font-display text-xl">Top aesthetics</p>
          <div className="mt-4 space-y-3">
            {analytics?.top_aesthetics.map((item) => (
              <div key={item.name}>
                <div className="mb-1 flex items-center justify-between text-sm">
                  <span>{item.name}</span>
                  <span>{item.count}</span>
                </div>
                <div className="h-2 rounded-full bg-sand">
                  <div className="h-2 rounded-full bg-rosewood" style={{ width: `${item.count * 20}%` }} />
                </div>
              </div>
            ))}
          </div>
        </div>
        <div className="rounded-[28px] border border-white/60 bg-white/65 p-5">
          <p className="font-display text-xl">Trending signals</p>
          <div className="mt-4 flex flex-wrap gap-2">
            {trending?.keywords.map((keyword) => (
              <span key={keyword} className="rounded-full bg-sand px-3 py-1 text-sm text-espresso/80">
                {keyword}
              </span>
            ))}
          </div>
        </div>
      </div>
    </SectionCard>
  );
}

