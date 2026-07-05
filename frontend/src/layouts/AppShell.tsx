import type { PropsWithChildren } from "react";

const navItems = ["Overview", "Catalog", "Outfits", "Boards", "Publishing"];

export function AppShell({ children }: PropsWithChildren) {
  return (
    <div className="min-h-screen px-4 py-6 md:px-8">
      <div className="mx-auto grid max-w-7xl gap-6 lg:grid-cols-[280px_minmax(0,1fr)]">
        <aside className="glass-card rounded-[36px] border border-white/70 p-6 shadow-card">
          <div className="rounded-[28px] bg-espresso p-5 text-sand">
            <p className="text-xs uppercase tracking-[0.35em] text-sand/70">Veloura AI Stylist</p>
            <h1 className="mt-3 font-display text-4xl leading-tight">Fashion automation for Pinterest-native growth.</h1>
          </div>
          <nav className="mt-6 space-y-2">
            {navItems.map((item, index) => (
              <div
                key={item}
                className={`rounded-2xl px-4 py-3 text-sm ${
                  index === 0 ? "bg-white text-espresso shadow-sm" : "text-espresso/70"
                }`}
              >
                {item}
              </div>
            ))}
          </nav>
          <div className="mt-6 rounded-[28px] border border-taupe/30 bg-white/60 p-5">
            <p className="text-xs uppercase tracking-[0.25em] text-rosewood/70">Signature aesthetics</p>
            <div className="mt-3 flex flex-wrap gap-2 text-sm">
              {["Old Money", "Clean Girl", "Office Chic", "Summer Vacation"].map((tag) => (
                <span key={tag} className="rounded-full bg-sand px-3 py-1 text-espresso/80">
                  {tag}
                </span>
              ))}
            </div>
          </div>
        </aside>
        <main className="space-y-6">{children}</main>
      </div>
    </div>
  );
}

