export class DomService {
  protected labForm: HTMLFormElement;
  protected rScale: HTMLInputElement;
  protected rScaleText: Element;
  protected canvas: HTMLElement;
  protected historyTable: HTMLTableElement;

  constructor() {
    this.labForm = this.refreshLabForm();
    this.rScale = this.refreshRScale();
    this.rScaleText = this.refreshRScaleText();
    this.canvas = this.refreshCanvas();
    this.historyTable = this.refreshHistoryTable();
  }

  public refreshLabForm(formId = "lab-form-params"): HTMLFormElement {
    const labForm = document.getElementById(formId);
    if (!(labForm && labForm instanceof HTMLFormElement)) {
      throw new Error("Не удалось найти форму с подходящим id.");
    }
    this.labForm = labForm;
    return this.getLabForm();
  }

  public getLabForm(): HTMLFormElement {
    return this.labForm;
  }

  public refreshRScale(
    rScaleSelector = 'input[name="R"][type="hidden"]',
  ): HTMLInputElement {
    const rScale = this.getLabForm().querySelector(
      rScaleSelector,
    ) as HTMLInputElement | null;
    if (rScale === null) {
      throw new Error("Не удалось найти скрытый input для R.");
    }
    this.rScale = rScale;
    return this.getRScale();
  }

  public getRScale(): HTMLInputElement {
    return this.rScale;
  }

  public refreshRScaleText(rScaleTextSelector = "r-last-scale"): Element {
    const rScalesText =
      this.getLabForm().getElementsByClassName(rScaleTextSelector);
    if (rScalesText.length === 0) {
      throw new Error("Не удалось найти контейнер с масштабом изображения.");
    }
    this.rScaleText = rScalesText[0] as Element;
    return this.getRScaleText();
  }

  public getRScaleText(): Element {
    return this.rScaleText;
  }

  public refreshCanvas(canvasId = "plot-area"): HTMLElement {
    const canvas = document.getElementById(canvasId);
    if (canvas === null) {
      throw new Error("Не удалось найти изображение для рендера точек.");
    }
    this.canvas = canvas;
    return this.getCanvas();
  }

  public getCanvas(): HTMLElement {
    return this.canvas;
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
