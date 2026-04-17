/** Typed fetch wrappers for the backend API. */

import type {
  ComponentSpec,
  FlashDrumRequest,
  FlashDrumResponse,
  McCabeThieleRequest,
  McCabeThieleResponse,
  ReactorRequest,
  ReactorResponse,
} from "./types";

const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

async function post<Req, Res>(path: string, body: Req): Promise<Res> {
  const res = await fetch(`${API_BASE}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    const detail = await res.json().catch(() => ({}));
    throw new Error(detail.detail ?? `API error ${res.status}`);
  }
  return res.json() as Promise<Res>;
}

export async function fetchComponents(): Promise<ComponentSpec[]> {
  const res = await fetch(`${API_BASE}/api/components`);
  if (!res.ok) throw new Error("Failed to fetch components");
  return res.json() as Promise<ComponentSpec[]>;
}

export function solveFlash(req: FlashDrumRequest) {
  return post<FlashDrumRequest, FlashDrumResponse>("/api/flash/solve", req);
}

export function solveMcCabeThiele(req: McCabeThieleRequest) {
  return post<McCabeThieleRequest, McCabeThieleResponse>(
    "/api/distillation/mccabe-thiele/solve",
    req,
  );
}

export function solveReactor(req: ReactorRequest) {
  return post<ReactorRequest, ReactorResponse>("/api/reactor/solve", req);
}
