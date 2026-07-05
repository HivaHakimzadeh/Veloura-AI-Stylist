import { useDeferredValue, useState } from "react";

import { api } from "../../api/client";
import { SectionCard } from "../../components/SectionCard";
import type { Product } from "../../types/domain";

interface ProductGridProps {
  products: Product[];
  onDeleted: () => void;
}

export function ProductGrid({ products, onDeleted }: ProductGridProps) {
  const [query, setQuery] = useState("");
  const [deletingId, setDeletingId] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);
  const deferredQuery = useDeferredValue(query);
  const filtered = products.filter((product) => {
    const search = deferredQuery.trim().toLowerCase();
    if (!search) return true;
    return (
      product.title.toLowerCase().includes(search) ||
      product.brand.toLowerCase().includes(search) ||
      product.aesthetic.toLowerCase().includes(search)
    );
  });

  const handleDelete = async (productId: number) => {
    setDeletingId(productId);
    setError(null);
    try {
      await api.deleteProduct(productId);
      onDeleted();
    } catch (deleteError) {
      setError(deleteError instanceof Error ? deleteError.message : "Unable to delete product.");
    } finally {
      setDeletingId(null);
    }
  };

  return (
    <SectionCard
      title="Catalog"
      eyebrow="Products"
      action={
        <input
          className="w-56 rounded-full border border-white/60 bg-white/70 px-4 py-2 text-sm"
          placeholder="Search products"
          value={query}
          onChange={(event) => setQuery(event.target.value)}
        />
      }
    >
      {error ? <p className="mb-4 text-sm text-rosewood">{error}</p> : null}
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        {filtered.map((product) => (
          <article key={product.id} className="overflow-hidden rounded-[28px] border border-white/60 bg-white/75">
            <img
              src={product.image_url}
              alt={product.title}
              className="h-56 w-full object-cover"
              onError={(event) => {
                event.currentTarget.src =
                  "https://images.unsplash.com/photo-1529139574466-a303027c1d8b?auto=format&fit=crop&w=900&q=80";
              }}
            />
            <div className="space-y-3 p-5">
              <div className="flex items-start justify-between gap-3">
                <div>
                  <h3 className="font-display text-xl">{product.title}</h3>
                  <p className="text-sm text-espresso/60">{product.brand}</p>
                </div>
                <span className="rounded-full bg-sand px-3 py-1 text-xs uppercase tracking-[0.2em]">
                  {product.category}
                </span>
              </div>
              <p className="text-sm text-espresso/75">{product.ai_summary}</p>
              <div className="flex flex-wrap gap-2">
                {[product.aesthetic, product.season, ...product.color_palette.slice(0, 2)].map((tag) => (
                  <span key={tag} className="rounded-full bg-espresso/5 px-3 py-1 text-xs text-espresso/70">
                    {tag}
                  </span>
                ))}
              </div>
              <div className="flex items-center justify-between">
                <p className="font-medium">${product.price.toFixed(2)}</p>
                <div className="flex items-center gap-3">
                  <a
                    className="text-sm text-rosewood underline-offset-4 hover:underline"
                    href={product.affiliate_link}
                    target="_blank"
                    rel="noreferrer"
                  >
                    Affiliate link
                  </a>
                  <button
                    className="rounded-full border border-rosewood/20 px-3 py-1 text-xs font-medium text-rosewood transition hover:bg-rosewood/10 disabled:opacity-60"
                    type="button"
                    onClick={() => void handleDelete(product.id)}
                    disabled={deletingId === product.id}
                  >
                    {deletingId === product.id ? "Deleting..." : "Delete"}
                  </button>
                </div>
              </div>
            </div>
          </article>
        ))}
        {!filtered.length ? <p className="text-sm text-espresso/60">No products yet.</p> : null}
      </div>
    </SectionCard>
  );
}
