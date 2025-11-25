import type { QueryError, ValidationError } from "@lib/dto.js";
import { ServerErrorSchema, type ServerErrorMap } from "@lib/errors/dto.js";
import { createContext } from "svelte";
import type { ZodType } from "zod";

export interface ServerErrorHandler {
  handle(response: Promise<any>): Promise<void>;
}

export const [ getServerErrorHandler, setServerErrorHandler ] = createContext<ServerErrorHandler>();

export class CustomErrorHandler implements ServerErrorHandler {
  constructor(private handlerMap: {
    [key in keyof ServerErrorMap]: (body: ServerErrorMap[key]) => void;
  }) {}

  public handle(response: Promise<any>): Promise<void> {
    response
      .then((body: unknown) => {
        if (body != null) {
          if (body instanceof Object) {
            const typedBody = body as Record<keyof ServerErrorMap, unknown>;
            for (const key in typedBody) {
              const value = typedBody[key as keyof ServerErrorMap];
              if (key in ServerErrorSchema.shape) {
                this.callHandlerForKey(key as keyof ServerErrorMap, value);
              } else {
                console.warn(`Unknown key "${key}" in server response.`);
              }
            }
          } else {
            console.error("Unknown error response from the server.");
          }
        }
    })
      .catch((err: Error) => {
        console.error(err);
      });
    return Promise.resolve();
  }

  private callHandlerForKey<K extends keyof ServerErrorMap>(key: K, value: unknown) {
    const schema = ServerErrorSchema.shape[key] as unknown as ZodType<ServerErrorMap[K]>;
    const result = schema.safeParse(value);
    if (result.success) {
      this.handlerMap[key](result.data);
    } else {
      console.warn(`Failed to parse server response for key "${key}"`);
    }
  }
}

export class DefaultErrorHandler extends CustomErrorHandler {
  constructor(element: Element) {
    super({
      "validation": (errors) => {
        for (const error of errors) {
          element.dispatchEvent(new CustomEvent<ValidationError>("validation-error", { detail: error }));
        }
      },
      "query": (error) => {
        element.dispatchEvent(new CustomEvent<QueryError>("query-error", { detail: error }))
      },
    });
  }
}