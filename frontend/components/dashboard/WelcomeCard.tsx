import { Card } from "@/components/ui/card";

export default function WelcomeCard() {
  return (
    <Card className="p-8">

      <h2 className="text-3xl font-bold">

        Enterprise AI Agent Platform

      </h2>

      <p className="mt-4 text-muted-foreground">

        Powered by GPT-5, FastAPI, Model Context Protocol,
        Docker, Kubernetes and Enterprise Observability.

      </p>

    </Card>
  );
}