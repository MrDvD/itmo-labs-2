import type { DotParams } from "./dto.js";
import { ParamsFormValidator, type FormValidationStatus } from "./validators.js";

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

export function clearErrorPlaceholders(form: HTMLFormElement) {
  const errorPlaceholders = form.getElementsByClassName("lab-form-error");
  for (const errorPlaceholder of errorPlaceholders) {
    errorPlaceholder.innerHTML = "";
  }
}

export function processValidatorErrors(status: FormValidationStatus, form: HTMLFormElement) {
  if (!status.errors || status.errors.length === 0) {
    console.warn("Список ошибок пуст, нечего обрабатывать.");
    return;
  }
  const errorPlaceholders = form.getElementsByClassName("lab-form-error");
  for (const error of status.errors) {
    const errorPlaceholder = errorPlaceholders[error.fieldIdx];
    if (errorPlaceholder) {
      errorPlaceholder.innerHTML += error.message + "<br>";
    } else {
      console.warn(`Ошибка с индексом ${error.fieldIdx} не отображена`);
    }
  }
}

addEventListener("DOMContentLoaded", function() {
  const formId = "lab-form-params";
  const labForm = this.document.getElementById(formId);
  if (labForm && labForm instanceof HTMLFormElement) {
    const formValidator = new ParamsFormValidator();
    labForm.addEventListener("submit", function(event) {
      event.preventDefault();
      clearErrorPlaceholders(labForm);
      const formValidationStatus = formValidator.validate(labForm);
      if (!formValidationStatus.valid) {
        processValidatorErrors(formValidationStatus, labForm);
        return;
      }
      const packedForms = packDotForm(this);
      for (const packetForm of packedForms) {
        sendHelios(packetForm);
      }
    });
    const inputY = labForm.querySelector("input[name='Y']");
    if (inputY && inputY instanceof HTMLInputElement) {
      inputY.addEventListener("keypress", function(event) {
        let forbiddenChars: RegExp; 
        if (/^\-/.test(inputY.value)) {
          forbiddenChars = /[^0-9]/;
        } else {
          forbiddenChars = /[^0-9\-]/;
        }
        if (forbiddenChars.test(event.key)) {
          event.preventDefault();
        }
      });
      inputY.addEventListener("compositionstart", function(event) {
        event.preventDefault();
      });
    }
  } else {
    console.error("Не удалось найти форму с подходящим id.");
  }
});