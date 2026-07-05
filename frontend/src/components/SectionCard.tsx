import type { PropsWithChildren, ReactNode } from "react";

interface SectionCardProps extends PropsWithChildren {
  title: string;
  eyebrow?: string;
  action?: ReactNode;
  className?: string;
}

export function SectionCard({ title, eyebrow, action, className, children }: SectionCardProps) {
  return (
    <section className={`glass-card rounded-[32px] border border-white/60 p-6 shadow-card ${className ?? ""}`}>
      <div className="mb-5 flex items-start justify-between gap-4">
        <div>
          {eyebrow ? <p className="text-xs uppercase tracking-[0.3em] text-rosewood/70">{eyebrow}</p> : null}
          <h2 className="font-display text-2xl text-espresso">{title}</h2>
        </div>
        {action}
      </div>
      {children}
    </section>
  );
}
