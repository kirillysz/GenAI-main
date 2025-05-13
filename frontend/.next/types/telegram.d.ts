declare global {
    interface Window {
      Telegram: {
        WebApp: {
          initDataUnsafe: {
            user?: {
              id: number;
              is_bot?: boolean;
              first_name: string;
              last_name?: string;
              username?: string;
              photo_url?: string;
            };
          };
          ready: () => void;
          expand: () => void;
          showPopup: (params: any) => void;
        };
      };
    }
  }
  
  export {};