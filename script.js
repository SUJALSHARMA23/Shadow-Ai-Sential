async function scanPrompt() {
  const promptInput = document.getElementById("prompt");
  const result = document.getElementById("result");
  const eventBody = document.getElementById("eventBody");
  const scanButton = document.getElementById("scanButton");

  const prompt = promptInput.value.trim();

  if (!prompt) {
    result.classList.remove("hidden");
    result.textContent = "Please enter a sample prompt first.";
    return;
  }

  // Start scanning animation
  scanButton.disabled = true;
  scanButton.textContent = "⟳ Scanning...";
  result.classList.remove("hidden");
  result.textContent = "Analyzing your sample prompt...";

  // Wait for 1.2 seconds
  await new Promise(resolve => setTimeout(resolve, 1200));

  // Demo result only
  const riskScore = 25;
  const riskLevel = "Low";
  const status = "Allowed";

  // Show result
  result.replaceChildren();

  const heading = document.createElement("h3");
  heading.textContent = "Scan Results";
  result.appendChild(heading);

  [
    `Status: ${status}`,
    `Risk Level: ${riskLevel}`,
    `Risk Score: ${riskScore}/100`,
    "Detection: Demo result — no real analysis"
  ].forEach(text => {
    const p = document.createElement("p");
    p.textContent = text;
    result.appendChild(p);
  });

  // Update risk meter
  document.getElementById("riskScore").textContent = riskScore;
  document.getElementById("riskLabel").textContent = "Low Risk";

  const circle = document.getElementById("riskCircle");
  circle.style.background =
    "conic-gradient(#39d99a 0deg 90deg, #26364d 90deg 360deg)";

  // Add event to table
  const row = eventBody.insertRow(0);

  const promptCell = row.insertCell(0);
  promptCell.textContent =
    prompt.length > 55 ? prompt.slice(0, 55) + "..." : prompt;

  row.insertCell(1).innerHTML =
    '<span class="badge low-badge">Low</span>';

  row.insertCell(2).innerHTML =
    '<span class="badge green-badge">Allowed</span>';

  row.insertCell(3).textContent =
    new Date().toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit"
    });

  // Finish animation
  scanButton.disabled = false;
  scanButton.textContent = "⌕ Scan Prompt";
}