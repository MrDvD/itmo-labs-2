function updateTime(container: HTMLElement) {
  container.innerText = new Date().toLocaleString();
}

addEventListener("DOMContentLoaded", function () {
  const timeField = this.document.getElementById("time");
  if (!(timeField && timeField instanceof HTMLElement)) {
    throw new Error("Не удалось найти контейнер текущего времени.");
  }
  updateTime(timeField);
  timeField.innerHTML;
  this.setInterval(() => {
    updateTime(timeField);
  }, 8000);
});
