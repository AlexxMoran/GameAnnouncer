import { useEffect, useRef, type RefObject } from "react";
import { useIntersection } from "react-use";

export const useIntersectionTrigger = (callback?: () => void) => {
  const ref = useRef<HTMLElement>(null);

  const { isIntersecting } =
    useIntersection(ref as RefObject<HTMLElement>, {
      rootMargin: "0px",
      threshold: 0.5,
    }) || {};

  useEffect(() => {
    if (isIntersecting) {
      callback?.();
    }
  }, [isIntersecting, callback]);

  return { ref };
};
