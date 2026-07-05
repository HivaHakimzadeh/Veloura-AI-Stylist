import { useState } from "react";

import { api } from "../../api/client";
import { SectionCard } from "../../components/SectionCard";
import type { Product } from "../../types/domain";

interface ProductFormProps {
  onCreated: (product: Product) => void;
}

export function ProductForm({ onCreated }: ProductFormProps) {
  const [importUrl, setImportUrl] = useState("");
  const [lastImported, setLastImported] = useState<Product | null>(null);
  const [importing, setImporting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [status, setStatus] = useState<string | null>(null);

  const normalizeImportUrl = (value: string) => {
    const trimmed = value.trim();
    if (!trimmed) return trimmed;
    return /^https?:\/\//i.test(trimmed) ? trimmed : `https://${trimmed}`;
  };

  const importFromUrl = async () => {
    if (!importUrl.trim()) return;
    setImporting(true);
    setError(null);
    setStatus(null);
    try {
      const normalizedUrl = normalizeImportUrl(importUrl);
      const preview = await api.importProductFromUrl({ url: normalizedUrl });
      const product = await api.createProduct({
        title: preview.title,
        category: preview.category,
        price: preview.price,
        image_url: preview.image_url,
        affiliate_link: preview.affiliate_link,
        color: preview.color,
        style_tags: preview.style_tags,
        brand: preview.brand,
        occasion_tags: preview.occasion_tags,
        run_ai_tagging: true
      });
      setLastImported(product);
      setImportUrl("");
      setStatus("Product imported and added to your catalog.");
      onCreated(product);
    } catch (importError) {
      setError(importError instanceof Error ? importError.message : "Unable to import product from URL.");
    } finally {
      setImporting(false);
    }
  };

  return (
    <SectionCard title="Product Intake" eyebrow="Catalog">
      <div className="flex flex-col gap-5 lg:flex-row lg:items-center lg:justify-between">
        <p className="max-w-md text-[0.95rem] leading-relaxed text-espresso/65">
          Paste any product page URL — Veloura pulls the metadata and image it can find and files the piece straight
          into your catalog.
        </p>
        <div className="flex w-full flex-col gap-3 sm:flex-row lg:max-w-xl">
          <input
            className="flex-1 rounded-full border border-line bg-parchment/80 px-5 py-3 text-sm outline-none transition-colors focus:border-rosewood/50"
            placeholder="https://…"
            value={importUrl}
            onChange={(event) => setImportUrl(event.target.value)}
          />
          <button
            className="shrink-0 rounded-full bg-rosewood px-6 py-3 text-sm font-medium text-white transition hover:bg-rosewood/90 disabled:opacity-60"
            onClick={() => void importFromUrl()}
            type="button"
            disabled={importing || !importUrl.trim()}
          >
            {importing ? "Importing…" : "Import Product"}
          </button>
        </div>
      </div>
      {status ? <p className="mt-3 text-sm text-moss">{status}</p> : null}
      {error ? <p className="mt-3 text-sm text-rosewood">{error}</p> : null}

      {lastImported ? (
        <div className="mt-6 grid gap-5 rounded-[22px] border border-line bg-parchment/60 p-4 sm:grid-cols-[200px_minmax(0,1fr)]">
          <img
            src={lastImported.image_url}
            alt={lastImported.title}
            className="h-56 w-full rounded-[16px] object-cover sm:h-full"
          />
          <div className="flex flex-col gap-3 py-1">
            <div className="flex items-start justify-between gap-3">
              <div>
                <p className="text-[10px] uppercase tracking-[0.28em] text-rosewood/70">Just imported</p>
                <h3 className="mt-1 font-display text-2xl leading-tight text-ink">{lastImported.title}</h3>
                <p className="text-sm text-espresso/55">{lastImported.brand}</p>
              </div>
              <span className="shrink-0 rounded-full bg-sand px-3 py-1 text-[10px] uppercase tracking-[0.18em] text-espresso/70">
                {lastImported.category}
              </span>
            </div>
            <p className="text-sm leading-relaxed text-espresso/65">{lastImported.ai_summary}</p>
            <div className="flex flex-wrap gap-2">
              {[lastImported.color, lastImported.aesthetic, lastImported.season].map((tag) => (
                <span key={tag} className="rounded-full bg-espresso/5 px-3 py-1 text-xs text-espresso/70">
                  {tag}
                </span>
              ))}
            </div>
            <div className="mt-auto flex items-center justify-between border-t border-line pt-3">
              <p className="font-display text-lg text-ink">${lastImported.price.toFixed(2)}</p>
              <a
                className="text-sm text-rosewood underline-offset-4 hover:underline"
                href={lastImported.affiliate_link}
                rel="noreferrer"
                target="_blank"
              >
                Source link →
              </a>
            </div>
          </div>
        </div>
      ) : null}
    </SectionCard>
  );
}
