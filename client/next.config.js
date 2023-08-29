/** @type {import('next').NextConfig} */
const nextConfig = {
    async rewrites() {
        return [
            {
                source: "/api/:path*",
                destination: `${process.env.API_URL || "http://localhost:8000"}/:path*`
            }
        ]
    },
    output: "standalone"
}

module.exports = nextConfig
