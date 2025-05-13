// components/assistant-ui/assistant.tsx
"use client";

import { AssistantRuntimeProvider } from "@assistant-ui/react";
import { useChatRuntime } from "@assistant-ui/react-ai-sdk";
import { ChatLayout } from "@/components/assistant-ui/chat-layout";
import { useState, useEffect } from "react";

interface TelegramUser {
  id: number;
  is_bot?: boolean;
  first_name: string;
  last_name?: string;
  username?: string;
  photo_url?: string;
}

export const Assistant = () => {
   const [user, setUser] = useState<TelegramUser | undefined>(undefined);

  useEffect(() => {
    if (window.Telegram?.WebApp?.initDataUnsafe?.user) {
      setUser(window.Telegram.WebApp.initDataUnsafe.user);
    }
  }, []);
  console.log(user)

  const runtime = useChatRuntime({
    api: "/api/chat",
    body: { user },
  });


  return (
    <AssistantRuntimeProvider runtime={runtime}>
      <ChatLayout />
    </AssistantRuntimeProvider>
  );
};
