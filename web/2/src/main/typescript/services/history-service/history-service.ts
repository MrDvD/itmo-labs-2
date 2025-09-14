export class HistoryService {
  private tableSelector: string

  public constructor(tableSelector: string = ".lab-query-history") {
    this.tableSelector = tableSelector;
  }

  public fillHistoryTable(outerHTML: string): void {
    const historyTable = document.querySelector(this.tableSelector);
    if (!historyTable) {
      console.error("Не удалось найти тело таблицы.");
      return
    }
    historyTable.outerHTML = outerHTML;
  }
}