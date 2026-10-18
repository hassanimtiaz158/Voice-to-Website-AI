import { useRunStream } from "../../hooks/useRunStream";

export function ChatPanel() {
  const events = useRunStream(null);
  return (
    <section>
      <h2>Chat</h2>
      {events.map((e, i) => (
        <pre key={i}>{`${e.agent}: ${e.text}`}</pre>
      ))}
    </section>
  );
}
