import Head from 'next/head';
import React from 'react';

export const metadata = {
  title: 'CS-Artifacts',
  description: 'CS-Artifacts',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <>
      <html>
      <Head>
        <title>{metadata.title}</title>
      </Head>
      <body>{children}</body>
      </html>
    </>
  )
}
