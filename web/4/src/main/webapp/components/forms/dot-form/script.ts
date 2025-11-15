import type { DotParams, DotStatus } from "@lib/dto.js";
import type { ItemRepository } from "@lib/repository/dot.js";

export async function handleClean(event: Event, dotsRepository: ItemRepository<DotStatus, DotParams>): Promise<void> {
  event.preventDefault();
  await dotsRepository.delete();
}

export function initTypeValidation(form: HTMLFormElement): void {
  form.querySelectorAll(".double-input").forEach((input) => {
    if (!(input instanceof HTMLInputElement)) {
      return;
    }
    const numbers = "0123456789";
    input.addEventListener("keypress", function (event) {
      const idx = input.selectionStart as number;
      const isNegative = event.key === "-" && idx === 0;
      const isFractional =
        event.key === "." &&
        idx > 0 &&
        numbers.indexOf(input.value[idx - 1] as string) !== -1 &&
        !/\./.test(input.value);
      const isNumber = numbers.indexOf(event.key) != -1;
      if (!(isNegative || isFractional || isNumber)) {
        event.preventDefault();
      }
    });
    input.addEventListener("compositionstart", function (event) {
      event.preventDefault();
      this.blur();
    });
    input.addEventListener("paste", function (event) {
      const clip = (event as ClipboardEvent).clipboardData?.getData("text") ?? "";
      const start = input.selectionStart ?? 0;
      const end = input.selectionEnd ?? 0;
      const newValue = input.value.slice(0, start) + clip + input.value.slice(end);
      if (
        !/^-?\d+(?:\.\d+)?$/.test(newValue)
      ) {
        event.preventDefault();
      }
    });
  });
}