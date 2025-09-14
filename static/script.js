
window.addEventListener("DOMContentLoaded", () =>
setTimeout(() =>
  document.querySelectorAll(".alert")
	.forEach(el => bootstrap.Alert.getOrCreateInstance(el).close()),
2275)
);
