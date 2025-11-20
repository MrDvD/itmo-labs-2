import * as zod from "zod";

export type ValidationError = {
  name: string;
  message: string;
}

export type QueryError = {
  message: string;
}

export const ValidationMessage = {
  TooLowNumber: function(has: number) {
    return `Введите число, не меньше ${has}`;
  },
  TooLowExclusiveNumber: function(has: number) {
    return `Введите число, больше ${has}`;
  },
  TooHighNumber: function(has: number) {
    return `Введите число, не больше ${has}`;
  },
  Required: "Поле необходимо заполнить",
  TrimSpaces: "Уберите лишние пробелы",
  PasswordMatch: "Пароли должны совпадать",
  TooShortString: function(min: number) {
    return `Введите значение, не меньше ${min} символов`;
  },
}

export const DotParamsSchema = zod.object({
  X: zod
      .number({
        error: (iss) => iss.input === undefined ? ValidationMessage.Required : "Invalid input.",
      })
      .gte(-3, ValidationMessage.TooLowNumber(-3))
      .lte(3, ValidationMessage.TooHighNumber(3)),
  Y: zod
      .number({
        error: (iss) => iss.input === undefined ? ValidationMessage.Required : "Invalid input.",
      })
      .gte(-3, ValidationMessage.TooLowNumber(-3))
      .lte(3, ValidationMessage.TooHighNumber(3)),
  R: zod
      .number({
        error: (iss) => iss.input === undefined ? ValidationMessage.Required : "Invalid input.",
      })
      .gt(0, ValidationMessage.TooLowExclusiveNumber(0))
      .lte(3, ValidationMessage.TooHighNumber(3)),
});

export type DotParams = zod.infer<typeof DotParamsSchema>;

export const DotStatusSchema = zod.object({
  dot: DotParamsSchema,
  hit: zod.boolean(),
  date: zod.string(),
});

export type DotStatus = zod.infer<typeof DotStatusSchema>;

export const NodeDotSchema = zod.object({
  key: zod.string(),
  value: DotStatusSchema,
});

export type NodeDot = zod.infer<typeof NodeDotSchema>;

export const NewUserSchema = zod.object({
  login: zod
      .string({
        error: (iss) => iss.input === undefined ? ValidationMessage.Required : "Invalid input.",
      })
      .refine((val) => val.trim().length > 0, ValidationMessage.Required)
      .refine((val) => val.trim() === val, ValidationMessage.TrimSpaces),
  password: zod
      .string({
        error: (iss) => iss.input === undefined ? ValidationMessage.Required : "Invalid input.",
      })
      .refine((val) => val.trim().length > 0, ValidationMessage.Required)
      .refine((val) => val.trim() === val, ValidationMessage.TrimSpaces)
      .refine((val) => val.length >= 8, ValidationMessage.TooShortString(8)),
});

export type NewUser = zod.infer<typeof NewUserSchema>;

export const PasswordMatchSchema = zod.object({
  password: zod.string(),
  password_again: zod.string(),
})
.refine((data) => data.password === data.password_again, {
  message: ValidationMessage.PasswordMatch,
  path: ["password_again"],
});

export type UserContext = {
  id: number;
  login: string;
};

export const ClientStateSchema = zod.object({
  isAuthorized: zod.boolean(),
});

export type ClientState = zod.infer<typeof ClientStateSchema>;