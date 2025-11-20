import type { DotStatus, QueryError, ValidationError } from "@lib/dto.ts";

export {};

interface CustomEventMap {
  "validation-error": CustomEvent<ValidationError>;
  "query-error": CustomEvent<QueryError>;
}

declare global {
  interface Document {
    initialData: {
      currentPageComponent: unknown;
    };
    addEventListener<K extends keyof CustomEventMap>(type: K,
        listener: (this: Document, ev: CustomEventMap[K]) => void): void;
    dispatchEvent<K extends keyof CustomEventMap>(ev: CustomEventMap[K]): void;
  }

  interface Element {
    addEventListener<K extends keyof CustomEventMap>(type: K,
        listener: (this: Document, ev: CustomEventMap[K]) => void): void;
    dispatchEvent<K extends keyof CustomEventMap>(ev: CustomEventMap[K]): void;
  }
}