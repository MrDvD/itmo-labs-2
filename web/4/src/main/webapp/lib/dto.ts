import * as zod from "zod";

export type ValidationError = {
  name: string;
  message: string;
}

export const ValidationMessage = {
  TooLowNumber: function(has: number) {
    return `Введите число, не меньше ${has}`;
  },
  TooHighNumber: function(has: number) {
    return `Введите число, не больше ${has}`;
  },
}

export const DotParamsSchema = zod.object({
  X: zod
      .number({
        error: (iss) => iss.input === undefined ? "Поле необходимо заполнить." : "Invalid input.",
      })
      .gte(-3, ValidationMessage.TooLowNumber(-3))
      .lte(3, ValidationMessage.TooHighNumber(3)),
  Y: zod
      .number({
        error: (iss) => iss.input === undefined ? "Поле необходимо заполнить." : "Invalid input.",
      })
      .gte(-3, ValidationMessage.TooLowNumber(-3))
      .lte(3, ValidationMessage.TooHighNumber(3)),
  R: zod
      .number({
        error: (iss) => iss.input === undefined ? "Поле необходимо заполнить." : "Invalid input.",
      })
      .gte(-3, ValidationMessage.TooLowNumber(-3))
      .lte(3, ValidationMessage.TooHighNumber(3)),
});

export type DotParams = zod.infer<typeof DotParamsSchema>;

export const DotStatusSchema = zod.object({
  entry: DotParamsSchema,
  hit: zod.boolean(),
  date: zod.string(),
});

export type DotStatus = zod.infer<typeof DotStatusSchema>;

export const NewUserSchema = zod.object({
  login: zod
      .string({
        error: (iss) => iss.input === undefined ? "Поле необходимо заполнить." : "Invalid input.",
      }),
  password: zod
      .string({
        error: (iss) => iss.input === undefined ? "Поле необходимо заполнить." : "Invalid input.",
      }),
});

export type NewUser = zod.infer<typeof NewUserSchema>;

export type UserContext = {
  id: number;
  login: string;
};

export const ClientStateSchema = zod.object({
  isAuthorized: zod.boolean(),
});

export type ClientState = zod.infer<typeof ClientStateSchema>;