import { CanvasService } from "../services/canvas-service/canvas-service.js";
import { DomService } from "../services/dom-service/dom-service.js";

addEventListener("DOMContentLoaded", function () {
  const domService = new DomService();
  const canvasService = new CanvasService(domService);
  domService.getCanvas().addEventListener("click", async (event) => {
    // if R is empty then throw error
    const R = 0;
    const X =
      Math.round(
        ((event.offsetX - domService.getCanvas().offsetWidth / 2) * 100 * R) /
          canvasService.getScale(),
      ) / 100;
    const Y =
      Math.round(
        ((event.offsetY - domService.getCanvas().offsetHeight / 2) * -100 * R) /
          canvasService.getScale(),
      ) / 100;
    const searchParams = new URLSearchParams();
    searchParams.append("X", String(X));
    searchParams.append("Y", String(Y));
    searchParams.append("R", String(R));
  });
  // double input validation
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
