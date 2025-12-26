// /** @type {import('next').NextConfig} */
// const nextConfig = {}

// module.exports = nextConfig


const repoName = 'SE-artifact'
const isProd = process.env.NODE_ENV === 'production'
module.exports = {
  output: 'export',
  basePath: isProd ? `/${repoName}` : '',
  assetPrefix: isProd ? `/${repoName}/` : '',
  images: { unoptimized: true },
}
