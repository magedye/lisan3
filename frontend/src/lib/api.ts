export class ApiError extends Error {
  constructor(
    message: string,
    public readonly status: number,
  ) {
    super(message);
    this.name = "ApiError";
  }
}

function responseMessage(payload: unknown, fallback: string) {
  if (!payload || typeof payload !== "object") return fallback;
  if ("message" in payload && typeof payload.message === "string") return payload.message;
  if ("detail" in payload && typeof payload.detail === "string") return payload.detail;
  return fallback;
}

export async function apiFetch<T>(url: string, init?: RequestInit): Promise<T> {
  const response = await fetch(url, { cache: "no-store", ...init });
  const payload: unknown = await response.json().catch(() => null);
  if (!response.ok) {
    throw new ApiError(responseMessage(payload, `HTTP ${response.status}`), response.status);
  }
  return payload as T;
}
