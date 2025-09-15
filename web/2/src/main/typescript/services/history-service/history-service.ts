import { DomService } from "../dom-service/dom-service.js";

export class HistoryService {
  private domService: DomService;

  public constructor(domService: DomService) {
    this.domService = domService;
  }

  public fillHistoryTable(outerHTML: string): void {
    this.domService.getHistoryTable().outerHTML = outerHTML;
    this.domService.refreshHistoryTable();
  }
}
