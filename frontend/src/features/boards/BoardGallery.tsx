import { useState } from "react";

import { api, resolveAssetUrl } from "../../api/client";
import { SectionCard } from "../../components/SectionCard";
import type { GeneratedBoard, Outfit } from "../../types/domain";

interface BoardGalleryProps {
  outfits: Outfit[];
  boards: GeneratedBoard[];
  onCreated: (board: GeneratedBoard) => void;
}

export function BoardGallery({ outfits, boards, onCreated }: BoardGalleryProps) {
  const [selectedOutfit, setSelectedOutfit] = useState<number>(outfits[0]?.id ?? 0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const createBoard = async () => {
    if (!selectedOutfit) return;
    setLoading(true);
    setError(null);
    try {
      const board = await api.generateBoard(selectedOutfit);
      onCreated(board);
    } catch (boardError) {
      setError(boardError instanceof Error ? boardError.message : "Unable to generate board.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <SectionCard title="Pinterest Boards" eyebrow="Collage Studio">
      <div className="mb-5 flex flex-col gap-3 md:flex-row md:items-center">
        <select
          className="rounded-full border border-white/60 bg-white/70 px-4 py-3 text-sm"
          value={selectedOutfit}
          onChange={(event) => setSelectedOutfit(Number(event.target.value))}
        >
          <option value={0}>Select outfit</option>
          {outfits.map((outfit) => (
            <option key={outfit.id} value={outfit.id}>
              {outfit.title}
            </option>
          ))}
        </select>
        <button
          className="rounded-full bg-moss px-5 py-3 text-sm font-medium text-white transition hover:opacity-90"
          onClick={() => void createBoard()}
          disabled={!selectedOutfit || loading}
        >
          {loading ? "Rendering..." : "Generate 1000x1500 Board"}
        </button>
        {error ? <p className="text-sm text-rosewood">{error}</p> : null}
      </div>
      <div className="grid gap-4 md:grid-cols-2">
        {boards.map((board) => (
          <article key={board.id} className="overflow-hidden rounded-[28px] border border-white/60 bg-white/75">
            <img src={resolveAssetUrl(board.image_url)} alt={board.title} className="h-[380px] w-full object-cover" />
            <div className="p-5">
              <h3 className="font-display text-xl">{board.title}</h3>
              <p className="mt-2 text-sm text-espresso/60">
                {board.width} x {board.height} • {board.status}
              </p>
            </div>
          </article>
        ))}
        {!boards.length ? (
          <div className="rounded-[28px] border border-dashed border-white/70 bg-white/40 p-6 text-sm text-espresso/70">
            Generate a board from one of your outfits to create a Pinterest-ready visual asset.
          </div>
        ) : null}
      </div>
    </SectionCard>
  );
}
