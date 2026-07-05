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
          className="w-56 rounded-full border border-line bg-parchment/70 px-4 py-2 text-sm"
          placeholder="Search products"
          value={query}
          onChange={(event) => setQuery(event.target.value)}
        />
      }
    >
      {error ? <p className="mb-4 text-sm text-rosewood">{error}</p> : null}
      <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
        {filtered.map((product) => (
          <article
            key={product.id}
            className="group flex flex-col overflow-hidden rounded-[20px] border border-line bg-parchment/70 transition-all duration-300 hover:-translate-y-1 hover:shadow-card"
          >
            <div className="relative overflow-hidden">
              <img
                src={product.image_url}
                alt={product.title}
                className="aspect-[4/5] w-full object-cover transition-transform duration-500 group-hover:scale-[1.04]"
                onError={(event) => {
                  event.currentTarget.src =
                    "https://images.unsplash.com/photo-1529139574466-a303027c1d8b?auto=format&fit=crop&w=900&q=80";
                }}
              />
              <span className="absolute left-3 top-3 rounded-full bg-paper/90 px-3 py-1 text-[10px] uppercase tracking-[0.18em] text-espresso/75 backdrop-blur">
                {product.category}
              </span>
              <button
                className="absolute right-3 top-3 rounded-full bg-paper/90 px-3 py-1 text-[10px] font-medium uppercase tracking-[0.14em] text-rosewood opacity-0 backdrop-blur transition hover:bg-rosewood hover:text-white group-hover:opacity-100 disabled:opacity-60"
                type="button"
                onClick={() => void handleDelete(product.id)}
                disabled={deletingId === product.id}
              >
                {deletingId === product.id ? "…" : "Remove"}
              </button>
            </div>
            <div className="flex flex-1 flex-col p-4">
              <h3 className="font-display text-lg leading-snug text-ink line-clamp-2">{product.title}</h3>
              <p className="mt-0.5 text-xs uppercase tracking-[0.12em] text-espresso/45">{product.brand}</p>
              <div className="mt-3 flex flex-wrap gap-1.5">
                {[product.aesthetic, product.season].map((tag) => (
                  <span
                    key={tag}
                    className="rounded-full bg-espresso/[0.06] px-2.5 py-1 text-[11px] text-espresso/65"
                  >
                    {tag}
                  </span>
                ))}
              </div>
              <div className="mt-auto flex items-center justify-between border-t border-line pt-4">
                <p className="font-display text-lg text-ink">${product.price.toFixed(2)}</p>
                <a
                  className="text-xs font-medium uppercase tracking-[0.14em] text-rosewood underline-offset-4 hover:underline"
                  href={product.affiliate_link}
                  target="_blank"
                  rel="noreferrer"
                >
                  Shop →
                </a>
              </div>
            </div>
          </article>
        ))}
        {!filtered.length ? (
          <p className="col-span-full rounded-[20px] border border-dashed border-line bg-parchment/40 p-8 text-center text-sm text-espresso/55">
            No products yet.
          </p>
        ) : null}
      </div>
    </SectionCard>
  );
}
