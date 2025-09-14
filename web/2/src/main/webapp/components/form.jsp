<%@page contentType="text/html" pageEncoding="UTF-8"%>
<form class="lab-form" id="lab-form-params" autocomplete="off">
  Проверка точки
  <div class="lab-form-field">
    <p><b>X</b></p>
    <select name="X">
    <% for (int i = 4; i >= -4; i--) { %>
      <option value="<%=i%>"><%=i%></option>
    <% } %>
    </select>
  </div>
  <div class="lab-form-error"></div>
  <div class="lab-form-field">
    <p><b>Y</b></p>
    <input name="Y" type="text" class="wide-input" placeholder="Введите дробное число">
  </div>
  <div class="lab-form-error"></div>
  <div class="lab-form-field">
    <p><b>R</b></p>
    <% for (float i = 1; i <= 3; i += 0.5) { %>
      <input name="R" type="button" value="<%=i%>">
    <% } %>
    <input name="R" type="hidden">
    <p class="r-last-scale"></p>
  </div>
  <div class="lab-form-error"></div>
  <button type="submit">Отправить</button>
</form>