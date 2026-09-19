import { NextRequest } from "next/server";
import * as fs from "fs";
import * as path from "path";

function getOwnerToken() {
  try {
    const p = path.resolve(process.cwd(), "..", ".lisan_owner_token");
    return fs.readFileSync(p, "utf-8").trim();
  } catch {
    return "";
  }
}

const BACKEND_URL = process.env.BACKEND_URL || "http://127.0.0.1:8000";

async function proxyRequest(req: NextRequest) {
  const url = new URL(req.url);
  const backendUrl = `${BACKEND_URL}${url.pathname.replace(/^\/api/, "")}${url.search}`;
  
  const headers = new Headers(req.headers);
  const token = getOwnerToken();
  if (token) {
    headers.set("X-Lisan-Owner-Token", token);
  }
  headers.delete("host");

  const response = await fetch(backendUrl, {
    method: req.method,
    headers,
    body: req.method !== "GET" && req.method !== "HEAD" ? req.body : undefined,
    duplex: 'half'
  } as RequestInit & { duplex: 'half' });

  return new Response(response.body, {
    status: response.status,
    headers: response.headers,
  });
}

export const GET = proxyRequest;
export const POST = proxyRequest;
export const PUT = proxyRequest;
export const DELETE = proxyRequest;
export const PATCH = proxyRequest;
