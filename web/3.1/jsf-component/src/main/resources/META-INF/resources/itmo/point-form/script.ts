document.addEventListener("DOMContentLoaded", function() {
  // async update of placeholder for slider values
  this.querySelectorAll(".input-slider").forEach((slider) => {
    const input = slider.querySelector("input");
    const placeholder =
      slider.nextElementSibling as HTMLParagraphElement | null;
    if (input != null && placeholder != null) {
      if (input.value.length > 0) {
        placeholder.innerText = input.value;
      }
      const observer = new MutationObserver((mutations) => {
        mutations.forEach((mutation) => {
          if (mutation.attributeName === "value") {
            placeholder.innerText = Number(input.value).toFixed(2);
          }
        });
      });
      observer.observe(input, { attributes: true });
    } else {
      console.warn(
        "Не удалось найти placeholder для вывода значения слайдера.",
      );
    }
  });
});