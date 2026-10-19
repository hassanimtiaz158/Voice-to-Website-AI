const BASE = "/api/v1";

export class ApiError extends Error {
  constructor(status, detail) {
    super(detail);
    this.name = "ApiError";
    this.status = status;
    this.detail = detail;
  }
}

export async function api(path, init) {
  const res = await fetch(`${BASE}${path}`, {
    // Auth sessions live in HttpOnly cookies, so every call must carry them.
    credentials: "include",
    headers: { "Content-Type": "application/json" },
    ...init,
  });

  if (!res.ok) throw new ApiError(res.status, await describeError(res));

  if (res.status === 204) return undefined;
  return res.json();
}

async function describeError(res) {
  const body = await res.json().catch(() => undefined);
  const { detail } = body ?? {};
  if (typeof detail === "string" && detail) return detail;
  if (Array.isArray(detail)) {
    const first = detail[0];
    if (first?.msg) {
      const field = Array.isArray(first.loc) ? String(first.loc.at(-1) ?? "") : "";
      return field ? `The ${field} value was rejected: ${first.msg}` : first.msg;
    }
  }
  return res.statusText || "Something went wrong. Please try again.";
}
