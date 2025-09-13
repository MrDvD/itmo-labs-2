<%@page contentType="text/html" pageEncoding="UTF-8"%>
<form class="lab-form" id="lab-form-params" autocomplete="off" action="/">
  Проверка точки
  <div class="lab-form-field">
    <p><b>X</b></p>
    <label class="underline-param-label">
      -5
      <input name="X" type="checkbox" value="-5">
    </label>
    <label class="underline-param-label">
      -4
      <input name="X" type="checkbox" value="-4">
    </label>
    <label class="underline-param-label">
      -3
      <input name="X" type="checkbox" value="-3">
    </label>
    <label class="underline-param-label">
      -2
      <input name="X" type="checkbox" value="-2">
    </label>
    <label class="underline-param-label">
      -1
      <input name="X" type="checkbox" value="-1">
    </label>
    <label class="underline-param-label">
      0
      <input name="X" type="checkbox" value="0">
    </label>
    <label class="underline-param-label">
      1
      <input name="X" type="checkbox" value="1">
    </label>
    <label class="underline-param-label">
      2
      <input name="X" type="checkbox" value="2">
    </label>
    <label class="underline-param-label">
      3
      <input name="X" type="checkbox" value="3">
    </label>
  </div>
  <div class="lab-form-error"></div>
  <div class="lab-form-field">
    <p><b>Y</b></p>
    <input name="Y" type="text" class="wide-input" placeholder="Введите дробное число">
  </div>
  <div class="lab-form-error"></div>
  <div class="lab-form-field">
    <p><b>R</b></p>
    <select name="R">
      <option value="1">1</option>
      <option value="1.5">1.5</option>
      <option value="2">2</option>
      <option value="2.5">2.5</option>
    </select>
  </div>
  <div class="lab-form-error"></div>
  <button type="submit">Отправить</button>
</form>