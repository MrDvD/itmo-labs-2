import { NewUserSchema, type NewUser, type ValidationError } from "@lib/dto.js";
import type { AuthRepository } from "@lib/repository/user.js";
import { clearErrorFields } from "../script.js";

export async function handleSubmit(event: Event, authRepository: AuthRepository<void, NewUser>): Promise<void> {
  event.preventDefault();
  const form = event.target;
  if (!(form instanceof HTMLFormElement)) {
    throw new Error("Event target is not a form element");
  }
  clearErrorFields(form);
  const newUser = packNewUser(form);
  if (!newUser) {
    return;
  }
  authRepository
    .login(newUser)
    .then(() => {
      console.log("YAY!");
    })
    .catch((error: Error) => {
      console.error("Error logging in:", error);
    });
  await authRepository.login(newUser);
}

export function packNewUser(form: HTMLFormElement): NewUser | null {
  let newUser: Partial<NewUser> = {};
  const t = NewUserSchema.keyof().options;
  for (const [key, value] of (new FormData(form)).entries()) {
    const numValue = value.toString();
    if (t.includes(key as any)) {
      newUser[key as keyof NewUser] = numValue;
    }
  }
  const parseResult = NewUserSchema.safeParse(newUser)
  if (!parseResult.success) {
    for (const err of parseResult.error.issues) {
      form.dispatchEvent(new CustomEvent<ValidationError>("validation-error", {
        detail: {
          name: String(err.path[0]),
          message: err.message,
        },
      }));
    }
    return null;
  }
  return parseResult.data;
}