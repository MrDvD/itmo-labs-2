export class DomService {
  labForm;
  constructor() {
    this.labForm = this.refreshLabForm();
  }
  refreshLabForm(formClass = "lab-form-keys") {
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
  getLabForm() {
    return this.labForm;
  }
  getCanvas(canvasId = "plot-area") {
    const canvas = document.getElementById(canvasId);
    if (canvas === null) {
      throw new Error("Не удалось найти изображение для рендера точек.");
    }
    return canvas;
  }
}
