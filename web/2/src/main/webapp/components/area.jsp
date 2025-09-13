<%@page contentType="text/html" import="com.itmo.mrdvd.dto.Dot" pageEncoding="UTF-8"%>
<footer class="lab-query-history">
  <table>
    <caption>
      <b>История запросов</b>
    </caption>
    <thead>
      <tr>
        <td colspan="100" class="centered-cell">
          <img src="/resources/images/png/hint.png" alt="Dot hint">
        </td>
      </tr>
      <tr class="header-row"><td>X</td><td>Y</td><td>R</td><td>Результат</td><td>Дата</td><td>Ожидание</td></tr>
      <%
         Dot[] dots = (Dot[]) request.getAttribute("dots");
         if (dots.length > 0) {
          for (int i = dots.length - 1; i >= 0; i--) { %>
          <tr>
            <td><%=dots[i].X()%></td>
            <td><%=dots[i].Y()%></td>
            <td><%=dots[i].R()%></td>
          </tr>
      <% }} else { %>
          <tr>
            <td colspan="100">Нет запросов!</td>
          </tr>
      <% } %>
    </thead>
    <tbody class="lab-query-history-body"></tbody>
  </table>
</footer>