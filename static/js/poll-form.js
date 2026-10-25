(() => {
  const container = document.querySelector("#option-forms");
  const addButton = document.querySelector("#add-option");
  const totalInput = document.querySelector("#id_options-TOTAL_FORMS");
  const template = document.querySelector("#empty-option-form");
  if (!container || !addButton || !totalInput || !template) return;

  const rows = () => [...container.querySelectorAll(".option-row")];

  function updateControls() {
    const currentRows = rows();
    currentRows.forEach((row, index) => {
      row.querySelectorAll("input, label").forEach((element) => {
        if (element.name) element.name = element.name.replace(/options-\d+-/, `options-${index}-`);
        if (element.id) element.id = element.id.replace(/id_options-\d+-/, `id_options-${index}-`);
        if (element.htmlFor) element.htmlFor = element.htmlFor.replace(/id_options-\d+-/, `id_options-${index}-`);
      });
    });
    totalInput.value = String(currentRows.length);
    addButton.hidden = currentRows.length >= 5;
    currentRows.forEach((row, index) => {
      const label = row.querySelector("label");
      const remove = row.querySelector(".remove-option");
      if (label) label.textContent = `Seçenek ${index + 1}`;
      if (remove) remove.hidden = currentRows.length <= 2;
    });
  }

  addButton.addEventListener("click", () => {
    const index = rows().length;
    if (rows().length >= 5) return;
    const wrapper = document.createElement("div");
    wrapper.innerHTML = template.innerHTML.replaceAll("__prefix__", String(index)).trim();
    container.append(wrapper.firstElementChild);
    updateControls();
  });

  container.addEventListener("click", (event) => {
    const button = event.target.closest(".remove-option");
    if (!button || rows().length <= 2) return;
    button.closest(".option-row").remove();
    updateControls();
  });

  updateControls();
})();
