console.log("C script loaded");

let lastSelectedText = null; 
let lastSelectionRect = null; 

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "get_selected_text") {
    const selection = window.getSelection();
    const selectedText = selection.toString();
    lastSelectedText = selectedText;

    // Store position of selection for popup placement
    if (selection.rangeCount > 0) {
      const range = selection.getRangeAt(0);
      lastSelectionRect = range.getBoundingClientRect();
    }

    console.log("Selected text:", selectedText);

    showPopup("Loading simplified definition...");

    fetch("http://127.0.0.1:5000/explain", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: selectedText, mode: "simplified" })
    })
    .then(res => res.json())
    .then(data => {
      console.log("✅ AI Simplified response:", data.reply);
      updatePopupContent("simplified", data.reply);
    })
    .catch(err => console.error("❌ Fetch error:", err));

    sendResponse({ selectedText });
    return true;
  }
});

// ========== Popup creation ==========

function showPopup(initialMessage) {
  const oldPopup = document.getElementById("ai-popup");
  if (oldPopup) oldPopup.remove();

  const popup = document.createElement("div");
  popup.id = "ai-popup";
  popup.style.position = "absolute";
  popup.style.zIndex = "9999";
  popup.style.width = "450px";
  popup.style.background = "white";
  popup.style.border = "1px solid #ccc";
  popup.style.borderRadius = "10px";
  popup.style.boxShadow = "0px 4px 16px rgba(0,0,0,0.2)";
  popup.style.fontFamily = "Arial, sans-serif";
  popup.style.overflow = "hidden";

  // Place popup just under the selected text
  if (lastSelectionRect) {
    const scrollY = window.scrollY || document.documentElement.scrollTop;
    const scrollX = window.scrollX || document.documentElement.scrollLeft;
    popup.style.top = `${lastSelectionRect.bottom + scrollY + 8}px`;
    popup.style.left = `${lastSelectionRect.left + scrollX}px`;
  } else {
    popup.style.position = "fixed";
    popup.style.bottom = "20px";
    popup.style.right = "20px";
  }

  popup.innerHTML = `
    <div style="display: flex; align-items: center; justify-content: space-between; background: #f5f5f5; border-bottom: 1px solid #ddd; padding: 6px 10px;">
      <div style="display: flex; gap: 6px; flex: 1;">
        <button id="tab-simplified" class="ai-tab active">Simplified</button>
        <button id="tab-detailed" class="ai-tab">Detailed</button>
        <button id="tab-questions" class="ai-tab">Questions</button>
      </div>
      <button id="close-popup" style="border:none; background:none; font-size:16px; cursor:pointer; color:#666;">×</button>
    </div>
    <div id="popup-content" style="padding: 12px; max-height: 200px; overflow-y: auto; font-size:14px; line-height:1.4;">
      ${initialMessage}
    </div>
    <div id="question-box" style="display:none; border-top:1px solid #ddd; padding:6px; background:#fafafa;">
      <input type="text" id="user-question" placeholder="Ask about this text..." 
        style="width:80%; padding:6px; font-size:13px; border:1px solid #ccc; border-radius:4px;">
      <button id="send-question" 
        style="width:18%; padding:6px; font-size:13px; border:none; background:#007bff; color:white; border-radius:4px; cursor:pointer;">
        Ask
      </button>
    </div>
  `;

  document.body.appendChild(popup);

  // Style for tab buttons
  const style = document.createElement("style");
  style.textContent = `
    .ai-tab {
      padding: 6px 10px;
      border: none;
      cursor: pointer;
      background: #f0f0f0;
      border-radius: 6px;
      font-size: 13px;
      transition: background 0.2s;
    }
    .ai-tab:hover {
      background: #e0e0e0;
    }
    .ai-tab.active {
      background: #007BFF;
      color: white;
      font-weight: bold;
    }
  `;
  document.head.appendChild(style);

  // Event listeners for tabs
  document.getElementById("tab-simplified").addEventListener("click", () => {
    setActiveTab("tab-simplified");
    document.getElementById("question-box").style.display = "none";
    requestMode("simplified");
  });

  document.getElementById("tab-detailed").addEventListener("click", () => {
    setActiveTab("tab-detailed");
    document.getElementById("question-box").style.display = "none";
    requestMode("detailed");
  });

  document.getElementById("tab-questions").addEventListener("click", () => {
    setActiveTab("tab-questions");
    document.getElementById("question-box").style.display = "block";
    document.getElementById("popup-content").innerHTML = "Type a question below 👇";
  });

  // Ask button logic
  document.getElementById("send-question").addEventListener("click", () => {
    const qInput = document.getElementById("user-question");
    const question = qInput.value.trim();
    if (!question) return;
    const popupContent = document.getElementById("popup-content");
    popupContent.innerHTML = "Thinking...";

    fetch("http://127.0.0.1:5000/explain", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: lastSelectedText, mode: "question", question: question })
    })
    .then(res => res.json())
    .then(data => {
      popupContent.innerHTML = data.reply;
    })
    .catch(err => {
      console.error("❌ Question fetch error:", err);
      popupContent.innerHTML = "Error fetching answer.";
    });
  });

  document.getElementById("close-popup").addEventListener("click", () => {
    popup.remove();
  });
}

// ========== Fetch AI response for a specific mode ==========

function requestMode(mode) {
  if (!lastSelectedText) {
    console.error("No text stored from selection!");
    return;
  }

  const popupContent = document.getElementById("popup-content");
  popupContent.innerHTML = `Loading ${mode} response...`;

  fetch("http://127.0.0.1:5000/explain", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text: lastSelectedText, mode: mode })
  })
  .then(res => res.json())
  .then(data => {
    console.log(`✅ AI ${mode} response:`, data.reply);
    updatePopupContent(mode, data.reply);
  })
  .catch(err => {
    console.error("❌ Fetch error:", err);
    popupContent.innerHTML = "Error fetching response.";
  });
}

// ========== Update popup content only ==========

function updatePopupContent(mode, text) {
  const popupContent = document.getElementById("popup-content");
  if (popupContent) {
    popupContent.innerHTML = text;
  }
}

// ========== Helper to update active tab style ==========

function setActiveTab(tabId) {
  document.querySelectorAll(".ai-tab").forEach(btn => {
    btn.classList.remove("active");
  });
  document.getElementById(tabId).classList.add("active");
}
