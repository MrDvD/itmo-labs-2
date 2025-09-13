import { isDotStatus, type DotParams, type DotStatus } from "./dto.js";
import { LabDotDomainService, type DotDomainService } from "./services/domain-service/domain-service.js";
import { HistoryService, HistoryServiceConstants } from "./services/history-service/history-service.js";
import { ParamsFormValidator, type FormValidationStatus } from "./validators.js";

export async function sendToServer(dotPackets: DotParams[], domainService: DotDomainService): Promise<DotStatus[] | null> {
  const response = await fetch(domainService.getDotDomain(), {
    method: "POST",
    body: JSON.stringify(dotPackets),
  });
  if (response.ok) {
    const responseObjects: unknown[] = await response.json();
    const validDots: DotStatus[] = [];
    for (const responseObject of responseObjects) {
      if (isDotStatus(responseObject)) {
        validDots.push(responseObject);
      } else {
        console.error("Не удалось обработать один из объектов от сервера.");
      }
    }
    return validDots
  } else {
    return null;
  }
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
    if (key === 'Y') {
      rawDotParams['Y'] = Number(value);
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
  const historyService = new HistoryService(HistoryServiceConstants.storageKey);
  const historyTable = this.document.querySelector(HistoryServiceConstants.historyTableSelector);
  if (historyTable instanceof HTMLTableElement) {
    historyService.initHistoryTable(historyTable);
  } else {
    console.error("Не удалось найти историю запросов с подходящим селектором.");
  }
  const formId = "lab-form-params";
  const labForm = this.document.getElementById(formId);
  if (labForm && labForm instanceof HTMLFormElement) {
    const formValidator = new ParamsFormValidator();
    labForm.addEventListener("submit", async function(event) {
      event.preventDefault();
      clearErrorPlaceholders(labForm);
      const formValidationStatus = formValidator.validate(labForm);
      if (!formValidationStatus.valid) {
        processValidatorErrors(formValidationStatus, labForm);
        return;
      }
      const dotResponse = await sendToServer(packDotForm(this), new LabDotDomainService());
      if (dotResponse && historyTable instanceof HTMLTableElement) {
        historyService.fillHistoryTable(dotResponse, historyTable);
      }
    });
    const inputY = labForm.querySelector("input[name='Y']");
    if (inputY && inputY instanceof HTMLInputElement) {
      const numbers = "0123456789";
      inputY.addEventListener("keypress", function(event) {
        const idx = inputY.selectionStart as number;
        const isNegative = event.key === '-' && idx === 0;
        const isFractional = event.key === '.' && idx > 0 && numbers.indexOf(inputY.value[idx - 1] as string) !== -1 && !/\./.test(inputY.value);
        const isNumber = numbers.indexOf(event.key) != -1;
        if (!(isNegative || isFractional || isNumber)) {
          event.preventDefault();
        }
      });
      inputY.addEventListener("compositionstart", function(event) {
        event.preventDefault();
        this.blur();
      });
    }
  } else {
    console.error("Не удалось найти форму с подходящим id.");
  }
});