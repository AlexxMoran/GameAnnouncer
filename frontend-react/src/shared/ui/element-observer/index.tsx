import type { IElementObserverProps } from "@shared/ui/element-observer/types";
import type { FC, RefObject } from "react";
import { useEffect, useRef } from "react";
import { useIntersection } from "react-use";

export const ElementObserver: FC<IElementObserverProps> = (props) => {
  const { onVisible, children } = props;

  const ref = useRef<HTMLDivElement>(null);

  const { isIntersecting } =
    useIntersection(ref as RefObject<HTMLDivElement>, {
      rootMargin: "0px",
      threshold: 0.5,
    }) || {};

  useEffect(() => {
    if (isIntersecting) onVisible?.();
  }, [isIntersecting, onVisible]);

  return <div ref={ref}>{children}</div>;
};
