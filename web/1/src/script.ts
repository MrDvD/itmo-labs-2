import type { DotParams } from "./types.js";
import { ParamsFormValidator } from "./validators.js";

export function sendHelios(packet: DotParams): void {
  console.log(JSON.stringify(packet));
}

export function packDotForm(form: HTMLFormElement): DotParams[] {
  const formData = new FormData(form);
  const dotPackets: DotParams[] = [];
  const arrayX: string[] = [];
  let rawDotParams: Omit<DotParams, 'X'> = { Y: 0, R: '0'};
  for (const [key, value] of formData.entries()) {
    if (key === 'X' && typeof value === 'string') {
      arrayX.push(value);
      continue;
    }
    rawDotParams = {
      ...rawDotParams,
      [key]: value,
    };
  }
  for (const X of arrayX) {
    dotPackets.push( { ...rawDotParams, X: X });
  }
  return dotPackets;
}

addEventListener("DOMContentLoaded", function() {
  const formId = "lab-form-params";
  const labForm = this.document.getElementById(formId);
  if (labForm && labForm instanceof HTMLFormElement) {
    const formValidator = new ParamsFormValidator();
    labForm.addEventListener("submit", function(event) {
      event.preventDefault();
      const formValidationStatus = formValidator.validate(labForm);
      if (!formValidationStatus.valid) {
        alert("Форма не прошла проверку валидации.");
        return;
      }
      const packedForms = packDotForm(this);
      for (const packetForm of packedForms) {
        sendHelios(packetForm);
      }
    })
  } else {
    this.alert("Не удалось найти форму с подходящим id.");
  }
});