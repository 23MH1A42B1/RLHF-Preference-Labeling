/**
 * RLHF Preference Labeling & Data Alignment Tool - Client Application
 */

const state = {
  annotatorId: "annotator_1",
  categoryFilter: "",
  currentPair: null,
  isSubmitting: false,
};

// DOM Elements
const elements = {
  // Tabs
  tabBtns: document.querySelectorAll(".tab-btn"),
  tabPanels: document.querySelectorAll(".tab-panel"),
  annotatorInput: document.getElementById("annotator-id-input"),

  // Labeling view
  pairContainer: document.getElementById("pair-container"),
  completedContainer: document.getElementById("completed-container"),
  progressText: document.getElementById("progress-text"),
  progressPercent: document.getElementById("progress-percent"),
  progressFill: document.getElementById("progress-fill"),
  categoryFilter: document.getElementById("category-filter"),
  pairCategory: document.getElementById("pair-category"),
  pairId: document.getElementById("pair-id"),
  pairPrompt: document.getElementById("pair-prompt"),
  textResponseA: document.getElementById("text-response-a"),
  textResponseB: document.getElementById("text-response-b"),
  btnChooseA: document.getElementById("btn-choose-a"),
  btnChooseB: document.getElementById("btn-choose-b"),
  btnChooseTie: document.getElementById("btn-choose-tie"),
  btnChooseSkip: document.getElementById("btn-choose-skip"),
  btnGoAnalytics: document.getElementById("btn-go-analytics"),
  btnGoExport: document.getElementById("btn-go-export"),

  // Analytics view
  kpiTotalLabels: document.getElementById("kpi-total-labels"),
  kpiAgreementRate: document.getElementById("kpi-agreement-rate"),
  kpiAgreementDesc: document.getElementById("kpi-agreement-desc"),
  kpiMultiPairs: document.getElementById("kpi-multi-pairs"),
  kpiKappa: document.getElementById("kpi-kappa"),
  btnRefreshAnalytics: document.getElementById("btn-refresh-analytics"),
  distBarA: document.getElementById("dist-bar-a"),
  distBarB: document.getElementById("dist-bar-b"),
  distBarTie: document.getElementById("dist-bar-tie"),
  distBarSkip: document.getElementById("dist-bar-skip"),
  distCountA: document.getElementById("dist-count-a"),
  distCountB: document.getElementById("dist-count-b"),
  distCountTie: document.getElementById("dist-count-tie"),
  distCountSkip: document.getElementById("dist-count-skip"),
  categoryTableBody: document.getElementById("category-table-body"),

  // Export view
  exportCategoryFilter: document.getElementById("export-category-filter"),
  downloadExportBtn: document.getElementById("download-export-btn"),
  jsonlPreview: document.getElementById("jsonl-preview"),

  // Toast
  toastContainer: document.getElementById("toast-container"),
};

// Show toast notification
function showToast(message, type = "info") {
  const toast = document.createElement("div");
  toast.className = "toast";
  toast.textContent = message;
  elements.toastContainer.appendChild(toast);
  setTimeout(() => {
    toast.style.opacity = "0";
    toast.style.transition = "opacity 0.3s ease";
    setTimeout(() => toast.remove(), 300);
  }, 2200);
}

// Fetch next unlabeled pair
async function fetchNextPair() {
  const { annotatorId, categoryFilter } = state;
  let url = `/api/pairs/next?annotator_id=${encodeURIComponent(annotatorId)}`;
  if (categoryFilter) {
    url += `&category=${encodeURIComponent(categoryFilter)}`;
  }

  try {
    const res = await fetch(url);
    if (res.status === 200) {
      const data = await res.json();
      state.currentPair = data;
      renderPair(data);
      elements.pairContainer.style.display = "block";
      elements.completedContainer.style.display = "none";
    } else if (res.status === 404) {
      state.currentPair = null;
      elements.pairContainer.style.display = "none";
      elements.completedContainer.style.display = "block";
    } else {
      showToast(`Error fetching pair: ${res.statusText}`, "error");
    }
  } catch (err) {
    console.error("fetchNextPair error:", err);
    showToast("Network error fetching next prompt pair", "error");
  }

  fetchProgress();
}

// Render pair data in UI
function renderPair(pair) {
  elements.pairPrompt.textContent = pair.prompt;
  elements.textResponseA.textContent = pair.response_a;
  elements.textResponseB.textContent = pair.response_b;
  elements.pairCategory.textContent = (pair.category || "General").replace("_", " ");
  elements.pairId.textContent = `Pair #${pair.id}`;
}

// Fetch annotator progress
async function fetchProgress() {
  const { annotatorId } = state;
  try {
    const res = await fetch(`/api/pairs/progress?annotator_id=${encodeURIComponent(annotatorId)}`);
    if (res.ok) {
      const data = await res.json();
      elements.progressText.textContent = `Labeled ${data.labeled_pairs} of ${data.total_pairs} pairs`;
      elements.progressPercent.textContent = `${data.completion_percentage}%`;
      elements.progressFill.style.width = `${data.completion_percentage}%`;
    }
  } catch (err) {
    console.error("fetchProgress error:", err);
  }
}

// Submit a label choice
async function submitLabel(choice) {
  if (!state.currentPair || state.isSubmitting) return;

  state.isSubmitting = true;
  const payload = {
    pair_id: state.currentPair.id,
    annotator_id: state.annotatorId,
    chosen: choice,
  };

  try {
    const res = await fetch("/api/labels", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (res.status === 201) {
      const labelDesc = choice === "A" ? "Choice A" : choice === "B" ? "Choice B" : choice.toUpperCase();
      showToast(`Recorded: ${labelDesc}`);
      // Animate card transition
      elements.pairContainer.style.opacity = "0.6";
      setTimeout(async () => {
        await fetchNextPair();
        elements.pairContainer.style.opacity = "1";
        state.isSubmitting = false;
      }, 150);
    } else {
      const err = await res.json();
      showToast(`Error: ${err.detail || "Submission failed"}`, "error");
      state.isSubmitting = false;
    }
  } catch (err) {
    console.error("submitLabel error:", err);
    showToast("Submission failed: Network error", "error");
    state.isSubmitting = false;
  }
}

// Fetch Analytics & Inter-rater Agreement metrics
async function fetchAnalytics() {
  try {
    const res = await fetch("/api/analytics");
    if (!res.ok) return;

    const data = await res.json();
    const total = data.total_labels || 0;
    const dist = data.label_distribution || { A: 0, B: 0, tie: 0, skip: 0 };

    elements.kpiTotalLabels.textContent = total;

    // Agreement rate
    const agreement = data.agreement_rate !== undefined ? data.agreement_rate : 1.0;
    const agreementPct = Math.round(agreement * 100);
    elements.kpiAgreementRate.textContent = `${agreementPct}%`;

    if (data.multi_labeled_pairs_count > 0) {
      elements.kpiAgreementDesc.textContent = `Based on ${data.multi_labeled_pairs_count} multi-rated pairs`;
    } else {
      elements.kpiAgreementDesc.textContent = "Rate multiple raters to see consensus";
    }

    elements.kpiMultiPairs.textContent = data.multi_labeled_pairs_count || 0;

    const kappa = data.cohens_kappa !== undefined ? data.cohens_kappa : 1.0;
    elements.kpiKappa.textContent = kappa.toFixed(2);

    // Update distribution bars
    const getPct = (cnt) => (total > 0 ? Math.round((cnt / total) * 100) : 0);

    const aPct = getPct(dist.A || 0);
    elements.distBarA.style.width = `${aPct}%`;
    elements.distCountA.textContent = `${dist.A || 0} (${aPct}%)`;

    const bPct = getPct(dist.B || 0);
    elements.distBarB.style.width = `${bPct}%`;
    elements.distCountB.textContent = `${dist.B || 0} (${bPct}%)`;

    const tiePct = getPct(dist.tie || 0);
    elements.distBarTie.style.width = `${tiePct}%`;
    elements.distCountTie.textContent = `${dist.tie || 0} (${tiePct}%)`;

    const skipPct = getPct(dist.skip || 0);
    elements.distBarSkip.style.width = `${skipPct}%`;
    elements.distCountSkip.textContent = `${dist.skip || 0} (${skipPct}%)`;

    // Category table
    elements.categoryTableBody.innerHTML = "";
    const catData = data.category_breakdown || {};
    const catKeys = Object.keys(catData);

    if (catKeys.length === 0) {
      elements.categoryTableBody.innerHTML = `
        <tr><td colspan="6" style="text-align: center; color: var(--text-muted);">No labels recorded yet.</td></tr>
      `;
    } else {
      catKeys.forEach((cat) => {
        const row = catData[cat];
        const tr = document.createElement("tr");
        tr.innerHTML = `
          <td><strong>${cat.replace("_", " ")}</strong></td>
          <td>${row.total || 0}</td>
          <td style="color: #60a5fa;">${row.A || 0}</td>
          <td style="color: #c084fc;">${row.B || 0}</td>
          <td style="color: #fcd34d;">${row.tie || 0}</td>
          <td style="color: #f87171;">${row.skip || 0}</td>
        `;
        elements.categoryTableBody.appendChild(tr);
      });
    }
  } catch (err) {
    console.error("fetchAnalytics error:", err);
  }
}

// Fetch export preview
async function fetchExportPreview() {
  const cat = elements.exportCategoryFilter.value;
  let url = "/api/export";
  if (cat) {
    url += `?category=${encodeURIComponent(cat)}`;
  }

  elements.downloadExportBtn.href = url;

  try {
    const res = await fetch(url);
    if (res.ok) {
      const text = await res.text();
      const lines = text.trim().split("\n").filter((l) => l.trim().length > 0);
      if (lines.length === 0) {
        elements.jsonlPreview.textContent = "// No preference labels available for export yet.\n// Complete pairwise annotations in the Labeling Studio to generate training data.";
      } else {
        // Show up to 4 formatted preview lines
        const previewLines = lines.slice(0, 4).map((line) => {
          try {
            return JSON.stringify(JSON.parse(line), null, 2);
          } catch (e) {
            return line;
          }
        });
        const summary = lines.length > 4 ? `\n... and ${lines.length - 4} more records.` : "";
        elements.jsonlPreview.textContent = previewLines.join("\n\n") + summary;
      }
    }
  } catch (err) {
    console.error("fetchExportPreview error:", err);
    elements.jsonlPreview.textContent = "Error loading export preview.";
  }
}

// Tab navigation handler
function switchTab(tabId) {
  elements.tabBtns.forEach((btn) => {
    btn.classList.toggle("active", btn.dataset.tab === tabId);
  });
  elements.tabPanels.forEach((panel) => {
    panel.classList.toggle("active", panel.id === `panel-${tabId}`);
  });

  if (tabId === "analytics") {
    fetchAnalytics();
  } else if (tabId === "export") {
    fetchExportPreview();
  }
}

// Setup Event Listeners
function setupEvents() {
  // Tabs
  elements.tabBtns.forEach((btn) => {
    btn.addEventListener("click", () => switchTab(btn.dataset.tab));
  });

  elements.btnGoAnalytics?.addEventListener("click", () => switchTab("analytics"));
  elements.btnGoExport?.addEventListener("click", () => switchTab("export"));

  // Annotator ID change
  elements.annotatorInput.addEventListener("change", (e) => {
    const val = e.target.value.trim() || "annotator_1";
    state.annotatorId = val;
    showToast(`Switched active annotator to '${val}'`);
    fetchNextPair();
  });

  // Category filter
  elements.categoryFilter.addEventListener("change", (e) => {
    state.categoryFilter = e.target.value;
    fetchNextPair();
  });

  // Action buttons
  elements.btnChooseA.addEventListener("click", () => submitLabel("A"));
  elements.btnChooseB.addEventListener("click", () => submitLabel("B"));
  elements.btnChooseTie.addEventListener("click", () => submitLabel("tie"));
  elements.btnChooseSkip.addEventListener("click", () => submitLabel("skip"));

  // Refresh Analytics button
  elements.btnRefreshAnalytics.addEventListener("click", () => {
    fetchAnalytics();
    showToast("Analytics metrics refreshed");
  });

  // Export category filter
  elements.exportCategoryFilter.addEventListener("change", () => {
    fetchExportPreview();
  });

  // Keyboard Shortcuts (A, B, T, S)
  window.addEventListener("keydown", (e) => {
    // Ignore keypresses if user is typing into an input
    if (e.target.tagName === "INPUT" || e.target.tagName === "TEXTAREA" || e.target.tagName === "SELECT") {
      return;
    }

    const key = e.key.toLowerCase();
    if (key === "a") {
      e.preventDefault();
      submitLabel("A");
    } else if (key === "b") {
      e.preventDefault();
      submitLabel("B");
    } else if (key === "t") {
      e.preventDefault();
      submitLabel("tie");
    } else if (key === "s") {
      e.preventDefault();
      submitLabel("skip");
    }
  });
}

// Initialization
document.addEventListener("DOMContentLoaded", () => {
  setupEvents();
  fetchNextPair();
});

