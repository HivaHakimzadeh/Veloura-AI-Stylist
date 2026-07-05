import { useState } from "react";

import { api } from "../../api/client";
import type { Product, ProductCategory } from "../../types/domain";
import { SectionCard } from "../../components/SectionCard";

const categories: ProductCategory[] = [
  "tops",
  "bottoms",
  "dresses",
  "shoes",
  "bags",
  "jewelry",
  "accessories"
];

interface ProductFormProps {
  onCreated: (product: Product) => void;
}

export function ProductForm({ onCreated }: ProductFormProps) {
  const [form, setForm] = useState({
    title: "",
    category: "" as ProductCategory | "",
    price: "",
    image_url: "",
    affiliate_link: "",
    color: "",
    style_tags: "",
    brand: "",
    occasion_tags: "",
    run_ai_tagging: true
  });
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const submit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setSubmitting(true);
    setError(null);
    try {
      const product = await api.createProduct({
        title: form.title,
        category: form.category || undefined,
        price: Number(form.price),
        image_url: form.image_url,
        affiliate_link: form.affiliate_link,
        color: form.color,
        style_tags: form.style_tags.split(",").map((item) => item.trim()).filter(Boolean),
        brand: form.brand,
        occasion_tags: form.occasion_tags.split(",").map((item) => item.trim()).filter(Boolean),
        run_ai_tagging: form.run_ai_tagging
      });
      onCreated(product);
      setForm({
        title: "",
        category: "",
        price: "",
        image_url: "",
        affiliate_link: "",
        color: "",
        style_tags: "",
        brand: "",
        occasion_tags: "",
        run_ai_tagging: true
      });
    } catch (submitError) {
      setError(submitError instanceof Error ? submitError.message : "Unable to create product.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <SectionCard title="Product Intake" eyebrow="Catalog">
      <form className="grid gap-4 md:grid-cols-2" onSubmit={submit}>
        <input
          className="rounded-2xl border border-white/60 bg-white/70 px-4 py-3"
          placeholder="Product title"
          value={form.title}
          onChange={(event) => setForm((current) => ({ ...current, title: event.target.value }))}
          required
        />
        <input
          className="rounded-2xl border border-white/60 bg-white/70 px-4 py-3"
          placeholder="Brand"
          value={form.brand}
          onChange={(event) => setForm((current) => ({ ...current, brand: event.target.value }))}
          required
        />
        <input
          className="rounded-2xl border border-white/60 bg-white/70 px-4 py-3"
          placeholder="Price"
          type="number"
          min="0"
          step="0.01"
          value={form.price}
          onChange={(event) => setForm((current) => ({ ...current, price: event.target.value }))}
          required
        />
        <input
          className="rounded-2xl border border-white/60 bg-white/70 px-4 py-3"
          placeholder="Color"
          value={form.color}
          onChange={(event) => setForm((current) => ({ ...current, color: event.target.value }))}
          required
        />
        <input
          className="rounded-2xl border border-white/60 bg-white/70 px-4 py-3"
          placeholder="Product image URL"
          value={form.image_url}
          onChange={(event) => setForm((current) => ({ ...current, image_url: event.target.value }))}
          required
        />
        <input
          className="rounded-2xl border border-white/60 bg-white/70 px-4 py-3"
          placeholder="Affiliate link"
          value={form.affiliate_link}
          onChange={(event) => setForm((current) => ({ ...current, affiliate_link: event.target.value }))}
          required
        />
        <select
          className="rounded-2xl border border-white/60 bg-white/70 px-4 py-3"
          value={form.category}
          onChange={(event) =>
            setForm((current) => ({ ...current, category: event.target.value as ProductCategory | "" }))
          }
        >
          <option value="">Auto classify category</option>
          {categories.map((category) => (
            <option key={category} value={category}>
              {category}
            </option>
          ))}
        </select>
        <input
          className="rounded-2xl border border-white/60 bg-white/70 px-4 py-3"
          placeholder="Occasion tags, comma separated"
          value={form.occasion_tags}
          onChange={(event) => setForm((current) => ({ ...current, occasion_tags: event.target.value }))}
        />
        <textarea
          className="md:col-span-2 rounded-2xl border border-white/60 bg-white/70 px-4 py-3"
          placeholder="Style tags, comma separated"
          value={form.style_tags}
          onChange={(event) => setForm((current) => ({ ...current, style_tags: event.target.value }))}
          rows={3}
        />
        <label className="flex items-center gap-3 text-sm text-espresso/80">
          <input
            type="checkbox"
            checked={form.run_ai_tagging}
            onChange={(event) => setForm((current) => ({ ...current, run_ai_tagging: event.target.checked }))}
          />
          Run AI enrichment on save
        </label>
        <div className="md:col-span-2 flex items-center gap-3">
          <button
            className="rounded-full bg-espresso px-5 py-3 text-sm font-medium text-sand transition hover:bg-rosewood disabled:opacity-60"
            disabled={submitting}
            type="submit"
          >
            {submitting ? "Saving..." : "Add Product"}
          </button>
          {error ? <p className="text-sm text-rosewood">{error}</p> : null}
        </div>
      </form>
    </SectionCard>
  );
}

