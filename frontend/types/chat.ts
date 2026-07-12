export interface ChatMessage {
    id: string;
    role: "user" | "assistant";
    content: string;
}

export interface ChatResponse {

    conversation: any;

    answer: string;

    execution: {
        status: string;
        duration_ms: number;
        tool: string;
        server: string;
        started_at: string;
        completed_at: string;
    };

    steps: any[];
}