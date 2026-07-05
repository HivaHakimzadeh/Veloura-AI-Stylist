import { useState } from "react";

import { api } from "../../api/client";
import { SectionCard } from "../../components/SectionCard";
import type { CampaignType, GeneratedBoard, PinterestBoard, ScheduledPost } from "../../types/domain";

const campaignTypes: CampaignType[] = ["daily", "weekly", "seasonal"];

interface SchedulePanelProps {
  boards: GeneratedBoard[];
  pinterestBoards: PinterestBoard[];
  scheduledPosts: ScheduledPost[];
  onScheduled: (scheduledPost: ScheduledPost) => void;
  onPinterestBoardCreated: (board: PinterestBoard) => void;
}

export function SchedulePanel({
  boards,
  pinterestBoards,
  scheduledPosts,
  onScheduled,
  onPinterestBoardCreated
}: SchedulePanelProps) {
  const [scheduleForm, setScheduleForm] = useState({
    generated_board_id: boards[0]?.id ?? 0,
    pinterest_board_id: pinterestBoards[0]?.id ?? 0,
    campaign_type: "daily" as CampaignType,
    scheduled_for: "",
    caption: "",
    hashtags: ""
  });
  const [boardForm, setBoardForm] = useState({ name: "", description: "" });
  const [submitting, setSubmitting] = useState(false);
  const [message, setMessage] = useState<string | null>(null);

  const autofill = async () => {
    if (!scheduleForm.generated_board_id) return;
    const data = await api.autofillCaption(scheduleForm.generated_board_id);
    setScheduleForm((current) => ({
      ...current,
      caption: data.caption,
      hashtags: data.hashtags.join(", ")
    }));
  };

  const createSchedule = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setSubmitting(true);
    setMessage(null);
    try {
      const scheduled = await api.createScheduledPost({
        generated_board_id: scheduleForm.generated_board_id,
        pinterest_board_id: scheduleForm.pinterest_board_id || null,
        campaign_type: scheduleForm.campaign_type,
        scheduled_for: new Date(scheduleForm.scheduled_for).toISOString(),
        caption: scheduleForm.caption,
        hashtags: scheduleForm.hashtags.split(",").map((item) => item.trim()).filter(Boolean)
      });
      onScheduled(scheduled);
      setMessage("Scheduled successfully.");
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "Unable to schedule post.");
    } finally {
      setSubmitting(false);
    }
  };

  const createPinterestBoard = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const board = await api.createPinterestBoard(boardForm);
    onPinterestBoardCreated(board);
    setBoardForm({ name: "", description: "" });
  };

  return (
    <SectionCard title="Publishing Scheduler" eyebrow="Campaigns">
      <div className="grid gap-6 xl:grid-cols-[1.1fr_0.9fr]">
        <form className="space-y-4" onSubmit={createSchedule}>
          <div className="grid gap-3 md:grid-cols-2">
            <select
              className="rounded-2xl border border-line bg-parchment/70 px-4 py-3"
              value={scheduleForm.generated_board_id}
              onChange={(event) =>
                setScheduleForm((current) => ({ ...current, generated_board_id: Number(event.target.value) }))
              }
            >
              <option value={0}>Select generated board</option>
              {boards.map((board) => (
                <option key={board.id} value={board.id}>
                  {board.title}
                </option>
              ))}
            </select>
            <select
              className="rounded-2xl border border-line bg-parchment/70 px-4 py-3"
              value={scheduleForm.pinterest_board_id}
              onChange={(event) =>
                setScheduleForm((current) => ({ ...current, pinterest_board_id: Number(event.target.value) }))
              }
            >
              <option value={0}>Pinterest board optional</option>
              {pinterestBoards.map((board) => (
                <option key={board.id} value={board.id}>
                  {board.name}
                </option>
              ))}
            </select>
            <select
              className="rounded-2xl border border-line bg-parchment/70 px-4 py-3"
              value={scheduleForm.campaign_type}
              onChange={(event) =>
                setScheduleForm((current) => ({
                  ...current,
                  campaign_type: event.target.value as CampaignType
                }))
              }
            >
              {campaignTypes.map((type) => (
                <option key={type} value={type}>
                  {type}
                </option>
              ))}
            </select>
            <input
              className="rounded-2xl border border-line bg-parchment/70 px-4 py-3"
              type="datetime-local"
              value={scheduleForm.scheduled_for}
              onChange={(event) => setScheduleForm((current) => ({ ...current, scheduled_for: event.target.value }))}
              required
            />
          </div>
          <textarea
            className="w-full rounded-2xl border border-line bg-parchment/70 px-4 py-3"
            rows={4}
            placeholder="Pinterest caption"
            value={scheduleForm.caption}
            onChange={(event) => setScheduleForm((current) => ({ ...current, caption: event.target.value }))}
            required
          />
          <input
            className="w-full rounded-2xl border border-line bg-parchment/70 px-4 py-3"
            placeholder="Hashtags, comma separated"
            value={scheduleForm.hashtags}
            onChange={(event) => setScheduleForm((current) => ({ ...current, hashtags: event.target.value }))}
          />
          <div className="flex flex-wrap gap-3">
            <button
              className="rounded-full bg-espresso px-5 py-3 text-sm font-medium text-sand"
              type="submit"
              disabled={submitting}
            >
              {submitting ? "Scheduling..." : "Schedule Pin"}
            </button>
            <button
              className="rounded-full border border-espresso/20 bg-parchment/70 px-5 py-3 text-sm font-medium text-espresso"
              type="button"
              onClick={() => void autofill()}
            >
              Autofill caption
            </button>
          </div>
          {message ? <p className="text-sm text-espresso/70">{message}</p> : null}
        </form>
        <div className="space-y-4">
          <form className="rounded-[28px] border border-line bg-parchment/60 p-5" onSubmit={createPinterestBoard}>
            <p className="font-display text-xl">Create Pinterest Board</p>
            <div className="mt-4 space-y-3">
              <input
                className="w-full rounded-2xl border border-line bg-parchment/80 px-4 py-3"
                placeholder="Board name"
                value={boardForm.name}
                onChange={(event) => setBoardForm((current) => ({ ...current, name: event.target.value }))}
                required
              />
              <textarea
                className="w-full rounded-2xl border border-line bg-parchment/80 px-4 py-3"
                placeholder="Board description"
                rows={3}
                value={boardForm.description}
                onChange={(event) => setBoardForm((current) => ({ ...current, description: event.target.value }))}
              />
              <button className="rounded-full bg-rosewood px-5 py-3 text-sm font-medium text-white" type="submit">
                Create Board
              </button>
            </div>
          </form>
          <div className="rounded-[28px] border border-line bg-parchment/60 p-5">
            <p className="font-display text-xl">Upcoming Queue</p>
            <div className="mt-4 space-y-3">
              {scheduledPosts.slice(0, 5).map((post) => (
                <div key={post.id} className="rounded-2xl bg-sand/70 p-4">
                  <p className="text-sm uppercase tracking-[0.2em] text-rosewood/70">{post.campaign_type}</p>
                  <p className="mt-1 font-medium">{new Date(post.scheduled_for).toLocaleString()}</p>
                  <p className="text-sm text-espresso/70">{post.caption.slice(0, 80)}</p>
                </div>
              ))}
              {!scheduledPosts.length ? <p className="text-sm text-espresso/60">No scheduled posts yet.</p> : null}
            </div>
          </div>
        </div>
      </div>
    </SectionCard>
  );
}

