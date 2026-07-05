import { useState } from "react";

import { api } from "../../api/client";
import { SectionCard } from "../../components/SectionCard";
import type { Outfit } from "../../types/domain";

const defaultAesthetics = [
  "Old Money",
  "Clean Girl",
  "Date Night",
  "Office Chic",
  "Summer Vacation",
  "Fall Capsule Wardrobe"
];

interface OutfitGalleryProps {
  outfits: Outfit[];
  recommendedAesthetics: string[];
  onGenerated: (outfits: Outfit[]) => void;
}

export function OutfitGallery({ outfits, recommendedAesthetics, onGenerated }: OutfitGalleryProps) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const generate = async () => {
    setLoading(true);
    setError(null);
    try {
      const aesthetics = recommendedAesthetics.length ? recommendedAesthetics : defaultAesthetics;
      const generated = await api.generateOutfits(aesthetics);
      onGenerated(generated);
    } catch (generationError) {
      setError(generationError instanceof Error ? generationError.message : "Unable to generate outfits.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <SectionCard
      title="Outfit Engine"
      eyebrow="AI Curation"
      action={
        <button
          className="rounded-full bg-rosewood px-5 py-3 text-sm font-medium text-white transition hover:opacity-90"
          onClick={() => void generate()}
          disabled={loading}
        >
          {loading ? "Generating..." : "Generate Outfits"}
        </button>
      }
    >
      <div className="mb-5 flex flex-wrap gap-2">
        {(recommendedAesthetics.length ? recommendedAesthetics : defaultAesthetics).map((tag) => (
          <span key={tag} className="rounded-full bg-sand px-3 py-1 text-sm text-espresso/80">
            {tag}
          </span>
        ))}
      </div>
      {error ? <p className="mb-4 text-sm text-rosewood">{error}</p> : null}
      <div className="grid gap-4 xl:grid-cols-2">
        {outfits.map((outfit) => (
          <article key={outfit.id} className="rounded-[28px] border border-white/60 bg-white/75 p-5">
            <div className="flex items-start justify-between gap-3">
              <div>
                <h3 className="font-display text-2xl">{outfit.title}</h3>
                <p className="text-sm text-espresso/60">{outfit.occasion}</p>
              </div>
              <span className="rounded-full bg-espresso px-3 py-1 text-xs uppercase tracking-[0.2em] text-sand">
                {outfit.aesthetic}
              </span>
            </div>
            <p className="mt-3 text-sm text-espresso/75">{outfit.description}</p>
            <div className="mt-4 grid gap-3 sm:grid-cols-2">
              {outfit.items.map((item) => (
                <div key={item.id} className="rounded-2xl bg-sand/70 p-3">
                  <p className="text-xs uppercase tracking-[0.2em] text-rosewood/70">{item.slot}</p>
                  <p className="mt-1 font-medium">{item.product.title}</p>
                  <p className="text-sm text-espresso/60">{item.product.brand}</p>
                </div>
              ))}
            </div>
            <div className="mt-4 flex flex-wrap gap-2">
              {outfit.keywords.map((keyword) => (
                <span key={keyword} className="rounded-full bg-white px-3 py-1 text-xs text-espresso/70">
                  {keyword}
                </span>
              ))}
            </div>
          </article>
        ))}
        {!outfits.length ? (
          <div className="rounded-[28px] border border-dashed border-white/70 bg-white/40 p-6 text-sm text-espresso/70">
            Add a few products, then generate outfits for Pinterest-ready aesthetics.
          </div>
        ) : null}
      </div>
    </SectionCard>
  );
}

