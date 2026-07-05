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
      <div className="rounded-[28px] border border-white/60 bg-white/55 p-5">
        <p className="font-display text-2xl text-espresso">Import From Product URL</p>
        <p className="mt-2 max-w-2xl text-sm text-espresso/70">
          Paste a product page URL and Veloura will pull the metadata it can find, including the product image, then add the item directly to your catalog.
        </p>
        <div className="mt-5 flex flex-col gap-3 md:flex-row">
          <input
            className="flex-1 rounded-2xl border border-white/60 bg-white/80 px-4 py-3"
            placeholder="https://..."
            value={importUrl}
            onChange={(event) => setImportUrl(event.target.value)}
          />
          <button
            className="rounded-full bg-rosewood px-5 py-3 text-sm font-medium text-white disabled:opacity-60"
            onClick={() => void importFromUrl()}
            type="button"
            disabled={importing || !importUrl.trim()}
          >
            {importing ? "Importing..." : "Import Product"}
          </button>
        </div>
        {status ? <p className="mt-4 text-sm text-moss">{status}</p> : null}
        {error ? <p className="mt-4 text-sm text-rosewood">{error}</p> : null}
      </div>

      {lastImported ? (
        <div className="mt-5 overflow-hidden rounded-[28px] border border-white/60 bg-white/75">
          <img src={lastImported.image_url} alt={lastImported.title} className="h-64 w-full object-cover" />
          <div className="space-y-3 p-5">
            <div className="flex items-start justify-between gap-3">
              <div>
                <h3 className="font-display text-2xl text-espresso">{lastImported.title}</h3>
                <p className="text-sm text-espresso/60">{lastImported.brand}</p>
              </div>
              <span className="rounded-full bg-sand px-3 py-1 text-xs uppercase tracking-[0.2em] text-espresso/80">
                {lastImported.category}
              </span>
            </div>
            <p className="text-sm text-espresso/70">{lastImported.ai_summary}</p>
            <div className="flex flex-wrap gap-2">
              {[lastImported.color, lastImported.aesthetic, lastImported.season].map((tag) => (
                <span key={tag} className="rounded-full bg-espresso/5 px-3 py-1 text-xs text-espresso/70">
                  {tag}
                </span>
              ))}
            </div>
            <div className="flex items-center justify-between">
              <p className="font-medium text-espresso">${lastImported.price.toFixed(2)}</p>
              <a
                className="text-sm text-rosewood underline-offset-4 hover:underline"
                href={lastImported.affiliate_link}
                rel="noreferrer"
                target="_blank"
              >
                Source link
              </a>
            </div>
          </div>
        </div>
      ) : null}
    </SectionCard>
  );
}
