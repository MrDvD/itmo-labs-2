import { NewUserSchema, type ClientState, type NewUser, type QueryError, type ValidationError } from "@lib/dto.js";
import type { AuthRepository } from "@lib/repository/user.js";
import { clearErrorFields } from "../script.js";
import { CLIENT_STATE } from "@scripts/stores.js";

export async function handleSubmit(event: Event, redirectPath: string, authRepository: AuthRepository<ClientState, NewUser>): Promise<void> {
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
    .register(newUser)
    .then((state) => {
      CLIENT_STATE.set(state);
      window.location.assign(redirectPath);
      console.log("redirecting...");
    })
    .catch((error: Error) => {
      if (error) {
        form.dispatchEvent(new CustomEvent<QueryError>("query-error", {
          detail: {
            message: error.message,
          }
        }));
        console.error("Error logging in:", error);
      }
    });
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
  const parseResult = NewUserSchema.safeParse(newUser);
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