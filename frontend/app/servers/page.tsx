"use client";

import { useEffect, useState } from "react";

import ServerCard from "@/services/ServerCard";

import { getServers } from "@/services/serverApi";

import { MCPServer } from "@/types/server";

export default function ServersPage() {

    const [servers, setServers] =

        useState<MCPServer[]>([]);

    useEffect(() => {

        getServers().then(setServers);

    }, []);

    return (

        <div className="p-10">

            <h1 className="mb-8 text-4xl font-bold text-white">

                MCP Servers

            </h1>

            <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-3">

                {servers.map((server) => (

                    <ServerCard

                        key={server.name}

                        server={server}

                    />

                ))}

            </div>

        </div>

    );

}