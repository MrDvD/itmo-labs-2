import type { Dot } from "../../dto.js";
import type { DomService } from "../dom-service/dom-service.js";

export class CanvasService {
  private domService: DomService;

  constructor(domService: DomService) {
    this.domService = domService;
  }

  protected getScale(): number {
    return this.domService.getCanvas().offsetWidth * 3 / 8;
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
    const table = this.domService.getHistoryTable().querySelectorAll("tr:nth-child(n+2)");
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
    const img = this.domService.getCanvas().querySelector("img") as HTMLImageElement;
    while (this.domService.getCanvas().firstChild) {
      this.domService.getCanvas().removeChild(this.domService.getCanvas().lastChild as Node);
    }
    this.domService.getCanvas().appendChild(img);
  }

  public renderDots(R: number): void {
    this.clearDots();
    for (const dot of this.parseDots()) {
      if (Math.max(Math.abs(dot.X), Math.abs(dot.Y)) > R) {
        continue;
      }
      const drawnDot = document.createElement("div");
      drawnDot.className = `dot ${dot.hit ? "correct" : "wrong"}`;
      drawnDot.style.transform = `translate(${dot.X * this.getScale() / R}px, ${-dot.Y * this.getScale() / R}px)`
      this.domService.getCanvas().appendChild(drawnDot);
    }
  }
}