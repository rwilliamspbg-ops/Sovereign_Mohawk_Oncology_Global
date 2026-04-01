const sections = {
  dashboard: {
    title: "Dashboard",
    subtitle: "47-node federated research network and live privacy budget telemetry."
  },
  trials: {
    title: "Research Trials",
    subtitle: "Active oncology and global disease studies across trusted compute regions."
  },
  pipeline: {
    title: "FL Pipeline",
    subtitle: "Live MOHAWK runtime sequence and Wasm capability enforcement stream."
  },
  compliance: {
    title: "HIPAA / GDPR",
    subtitle: "Mapped architectural controls with regulatory alignment and status."
  },
  security: {
    title: "Security",
    subtitle: "Layered defense model using TPM, signatures, DP, and zero-trust policy."
  },
  consent: {
    title: "Consent Management",
    subtitle: "Patient study consent toggles and legal basis checkpoints."
  },
  metrics: {
    title: "Prometheus Metrics",
    subtitle: "Real-time scrape simulation with alert-state transitions and health traces."
  },
  dpia: {
    title: "DPIA Generator",
    subtitle: "Guided GDPR Art.35 workflow for DPO and supervisory authority readiness."
  },
  llm: {
    title: "LLM Input Workflow",
    subtitle: "Controlled model intake with helper auto-tuners, policy validation, and auditable execution."
  },
  assist: {
    title: "Assist + Threat Analysis",
    subtitle: "AI-assisted research and review workflows with platform-wide threat posture generation."
  },
  professor: {
    title: "Professor Plan",
    subtitle: "Execution-grade roadmap and plug-and-play instrumentation planning for translational oncology research."
  },
  goldsec: {
    title: "Security Gold",
    subtitle: "Top-tier security execution center with do-now controls, scorecards, and 30/60/90 delivery checkpoints."
  }
};

const regionNodes = [
  { name: "N. America", nodes: 9, availability: 99.3 },
  { name: "S. America", nodes: 4, availability: 97.8 },
  { name: "Europe", nodes: 12, availability: 99.1 },
  { name: "Africa", nodes: 5, availability: 96.9 },
  { name: "Asia-Pacific", nodes: 11, availability: 95.8 },
  { name: "Middle East", nodes: 3, availability: 97.2 },
  { name: "Oceania", nodes: 3, availability: 98.7 }
];

const pipelineStages = [
  "LOCAL NODE AGENT",
  "DP GRADIENT CLIP",
  "Ed25519 SIGN",
  "WASM CAP SANDBOX",
  "FL AGGREGATOR",
  "GLOBAL MODEL"
];

const trials = [
  ["SMOP-2024-001", "Oncology", "Lung Cancer", "US/EU", "Enrolling"],
  ["SMOP-2024-002", "Oncology", "Pancreatic", "US/APAC", "Enrolling"],
  ["SMOP-2024-003", "Oncology", "Breast Cancer", "EU", "Active"],
  ["SMOP-2024-004", "Neurological", "Alzheimer", "US/EU", "Active"],
  ["SMOP-2024-005", "Infectious", "Tuberculosis", "Africa/APAC", "Review"],
  ["SMOP-2024-006", "Rare", "ALS", "Global", "Planning"]
];

const complianceRows = [
  ["Federated learning (no PHI transfer)", "HIPAA 164.502", "GDPR Art.5/25", "Pass"],
  ["Differential privacy eps=0.8 sigma=1.1", "HIPAA 164.514", "GDPR Art.89", "Pass"],
  ["Wasmtime capability sandbox", "HIPAA 164.514(d)", "GDPR Art.5(1)(c)", "Pass"],
  ["TPM attestation", "HIPAA 164.312(a)", "GDPR Art.32", "Pass"],
  ["Cross-border gradient transfer", "HIPAA BAAs", "GDPR Art.44/46", "Review"],
  ["Key management + rotation", "HIPAA 164.312", "GDPR Art.32", "Pass"],
  ["Audit trail and retention", "HIPAA 164.312(b)", "GDPR Art.30", "Pass"],
  ["Data minimization policy", "HIPAA minimum necessary", "GDPR Art.5", "Pass"],
  ["Incident response workflow", "HIPAA 164.308(a)(6)", "GDPR Art.33", "Review"],
  ["Subject rights fulfillment", "HIPAA amendment rights", "GDPR Art.15-22", "Pass"]
];

const securityCards = [
  ["Wasmtime Sandbox", "Capability-based WASM isolation with syscall allowlist."],
  ["TPM Attestation", "Node integrity proof and boot chain verification."],
  ["Ed25519 Signatures", "Manifest authenticity and replay prevention."],
  ["Differential Privacy", "Bounded disclosure with controlled epsilon budget."],
  ["Secure Aggregation", "Encrypted gradient mixing with no single-site exposure."],
  ["Zero-Trust Overlay", "Mutual auth + policy gating on every service call."]
];

const consentItems = [
  "Genomic Secondary Use",
  "Cross-border Processing",
  "AI Outcome Analytics",
  "Longitudinal Follow-up",
  "Contact for New Trial"
];

const allowedCaps = ["read_model_weights", "write_clipped_gradient", "verify_manifest", "tpm_quote", "secure_agg_send"];
const blockedCaps = ["open_network_socket", "raw_disk_read", "exec_host_process", "export_phi_payload"];

const nav = document.getElementById("main-nav");
const sectionTitle = document.getElementById("section-title");
const sectionSubtitle = document.getElementById("section-subtitle");

function renderSection(sectionKey) {
  const info = sections[sectionKey];
  sectionTitle.textContent = info.title;
  sectionSubtitle.textContent = info.subtitle;

  document.querySelectorAll("[data-view]").forEach((panel) => {
    panel.hidden = panel.dataset.view !== sectionKey;
  });

  document.querySelectorAll(".nav-item").forEach((btn) => {
    btn.classList.toggle("active", btn.dataset.section === sectionKey);
  });
}

nav.addEventListener("click", (event) => {
  const button = event.target.closest(".nav-item");
  if (!button) return;
  renderSection(button.dataset.section);
});

const nodeMap = document.getElementById("node-map");
const nodeDetail = document.getElementById("node-detail");
regionNodes.forEach((region) => {
  const node = document.createElement("button");
  node.className = "node";
  node.textContent = `${region.name} (${region.nodes})`;
  node.addEventListener("click", () => {
    nodeDetail.textContent = `${region.name}: ${region.nodes} active research nodes, ${region.availability.toFixed(1)}% availability, secure aggregation quorum healthy.`;
  });
  nodeMap.appendChild(node);
});

const pipelineEl = document.getElementById("pipeline-stages");
pipelineStages.forEach((stage, idx) => {
  const stageEl = document.createElement("button");
  stageEl.className = "stage";
  stageEl.textContent = stage;
  stageEl.addEventListener("click", () => {
    nodeDetail.textContent = `Pipeline stage selected: ${stage}. Sequence index ${idx + 1}/6 currently observed in runtime logs.`;
  });
  pipelineEl.appendChild(stageEl);
});

const trialTable = document.getElementById("trial-table");
trialTable.innerHTML = `<thead><tr><th>Trial ID</th><th>Domain</th><th>Target</th><th>Regions</th><th>Status</th></tr></thead>`;
const trialBody = document.createElement("tbody");
const trialDetail = document.getElementById("trial-detail");
trials.forEach((trial) => {
  const tr = document.createElement("tr");
  tr.innerHTML = `<td>${trial[0]}</td><td>${trial[1]}</td><td>${trial[2]}</td><td>${trial[3]}</td><td>${trial[4]}</td>`;
  tr.addEventListener("click", () => {
    trialDetail.textContent = `${trial[0]}: ${trial[2]} study in ${trial[3]} is ${trial[4]}. Next governance checkpoint in 12 days.`;
  });
  trialBody.appendChild(tr);
});
trialTable.appendChild(trialBody);

const complianceTable = document.getElementById("compliance-table");
complianceTable.innerHTML = `<thead><tr><th>Architectural Control</th><th>HIPAA</th><th>GDPR</th><th>Status</th></tr></thead>`;
const complianceBody = document.createElement("tbody");
complianceRows.forEach((row) => {
  const tr = document.createElement("tr");
  tr.innerHTML = `<td>${row[0]}</td><td>${row[1]}</td><td>${row[2]}</td><td>${row[3]} ${row[3] === "Review" ? "↗" : ""}</td>`;
  complianceBody.appendChild(tr);
});
complianceTable.appendChild(complianceBody);

const securityContainer = document.getElementById("security-cards");
securityCards.forEach(([title, text]) => {
  const card = document.createElement("article");
  card.className = "card";
  card.innerHTML = `<h4>${title}</h4><p>${text}</p>`;
  securityContainer.appendChild(card);
});

const consentSwitches = document.getElementById("consent-switches");
consentItems.forEach((item) => {
  const row = document.createElement("div");
  row.className = "switch-row";
  const checkboxId = `consent-${item.toLowerCase().replace(/\s+/g, "-")}`;
  row.innerHTML = `<span>${item}</span><label><input type="checkbox" id="${checkboxId}" checked /></label>`;
  consentSwitches.appendChild(row);
});

document.getElementById("allowed-caps").innerHTML = allowedCaps.map((cap) => `<li>${cap}</li>`).join("");
document.getElementById("blocked-caps").innerHTML = blockedCaps.map((cap) => `<li>${cap}</li>`).join("");

const runtimeLog = document.getElementById("runtime-log");
const auditLog = document.getElementById("audit-log");
const runtimeEvents = [
  "node-agent[eu-04]: collected local batch gradients",
  "dp-clip: l2_norm=0.97 clipped to threshold=0.85",
  "manifest-sign: Ed25519 signature verified",
  "wasmtime: capability gate passed (write_clipped_gradient)",
  "secure-agg: encrypted shard submitted",
  "aggregator: global round 481 committed"
];

function appendLog(container, line) {
  const ts = new Date().toISOString().slice(11, 19);
  container.textContent = `[${ts}] ${line}\n` + container.textContent;
}

setInterval(() => {
  const eventLine = runtimeEvents[Math.floor(Math.random() * runtimeEvents.length)];
  appendLog(runtimeLog, eventLine);
}, 3000);

const auditEvents = [
  "policy-engine: SCC validity check complete",
  "dp-budget: epsilon consumption advanced by 0.01",
  "risk-monitor: Asia-Pacific quorum rebalanced",
  "subject-rights: DSAR queue processed",
  "attestation: TPM quote accepted"
];

setInterval(() => {
  const eventLine = auditEvents[Math.floor(Math.random() * auditEvents.length)];
  appendLog(auditLog, eventLine);
}, 3000);

const epsValueEl = document.getElementById("eps-value");
const epsMeter = document.getElementById("eps-meter");
let epsilon = 0.62;
setInterval(() => {
  epsilon = Math.max(0.35, Math.min(0.92, epsilon + (Math.random() - 0.45) * 0.03));
  epsValueEl.textContent = `${epsilon.toFixed(2)} / 0.80`;
  epsMeter.style.width = `${Math.min(100, (epsilon / 0.8) * 100).toFixed(1)}%`;
}, 2800);

const diseaseFilter = document.getElementById("disease-filter");
diseaseFilter.addEventListener("click", (event) => {
  const btn = event.target.closest(".chip");
  if (!btn) return;
  document.querySelectorAll(".chip").forEach((chip) => chip.classList.remove("active"));
  btn.classList.add("active");
  const value = btn.dataset.disease;
  const rows = trialBody.querySelectorAll("tr");
  rows.forEach((row) => {
    const domain = row.children[1].textContent.toLowerCase();
    row.hidden = value !== "all" && !domain.includes(value);
  });
});

document.querySelector(".quick-actions").addEventListener("click", (event) => {
  const btn = event.target.closest("button");
  if (!btn) return;
  const actionMap = {
    risk: "Triggered risk deep-dive. Residual risk score now in analyst queue.",
    dpia: "Opened DPIA workflow and prefilled processing metadata.",
    scc: "Opened cross-border SCC review packet for legal signoff."
  };
  appendLog(auditLog, actionMap[btn.dataset.action]);
});

const metricFeeds = {
  throughput: { label: "FL Throughput", unit: "updates/min", base: 210 },
  epsilon: { label: "Epsilon Consumption", unit: "epsilon", base: 0.64 },
  latency: { label: "Round Latency P95", unit: "ms", base: 890 },
  health: { label: "Node Health", unit: "%", base: 98.5 }
};

const metricWindows = {
  30: 30,
  60: 60,
  300: 300
};

let activeFeed = "throughput";
let activeWindow = 60;
const metricData = [];

const feedContainer = document.getElementById("metric-feed");
const windowContainer = document.getElementById("metric-window");
const canvas = document.getElementById("metrics-canvas");
const ctx = canvas.getContext("2d");
const alarmBanner = document.getElementById("alarm-banner");
const metricBottom = document.getElementById("metric-bottom");

Object.keys(metricFeeds).forEach((key) => {
  const b = document.createElement("button");
  b.textContent = metricFeeds[key].label;
  b.className = key === activeFeed ? "active" : "";
  b.addEventListener("click", () => {
    activeFeed = key;
    metricData.length = 0;
    updateMetricButtons();
  });
  feedContainer.appendChild(b);
});

Object.keys(metricWindows).forEach((key) => {
  const b = document.createElement("button");
  b.textContent = key === "30" ? "30s" : key === "60" ? "1m" : "5m";
  b.className = Number(key) === activeWindow ? "active" : "";
  b.addEventListener("click", () => {
    activeWindow = Number(key);
    updateMetricButtons();
  });
  windowContainer.appendChild(b);
});

function updateMetricButtons() {
  [...feedContainer.children].forEach((el, i) => {
    el.classList.toggle("active", Object.keys(metricFeeds)[i] === activeFeed);
  });
  [...windowContainer.children].forEach((el, i) => {
    el.classList.toggle("active", Number(Object.keys(metricWindows)[i]) === activeWindow);
  });
}

function nextMetricValue() {
  const feed = metricFeeds[activeFeed];
  const jitter = (Math.random() - 0.5) * (feed.base * 0.08);
  return Math.max(0.001, feed.base + jitter);
}

function drawChart() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  if (!metricData.length) return;

  const vals = metricData.map((m) => m.value);
  const min = Math.min(...vals) * 0.95;
  const max = Math.max(...vals) * 1.05;

  ctx.strokeStyle = "#1e6f5c";
  ctx.lineWidth = 2;
  ctx.beginPath();
  metricData.forEach((point, idx) => {
    const x = (idx / (metricData.length - 1 || 1)) * (canvas.width - 40) + 20;
    const y = canvas.height - ((point.value - min) / (max - min || 1)) * (canvas.height - 30) - 15;
    if (idx === 0) ctx.moveTo(x, y);
    else ctx.lineTo(x, y);
  });
  ctx.stroke();

  ctx.fillStyle = "#4d5b43";
  ctx.font = "12px IBM Plex Mono";
  ctx.fillText(`${metricFeeds[activeFeed].label} (${metricFeeds[activeFeed].unit})`, 20, 18);
  ctx.fillText(`Window: ${activeWindow}s`, canvas.width - 120, 18);
}

function updateAlarmAndBottom() {
  const apacAvailability = 94 + Math.random() * 6;
  const sandboxViolations = Math.random() > 0.78 ? Math.floor(Math.random() * 3) + 1 : 0;
  const epsPct = (epsilon / 0.8) * 100;

  let cls = "ok";
  let label = "Status: NORMAL";
  if (epsPct > 87) {
    cls = "critical";
    label = "Status: CRITICAL - epsilon budget threshold";
  } else if (apacAvailability < 96 || sandboxViolations > 0) {
    cls = "warn";
    label = "Status: WARN - node health fluctuation";
  }

  alarmBanner.className = `alarm ${cls}`;
  alarmBanner.textContent = label;

  metricBottom.innerHTML = `
    <div class="metric-pill">N. America Availability: ${(97 + Math.random() * 2).toFixed(2)}%</div>
    <div class="metric-pill">Europe Availability: ${(97.2 + Math.random() * 1.9).toFixed(2)}%</div>
    <div class="metric-pill">Asia-Pacific Availability: ${apacAvailability.toFixed(2)}%</div>
    <div class="metric-pill">Wasm Sandbox Violations: <strong style="color:${sandboxViolations ? "#b62835" : "#185423"}">${sandboxViolations}</strong></div>
  `;
}

setInterval(() => {
  metricData.push({ t: Date.now(), value: nextMetricValue() });
  const maxPoints = Math.max(15, Math.floor(activeWindow / 2));
  if (metricData.length > maxPoints) metricData.shift();
  drawChart();
  updateAlarmAndBottom();
}, 2000);

const dpiaSteps = [
  "Processing Description",
  "Necessity & Proportionality",
  "Risk Assessment",
  "Data Subject Rights",
  "Authority Consultation"
];

const dpiaState = {
  currentStep: 1,
  values: {
    trialId: "",
    irbNumber: "",
    dpo: "",
    legalBasis: "",
    processingSummary: "",
    necessityMinData: "yes",
    necessityRetention: "yes",
    necessityAccessControls: "yes",
    riskLevel: "medium",
    riskNotes: "",
    rightsMechanism: "",
    rightsSlaDays: "30",
    authorityTrigger: "no",
    authorityNotes: ""
  }
};

const stepper = document.getElementById("dpia-stepper");
const form = document.getElementById("dpia-form");
const feedback = document.getElementById("dpia-feedback");
const report = document.getElementById("dpia-report");

function stepButton(label, idx) {
  return `<span class="step ${dpiaState.currentStep === idx + 1 ? "active" : ""}">${idx + 1}. ${label}</span>`;
}

function renderStepper() {
  stepper.innerHTML = dpiaSteps.map((label, idx) => stepButton(label, idx)).join("");
}

function input(label, name, required = false, type = "text") {
  const value = dpiaState.values[name] || "";
  return `<label>${label}${required ? " *" : ""}<input type="${type}" name="${name}" value="${value}" /></label>`;
}

function textarea(label, name, required = false) {
  const value = dpiaState.values[name] || "";
  return `<label>${label}${required ? " *" : ""}<textarea name="${name}" rows="3">${value}</textarea></label>`;
}

function select(label, name, options) {
  const value = dpiaState.values[name];
  const html = options.map((opt) => `<option value="${opt}" ${opt === value ? "selected" : ""}>${opt.toUpperCase()}</option>`).join("");
  return `<label>${label}<select name="${name}">${html}</select></label>`;
}

function renderDpiaForm() {
  renderStepper();
  const step = dpiaState.currentStep;

  if (step === 1) {
    form.innerHTML = [
      input("Trial ID", "trialId", true),
      input("IRB Number", "irbNumber", true),
      input("DPO Name", "dpo", true),
      input("Legal Basis (Art.6/9)", "legalBasis", true),
      textarea("Processing Description", "processingSummary", true)
    ].join("");
  }

  if (step === 2) {
    form.innerHTML = [
      select("Minimum necessary data (HIPAA 164.514(d) / GDPR Art.5)", "necessityMinData", ["yes", "no"]),
      select("Retention schedule defined (GDPR Art.5(1)(e))", "necessityRetention", ["yes", "no"]),
      select("Access controls validated (HIPAA 164.312 / GDPR Art.32)", "necessityAccessControls", ["yes", "no"])
    ].join("");
  }

  if (step === 3) {
    form.innerHTML = [
      select("Residual risk level", "riskLevel", ["low", "medium", "high"]),
      textarea("Risk treatment notes", "riskNotes", true)
    ].join("");
  }

  if (step === 4) {
    form.innerHTML = [
      textarea("Data subject rights mechanism (Art.15-22)", "rightsMechanism", true),
      input("Response SLA (days)", "rightsSlaDays", true, "number")
    ].join("");
  }

  if (step === 5) {
    form.innerHTML = [
      select("Supervisory authority consultation required (Art.36)", "authorityTrigger", ["no", "yes"]),
      textarea("Authority consultation notes", "authorityNotes")
    ].join("");
  }
}

form.addEventListener("input", (event) => {
  const target = event.target;
  dpiaState.values[target.name] = target.value;
});

document.getElementById("dpia-next").addEventListener("click", () => {
  dpiaState.currentStep = Math.min(5, dpiaState.currentStep + 1);
  renderDpiaForm();
});

document.getElementById("dpia-prev").addEventListener("click", () => {
  dpiaState.currentStep = Math.max(1, dpiaState.currentStep - 1);
  renderDpiaForm();
});

function validateDpia() {
  const requiredFields = [
    "trialId",
    "irbNumber",
    "dpo",
    "legalBasis",
    "processingSummary",
    "riskNotes",
    "rightsMechanism",
    "rightsSlaDays"
  ];
  const missing = requiredFields.filter((field) => !String(dpiaState.values[field] || "").trim());
  if (missing.length) {
    feedback.textContent = `Validation failed: missing required fields -> ${missing.join(", ")}`;
    return false;
  }
  feedback.textContent = "Validation passed: DPIA package is complete for report generation.";
  return true;
}

document.getElementById("dpia-validate").addEventListener("click", validateDpia);

document.getElementById("dpia-generate").addEventListener("click", () => {
  if (!validateDpia()) return;

  const v = dpiaState.values;
  const riskScore = v.riskLevel === "high" ? 84 : v.riskLevel === "medium" ? 58 : 31;
  const authority = v.authorityTrigger === "yes" ? "Required under Art.36" : "Not required at present";

  report.textContent = [
    "SOVEREIGN MOHAWK DPIA REPORT",
    "----------------------------------",
    `Trial ID: ${v.trialId}`,
    `IRB: ${v.irbNumber}`,
    `DPO: ${v.dpo}`,
    `Legal Basis: ${v.legalBasis}`,
    "",
    "1) Processing Description",
    `${v.processingSummary}`,
    "",
    "2) Necessity & Proportionality",
    `Minimum Data: ${v.necessityMinData}`,
    `Retention Schedule: ${v.necessityRetention}`,
    `Access Controls: ${v.necessityAccessControls}`,
    "",
    "3) Risk Assessment",
    `Residual Risk: ${v.riskLevel.toUpperCase()} (${riskScore}/100)` ,
    `Mitigation Notes: ${v.riskNotes}`,
    "",
    "4) Data Subject Rights",
    `Mechanism: ${v.rightsMechanism}`,
    `SLA: ${v.rightsSlaDays} days`,
    "",
    "5) Supervisory Authority",
    `${authority}`,
    `Notes: ${v.authorityNotes || "N/A"}`,
    "",
    "Formal Submission Draft",
    "This DPIA confirms implementation of data minimisation, access control, and safeguards consistent with HIPAA 164.514 and GDPR Art.5/25/32/35. Residual risks are monitored under continuous federated governance and reviewed by the DPO.",
    "----------------------------------",
    `Generated: ${new Date().toISOString()}`
  ].join("\n");

  feedback.textContent = "DPIA report generated for DPO submission draft.";
});

const modelRegistryForm = document.getElementById("model-registry-form");
const modelFeedback = document.getElementById("model-feedback");
const promptTemplate = document.getElementById("prompt-template");
const promptFeedback = document.getElementById("prompt-feedback");
const gateList = document.getElementById("gate-list");
const gateFeedback = document.getElementById("gate-feedback");
const llmAuditTable = document.getElementById("llm-audit-table");

const modelRegistry = [];
const llmAuditRows = [];

const modelState = {
  modelName: "",
  provider: "Sovereign Hosted",
  endpoint: "",
  version: "",
  taskType: "cohort-summary",
  riskTier: "moderate",
  contextWindow: "16384",
  temperature: "0.2",
  maxTokens: "900",
  topP: "0.9",
  freqPenalty: "0.1",
  phiMode: "strict"
};

const governanceGates = [
  { id: "irbApproved", label: "IRB approval verified", required: true },
  { id: "dpoReviewed", label: "DPO reviewed model purpose", required: true },
  { id: "dataDeIdentified", label: "Data de-identification confirmed", required: true },
  { id: "baaSigned", label: "HIPAA BAAs or processor terms documented", required: true },
  { id: "dpBudgetAllocated", label: "Differential privacy budget allocated", required: true },
  { id: "crossBorderScc", label: "Cross-border SCC packet approved", required: false },
  { id: "humanInLoop", label: "Human reviewer assigned for output sign-off", required: true }
];

const gateState = governanceGates.reduce((acc, gate) => {
  acc[gate.id] = false;
  return acc;
}, {});

function modelInput(label, name, type = "text") {
  const value = modelState[name] || "";
  return `<label>${label}<input type="${type}" name="${name}" value="${value}" /></label>`;
}

function modelSelect(label, name, options) {
  const value = modelState[name] || "";
  const optionHtml = options.map((opt) => `<option value="${opt}" ${opt === value ? "selected" : ""}>${opt}</option>`).join("");
  return `<label>${label}<select name="${name}">${optionHtml}</select></label>`;
}

function renderModelRegistryForm() {
  modelRegistryForm.innerHTML = [
    modelInput("Model Name", "modelName"),
    modelInput("Version", "version"),
    modelInput("Endpoint", "endpoint"),
    modelSelect("Provider", "provider", ["Sovereign Hosted", "Azure OpenAI", "OpenAI", "Anthropic", "Local Inference"]),
    modelSelect("Task Type", "taskType", ["cohort-summary", "adverse-event-triage", "trial-qa", "protocol-drafting"]),
    modelSelect("Risk Tier", "riskTier", ["low", "moderate", "high"]),
    modelSelect("PHI Mode", "phiMode", ["strict", "redacted-only", "research-limited"]),
    `<div class="hint-row">${modelInput("Context Window", "contextWindow", "number")}${modelInput("Temperature", "temperature", "number")}</div>`,
    `<div class="hint-row">${modelInput("Max Tokens", "maxTokens", "number")}${modelInput("Top-p", "topP", "number")}</div>`,
    modelInput("Frequency Penalty", "freqPenalty", "number")
  ].join("");
}

modelRegistryForm.addEventListener("input", (event) => {
  const target = event.target;
  modelState[target.name] = target.value;
});

function autoFillModelHelper() {
  const presets = {
    "cohort-summary": { temperature: "0.15", maxTokens: "900", topP: "0.88", freqPenalty: "0.05", contextWindow: "16384" },
    "adverse-event-triage": { temperature: "0.05", maxTokens: "700", topP: "0.82", freqPenalty: "0.2", contextWindow: "8192" },
    "trial-qa": { temperature: "0.2", maxTokens: "850", topP: "0.9", freqPenalty: "0.1", contextWindow: "16384" },
    "protocol-drafting": { temperature: "0.3", maxTokens: "1400", topP: "0.93", freqPenalty: "0.05", contextWindow: "32768" }
  };
  Object.assign(modelState, presets[modelState.taskType]);
  renderModelRegistryForm();
  modelFeedback.textContent = `Helper applied for ${modelState.taskType}: tuned defaults loaded for research-safe output stability.`;
}

function autoTuneModelRuntime() {
  const riskWeight = modelState.riskTier === "high" ? 0.55 : modelState.riskTier === "moderate" ? 0.8 : 1;
  const phiWeight = modelState.phiMode === "strict" ? 0.7 : modelState.phiMode === "redacted-only" ? 0.85 : 1;
  const factor = Math.max(0.45, riskWeight * phiWeight);

  modelState.temperature = (0.32 * factor).toFixed(2);
  modelState.topP = (0.76 + factor * 0.16).toFixed(2);
  modelState.maxTokens = String(Math.round(1200 * factor + 450));
  modelState.freqPenalty = (0.28 - factor * 0.16).toFixed(2);

  renderModelRegistryForm();
  modelFeedback.textContent = `Auto-tuner updated controls for risk=${modelState.riskTier}, phi=${modelState.phiMode}. Temperature=${modelState.temperature}, maxTokens=${modelState.maxTokens}.`;
}

function saveModelRegistryEntry() {
  const required = ["modelName", "version", "endpoint"];
  const missing = required.filter((f) => !String(modelState[f] || "").trim());
  if (missing.length) {
    modelFeedback.textContent = `Cannot save model entry. Missing fields: ${missing.join(", ")}.`;
    return;
  }

  const entry = {
    id: `mdl-${Date.now().toString().slice(-6)}`,
    ...modelState,
    savedAt: new Date().toISOString()
  };
  modelRegistry.unshift(entry);
  modelFeedback.textContent = `Model saved: ${entry.modelName} ${entry.version}. Registry size: ${modelRegistry.length}.`;
  appendLog(auditLog, `llm-registry: ${entry.modelName} saved with ${entry.riskTier} risk policy`);
}

document.getElementById("model-helper").addEventListener("click", autoFillModelHelper);
document.getElementById("model-autotune").addEventListener("click", autoTuneModelRuntime);
document.getElementById("model-save").addEventListener("click", saveModelRegistryEntry);

function validatePromptTemplateContent() {
  const template = promptTemplate.value.trim();
  const requiredPlaceholders = ["{{trial_id}}", "{{cohort_id}}", "{{analysis_goal}}"];
  const blockedPatterns = ["patient_name", "full_name", "ssn", "date_of_birth", "email@", "phone_number", "address"]; 

  if (!template) {
    promptFeedback.textContent = "Template is empty. Add a structured prompt template before validation.";
    return { ok: false, score: 0 };
  }

  const missing = requiredPlaceholders.filter((ph) => !template.includes(ph));
  const hits = blockedPatterns.filter((pattern) => template.toLowerCase().includes(pattern));
  let score = 100;
  score -= missing.length * 15;
  score -= hits.length * 20;

  if (hits.length) {
    promptFeedback.textContent = `Validation failed: disallowed identifiers detected (${hits.join(", ")}). Remove direct identifiers.`;
    return { ok: false, score: Math.max(score, 0) };
  }

  if (missing.length) {
    promptFeedback.textContent = `Template partially valid. Missing placeholders: ${missing.join(", ")}.`;
    return { ok: false, score: Math.max(score, 0) };
  }

  promptFeedback.textContent = `Template valid. Policy score ${Math.max(score, 0)}/100 with no direct identifier keywords.`;
  return { ok: true, score: Math.max(score, 0) };
}

document.getElementById("prompt-helper").addEventListener("click", () => {
  promptTemplate.value = [
    "System: You are a research analysis assistant. Reject direct identifiers.",
    "Task: {{analysis_goal}}",
    "Trial: {{trial_id}}",
    "Cohort: {{cohort_id}}",
    "Data policy: Use de-identified values only. If PHI appears, return POLICY_BLOCK.",
    "Output format: bullet findings, confidence, required human-review flags."
  ].join("\n");
  promptFeedback.textContent = "Safe starter template inserted with required placeholders and policy guardrails.";
});

document.getElementById("prompt-validate").addEventListener("click", validatePromptTemplateContent);

document.getElementById("prompt-autotune").addEventListener("click", () => {
  const template = promptTemplate.value;
  const tuneNotes = [];
  if (!template.includes("POLICY_BLOCK")) tuneNotes.push("Added POLICY_BLOCK fail-closed behavior");
  if (!template.includes("human-review")) tuneNotes.push("Added human-review enforcement");

  const additions = [];
  if (!template.includes("POLICY_BLOCK")) additions.push("If any direct identifier appears, return POLICY_BLOCK and do not answer.");
  if (!template.includes("human-review")) additions.push("Mark high-impact outputs as human-review required.");

  promptTemplate.value = [template.trim(), ...additions].filter(Boolean).join("\n");
  const result = validatePromptTemplateContent();
  promptFeedback.textContent = `Prompt auto-tuner complete (${result.score}/100). ${tuneNotes.length ? tuneNotes.join("; ") : "No additional controls were needed."}`;
});

function renderGovernanceGates() {
  gateList.innerHTML = governanceGates.map((gate) => {
    const checked = gateState[gate.id] ? "checked" : "";
    const requiredTag = gate.required ? "required" : "optional";
    return `<div class="switch-row"><span>${gate.label} (${requiredTag})</span><label><input type="checkbox" data-gate="${gate.id}" ${checked} /></label></div>`;
  }).join("");
}

gateList.addEventListener("input", (event) => {
  const target = event.target;
  if (!target.dataset.gate) return;
  gateState[target.dataset.gate] = target.checked;
});

document.getElementById("gate-helper").addEventListener("click", () => {
  governanceGates.forEach((gate) => {
    gateState[gate.id] = gate.required;
  });
  renderGovernanceGates();
  gateFeedback.textContent = "Recommended defaults applied: all required controls enabled, optional cross-border gate left for legal confirmation.";
});

function evaluateGovernanceReadiness() {
  const failed = governanceGates
    .filter((gate) => gate.required && !gateState[gate.id])
    .map((gate) => gate.label);

  const promptResult = validatePromptTemplateContent();
  const hasModel = modelRegistry.length > 0;

  if (!hasModel) {
    gateFeedback.textContent = "Readiness blocked: save at least one model registry entry before execution.";
    return false;
  }

  if (failed.length || !promptResult.ok) {
    gateFeedback.textContent = `Readiness blocked. Required gates missing: ${failed.join(", ") || "none"}. Prompt valid: ${promptResult.ok ? "yes" : "no"}.`;
    return false;
  }

  gateFeedback.textContent = `Readiness passed. ${modelRegistry[0].modelName} is approved for controlled execution.`;
  return true;
}

document.getElementById("gate-evaluate").addEventListener("click", evaluateGovernanceReadiness);

function renderLlmAuditTable() {
  llmAuditTable.innerHTML = `<thead><tr><th>Time</th><th>Event</th><th>Model</th><th>Result</th><th>Details</th></tr></thead>`;
  const body = document.createElement("tbody");
  llmAuditRows.forEach((row) => {
    const tr = document.createElement("tr");
    tr.innerHTML = `<td>${row.time}</td><td>${row.event}</td><td>${row.model}</td><td>${row.result}</td><td>${row.details}</td>`;
    body.appendChild(tr);
  });
  llmAuditTable.appendChild(body);
}

function quickHash(value) {
  let hash = 0;
  for (let i = 0; i < value.length; i += 1) {
    hash = (hash * 31 + value.charCodeAt(i)) >>> 0;
  }
  return hash.toString(16).padStart(8, "0");
}

function addAuditEntry(event, model, result, details) {
  llmAuditRows.unshift({
    time: new Date().toISOString().slice(11, 19),
    event,
    model,
    result,
    details
  });
  if (llmAuditRows.length > 12) llmAuditRows.pop();
  renderLlmAuditTable();
}

document.getElementById("audit-simulate").addEventListener("click", () => {
  const ready = evaluateGovernanceReadiness();
  const model = modelRegistry[0]?.modelName || "unspecified";
  if (!ready) {
    addAuditEntry("execution_attempt", model, "blocked", "Governance or prompt policy checks failed.");
    appendLog(auditLog, "llm-exec: blocked due to failed readiness checks");
    return;
  }

  const traceId = `trace-${Date.now().toString().slice(-7)}`;
  const templateHash = quickHash(promptTemplate.value);
  addAuditEntry("execution_start", model, "pass", `trace=${traceId}; template_hash=${templateHash}`);
  addAuditEntry("policy_guard", model, "pass", "PHI filter strict mode active; human-review flag attached.");
  addAuditEntry("execution_finish", model, "pass", "Output queued for reviewer sign-off within SLA.");
  appendLog(auditLog, `llm-exec: completed ${traceId} with model ${model}`);
});

document.getElementById("audit-clear").addEventListener("click", () => {
  llmAuditRows.length = 0;
  renderLlmAuditTable();
  appendLog(auditLog, "llm-audit: execution viewer cleared by operator");
});

const assistMode = document.getElementById("assist-mode");
const assistObjective = document.getElementById("assist-objective");
const assistContext = document.getElementById("assist-context");
const assistFeedback = document.getElementById("assist-feedback");
const assistOutput = document.getElementById("assist-output");

const threatSummary = document.getElementById("threat-summary");
const threatTable = document.getElementById("threat-table");

const threatCatalog = [
  {
    id: "spoofing",
    category: "Spoofing / Identity",
    vector: "Untrusted node or model endpoint impersonation",
    baseLikelihood: 2.4,
    baseImpact: 4.8,
    mitigation: "TPM attestation + mTLS pinning + model endpoint allowlist"
  },
  {
    id: "tampering",
    category: "Tampering",
    vector: "Gradient or prompt-template manipulation in transit",
    baseLikelihood: 2.8,
    baseImpact: 4.5,
    mitigation: "Ed25519 manifest signing + immutable audit log + hash checks"
  },
  {
    id: "repudiation",
    category: "Repudiation",
    vector: "Operator denies model execution or data policy override",
    baseLikelihood: 2.1,
    baseImpact: 3.8,
    mitigation: "Trace IDs, signed execution records, and reviewer attribution"
  },
  {
    id: "information-disclosure",
    category: "Information Disclosure",
    vector: "Prompt leakage of direct identifiers or sensitive trial data",
    baseLikelihood: 3.2,
    baseImpact: 5.0,
    mitigation: "Prompt validator, PHI strict mode, and fail-closed POLICY_BLOCK"
  },
  {
    id: "dos",
    category: "Denial of Service",
    vector: "Compute saturation during FL rounds and LLM review bursts",
    baseLikelihood: 2.7,
    baseImpact: 3.9,
    mitigation: "Rate limiting, per-workload quotas, and round-aware scheduling"
  },
  {
    id: "eop",
    category: "Elevation of Privilege",
    vector: "Capability escalation in Wasm sandbox or assistant actions",
    baseLikelihood: 2.0,
    baseImpact: 4.9,
    mitigation: "Capability deny-by-default, policy engine guardrails, and approval gates"
  }
];

const threatTuneState = {
  monitoringBoost: 1,
  governanceBoost: 1,
  runtimeBoost: 1
};

function setAssistHelperPrompt() {
  const mode = assistMode.value;
  const templates = {
    research: {
      objective: "Generate a cross-region enrollment and outcome drift analysis",
      context: "Trial scope: SMOP-2024-001 and SMOP-2024-002\nFocus: enrollment velocity, cohort imbalance, adverse events\nOutput: prioritized hypotheses, follow-up analyses, and FL-safe data asks"
    },
    review: {
      objective: "Review protocol deviations and propose corrective actions",
      context: "Review checklist: endpoint integrity, missing visits, consent exceptions\nCompare active trials by region and governance status\nOutput: risk-ranked issues and remediation owners"
    },
    compliance: {
      objective: "Assess readiness for HIPAA/GDPR oversight review",
      context: "Map controls to HIPAA 164.312 and GDPR Art.5/25/32/35\nConfirm SCC and DPO checkpoints\nOutput: pass/review items and escalation triggers"
    }
  };
  assistObjective.value = templates[mode].objective;
  assistContext.value = templates[mode].context;
  assistFeedback.textContent = `Smart helper prompt loaded for ${mode} mode.`;
}

function runAssistanceAgent() {
  const mode = assistMode.value;
  const objective = assistObjective.value.trim();
  const context = assistContext.value.trim();

  if (!objective || !context) {
    assistFeedback.textContent = "Assistance blocked: provide both objective and context.";
    return;
  }

  const topTrial = trials[0][0];
  const reviewPending = complianceRows.filter((row) => row[3] === "Review").length;
  const llmReady = modelRegistry.length > 0 ? "yes" : "no";
  const score = Math.min(100, 62 + (llmReady === "yes" ? 14 : 0) - reviewPending * 4);

  const actionPack = [
    "1) Build evidence set from trial activity, FL logs, and compliance table",
    "2) Run bias and privacy checks before drafting conclusions",
    "3) Generate reviewer packet with owners, due dates, and escalation paths"
  ];

  assistOutput.textContent = [
    `ASSISTANCE AGENT RESULT (${mode.toUpperCase()})`,
    "----------------------------------",
    `Objective: ${objective}`,
    `Context length: ${context.length} chars`,
    `Primary trial anchor: ${topTrial}`,
    `LLM workflow registered: ${llmReady}`,
    `Compliance review items open: ${reviewPending}`,
    `Confidence score: ${score}/100`,
    "",
    "Recommended Actions",
    ...actionPack,
    "",
    "Suggested Deliverables",
    "- Executive summary with risks and decisions",
    "- Technical appendix with runtime/audit excerpts",
    "- Compliance appendix mapped to HIPAA/GDPR controls",
    "----------------------------------",
    `Generated: ${new Date().toISOString()}`
  ].join("\n");

  assistFeedback.textContent = `Assistance run complete in ${mode} mode. Confidence ${score}/100.`;
  appendLog(auditLog, `assist-agent: completed ${mode} run with score ${score}/100`);
}

function buildReviewPacket() {
  const objective = assistObjective.value.trim();
  if (!objective) {
    assistFeedback.textContent = "Review packet blocked: objective is required.";
    return;
  }

  const packet = [
    "REVIEW PACKET",
    "----------------------------------",
    `Objective: ${objective}`,
    `Date: ${new Date().toISOString().slice(0, 10)}`,
    "",
    "Sections",
    "1) Research question and assumptions",
    "2) Data boundaries and federated constraints",
    "3) Threat posture and mitigation status",
    "4) Regulatory mapping and unresolved controls",
    "5) Reviewer sign-off checklist",
    "",
    "Auto-attached signals",
    `- Runtime stream active: yes`,
    `- LLM models registered: ${modelRegistry.length}`,
    `- Open compliance review rows: ${complianceRows.filter((row) => row[3] === "Review").length}`,
    "----------------------------------"
  ].join("\n");

  assistOutput.textContent = packet;
  assistFeedback.textContent = "Review packet generated and ready for human reviewer handoff.";
  appendLog(auditLog, "assist-agent: review packet generated");
}

document.getElementById("assist-helper").addEventListener("click", setAssistHelperPrompt);
document.getElementById("assist-run").addEventListener("click", runAssistanceAgent);
document.getElementById("assist-review-packet").addEventListener("click", buildReviewPacket);

function computeThreatRows() {
  const llmRiskBoost = modelRegistry[0]?.riskTier === "high" ? 1.2 : modelRegistry[0]?.riskTier === "moderate" ? 1.05 : 0.95;
  const epsPressure = Math.max(0.9, Math.min(1.2, epsilon / 0.8));
  const reviewPressure = 1 + complianceRows.filter((row) => row[3] === "Review").length * 0.04;

  return threatCatalog.map((threat) => {
    const likelihood = threat.baseLikelihood * epsPressure * threatTuneState.monitoringBoost;
    const impact = threat.baseImpact * llmRiskBoost * threatTuneState.runtimeBoost;
    const score = likelihood * impact * reviewPressure * threatTuneState.governanceBoost;
    const severity = score >= 16 ? "High" : score >= 10 ? "Medium" : "Low";
    return {
      ...threat,
      likelihood: Math.min(5, likelihood).toFixed(2),
      impact: Math.min(5, impact).toFixed(2),
      score: Math.min(25, score).toFixed(2),
      severity
    };
  });
}

function renderThreatTable(rows) {
  threatTable.innerHTML = `<thead><tr><th>Category</th><th>Vector</th><th>Likelihood</th><th>Impact</th><th>Score</th><th>Severity</th><th>Mitigation</th></tr></thead>`;
  const body = document.createElement("tbody");
  rows.forEach((row) => {
    const tr = document.createElement("tr");
    tr.innerHTML = `<td>${row.category}</td><td>${row.vector}</td><td>${row.likelihood}</td><td>${row.impact}</td><td>${row.score}</td><td>${row.severity}</td><td>${row.mitigation}</td>`;
    body.appendChild(tr);
  });
  threatTable.appendChild(body);
}

function summarizeThreats(rows) {
  const high = rows.filter((row) => row.severity === "High").length;
  const medium = rows.filter((row) => row.severity === "Medium").length;
  const avg = (rows.reduce((sum, row) => sum + Number(row.score), 0) / rows.length).toFixed(2);
  const status = high > 1 ? "Elevated" : high === 1 ? "Guarded" : "Stable";
  threatSummary.textContent = `Threat posture: ${status}. High=${high}, Medium=${medium}, Average score=${avg}/25.`;
}

function generateThreatAnalysis() {
  const rows = computeThreatRows();
  renderThreatTable(rows);
  summarizeThreats(rows);
  const highest = rows.reduce((max, row) => (Number(row.score) > Number(max.score) ? row : max), rows[0]);
  appendLog(auditLog, `threat-analysis: generated, top risk ${highest.category} (${highest.score})`);
}

document.getElementById("threat-autotune").addEventListener("click", () => {
  const hasRegisteredModel = modelRegistry.length > 0;
  threatTuneState.monitoringBoost = hasRegisteredModel ? 0.92 : 1.04;
  threatTuneState.governanceBoost = evaluateGovernanceReadiness() ? 0.88 : 1.1;
  threatTuneState.runtimeBoost = modelState.phiMode === "strict" ? 0.9 : 1.03;
  generateThreatAnalysis();
  threatSummary.textContent += " Auto-tuner applied mitigation weights from governance and PHI controls.";
});

document.getElementById("threat-generate").addEventListener("click", generateThreatAnalysis);

const roadmapStatus = document.getElementById("roadmap-status");
const roadmapOutput = document.getElementById("roadmap-output");
const equipmentTable = document.getElementById("equipment-table");
const equipSummary = document.getElementById("equip-summary");
const standardsChecklist = document.getElementById("standards-checklist");
const standardsSummary = document.getElementById("standards-summary");
const pilotFocus = document.getElementById("pilot-focus");
const procureSummary = document.getElementById("procure-summary");
const procureOutput = document.getElementById("procure-output");

const roadmapPhases = {
  week0: {
    label: "Weeks 0-2",
    goals: [
      "Finalize canonical study data contract (specimen, assay, imaging, outcomes, consent)",
      "Select 3 flagship use cases: response prediction, toxicity signals, eligibility stratification",
      "Approve one disease pilot and one IRB-aligned endpoint definition"
    ]
  },
  week6: {
    label: "Weeks 3-6",
    goals: [
      "Integrate first real connectors: NGS, pathology imaging, and one clinical feed",
      "Enable wet-lab to analytics QA loop with contamination and batch effect alerts",
      "Configure model governance gates with drift thresholds and reviewer sign-off"
    ]
  },
  week12: {
    label: "Weeks 7-12",
    goals: [
      "Launch prospective pilot in chosen focus area with weekly utility reviews",
      "Run threat and compliance drills with audit artifacts ready for oversight",
      "Publish translational outcomes report with operational and scientific KPIs"
    ]
  }
};

const equipmentCatalog = [
  { category: "NGS", system: "Illumina / Thermo / ONT connector", interface: "FASTQ/BCL + run metadata", tier: ["lean", "mid", "comprehensive"], capexK: 280, leadWeeks: 8 },
  { category: "Pathology", system: "Whole-slide scanner bridge", interface: "DICOM / WSI export", tier: ["lean", "mid", "comprehensive"], capexK: 220, leadWeeks: 6 },
  { category: "Flow Cytometry", system: "Flow + spectral panel ingest", interface: "FCS + panel manifest", tier: ["mid", "comprehensive"], capexK: 160, leadWeeks: 7 },
  { category: "Radiology", system: "CT/MRI/PET ingestion", interface: "DICOM + longitudinal tags", tier: ["mid", "comprehensive"], capexK: 190, leadWeeks: 5 },
  { category: "Biobank", system: "LIMS + barcode chain-of-custody", interface: "HL7/FHIR + LIMS API", tier: ["lean", "mid", "comprehensive"], capexK: 120, leadWeeks: 4 },
  { category: "Clinical Trials", system: "EHR + EDC bridge", interface: "FHIR + CSV harmonizer", tier: ["lean", "mid", "comprehensive"], capexK: 140, leadWeeks: 6 },
  { category: "Liquid Biopsy / Proteomics", system: "Mass spec + ctDNA ingest", interface: "Vendor API + mzML", tier: ["comprehensive"], capexK: 240, leadWeeks: 10 },
  { category: "Secure Edge", system: "TPM-backed federated node", interface: "Signed manifest + attestation", tier: ["mid", "comprehensive"], capexK: 180, leadWeeks: 5 }
];

let activeEquipTier = "lean";
let activeRoadmapPhase = "week0";

const standardsItems = [
  { id: "fhir", label: "Clinical interoperability mapping complete", required: true },
  { id: "dicom", label: "Imaging interoperability validated", required: true },
  { id: "omics", label: "Omics metadata schema validated", required: true },
  { id: "identity", label: "Device identity and attestation enforced", required: true },
  { id: "signing", label: "Payload signing and traceability enabled", required: true },
  { id: "qaLoop", label: "Wet-lab QA loop automated", required: true },
  { id: "drift", label: "Model drift monitoring thresholds configured", required: true },
  { id: "pilotKpi", label: "Prospective pilot KPIs approved", required: true },
  { id: "externalAudit", label: "External pre-audit rehearsal complete", required: false }
];

const standardsState = standardsItems.reduce((acc, item) => {
  acc[item.id] = false;
  return acc;
}, {});

function computeRoadmapCompletion(phaseKey) {
  if (phaseKey === "week0") return 34;
  if (phaseKey === "week6") return 68;
  return 100;
}

function renderRoadmap(phaseKey) {
  activeRoadmapPhase = phaseKey;
  const phase = roadmapPhases[phaseKey];
  const completion = computeRoadmapCompletion(phaseKey);
  roadmapStatus.textContent = `Roadmap phase: ${phase.label}. Program completion ${completion}%.`;
  roadmapOutput.textContent = [
    `PROFESSOR ROADMAP (${phase.label.toUpperCase()})`,
    "----------------------------------",
    ...phase.goals.map((goal, idx) => `${idx + 1}) ${goal}`),
    "",
    "Scientific Success Metrics",
    "- Time-to-ingest for new modality < 10 business days",
    "- Federated pipeline uptime > 98%",
    "- Reviewer turnaround for high-impact outputs <= 48h",
    "- Prospective utility endpoint tracked weekly",
    "----------------------------------"
  ].join("\n");
  appendLog(auditLog, `professor-plan: roadmap updated to ${phase.label}`);
}

function simulatedReadiness(entry) {
  const base = activeEquipTier === "lean" ? 78 : activeEquipTier === "mid" ? 86 : 92;
  const variance = Math.floor(Math.random() * 9) - 4;
  const score = Math.max(62, Math.min(99, base + variance - Math.floor(entry.leadWeeks / 5)));
  return {
    score,
    status: score >= 90 ? "Pass" : score >= 80 ? "Review" : "Gap"
  };
}

function tierLabel(tier) {
  if (tier === "lean") return "Lean Lab";
  if (tier === "mid") return "Mid-Scale Center";
  return "Comprehensive Center";
}

function renderEquipmentMatrix() {
  const filtered = equipmentCatalog.filter((entry) => entry.tier.includes(activeEquipTier));
  equipmentTable.innerHTML = `<thead><tr><th>Category</th><th>System</th><th>Interface</th><th>Lead Time (w)</th><th>CAPEX (kUSD)</th><th>Readiness</th><th>Status</th></tr></thead>`;
  const body = document.createElement("tbody");
  let readyCount = 0;

  filtered.forEach((entry) => {
    const readiness = simulatedReadiness(entry);
    if (readiness.status === "Pass") readyCount += 1;
    const statusClass = readiness.status === "Pass" ? "status-pass" : readiness.status === "Review" ? "status-review" : "status-gap";
    const tr = document.createElement("tr");
    tr.innerHTML = `<td>${entry.category}</td><td>${entry.system}</td><td>${entry.interface}</td><td>${entry.leadWeeks}</td><td>${entry.capexK}</td><td>${readiness.score}%</td><td class="${statusClass}">${readiness.status}</td>`;
    body.appendChild(tr);
  });

  equipmentTable.appendChild(body);
  equipSummary.textContent = `${tierLabel(activeEquipTier)} stack loaded: ${filtered.length} systems, ${readyCount} pass-ready, ${filtered.length - readyCount} need review.`;
}

function renderStandardsChecklist() {
  standardsChecklist.innerHTML = standardsItems.map((item) => {
    const checked = standardsState[item.id] ? "checked" : "";
    return `<div class="switch-row"><span>${item.label} (${item.required ? "required" : "optional"})</span><label><input type="checkbox" data-standard="${item.id}" ${checked} /></label></div>`;
  }).join("");
}

function computeStandardsScore() {
  const total = standardsItems.length;
  const completed = standardsItems.filter((item) => standardsState[item.id]).length;
  const required = standardsItems.filter((item) => item.required);
  const requiredDone = required.filter((item) => standardsState[item.id]).length;
  const score = Math.round((completed / total) * 100);
  const requiredCoverage = Math.round((requiredDone / required.length) * 100);

  if (requiredCoverage < 100) {
    standardsSummary.textContent = `Completion ${score}% with required coverage ${requiredCoverage}%. Outstanding required controls must be closed before pilot escalation.`;
  } else {
    standardsSummary.textContent = `Completion ${score}% with required coverage ${requiredCoverage}%. Program is governance-ready for pilot expansion.`;
  }

  appendLog(auditLog, `professor-plan: standards score ${score}% (required ${requiredCoverage}%)`);
  return { score, requiredCoverage };
}

function applyRecommendedStandardsBaseline() {
  standardsItems.forEach((item) => {
    standardsState[item.id] = item.required;
  });
  standardsState.externalAudit = false;
  renderStandardsChecklist();
  standardsSummary.textContent = "Recommended baseline applied: all required standards checked, optional external audit left pending.";
}

function buildProcurementPack() {
  const focus = pilotFocus.value;
  const stack = equipmentCatalog.filter((entry) => entry.tier.includes(activeEquipTier));
  const capex = stack.reduce((sum, entry) => sum + entry.capexK, 0);
  const integration = Math.round(capex * 0.18);
  const training = Math.round(capex * 0.07);
  const total = capex + integration + training;

  procureSummary.textContent = `${tierLabel(activeEquipTier)} procurement pack ready for ${focus}: estimated total ${total}k USD.`;
  procureOutput.textContent = [
    `PROCUREMENT PACK (${tierLabel(activeEquipTier).toUpperCase()})`,
    "----------------------------------",
    `Pilot focus: ${focus}`,
    `Base CAPEX: ${capex}k USD`,
    `Integration services (18%): ${integration}k USD`,
    `Training and SOP onboarding (7%): ${training}k USD`,
    `Total estimate: ${total}k USD`,
    "",
    "Priority Acquisition Order",
    ...stack.map((entry, idx) => `${idx + 1}) ${entry.category}: ${entry.system} (${entry.capexK}k, ${entry.leadWeeks}w)`),
    "",
    "Pilot Milestones",
    "- Week 2: data contract signed and instrument mappings approved",
    "- Week 6: three live connectors running with QA loop",
    "- Week 9: prospective pilot enrollment monitoring",
    "- Week 12: utility and translational impact review",
    "----------------------------------"
  ].join("\n");

  appendLog(auditLog, `professor-plan: procurement pack built (${focus}, ${total}k USD)`);
}

function generatePiBrief() {
  const focus = pilotFocus.value;
  const { score, requiredCoverage } = computeStandardsScore();
  const completion = computeRoadmapCompletion(activeRoadmapPhase);
  const brief = [
    "PI EXECUTIVE BRIEF",
    "----------------------------------",
    `Focus Program: ${focus}`,
    `Roadmap Completion: ${completion}%`,
    `Standards Completion: ${score}%`,
    `Required Control Coverage: ${requiredCoverage}%`,
    `Equipment Tier: ${tierLabel(activeEquipTier)}`,
    "",
    "Decision Recommendation",
    completion >= 68 && requiredCoverage === 100
      ? "Proceed to prospective pilot execution with weekly governance checkpoints."
      : "Do not escalate yet. Close standards and execution gaps before prospective pilot.",
    "----------------------------------"
  ].join("\n");
  procureOutput.textContent = brief;
  procureSummary.textContent = `PI brief generated for ${focus}.`;
  appendLog(auditLog, "professor-plan: PI executive brief generated");
}

document.getElementById("roadmap-week0").addEventListener("click", () => renderRoadmap("week0"));
document.getElementById("roadmap-week6").addEventListener("click", () => renderRoadmap("week6"));
document.getElementById("roadmap-week12").addEventListener("click", () => renderRoadmap("week12"));

document.getElementById("equip-tier-lean").addEventListener("click", () => {
  activeEquipTier = "lean";
  renderEquipmentMatrix();
});

document.getElementById("equip-tier-mid").addEventListener("click", () => {
  activeEquipTier = "mid";
  renderEquipmentMatrix();
});

document.getElementById("equip-tier-comprehensive").addEventListener("click", () => {
  activeEquipTier = "comprehensive";
  renderEquipmentMatrix();
});

document.getElementById("equip-refresh").addEventListener("click", renderEquipmentMatrix);

standardsChecklist.addEventListener("input", (event) => {
  const target = event.target;
  if (!target.dataset.standard) return;
  standardsState[target.dataset.standard] = target.checked;
});

document.getElementById("standards-recommended").addEventListener("click", applyRecommendedStandardsBaseline);
document.getElementById("standards-score").addEventListener("click", computeStandardsScore);
document.getElementById("procure-build").addEventListener("click", buildProcurementPack);
document.getElementById("procure-export").addEventListener("click", generatePiBrief);

const todaySecurityList = document.getElementById("today-security-list");
const todaySecuritySummary = document.getElementById("today-security-summary");
const goldscoreSummary = document.getElementById("goldscore-summary");
const goldscoreTable = document.getElementById("goldscore-table");
const goldRoadmapSummary = document.getElementById("gold-roadmap-summary");
const goldRoadmapOutput = document.getElementById("gold-roadmap-output");
const sloTable = document.getElementById("slo-table");
const sloOutput = document.getElementById("slo-output");

const todaySecurityItems = [
  { id: "mfa", label: "Enforce phishing-resistant MFA for all admins", feasibleToday: true },
  { id: "secrets", label: "Rotate high-risk service secrets and disable shared credentials", feasibleToday: true },
  { id: "egress", label: "Apply default-deny egress policy to runtime workloads", feasibleToday: true },
  { id: "signedArtifacts", label: "Block unsigned artifacts in CI/CD promotion gates", feasibleToday: true },
  { id: "attestationGate", label: "Enable TPM attestation gate before job admission", feasibleToday: true },
  { id: "soc24x7", label: "Stand up 24/7 SOC coverage rota", feasibleToday: false },
  { id: "redteam", label: "Schedule external red-team engagement", feasibleToday: false },
  { id: "hsm", label: "Migrate key operations to HSM-backed custody", feasibleToday: false }
];

const todaySecurityState = todaySecurityItems.reduce((acc, item) => {
  acc[item.id] = false;
  return acc;
}, {});

const goldControlDomains = [
  { domain: "Identity + Zero Trust", owner: "Security Engineering", baseline: 72 },
  { domain: "Hardware Root of Trust", owner: "Platform", baseline: 75 },
  { domain: "Data Protection", owner: "Data Platform", baseline: 78 },
  { domain: "Key Management", owner: "Crypto Operations", baseline: 69 },
  { domain: "Supply Chain Security", owner: "DevSecOps", baseline: 74 },
  { domain: "Runtime Hardening", owner: "SRE", baseline: 71 },
  { domain: "Detection and Response", owner: "SOC", baseline: 66 },
  { domain: "LLM Safety Controls", owner: "AI Governance", baseline: 73 }
];

const securityRoadmap = {
  day30: [
    "Complete MFA rollout and privileged access hardening",
    "Enable attestation gate and signed-manifest admission checks",
    "Finish secret rotation and default-deny egress baseline",
    "Turn on SBOM and signature validation in CI/CD"
  ],
  day60: [
    "Deploy behavior-based detections and SOAR incident playbooks",
    "Implement HSM-backed key custody with split-duty controls",
    "Enforce LLM guardrails for prompt injection and exfiltration",
    "Execute tabletop incidents for privacy and model compromise scenarios"
  ],
  day90: [
    "Run independent penetration test and red-team validation",
    "Finalize continuous control monitoring evidence exports",
    "Close all high-severity findings and verify MTTR targets",
    "Publish board-level security assurance report"
  ]
};

const sloCatalog = [
  { metric: "Critical patch SLA", target: "<= 7 days", current: 9, unit: "days" },
  { metric: "Incident MTTR", target: "<= 4 hours", current: 5.3, unit: "hours" },
  { metric: "High-risk finding closure", target: "<= 14 days", current: 13, unit: "days" },
  { metric: "Key rotation interval", target: "<= 30 days", current: 42, unit: "days" },
  { metric: "Unsigned deployment rate", target: "0%", current: 2.2, unit: "%" }
];

let goldHardeningBoost = 1;

function renderTodaySecurityList() {
  todaySecurityList.innerHTML = todaySecurityItems.map((item) => {
    const checked = todaySecurityState[item.id] ? "checked" : "";
    const tag = item.feasibleToday ? "today" : "roadmap";
    return `<div class="switch-row"><span>${item.label} (${tag})</span><label><input type="checkbox" data-today-security="${item.id}" ${checked} /></label></div>`;
  }).join("");
}

function computeTodaySecurityScore() {
  const completed = todaySecurityItems.filter((item) => todaySecurityState[item.id]);
  const feasible = todaySecurityItems.filter((item) => item.feasibleToday);
  const feasibleDone = feasible.filter((item) => todaySecurityState[item.id]);
  const score = Math.round((completed.length / todaySecurityItems.length) * 100);
  const todayCoverage = Math.round((feasibleDone.length / feasible.length) * 100);
  todaySecuritySummary.textContent = `Today sprint score ${score}%. Feasible-today coverage ${todayCoverage}% (${feasibleDone.length}/${feasible.length}).`;
  appendLog(auditLog, `gold-security: today sprint ${todayCoverage}% feasible controls complete`);
  return { score, todayCoverage };
}

function autoApplyFeasibleToday() {
  todaySecurityItems.forEach((item) => {
    if (item.feasibleToday) todaySecurityState[item.id] = true;
  });
  renderTodaySecurityList();
  const result = computeTodaySecurityScore();
  todaySecuritySummary.textContent = `Auto-applied feasible controls. Today coverage ${result.todayCoverage}% with immediate hardening uplift.`;
}

function domainStatus(score) {
  if (score >= 88) return { label: "Strong", cls: "status-strong" };
  if (score >= 78) return { label: "Watch", cls: "status-watch" };
  return { label: "Critical", cls: "status-critical" };
}

function renderGoldScorecard() {
  const todayResult = computeTodaySecurityScore();
  goldscoreTable.innerHTML = `<thead><tr><th>Domain</th><th>Owner</th><th>Score</th><th>Status</th><th>Priority</th></tr></thead>`;
  const body = document.createElement("tbody");

  const rows = goldControlDomains.map((domain, idx) => {
    const stochastic = ((idx % 2 === 0 ? 1 : -1) * (Math.random() * 2.5));
    const score = Math.max(58, Math.min(98, domain.baseline * goldHardeningBoost + todayResult.todayCoverage * 0.12 + stochastic));
    const status = domainStatus(score);
    const priority = score < 78 ? "P1" : score < 88 ? "P2" : "P3";
    return { ...domain, score: score.toFixed(1), status, priority };
  });

  rows.forEach((row) => {
    const tr = document.createElement("tr");
    tr.innerHTML = `<td>${row.domain}</td><td>${row.owner}</td><td>${row.score}%</td><td class="${row.status.cls}">${row.status.label}</td><td>${row.priority}</td>`;
    body.appendChild(tr);
  });
  goldscoreTable.appendChild(body);

  const critical = rows.filter((row) => row.status.label === "Critical").length;
  const avg = (rows.reduce((sum, row) => sum + Number(row.score), 0) / rows.length).toFixed(1);
  goldscoreSummary.textContent = `Control average ${avg}%. Critical domains ${critical}. Focus first on P1 areas this sprint.`;
}

function renderSecurityRoadmap(stage) {
  const map = {
    day30: { title: "30-Day Security Plan", completion: "33%" },
    day60: { title: "60-Day Security Plan", completion: "66%" },
    day90: { title: "90-Day Security Plan", completion: "100%" }
  };
  const info = map[stage];
  goldRoadmapSummary.textContent = `${info.title} loaded. Program completion target ${info.completion}.`;
  goldRoadmapOutput.textContent = [
    info.title.toUpperCase(),
    "----------------------------------",
    ...securityRoadmap[stage].map((step, idx) => `${idx + 1}) ${step}`),
    "----------------------------------"
  ].join("\n");
  appendLog(auditLog, `gold-security: roadmap stage ${stage} selected`);
}

function compareToTarget(current, targetText, unit) {
  if (targetText.includes("0%")) {
    return current === 0 ? "Strong" : current <= 1 ? "Watch" : "Critical";
  }
  const target = Number(targetText.replace(/[^0-9.]/g, ""));
  if (Number.isNaN(target)) return "Watch";
  if (current <= target) return "Strong";
  if (current <= target * 1.25) return "Watch";
  return "Critical";
}

function renderSloTable() {
  sloTable.innerHTML = `<thead><tr><th>SLO</th><th>Target</th><th>Current</th><th>Status</th></tr></thead>`;
  const body = document.createElement("tbody");
  const statuses = [];

  sloCatalog.forEach((item) => {
    const jitter = (Math.random() - 0.5) * 0.9;
    const current = Math.max(0, Number((item.current + jitter).toFixed(2)));
    const label = compareToTarget(current, item.target, item.unit);
    const cls = label === "Strong" ? "status-strong" : label === "Watch" ? "status-watch" : "status-critical";
    statuses.push(label);
    const tr = document.createElement("tr");
    tr.innerHTML = `<td>${item.metric}</td><td>${item.target}</td><td>${current} ${item.unit}</td><td class="${cls}">${label}</td>`;
    body.appendChild(tr);
  });
  sloTable.appendChild(body);

  const critical = statuses.filter((s) => s === "Critical").length;
  const watch = statuses.filter((s) => s === "Watch").length;
  sloOutput.textContent = `SLO posture: ${critical} critical, ${watch} watch. Trigger escalations for critical metrics with owner and ETA.`;
}

function generateSloEscalationPack() {
  const todayResult = computeTodaySecurityScore();
  renderSloTable();
  sloOutput.textContent += `\n\nEscalation Pack\n1) Assign P1 owners for key rotation and patch SLA gaps.\n2) Freeze unsigned deployment paths until 0% target reached.\n3) Execute 48h remediation checkpoint and update board summary.\n4) Today security feasible coverage currently ${todayResult.todayCoverage}%.`;
  appendLog(auditLog, "gold-security: SLO escalation pack generated");
}

todaySecurityList.addEventListener("input", (event) => {
  const target = event.target;
  if (!target.dataset.todaySecurity) return;
  todaySecurityState[target.dataset.todaySecurity] = target.checked;
});

document.getElementById("today-security-autofill").addEventListener("click", autoApplyFeasibleToday);
document.getElementById("today-security-score").addEventListener("click", computeTodaySecurityScore);
document.getElementById("goldscore-refresh").addEventListener("click", renderGoldScorecard);
document.getElementById("goldscore-hardening").addEventListener("click", () => {
  goldHardeningBoost = 1.08;
  renderGoldScorecard();
  goldscoreSummary.textContent += " Hardening auto-tuner applied: raised baseline by identity, runtime, and supply-chain controls.";
});
document.getElementById("roadmap-30").addEventListener("click", () => renderSecurityRoadmap("day30"));
document.getElementById("roadmap-60").addEventListener("click", () => renderSecurityRoadmap("day60"));
document.getElementById("roadmap-90").addEventListener("click", () => renderSecurityRoadmap("day90"));
document.getElementById("slo-refresh").addEventListener("click", renderSloTable);
document.getElementById("slo-escalate").addEventListener("click", generateSloEscalationPack);

renderModelRegistryForm();
renderGovernanceGates();
renderLlmAuditTable();
generateThreatAnalysis();
renderRoadmap("week0");
renderEquipmentMatrix();
renderStandardsChecklist();
applyRecommendedStandardsBaseline();
buildProcurementPack();
renderTodaySecurityList();
autoApplyFeasibleToday();
renderGoldScorecard();
renderSecurityRoadmap("day30");
renderSloTable();

renderDpiaForm();
renderSection("dashboard");
appendLog(runtimeLog, "runtime initialized: waiting for next FL round tick");
appendLog(auditLog, "audit initialized: compliance monitor online");
