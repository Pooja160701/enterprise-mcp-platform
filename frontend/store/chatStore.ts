"use client";

import { create } from "zustand";
import { api } from "@/services/api";

export interface Message {

  id: string;

  role: "user" | "assistant";

  content: string;

}

interface Execution {

  status: string;

  duration_ms: number;

  tool: string;

  server: string;

  started_at: string;

  completed_at: string;

}

interface ChatState {

  messages: Message[];

  execution: Execution | null;

  steps: any[];

  loading: boolean;

  sendMessage: (message: string) => Promise<void>;

}

export const useChatStore = create<ChatState>((set, get) => ({

  messages: [],

  execution: null,

  steps: [],

  loading: false,

  async sendMessage(message: string) {

    const userMessage: Message = {

      id: Date.now().toString(),

      role: "user",

      content: message,

    };

    set({

      loading: true,

      messages: [...get().messages, userMessage],

    });

    try {

      const response = await api.post("/chat", {

        message,

      });

      const data = response.data;

      const assistant: Message = {

        id: (Date.now() + 1).toString(),

        role: "assistant",

        content: data.answer,

      };

      set({

        messages: [...get().messages, assistant],

        execution: data.execution,

        steps: data.steps,

        loading: false,

      });

    } catch (error) {

      const assistant: Message = {

        id: (Date.now() + 1).toString(),

        role: "assistant",

        content: "Unable to connect to backend.",

      };

      set({

        messages: [...get().messages, assistant],

        loading: false,

      });

      console.error(error);

    }

  },

}));