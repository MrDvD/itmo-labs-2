export function fillCoords(form: HTMLFormElement, event: MouseEvent) {
  const canvas = event.target as unknown as HTMLElement;
  const scale = canvas.offsetWidth * 3 / 8
  const R = getR(form);
  if (R == null || isNaN(R)) {
    console.error("wawaw!!!");
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

function getR(form: HTMLFormElement): number | null {
  const input = form.querySelector("input[name=R]") as HTMLInputElement | null;
  if (input == null) {
    return null;
  }
  return input.valueAsNumber;
}

export function main() {
  document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll(".dynamic-slider").forEach((slider) => {
      const track = slider.querySelector("p:nth-of-type(2)");
      if (track == null) {
        return;
      }
      const sliderInput = slider.querySelector("input[type=range]") as HTMLInputElement | null;
      if (sliderInput == null) {
        return;
      }
      track.innerHTML = sliderInput.value;
      sliderInput.addEventListener("input", (event) => {
        const target = event.target;
        if (target instanceof HTMLInputElement) {
          track.innerHTML = target.value;
        }
      });
    });
  });
}