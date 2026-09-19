import type { NextConfig } from "next";

const apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000";

const nextConfig: NextConfig = {
  reactStrictMode: true,
  async rewrites() {
    return [
      { source: "/docs", destination: `${apiBaseUrl}/docs` },
      { source: "/redoc", destination: `${apiBaseUrl}/redoc` },
      { source: "/openapi.json", destination: `${apiBaseUrl}/openapi.json` },
      { source: "/health", destination: `${apiBaseUrl}/health` },
    ];
  },
};

export default nextConfig;
