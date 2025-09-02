export interface FormValidator {
  validate(form: HTMLFormElement): FormValidationStatus;
}

export type FormValidationStatus = {
  valid: boolean;
}

export class ParamsFormValidator implements FormValidator {
  public validate(_: HTMLFormElement): FormValidationStatus {
    return { valid: true };
  } 
}