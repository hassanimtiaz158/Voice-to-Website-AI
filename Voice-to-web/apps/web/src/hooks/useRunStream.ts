import { useEffect, useState } from "react";

export type AgentEvent = { agent: string; text: string };

/** Streams agent events for a run over SSE. */
export function useRunStream(runId: string | null) {
  const [events, setEvents] = useState<AgentEvent[]>([]);
  useEffect(() => {
    if (!runId) return;
    const es = new EventSource(`/api/v1/runs/${runId}/events`);
    es.onmessage = (m) => setEvents((e) => [...e, JSON.parse(m.data)]);
    return () => es.close();
  }, [runId]);
  return events;
}
