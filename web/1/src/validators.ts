export interface FormValidator {
  validate(form: HTMLFormElement): FormValidationStatus;
}

export type FormValidationStatus = {
  valid: boolean;
}