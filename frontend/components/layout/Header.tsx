import { Badge } from "@/components/ui/badge";

export default function Header() {
  return (
    <header className="h-16 border-b border-zinc-800 bg-[#111827]">

      <div className="mx-auto flex h-full items-center justify-between px-8">

        <div>

          <h1 className="text-2xl font-bold text-white">
            Enterprise MCP Platform
          </h1>

          <p className="text-sm text-zinc-400">
            AI Infrastructure Assistant
          </p>

        </div>

        <div className="flex items-center gap-3">

          <Badge className="bg-green-600">
            Connected
          </Badge>

          <Badge variant="outline">
            GPT-5
          </Badge>

        </div>

      </div>

    </header>
  );
}