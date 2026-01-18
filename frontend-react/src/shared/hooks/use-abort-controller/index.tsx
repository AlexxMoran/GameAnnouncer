import { useRootService } from "@shared/hooks/use-root-service";
import { useEffect } from "react";

// TODO добавить HOC
export const useAbortController = () => {
  const { baseApiService } = useRootService();
  const { cancelAllRequests } = baseApiService;

  useEffect(() => {
    return () => {
      cancelAllRequests();
    };
  }, []);
};
