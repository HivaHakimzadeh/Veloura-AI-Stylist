import type { PropsWithChildren, ReactNode } from "react";

interface SectionCardProps extends PropsWithChildren {
  title: string;
  eyebrow?: string;
  action?: ReactNode;
  className?: string;
}

export function SectionCard({ title, eyebrow, action, className, children }: SectionCardProps) {
  return (
    <section
      className={`glass-card rounded-[32px] border border-line p-6 shadow-editorial md:p-8 ${className ?? ""}`}
    >
      <div className="mb-6 flex flex-wrap items-end justify-between gap-4">
        <div className="min-w-0">
          {eyebrow ? (
            <p className="flex items-center gap-3 text-[10px] font-medium uppercase tracking-[0.32em] text-rosewood/75">
              <span className="h-px w-6 bg-rosewood/40" aria-hidden />
              {eyebrow}
            </p>
          ) : null}
          <h2 className="mt-2 font-display text-[1.9rem] font-light leading-tight tracking-tight text-ink">
            {title}
          </h2>
        </div>
        {action ? <div className="shrink-0">{action}</div> : null}
      </div>
      <div className="hairline mb-6 -mt-1" />
      {children}
    </section>
  );
}
