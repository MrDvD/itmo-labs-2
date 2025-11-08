import { DotParamsSchema, type DotParams, type DotStatus, type ValidationError } from "lib/dto.js";
import { type ItemRepository } from "lib/repository/dots.js";

export function handleSubmit(event: Event, dotsRepository: ItemRepository<DotStatus, DotParams>): void {
  event.preventDefault();
  const form = event.target;
  if (!(form instanceof HTMLFormElement)) {
    throw new Error("Event target is not a form element");
  }
  clearErrorFields(form);
  const dotParams = packDotForm(form);
  if (dotParams == null) {
    return;
  }
  dotsRepository
  .post(dotParams)
  .then((dotStatus: DotStatus) => {
    document.dispatchEvent(new CustomEvent<DotStatus>('dot-add', {
      detail: dotStatus,
    }));
  })
  .catch((error: Error) => {
    console.error("Error sending dot to server:", error);
  });
}

export function clearErrorFields(form: HTMLFormElement) {
  form.querySelectorAll(".form-error").forEach((error) => {
    error.innerHTML = "";
  });
}

export function packDotForm(form: HTMLFormElement): DotParams | null {
  let dotParams: Partial<DotParams> = {};
  const t = DotParamsSchema.keyof().options;
  for (const [key, value] of (new FormData(form)).entries()) {
    const numValue = parseInt(value.toString());
    if (t.includes(key as any) && !isNaN(numValue)) {
      dotParams[key as keyof DotParams] = numValue;
    }
  }
  const parseResult = DotParamsSchema.safeParse(dotParams)
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

export function main() {
  document.addEventListener("DOMContentLoaded", function() {
    const form = document.querySelector(".lab-form");
    if (form == null) {
      console.error("Form element not found");
      return;
    }
    form.querySelectorAll(".form-field").forEach((field) => {
      const errorMessage = field.nextElementSibling;
      if (errorMessage == null) {
        return;
      }
      const input = field.querySelector("input") as HTMLInputElement;
      form.addEventListener("validation-error", (event) => {
        if (event.detail.name == input.name) {
          errorMessage.innerHTML = event.detail.message;
        }
      });
    });
  });
}