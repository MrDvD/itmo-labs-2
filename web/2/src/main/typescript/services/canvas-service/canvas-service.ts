import type { Dot } from "../../dto.js";

export class CanvasService {
  private canvasId: string;
  private tableSelector: string;
  private scale: number;

  constructor(canvasId = "plot-area", tableSelector = ".lab-query-history tr:nth-child(n+3)") {
    this.canvasId = canvasId;
    this.tableSelector = tableSelector;
    this.scale = this.calculateScale();
  }

  protected calculateScale(): number {
    const canvas = document.getElementById(this.canvasId);
    if (canvas === null) {
      console.error("Не удалось найти изображение для рендера точек.");
      return 0;
    }
    return canvas.offsetWidth * 3 / 8;
  }

  protected parseDotFromTr(tr: HTMLTableRowElement): Dot | null {
    if (tr.cells.length < 4) {
      return null;
    }
    return {
      X: Number(tr.cells[0]?.innerText),
      Y: Number(tr.cells[1]?.innerText),
      R: Number(tr.cells[2]?.innerText),
      hit: tr.cells[3]?.innerText === "да",
    }
  }

  protected parseDots(): Dot[] {
    const dots: Dot[] = [];
    const table = document.querySelectorAll(this.tableSelector);
    for (const tr of table) {
      if (tr instanceof HTMLTableRowElement) {
        const dot = this.parseDotFromTr(tr);
        if (dot) {
          dots.push(dot);
        }
      }
    }
    return dots;
  }

  public clearDots(): void {
    const canvas = document.getElementById(this.canvasId);
    if (canvas === null) {
      console.error("Не удалось найти изображение для рендера точек.");
      return;
    }
    const img = canvas.querySelector("img") as HTMLImageElement;
    while (canvas.firstChild) {
      canvas.removeChild(canvas.lastChild as Node);
    }
    canvas.appendChild(img);
  }

  public renderDots(R: number): void {
    this.clearDots();
    const canvas = document.getElementById(this.canvasId);
    if (canvas === null) {
      console.error("Не удалось найти изображение для рендера точек.");
      return;
    }
    for (const dot of this.parseDots()) {
      if (Math.max(Math.abs(dot.X), Math.abs(dot.Y)) > R) {
        continue;
      }
      const drawnDot = document.createElement("div");
      drawnDot.className = `dot ${dot.hit ? "correct" : "wrong"}`;
      drawnDot.style.transform = `translate(${dot.X * this.scale / R}px, ${-dot.Y * this.scale / R}px)`
      canvas.appendChild(drawnDot);
    }
  }
}