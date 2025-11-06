export function main() {
  document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll(".dynamic-slider").forEach((slider) => {
      const track = slider.querySelector("p:nth-of-type(2)");
      if (track == null) {
        return;
      }
      slider.querySelector("input[type=range]")?.addEventListener("input", (event) => {
        const target = event.target;
        if (target instanceof HTMLInputElement) {
          track.innerHTML = target.value;
        }
      });
    });
  });
}