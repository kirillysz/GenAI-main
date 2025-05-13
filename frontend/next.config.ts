import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
};

export default nextConfig;

module.exports = {
  env: {
    FASTAPI_URL: process.env.FASTAPI_URL,
  },
}
