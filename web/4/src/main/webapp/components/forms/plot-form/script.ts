export function fillCoords(form: HTMLFormElement, event: MouseEvent, R: number) {
  const canvas = event.target as unknown as HTMLElement;
  const scale = getScale(canvas);
  if (R == null || isNaN(R)) {
    return;
  }
  const inputX = form.querySelector("input[name=X]") as HTMLInputElement | null;
  if (inputX == null) {
    console.error("Could not found hidden input X element.");
    return;
  }
  const inputY = form.querySelector("input[name=Y]") as HTMLInputElement | null;
  if (inputY == null) {
    console.error("Could not found hidden input Y element.");
    return;
  }
  const X = 
    Math.round(
      ((event.offsetX - canvas.offsetWidth / 2) * 100 * R) /
        scale,
    ) / 100;
  const Y =
    Math.round(
      ((event.offsetY - canvas.offsetHeight / 2) * -100 * R) /
        scale,
    ) / 100;
  inputX.value = String(X);
  inputY.value = String(Y);
  form.requestSubmit();
}

export function getScale(elem: HTMLElement): number {
  return elem.offsetWidth * 3 / 8;
}