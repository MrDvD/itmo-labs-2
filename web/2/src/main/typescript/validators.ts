export interface URLParamsValidator {
  validate(params: URLSearchParams): URLParamsValidationStatus;
}

export type URLParamsValidationStatus = {
  valid: boolean;
  errors?: URLParamsValidationError[];
}

export type URLParamsValidationError = {
  message: string;
  fieldIdx: number;
}

export class ParamsFormValidator implements URLParamsValidator {
  public validate(params: URLSearchParams): URLParamsValidationStatus {
    const errors: URLParamsValidationError[] = [];
    const isParamPresent = [false, false, false];
    for (const [key, value] of params) {
      switch (key) {
        case "X":
          const X = Number(value);
          const intX = Number.parseInt(value);
          isParamPresent[0] = true;
          if (isNaN(X) || X !== intX || Math.abs(X) > 4) {
            errors.push({ message: "X должен быть целым от -4 до 4 включительно.", fieldIdx: 0 });
          }
          continue;
        case "Y":
          const Y = Number.parseFloat(value);
          isParamPresent[1] = true;
          if (isNaN(Y) || Math.abs(Y) > 5) {
            errors.push({ message: "Y должен быть дробным от -5 до 5 включительно.", fieldIdx: 1 });
          }
          continue;
        case "R":
          const R = Number.parseFloat(value);
          isParamPresent[2] = true;
          if ([1, 1.5, 2, 2.5, 3].indexOf(R) === -1) {
            errors.push({ message: "R должен быть одним из значений: 1, 1.5, 2, 2.5, 3.", fieldIdx: 2 });
          }
          continue;
      }
    }
    const paramNames = "XYR";
    for (let i = 0; i < 3; i++) {
      if (!isParamPresent[i]) {
        errors.push({ message: `Введите параметр ${paramNames[i]}`, fieldIdx: i });
      }
    }
    if (errors.length) {
      return { valid: false, errors: errors };
    } else {
      return { valid: true };
    }
  } 
}