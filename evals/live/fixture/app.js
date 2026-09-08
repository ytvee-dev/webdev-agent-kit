const theme = document.querySelector("#theme");
const status = document.querySelector("#status");
theme.value = localStorage.getItem("workspace-theme") || "light";
document.querySelector("#save").addEventListener("click", () => {
  localStorage.setItem("theme", theme.value);
  status.textContent = "Saved";
});
