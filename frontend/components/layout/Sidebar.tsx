"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

import clsx from "clsx";

import {
  Bot,
  Folder,
  Activity,
  History,
  Settings,
  Sparkles,
} from "lucide-react";

const items = [
  {
    title: "Chat",
    href: "/",
    icon: Bot,
  },
  {
    title: "MCP Servers",
    href: "/servers",
    icon: Folder,
  },
  {
    title: "Monitoring",
    href: "/monitoring",
    icon: Activity,
  },
  {
    title: "History",
    href: "/history",
    icon: History,
  },
  {
    title: "Settings",
    href: "/settings",
    icon: Settings,
  },
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="flex h-screen w-64 flex-col border-r border-zinc-800 bg-zinc-950">

      <div className="flex items-center gap-3 border-b border-zinc-800 p-6">

        <div className="rounded-xl bg-blue-600 p-2">
          <Sparkles className="h-5 w-5 text-white" />
        </div>

        <div>
          <h2 className="font-bold text-white">
            Enterprise MCP
          </h2>

          <p className="text-xs text-zinc-400">
            AI Agent Platform
          </p>
        </div>

      </div>

      <nav className="flex-1 p-4 space-y-2">

        {items.map((item) => {

          const Icon = item.icon;

          return (
            <Link
              key={item.href}
              href={item.href}
              className={clsx(
                "flex items-center gap-3 rounded-xl px-4 py-3 transition-all",

                pathname === item.href
                  ? "bg-blue-600 text-white shadow-lg"
                  : "text-zinc-400 hover:bg-zinc-900 hover:text-white"
              )}
            >
              <Icon size={18} />

              {item.title}

            </Link>
          );
        })}
      </nav>

      <div className="border-t border-zinc-800 p-6">

        <div className="rounded-xl bg-zinc-900 p-4">

          <p className="text-sm text-white">

            GPT-5

          </p>

          <p className="text-xs text-zinc-500">

            Enterprise MCP v1.0

          </p>

        </div>

      </div>

    </aside>
  );
}