import { useCallback, useEffect, useState } from "react";

/** Returns [secondsLeft, start] - call start(seconds) to begin a cooldown. */
export function useCountdown() {
  const [secondsLeft, setSecondsLeft] = useState(0);

  useEffect(() => {
    if (secondsLeft <= 0) return undefined;
    const id = setTimeout(() => setSecondsLeft((s) => s - 1), 1000);
    return () => clearTimeout(id);
  }, [secondsLeft]);

  const start = useCallback((seconds) => setSecondsLeft(seconds), []);

  return [secondsLeft, start];
}
