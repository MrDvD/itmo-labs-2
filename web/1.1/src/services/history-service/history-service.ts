import { isDotStatus, type DotStatus } from "../../dto.js";

export enum HistoryServiceConstants {
  storageKey = "lab-dot-status-history",
  historyTableSelector = ".lab-query-history > table"
}

export class HistoryService {
  private isEmpty = false;
  private storageKey: string

  public constructor(storageKey: string) {
    this.storageKey = storageKey;
  }

  public loadFromHistory(): DotStatus[] {
    let dotsStorageJson = localStorage.getItem(this.storageKey);
    if (dotsStorageJson === null) {
      localStorage.setItem(this.storageKey, "[]");
      dotsStorageJson = "[]";
    }
    const dotsStorage: unknown = JSON.parse(dotsStorageJson);
    if (Array.isArray(dotsStorage) && dotsStorage.every((x) => isDotStatus(x))) {
      return dotsStorage;
    } else {
      throw new Error("Некорректное содержимое истории. Очистите данные для корректной работы!");
    }
  }

  public initHistoryTable(historyTable: HTMLTableElement): void {
    const dotStatuses = this.loadFromHistory();
    if (dotStatuses.length === 0) {
      const tbodyElement = historyTable.querySelector("tbody");
      if (tbodyElement) {
        const emptyRow = tbodyElement.insertRow();
        const emptyCell = emptyRow.insertCell();
        emptyCell.colSpan = 100;
        emptyCell.innerText = "Нет запросов!";
        this.isEmpty = true;
      } else {
        console.error("Не удалось найти тело таблицы.");
      }
    } else {
      this.fillHistoryTable(dotStatuses, historyTable, false);
    }
  }

  public appendToHistory(dotStatuses: DotStatus[]): void {
    let dotsStorageJson = localStorage.getItem(this.storageKey);
    if (dotsStorageJson === null) {
      localStorage.setItem(this.storageKey, "[]");
      dotsStorageJson = "[]";
    }
    const dotsStorage: unknown = JSON.parse(dotsStorageJson);
    if (!Array.isArray(dotsStorage) || !dotsStorage.every((x) => isDotStatus(x))) {
      throw new Error("Некорректное содержимое истории. Очистите данные для корректной работы!");
    }
    dotsStorage.push(...dotStatuses);
    localStorage.setItem(this.storageKey, JSON.stringify(dotsStorage));
  }

  public fillHistoryTable(dotStatuses: DotStatus[], historyTable: HTMLTableElement, saveToHistory = true): void {
    const tbodyElement = historyTable.querySelector("tbody");
    if (tbodyElement === null) {
      console.error("Не удалось найти тело таблицы.");
      return;
    }
    if (this.isEmpty && dotStatuses.length > 0) {
      tbodyElement.deleteRow(0);
      this.isEmpty = false;
    }
    for (const dotStatus of dotStatuses) {
      const newRow = tbodyElement.insertRow(0);
      const cellX = newRow.insertCell();
      cellX.innerText = dotStatus.entry.X;
      const cellY = newRow.insertCell();
      cellY.innerText = String(dotStatus.entry.Y);
      const cellR = newRow.insertCell();
      cellR.innerText = dotStatus.entry.R;
      const cellResult = newRow.insertCell();
      cellResult.innerText = dotStatus.hit ? "да" : "нет";
      const cellDate = newRow.insertCell();
      cellDate.innerText = dotStatus.date;
      const cellDuration = newRow.insertCell();
      cellDuration.innerText = dotStatus.duration;
    }
    if (saveToHistory) {
      this.appendToHistory(dotStatuses);
    }
  }
}