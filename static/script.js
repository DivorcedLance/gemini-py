document.getElementById("uploadForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const fileInput = document.getElementById("fileInput");
  const promptInput = document.getElementById("promptInput");
  const resultEl = document.getElementById("result");
  const previewEl = document.getElementById("preview");

  if (fileInput.files.length === 0) {
    alert("Por favor selecciona una imagen.");
    return;
  }

  // Vista previa
  const file = fileInput.files[0];
  const reader = new FileReader();
  reader.onload = () => {
    previewEl.innerHTML = `<img src="${reader.result}" alt="preview">`;
  };
  reader.readAsDataURL(file);

  // Construir form data
  const formData = new FormData();
  formData.append("file", file);
  formData.append("prompt", promptInput.value);

  resultEl.textContent = "Procesando...";

  try {
    const response = await fetch("/analyze-image", {
      method: "POST",
      body: formData
    });
    const data = await response.json();
    if (data.result) {
      resultEl.textContent = data.result;
    } else {
      resultEl.textContent = "Error: " + JSON.stringify(data);
    }
  } catch (err) {
    resultEl.textContent = "Error de red: " + err.message;
  }
});
