import { type DotParams, type DotStatus } from "lib/dto.js";
import { type ItemRepository } from "lib/repository/dots.js";

export function handleSubmit(event: Event, dotsRepository: ItemRepository<DotStatus, DotParams>): void {
  event.preventDefault();
  const form = event.target as HTMLFormElement;
  const dotParams = packDotForm(form);
  dotsRepository.post(dotParams).then((dotStatus: DotStatus) => {
    const dotEvent = new CustomEvent<DotStatus>('dot-added', {
      detail: dotStatus,
    });
    form.dispatchEvent(dotEvent);
  }).catch((error: Error) => {
    console.error("Error sending dot to server:", error);
  });
}

export function packDotForm(form: HTMLFormElement): DotParams {
  let dotParams: DotParams = { X: 0, Y: 0, R: 0};
  for (const [key, value] of (new FormData(form)).entries()) {
    if ('XYR'.includes(key)) {
      dotParams[key as keyof DotParams] = Number(value);
    }
  }
  return dotParams;
}