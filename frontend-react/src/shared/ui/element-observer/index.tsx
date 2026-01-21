import type { IElementObserverProps } from "@shared/ui/element-observer/types";
import type { FC, RefObject } from "react";
import { createElement, useEffect, useRef } from "react";
import { useIntersection } from "react-use";

export const ElementObserver: FC<IElementObserverProps> = (props) => {
  const { onVisible } = props;

  const ref = useRef<HTMLElement>(null);

  // eslint-disable-next-line react-hooks/refs
  const children = createElement(props.children, { ref: ref });

  const { isIntersecting } =
    useIntersection(ref as RefObject<HTMLElement>, {
      rootMargin: "0px",
      threshold: 0.5,
    }) || {};

  useEffect(() => {
    if (isIntersecting) onVisible?.();
  }, [isIntersecting, onVisible]);

  return children;
};
