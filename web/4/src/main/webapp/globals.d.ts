import type { DotStatus, ValidationError } from "lib/dto.ts";

export {};

interface CustomEventMap {
  "validation-error": CustomEvent<ValidationError>;
  "dot-add": CustomEvent<DotStatus>;
}

declare global {
  interface Window {
    initialData: {
      currentPageComponent: any;
    };
  }

  interface Document {
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