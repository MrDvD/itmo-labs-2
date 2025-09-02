const formMap = new Map();
export function sendHelios(formId) {
    const selectedForm = document.getElementById(formId);
    if (selectedForm === null) {
        alert("Не удалось найти форму с подходящим id.");
        return;
    }
    if (!(selectedForm instanceof HTMLFormElement)) {
        alert("Элемент с подходящим id не является формой.");
        return;
    }
    const formValidator = getFormValidator(formId);
    if (formValidator && !formValidator.validate(selectedForm)) {
        alert("Форма не прошла проверку валидации.");
        return;
    }
    alert(selectedForm);
}
export function getFormValidator(formId) {
    const formValidator = formMap.get(formId);
    if (formValidator) {
        return formValidator;
    }
    return null;
}
