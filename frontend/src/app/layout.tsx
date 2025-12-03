import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Viral Content Agent Team",
  description: "Transform boring topics into viral social media content using AI agents",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className="antialiased">
        {children}
      </body>
    </html>
  );
}
