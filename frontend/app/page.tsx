import HomeContent from "@/components/HomeContent";
import { API_BASE_URL, getHealth } from "@/lib/api";

// This page's content is genuinely dynamic — a live, uncached backend health
// check on every request — so it's correctly a blocking route rather than a
// statically prerendered one. Next.js 16's Cache Components otherwise fails
// the build on any uncached fetch outside Suspense; `instant = false` is its
// documented opt-out for a segment that's meant to render on each request.
export const instant = false;

export default async function Home() {
  let apiOnline = false;
  try {
    const health = await getHealth();
    apiOnline = health.status === "ok";
  } catch {
    apiOnline = false;
  }

  return <HomeContent apiOnline={apiOnline} apiBaseUrl={API_BASE_URL} />;
}
