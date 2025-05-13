import type { FC } from "react";
import { useState, useEffect } from 'react';
import {
  ThreadListItemPrimitive,
  ThreadListPrimitive,
} from "@assistant-ui/react";
import { ArchiveIcon, PlusIcon } from "lucide-react";
import { motion, AnimatePresence  } from "framer-motion";

import { Button } from "@/components/ui/button";

interface TelegramUser {
  id: number;
  is_bot?: boolean;
  first_name: string;
  last_name?: string;
  username?: string;
  photo_url?: string;
}

export const ThreadList: FC = () => {
  const [user, setUser] = useState<TelegramUser | undefined>(undefined);
  const [isLoaded, setIsLoaded] = useState(false);

  useEffect(() => {
    const initTelegram = () => {
      if (window.Telegram?.WebApp) {
        window.Telegram.WebApp.ready();

        setUser(window.Telegram.WebApp.initDataUnsafe.user || undefined);
        setIsLoaded(true);
        
        console.log(window.Telegram.WebApp.initDataUnsafe.user)

      } else {
        setTimeout(initTelegram, 500);
      }
    };

    if (typeof window !== 'undefined') {
      initTelegram();
    }
  }, []);

  return (
    <ThreadListPrimitive.Root className="flex flex-col items-stretch gap-1.5 h-full p-4 overflow-y-auto">
      <ThreadListNew />
      
      <div className="mt-4 flex-1">
        <ThreadListItems />
      </div>

      <UserPanel user={user} isLoaded={isLoaded} />
    </ThreadListPrimitive.Root>
  );
};

interface TelegramUser {
  id: number;
  is_bot?: boolean;
  first_name: string;
  last_name?: string;
  username?: string;
  photo_url?: string;
}

interface UserPanelProps {
  user?: TelegramUser;
  isLoaded: boolean;
}

const UserPanel: FC<UserPanelProps> = ({ user }) => {
  const getDisplayName = () => {
    if (!user) return "Loading...";
    
    const username = user.username || `${user.first_name}${user.last_name ? ` ${user.last_name}` : ''}`;
    return username.length > 15 ? `${username.slice(0, 12)}...` : username;
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="sticky bottom-0 mt-4 pt-4 bg-background border-t"
    >
      <div className="flex items-center gap-3 px-2 py-3">
        {user ? (
          user.photo_url ? (
            <img
              src={user.photo_url}
              alt="User avatar"
              className="w-10 h-10 rounded-full object-cover"
            />
          ) : (
            <div className="w-10 h-10 rounded-full bg-muted flex items-center justify-center">
              <span className="text-xs">no avatar</span>
            </div>
          )
        ) : (
          <div className="w-10 h-10 rounded-full bg-muted animate-pulse" />
        )}
        
        <div className="flex-1 min-w-0">
          <p className="text-sm font-medium truncate">
            {getDisplayName()}
          </p>
          
          {user ? (
            user.username ? (
              <p className="text-xs text-muted-foreground truncate">
                @{user.username}
              </p>
            ) : (
              <p className="text-xs text-muted-foreground">no username</p>
            )
          ) : (
            <div className="h-4 w-20 bg-muted rounded animate-pulse" />
          )}
        </div>
      </div>
    </motion.div>
  );
};

const ThreadListNew: FC = () => {
  const [user, setUser] = useState<TelegramUser | undefined>(undefined)
  console.log(user)
  
  const createNewThread = async () => {
    if (!user?.id) {
      console.error('User ID not available');
      return;
    }

    try {
      const response = await fetch('/api/threads', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_id: user.id,
          timestamp: new Date().toISOString(),
        }),
      });

      if (!response.ok) throw new Error('Failed to create thread');
      
    } catch (error) {
      console.error('Error:', error);
    }

  };

  return (
    <ThreadListPrimitive.New asChild>
      <Button onClick={createNewThread}
        className="data-[active]:bg-muted hover:bg-muted flex items-center justify-start gap-1 rounded-lg px-2.5 py-2 text-start" 
        variant="ghost"
      >
        <PlusIcon className="w-4 h-4" />
        New Thread
      </Button>
    </ThreadListPrimitive.New>
  );
};

const ThreadListItems: FC = () => {
  return (
    <div className="space-y-2">
      <AnimatePresence>
        <ThreadListPrimitive.Items components={{ ThreadListItem }} />
      </AnimatePresence>
    </div>
  );
};

const ThreadListItem: FC = () => {
  return (
    <motion.div
      initial={{ opacity: 0, x: -20 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: -20 }}
      transition={{ duration: 0.2 }}
    >
      <ThreadListItemPrimitive.Root className="data-[active]:bg-muted hover:bg-muted focus-visible:bg-muted focus-visible:ring-ring flex items-center gap-2 rounded-lg transition-all focus-visible:outline-none focus-visible:ring-2">
        <ThreadListItemPrimitive.Trigger className="flex-grow px-3 py-2 text-start">
          <ThreadListItemTitle />
        </ThreadListItemPrimitive.Trigger>
        <ThreadListItemArchive />
      </ThreadListItemPrimitive.Root>
    </motion.div>
  );
};

const ThreadListItemTitle: FC = () => {
  return (
    <p className="text-sm">
      <ThreadListItemPrimitive.Title fallback="New Chat" />
    </p>
  );
};

const ThreadListItemArchive: FC = () => {
  return (
    <ThreadListItemPrimitive.Archive asChild>
      <Button
        className="text-foreground ml-auto mr-3 size-4 p-0"
        variant="ghost"
      >
        <ArchiveIcon className="w-4 h-4" />
      </Button>
    </ThreadListItemPrimitive.Archive>
  );
};