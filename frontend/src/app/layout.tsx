import type { Metadata } from "next";
import { Inter, Outfit } from "next/font/google";
import "./globals.css";
import { Providers } from "./providers";
import { Header } from "@/components/layout/Header";
import { Footer } from "@/components/layout/Footer";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
});

const outfit = Outfit({
  subsets: ["latin"],
  variable: "--font-outfit",
});

export const metadata: Metadata = {
  title: "Kuya Cloud - Transform Your Data Instantly",
  description:
    "Upload CSV or Excel files and get automated data cleaning, exploratory data analysis, beautiful charts, and downloadable PDF reports — all in seconds.",
  keywords: [
    "data cleaning",
    "data analysis",
    "EDA",
    "CSV processing",
    "Excel processing",
    "data visualization",
    "automated reports",
  ],
  authors: [{ name: "Kuya Cloud" }],
  openGraph: {
    title: "Kuya Cloud - Transform Your Data Instantly",
    description:
      "Upload CSV or Excel files and get automated data cleaning, exploratory data analysis, beautiful charts, and downloadable PDF reports.",
    url: "https://kuyacloud.com",
    siteName: "Kuya Cloud",
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "Kuya Cloud - Transform Your Data Instantly",
    description:
      "Automated data cleaning and analysis in seconds.",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={`${inter.variable} ${outfit.variable} antialiased`} suppressHydrationWarning>
        <Providers>
          <div className="min-h-screen flex flex-col">
            <Header />
            <main className="flex-1">{children}</main>
            <Footer />
          </div>
        </Providers>
      </body>
    </html>
  );
}
