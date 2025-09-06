export interface FormValidator {
  validate(form: HTMLFormElement): FormValidationStatus;
}

export type FormValidationStatus = {
  valid: boolean;
  errors?: FormValidationError[];
}

export type FormValidationError = {
  message: string;
  fieldIdx: number;
}

export class ParamsFormValidator implements FormValidator {
  public validate(form: HTMLFormElement): FormValidationStatus {
    const formInputs = form.querySelectorAll("input");
    const errors: FormValidationError[] = [];
    let hasX = false;
    for (const formInput of formInputs) {
      switch (formInput.name) {
        case "X":
          if (!formInput.checked) {
            continue;
          }
          hasX = true;
          const X = Number(formInput.value);
          const intX = Number.parseInt(formInput.value);
          if (isNaN(X) || X !== intX || X < -5 || X > 3) {
            errors.push({ message: "X должен быть целым от -5 до 3 включительно.", fieldIdx: 0 });
          }
          continue;
        case "Y":
          const Y = Number(formInput.value);
          if (isNaN(Y) || Y < -5 || Y > 3) {
            errors.push({ message: "Y должен быть дробным от -5 до 3 включительно.", fieldIdx: 1 });
          }
          continue;
        case "R":
          const R = formInput.value;
          if (['1', '1.5', '2', '2.5', '3'].indexOf(R) === -1) {
            errors.push({ message: "R должен быть одним из значений: 1, 1.5, 2, 2.5, 3.", fieldIdx: 2 });
          }
          continue;
      }
    }
    if (!hasX) {
      errors.push({ message: "X обязателен для заполнения.", fieldIdx: 0 });
    }
    if (errors.length) {
      return { valid: false, errors: errors };
    } else {
      return { valid: true };
    }
  } 
}