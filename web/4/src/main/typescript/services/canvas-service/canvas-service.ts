import type { DomService } from "../dom-service/dom-service.js";

export class CanvasService {
  private domService: DomService;

  constructor(domService: DomService) {
    this.domService = domService;
  }

  public getClickNormalizedCoordinates(
    clickEvent: MouseEvent,
  ): [number, number] {
    const X =
      Math.round(
        ((clickEvent.offsetX - this.domService.getCanvas().offsetWidth / 2) *
          100) /
          this.getScale(),
      ) / 100;
    const Y =
      Math.round(
        ((clickEvent.offsetY - this.domService.getCanvas().offsetHeight / 2) *
          -100) /
          this.getScale(),
      ) / 100;
    return [X, Y];
  }

  public getScale(): number {
    return (this.domService.getCanvas().offsetWidth * 3) / 8;
  }
}
