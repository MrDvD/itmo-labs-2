export class CanvasService {
  domService;
  constructor(domService) {
    this.domService = domService;
  }
  getClickNormalizedCoordinates(clickEvent) {
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
  getScale() {
    return (this.domService.getCanvas().offsetWidth * 3) / 8;
  }
}
