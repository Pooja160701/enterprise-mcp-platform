"use client";

import { useChatStore } from "@/store/chatStore";

export default function ActivityPanel() {
  const execution = useChatStore((state) => state.execution);

  return (
    <div className="p-6">

      <h2 className="mb-6 text-2xl font-bold text-white">
        Live Execution
      </h2>

      <InfoCard
        title="Current Server"
        value={execution?.server || "Filesystem"}
      />

      <InfoCard
        title="Current Tool"
        value={execution?.tool || "Waiting..."}
      />

      <InfoCard
        title="Duration"
        value={
          execution
            ? `${execution.duration_ms.toFixed(0)} ms`
            : "0 ms"
        }
      />

      <InfoCard
        title="Status"
        value={execution?.status || "Ready"}
      />

    </div>
  );
}

function InfoCard({
  title,
  value,
}: {
  title: string;
  value: string;
}) {
  return (
    <div className="mb-4 rounded-xl border border-zinc-700 bg-zinc-900 p-5">

      <p className="text-xs uppercase tracking-widest text-zinc-500">
        {title}
      </p>

      <p className="mt-3 text-lg font-semibold text-white">
        {value}
      </p>

    </div>
  );
}