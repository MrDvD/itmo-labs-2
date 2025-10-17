export class DomService {
  public getCanvas(canvasId = "plot-area"): HTMLElement {
    const canvas = document.getElementById(canvasId);
    if (canvas === null) {
      throw new Error("Не удалось найти изображение для рендера точек.");
    }
    return canvas;
  }
}
