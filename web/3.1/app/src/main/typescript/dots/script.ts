import { CanvasService } from "../services/canvas-service/canvas-service.js";
import { DomService } from "../services/dom-service/dom-service.js";

export const domService = new DomService();
export const canvasService = new CanvasService(domService);

addEventListener("DOMContentLoaded", function () {
  // async R update for plot dots
  const plotRadius = this.document.querySelector(
    "#plot-area .input-slider input",
  );
  if (plotRadius == null) {
    throw Error("Не удалось найти скрытый input радиуса для plot form");
  }
  const observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
      if (mutation.attributeName === "value") {
        this.window.updatePlotRadius();
      }
    });
  });
  observer.observe(plotRadius, { attributes: true });
  // set scale for plot
  const plotScale = this.document.getElementById("plot-params:plotScale");
  if (!(plotScale && plotScale instanceof HTMLInputElement)) {
    throw new Error("Не удалось найти поле plotScale");
  }
  const plotParams = this.document.getElementById("plot-params");
  if (!(plotParams && plotParams instanceof HTMLFormElement)) {
    throw new Error("Не удалось найти форму со скрытыми параметрами.");
  }
  plotScale.value = String(canvasService.getScale());
  faces.ajax.request(plotParams, {} as Event, {
    execute: "@form",
    render: "@form",
  });
  // sending plot form on click
  domService
    .getCanvas()
    .querySelector("img")
    ?.addEventListener("click", (event) => {
      const [X, Y] = canvasService.getClickNormalizedCoordinates(event);
      const plotArea = this.document.getElementById("plot-area");
      if (!(plotArea && plotArea instanceof HTMLFormElement)) {
        throw new Error("Не удалось найти форму с графиком.");
      }
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
        onevent: function (data: { status: string }) {
          if (data.status === "success") {
            window.sendPlot();
          }
        },
      });
    });
});
