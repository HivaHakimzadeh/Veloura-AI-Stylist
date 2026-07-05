interface MetricCardProps {
  label: string;
  value: string;
  tone?: "default" | "accent";
}

export function MetricCard({ label, value, tone = "default" }: MetricCardProps) {
  return (
    <div
      className={`rounded-[28px] border p-5 ${
        tone === "accent"
          ? "border-rosewood/20 bg-rosewood/10 text-rosewood"
          : "border-white/50 bg-white/65 text-espresso"
      }`}
    >
      <p className="text-sm uppercase tracking-[0.2em] text-current/70">{label}</p>
      <p className="mt-3 font-display text-3xl">{value}</p>
    </div>
  );
}

