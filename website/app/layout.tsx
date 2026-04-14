import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Smart Fan Energy Watch",
  description: "Real-time IoT energy monitoring powered by ESP32, Supabase & weather-adaptive intelligence.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
