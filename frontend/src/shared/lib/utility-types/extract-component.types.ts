import { InputSignal, OutputEmitterRef, WritableSignal } from '@angular/core';

export type TInputSignalType<T> = T extends InputSignal<infer U> ? U : never;

export type TOutputEmitterType<T> = T extends OutputEmitterRef<infer U> ? U : never;

export type TExtractInputs<T> = {
  [K in keyof T as TInputSignalType<T[K]> extends never ? never : K]?:
    | WritableSignal<TInputSignalType<T[K]>>
    | TInputSignalType<T[K]>;
};

export type TExtractOutputs<T> = {
  [K in keyof T as TOutputEmitterType<T[K]> extends never ? never : K]?: (
    params: TOutputEmitterType<T[K]>,
  ) => void;
};
