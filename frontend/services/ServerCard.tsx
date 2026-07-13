"use client";

import { MCPServer } from "@/types/server";

export default function ServerCard({
    server,
}: {
    server: MCPServer;
}) {

    const online = server.status === "connected";

    return (

        <div className="rounded-xl border border-zinc-700 bg-zinc-900 p-6">

            <div className="flex items-center justify-between">

                <h3 className="text-xl font-semibold text-white">

                    {server.name}

                </h3>

                <div
                    className={`h-3 w-3 rounded-full ${
                        online
                            ? "bg-green-500"
                            : "bg-red-500"
                    }`}
                />

            </div>

            <p className="mt-4 text-zinc-400">

                {server.tool_count} tools

            </p>

            <p className="mt-1 text-sm">

                {server.status}

            </p>

        </div>

    );

}