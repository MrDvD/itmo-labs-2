import { CanvasService } from "../services/canvas-service/canvas-service.js";
import { DomService } from "../services/dom-service/dom-service.js";
import {
  LabDotDomainService,
  type DotDomainService,
} from "../services/domain-service/domain-service.js";
import { HistoryService } from "../services/history-service/history-service.js";
import {
  ParamsFormValidator,
  type URLParamsValidationStatus,
} from "../validators.js";

export async function sendToServer(
  params: URLSearchParams,
  domainService: DotDomainService,
): Promise<string | null> {
  const response = await fetch(
    domainService.getDotDomain() + `?${params.toString()}`,
    {
      method: "GET",
    },
  );
  if (response.ok) {
    return response.text();
  } else {
    return null;
  }
}

export async function analyzeDots(
  searchParams: URLSearchParams,
  R: number,
  domService: DomService,
  historyService: HistoryService,
  canvasService: CanvasService,
  searchValidator: ParamsFormValidator | null,
): Promise<void> {
  if (searchValidator) {
    const formValidationStatus = searchValidator.validate(searchParams);
    if (!formValidationStatus.valid) {
      processValidatorErrors(formValidationStatus, domService.getLabForm());
      return;
    }
  }
  const dotResponse = await sendToServer(
    searchParams,
    new LabDotDomainService(),
  );
  if (dotResponse) {
    historyService.fillHistoryTable(dotResponse);
    canvasService.renderDots(R);
  }
}

export function clearErrorPlaceholders(form: HTMLFormElement) {
  const errorPlaceholders = form.getElementsByClassName("lab-form-error");
  for (const errorPlaceholder of errorPlaceholders) {
    errorPlaceholder.innerHTML = "";
  }
}

export function processValidatorErrors(
  status: URLParamsValidationStatus,
  form: HTMLFormElement,
) {
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

addEventListener("DOMContentLoaded", function () {
  const domService = new DomService();
  const searchValidator = new ParamsFormValidator();
  const historyService = new HistoryService(domService);
  const canvasService = new CanvasService(domService);
  let R: number | null = null;
  if (R !== null) {
    canvasService.renderDots(R);
  }
  domService
    .getLabForm()
    .querySelectorAll('input[name="R"][type="button"]')
    .forEach((input) => {
      input.addEventListener("click", (event) => {
        domService.getRScaleText().innerHTML = (
          event.target as HTMLInputElement
        ).value;
        domService.getRScale().value = domService.getRScaleText().innerHTML;
        R = Number(domService.getRScaleText().innerHTML);
        canvasService.renderDots(R);
      });
    });
  // image submit
  domService.getCanvas().addEventListener("click", async (event) => {
    if (R === null) {
      clearErrorPlaceholders(domService.getLabForm());
      processValidatorErrors(
        {
          valid: false,
          errors: [{ message: "Установите R для однозначности.", fieldIdx: 2 }],
        },
        domService.getLabForm(),
      );
      return;
    }
    clearErrorPlaceholders(domService.getLabForm());
    const X =
      Math.round(
        ((event.offsetX - domService.getCanvas().offsetWidth / 2) * 100 * R) /
          canvasService.getScale(),
      ) / 100;
    const Y =
      Math.round(
        ((event.offsetY - domService.getCanvas().offsetHeight / 2) * -100 * R) /
          canvasService.getScale(),
      ) / 100;
    const searchParams = new URLSearchParams();
    searchParams.append("X", String(X));
    searchParams.append("Y", String(Y));
    searchParams.append("R", String(R));
    await analyzeDots(
      searchParams,
      R,
      domService,
      historyService,
      canvasService,
      null,
    );
  });
  // basic submit
  domService.getLabForm().addEventListener("submit", async function (event) {
    event.preventDefault();
    clearErrorPlaceholders(domService.getLabForm());
    const formData = new FormData(domService.getLabForm());
    const searchParams = new URLSearchParams(
      Array.from(formData.entries()).filter(
        ([_, value]) => typeof value === "string",
      ) as [string, string][],
    );
    if (R !== null) {
      await analyzeDots(
        searchParams,
        R,
        domService,
        historyService,
        canvasService,
        searchValidator,
      );
    }
  });
  // Y input validation
  const inputY = domService.getLabForm().querySelector("input[name='Y']");
  if (inputY && inputY instanceof HTMLInputElement) {
    const numbers = "0123456789";
    inputY.addEventListener("keypress", function (event) {
      const idx = inputY.selectionStart as number;
      const isNegative = event.key === "-" && idx === 0;
      const isFractional =
        event.key === "." &&
        idx > 0 &&
        numbers.indexOf(inputY.value[idx - 1] as string) !== -1 &&
        !/\./.test(inputY.value);
      const isNumber = numbers.indexOf(event.key) != -1;
      if (!(isNegative || isFractional || isNumber)) {
        event.preventDefault();
      }
    });
    inputY.addEventListener("compositionstart", function (event) {
      event.preventDefault();
      this.blur();
    });
    inputY.addEventListener("paste", function (event) {
      if (
        !/-?[0123456789]+(?:\.[0123456789]+)?/.test(
          (event as ClipboardEvent).clipboardData?.getData("text") ?? "",
        )
      ) {
        event.preventDefault();
      }
    });
  }
});
