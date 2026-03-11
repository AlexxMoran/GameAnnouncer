import type { TObjectAny } from "@shared/types/main.types";

export function trimObjectValues<T extends TObjectAny>(values: T) {
  return Object.entries(values).reduce<T>((acc, [key, value]: [key: keyof T, value: T[keyof T]]) => {
    acc[key] = typeof value === "string" ? value.trim() : value;

    return acc;
  }, {} as T);
}
