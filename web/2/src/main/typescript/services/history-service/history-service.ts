export enum HistoryServiceConstants {
  storageKey = "lab-dot-status-history",
  historyTableSelector = ".lab-query-history > table"
}

export class HistoryService {
  // private isEmpty = false;
  // private storageKey: string

  // public constructor(storageKey: string) {
  //   this.storageKey = storageKey;
  // }

  public fillHistoryTable(historyTable: HTMLTableElement): void {
    const tbodyElement = historyTable.querySelector("tbody");
    if (tbodyElement === null) {
      console.error("Не удалось найти тело таблицы.");
      return;
    }
    // if (this.isEmpty && dotStatuses.length > 0) {
    //   tbodyElement.deleteRow(0);
    //   this.isEmpty = false;
    // }
    // for (const dotStatus of dotStatuses) {
    //   const newRow = tbodyElement.insertRow(0);
    //   const cellX = newRow.insertCell();
    //   cellX.innerText = dotStatus.entry.X;
    //   const cellY = newRow.insertCell();
    //   cellY.innerText = String(dotStatus.entry.Y);
    //   const cellR = newRow.insertCell();
    //   cellR.innerText = dotStatus.entry.R;
    //   const cellResult = newRow.insertCell();
    //   cellResult.innerText = dotStatus.hit ? "да" : "нет";
    //   const cellDate = newRow.insertCell();
    //   cellDate.innerText = dotStatus.date;
    //   const cellDuration = newRow.insertCell();
    //   cellDuration.innerText = dotStatus.duration;
    // }
    // if (saveToHistory) {
    //   this.appendToHistory(dotStatuses);
    // }
  }
}