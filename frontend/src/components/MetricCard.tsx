interface MetricCardProps {
  label: string;
  value: string;
  tone?: "default" | "accent";
  index?: number;
}

export function MetricCard({ label, value, tone = "default", index }: MetricCardProps) {
  const accent = tone === "accent";
  return (
    <div
      className={`group relative overflow-hidden rounded-[26px] border p-6 transition-shadow duration-300 hover:shadow-card ${
        accent
          ? "border-rosewood/25 bg-gradient-to-br from-rosewood/12 to-blush/40 text-rosewood"
          : "border-line bg-parchment/70 text-ink"
      }`}
    >
      <div className="flex items-start justify-between">
        <p
          className={`text-[10px] font-medium uppercase tracking-[0.28em] ${
            accent ? "text-rosewood/70" : "text-espresso/45"
          }`}
        >
          {label}
        </p>
        {typeof index === "number" ? (
          <span
            className={`font-display text-xs ${accent ? "text-rosewood/50" : "text-taupe"}`}
          >
            0{index + 1}
          </span>
        ) : null}
      </div>
      <p className="mt-6 font-display text-[2.6rem] font-light leading-none tracking-tight">
        {value}
      </p>
      <div
        className={`mt-5 h-px w-full ${accent ? "bg-rosewood/20" : "bg-line"}`}
        aria-hidden
      />
    </div>
  );
}
