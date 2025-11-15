import * as zod from "zod";

export const ServerErrorSchema = zod.object({
  "validation-errors": zod.array(
    zod.object({
      name: zod.string(),
      message: zod.string(),
    })
  ),
});

export type ServerErrorMap = zod.infer<typeof ServerErrorSchema>;

export class ServerError<T extends keyof ServerErrorMap> extends Error {
  constructor(public type: T, public body: ServerErrorMap[T]) {
    super();
    Object.setPrototypeOf(this, ServerError.prototype);
  }
}