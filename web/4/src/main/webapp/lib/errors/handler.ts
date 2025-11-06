import type { ValidationError } from "lib/dto.js";
import { ServerErrorSchema, type ServerErrorMap } from "./dto.js";

export interface ServerErrorHandler {
  handle(response: Promise<any>): Promise<void>;
}

export class CustomErrorHandler implements ServerErrorHandler {
  constructor(private handlerMap: {
    [key in keyof ServerErrorMap]: (body: ServerErrorMap[key]) => void;
  }) {}

  public handle(response: Promise<any>): Promise<void> {
    response
      .then((body: unknown) => {
        if (body != null) {
          if (body instanceof Object) {
            const typedBody = body as Record<string, any>;
            for (const key in typedBody) {
              const value = typedBody[key];
              if (key in ServerErrorSchema.shape) {
                const result = ServerErrorSchema.shape[key as keyof ServerErrorMap].safeParse(value);
                if (result.success) {
                  this.handlerMap[key as keyof ServerErrorMap](result.data);
                } else {
                  console.warn(`Failed to parse server response for key "${key}"`);
                }
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
}

export class DefaultErrorHandler extends CustomErrorHandler {
  constructor() {
    super({
      "validation-errors": (errors) => {
        for (const error of errors) {
          window.dispatchEvent(new CustomEvent<ValidationError>("validation-error", { detail: error }));
        }
      }
    });
  }
}