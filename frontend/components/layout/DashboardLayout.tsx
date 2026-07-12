"use client";

import Header from "./Header";
import Sidebar from "./Sidebar";

interface DashboardLayoutProps {
  children: React.ReactNode;
  activity: React.ReactNode;
}

export default function DashboardLayout({
  children,
  activity,
}: DashboardLayoutProps) {
  return (
    <div className="flex h-screen bg-[#09090B]">

      <Sidebar />

      <div className="flex flex-1 flex-col">

        <Header />

        <div className="flex flex-1 overflow-hidden">

          <main className="flex-1 overflow-hidden bg-[#18181B]">
            {children}
          </main>

          <aside className="w-80 border-l border-zinc-800 bg-[#111827]">
            {activity}
          </aside>

        </div>

      </div>

    </div>
  );
}