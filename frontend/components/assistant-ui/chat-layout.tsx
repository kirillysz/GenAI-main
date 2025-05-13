// components/chat-layout.tsx
"use client";

import { useState, useEffect } from "react";
import { Menu, X } from "lucide-react";
import { ThreadList } from "./thread-list";
import { Thread } from "./thread";
import { cn } from "@/lib/utils";
import { AnimatePresence, motion } from "framer-motion";

export const ChatLayout = () => {
  const [isPanelOpen, setIsPanelOpen] = useState(true);
  const [isMobile, setIsMobile] = useState(false);

  useEffect(() => {
    const checkMobile = () => {
      const mobile = window.innerWidth < 768;
      setIsMobile(mobile);
      if (mobile) setIsPanelOpen(false);
    };
    
    checkMobile();
    window.addEventListener("resize", checkMobile);
    return () => window.removeEventListener("resize", checkMobile);
  }, []);

  return (
    <div className="flex h-screen relative">
      <AnimatePresence>
        {isMobile && isPanelOpen && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/50 z-20 md:hidden"
            onClick={() => setIsPanelOpen(false)}
          />
        )}
      </AnimatePresence>

      <motion.div
        className={cn(
          "h-full bg-background border-r",
          "w-64 fixed top-0 left-0 z-30 shadow-lg pt-16",
        )}
        initial={{ x: '-100%' }}
        animate={{ 
          x: isPanelOpen ? 0 : '-100%',
          boxShadow: isPanelOpen ? 'rgba(0, 0, 0, 0.15) 0px 3px 12px' : 'none'
        }}
        transition={{ type: 'spring', stiffness: 300, damping: 30 }}
      >
        <ThreadList />
      </motion.div>

      <div className={cn(
        "flex-1 h-full transition-all duration-300 pt-20",
        isMobile ? "overflow-x-hidden" : ""
      )}>
        <motion.button
          onClick={() => setIsPanelOpen(!isPanelOpen)}
          className={cn(
            "fixed z-40 p-2 rounded-lg backdrop-blur-sm",
            "transition-all top-6 hover:bg-muted/50",
            isPanelOpen ? "left-4" : "left-4 md:left-6",
          )}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          <AnimatePresence mode="wait">
            {isPanelOpen ? (
              <motion.span
                key="close"
                initial={{ rotate: -90, opacity: 0 }}
                animate={{ rotate: 0, opacity: 1 }}
                exit={{ rotate: 90, opacity: 0 }}
                transition={{ duration: 0.2 }}
              >
                <X className="w-5 h-5" />
              </motion.span>
            ) : (
              <motion.span
                key="menu"
                initial={{ rotate: 90, opacity: 0 }}
                animate={{ rotate: 0, opacity: 1 }}
                exit={{ rotate: -90, opacity: 0 }}
                transition={{ duration: 0.2 }}
              >
                <Menu className="w-5 h-5" />
              </motion.span>
            )}
          </AnimatePresence>
        </motion.button>

        <Thread />
      </div>
    </div>
  );
};