export class DomService {
  protected labForm: HTMLFormElement;
  protected historyTable: HTMLTableElement;

  constructor() {
    this.labForm = this.refreshLabForm();
    this.historyTable = this.refreshHistoryTable();
  }

  public refreshLabForm(formClass = "lab-form-keys"): HTMLFormElement {
    const labForms = document.getElementsByClassName(formClass);
    if (labForms.length === 0) {
      throw new Error("Не удалось найти форму по классу.");
    }
    const labForm = labForms.item(0);
    if (!(labForm instanceof HTMLFormElement)) {
      throw new Error("Переданный класс не соответствует HTML-форме.");
    }
    this.labForm = labForm;
    return this.getLabForm();
  }

  public getLabForm(): HTMLFormElement {
    return this.labForm;
  }

  public getCanvas(canvasId = "plot-area"): HTMLElement {
    const canvas = document.getElementById(canvasId);
    if (canvas === null) {
      throw new Error("Не удалось найти изображение для рендера точек.");
    }
    return canvas;
  }

  public refreshHistoryTable(
    tableSelector = ".lab-query-history",
  ): HTMLTableElement {
    const historyTable = document.querySelector(tableSelector);
    if (!historyTable) {
      throw new Error("Не удалось найти тело таблицы.");
    }
    this.historyTable = historyTable as HTMLTableElement;
    return this.getHistoryTable();
  }

  public getHistoryTable(): HTMLTableElement {
    return this.historyTable;
  }
}
