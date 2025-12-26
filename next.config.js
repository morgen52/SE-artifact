// /** @type {import('next').NextConfig} */
// const nextConfig = {}

// module.exports = nextConfig

const isProd = process.env.NODE_ENV === 'production'
const repoName = 'SE-artifact'

module.exports = {
  output: 'export',
  basePath: isProd ? `/${repoName}` : '',
  assetPrefix: isProd ? `/${repoName}/` : '',
  images: { unoptimized: true },
}
