import { CanvasService } from "../services/canvas-service/canvas-service.js";
import { DomService } from "../services/dom-service/dom-service.js";

const domService = new DomService();
const canvasService = new CanvasService(domService);

addEventListener("DOMContentLoaded", function () {
  const plotScale = domService
    .getCanvas()
    .querySelector("#plot-area\\:plotScale");
  if (!(plotScale && plotScale instanceof HTMLInputElement)) {
    throw new Error("Не удалось найти поле plotScale");
  }
  plotScale.value = String(canvasService.getScale());
  domService
    .getCanvas()
    .querySelector("img")
    ?.addEventListener("click", (event) => {
      const [X, Y] = canvasService.getClickNormalizedCoordinates(event);
      const plotX = domService.getCanvas().querySelector("#plot-area\\:plotX");
      if (!(plotX && plotX instanceof HTMLInputElement)) {
        throw new Error("Не удалось найти поле plotX");
      }
      plotX.value = String(X);
      const plotY = domService.getCanvas().querySelector("#plot-area\\:plotY");
      if (!(plotY && plotY instanceof HTMLInputElement)) {
        throw new Error("Не удалось найти поле plotY");
      }
      plotY.value = String(Y);
    });
  // live input validation for Double
  domService
    .getLabForm()
    .querySelectorAll(".double-input")
    .forEach((input) => {
      if (input instanceof HTMLInputElement) {
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
          if (
            !/-?[0123456789]+(?:\.[0123456789]+)?/.test(
              (event as ClipboardEvent).clipboardData?.getData("text") ?? "",
            )
          ) {
            event.preventDefault();
          }
        });
      }
    });
});
