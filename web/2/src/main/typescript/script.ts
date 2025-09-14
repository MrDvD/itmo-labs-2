import { LabDotDomainService, type DotDomainService } from "./services/domain-service/domain-service.js";
import { HistoryService } from "./services/history-service/history-service.js";
import { ParamsFormValidator, type URLParamsValidationStatus } from "./validators.js";

export async function sendToServer(params: URLSearchParams, domainService: DotDomainService): Promise<string | null> {
  const response = await fetch(domainService.getDotDomain() + `?${params.toString()}`, {
    method: "GET",
  });
  if (response.ok) {
    return response.text();
  } else {
    return null;
  }
}

export function clearErrorPlaceholders(form: HTMLFormElement) {
  const errorPlaceholders = form.getElementsByClassName("lab-form-error");
  for (const errorPlaceholder of errorPlaceholders) {
    errorPlaceholder.innerHTML = "";
  }
}

export function processValidatorErrors(status: URLParamsValidationStatus, form: HTMLFormElement) {
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
    const searchValidator = new ParamsFormValidator();
    const historyService = new HistoryService();
    labForm.addEventListener("submit", async function(event) {
      event.preventDefault();
      clearErrorPlaceholders(labForm);
      const formData = new FormData(labForm);
      const submitter = (event as SubmitEvent).submitter as HTMLInputElement | null;
      if (submitter && submitter.name) {
        formData.append(submitter.name, submitter.value);
      }
      const searchParams = new URLSearchParams(
        Array.from(
          formData.entries()).filter(([_, value]) => typeof value === 'string'
        ) as [string, string][]
      );
      const formValidationStatus = searchValidator.validate(searchParams);
      if (!formValidationStatus.valid) {
        processValidatorErrors(formValidationStatus, labForm);
        return;
      }
      const dotResponse = await sendToServer(searchParams, new LabDotDomainService());
      if (dotResponse) {
        historyService.fillHistoryTable(dotResponse);
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