console.log("C script loaded");

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    console.log("Message received in content script:", request);
    if (request.action === "get_selected_text") {
        const selectedText = window.getSelection().toString();
        console.log("Selected text:", selectedText);

        fetch("http://127.0.0.1:5000/log", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ selected_text: selectedText })
        })
        .then(res => res.text())
        .then(txt => console.log("✅ Sent to Python, response:", txt))
        .catch(err => console.error("❌ Fetch error:", err));

        sendResponse({ selectedText });
        return true;
    }
});
