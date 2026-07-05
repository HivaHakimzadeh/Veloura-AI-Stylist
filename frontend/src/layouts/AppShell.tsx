import type { PropsWithChildren } from "react";

const navItems = [
  { label: "Overview", note: "The desk" },
  { label: "Catalog", note: "Sourcing" },
  { label: "Outfits", note: "Styling" },
  { label: "Boards", note: "Art dept." },
  { label: "Publishing", note: "Distribution" }
];

export function AppShell({ children }: PropsWithChildren) {
  return (
    <div className="min-h-screen overflow-x-hidden">
      {/* Masthead */}
      <header className="sticky top-0 z-30 border-b border-line/70 bg-paper/85 backdrop-blur-xl">
        <div className="mx-auto max-w-[1500px] px-5 md:px-10">
          <div className="flex flex-wrap items-center justify-between gap-x-6 gap-y-2 py-4">
            <div className="flex items-baseline gap-4">
              <span className="font-display text-2xl font-medium tracking-masthead text-ink md:text-[1.7rem]">
                VELOURA
              </span>
              <span className="hidden text-[11px] uppercase tracking-[0.3em] text-rosewood/70 sm:inline">
                The Studio Edition
              </span>
            </div>
            <div className="flex items-center gap-4 text-[11px] uppercase tracking-[0.26em] text-espresso/55">
              <span className="hidden md:inline">AI Stylist</span>
              <span className="hidden h-3 w-px bg-line md:inline" aria-hidden />
              <span className="hidden sm:inline">Vol. 01</span>
              <span className="inline-flex items-center gap-2 rounded-full border border-line bg-parchment/70 px-3 py-1 text-moss">
                <span className="h-1.5 w-1.5 rounded-full bg-moss" aria-hidden />
                Live
              </span>
            </div>
          </div>

          {/* Horizontal numbered index nav */}
          <nav className="border-t border-line/60">
            <ul className="rail-scroll -mx-1 flex gap-6 overflow-x-auto px-1 md:gap-10">
              {navItems.map((item, index) => {
                const active = index === 0;
                return (
                  <li key={item.label} className="shrink-0">
                    <a
                      href="#"
                      className={`group flex items-center gap-2.5 border-b-2 py-3 transition-colors ${
                        active
                          ? "border-ink text-ink"
                          : "border-transparent text-espresso/50 hover:text-ink"
                      }`}
                    >
                      <span className={`font-display text-xs ${active ? "text-rosewood" : "text-taupe"}`}>
                        0{index + 1}
                      </span>
                      <span className="font-display text-[0.95rem] leading-none">{item.label}</span>
                      <span className="hidden text-[10px] uppercase tracking-[0.24em] text-espresso/35 lg:inline">
                        · {item.note}
                      </span>
                    </a>
                  </li>
                );
              })}
            </ul>
          </nav>
        </div>
      </header>

      <main className="mx-auto max-w-[1500px] space-y-6 px-5 py-6 md:px-10 md:py-8">{children}</main>

      <footer className="mx-auto max-w-[1500px] px-5 pb-10 md:px-10">
        <div className="hairline mb-4" />
        <p className="text-center text-[11px] uppercase tracking-[0.3em] text-espresso/40">
          Veloura Studio · Curated fashion, automated
        </p>
      </footer>
    </div>
  );
}
