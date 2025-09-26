import { CanvasService } from "../services/canvas-service/canvas-service.js";
import { DomService } from "../services/dom-service/dom-service.js";

export const domService = new DomService();
export const canvasService = new CanvasService(domService);

addEventListener("DOMContentLoaded", function () {
  const plotScale = this.document.getElementById("plot-params:plotScale");
  if (!(plotScale && plotScale instanceof HTMLInputElement)) {
    throw new Error("Не удалось найти поле plotScale");
  }
  plotScale.value = String(canvasService.getScale());
  domService
    .getCanvas()
    .querySelector("a")
    ?.addEventListener("click", (event) => {
      const [X, Y] = canvasService.getClickNormalizedCoordinates(event);
      const plotParams = this.document.getElementById("plot-params");
      if (!(plotParams && plotParams instanceof HTMLFormElement)) {
        throw new Error("Не удалось найти форму со скрытыми параметрами.");
      }
      const plotX = this.document.getElementById("plot-params:plotX");
      if (!(plotX && plotX instanceof HTMLInputElement)) {
        throw new Error("Не удалось найти поле plotX");
      }
      plotX.value = String(X);
      const plotY = this.document.getElementById("plot-params:plotY");
      if (!(plotY && plotY instanceof HTMLInputElement)) {
        throw new Error("Не удалось найти поле plotY");
      }
      plotY.value = String(Y);
      faces.ajax.request(plotParams, event, {
        execute: "@form",
        render: "@form",
      });
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
