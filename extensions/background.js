// background.js
chrome.commands.onCommand.addListener((command) => {
    console.log("Command triggered:", command); // <-- should appear when you press shortcut
    if (command === "send_selected_text") {
        chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
            if (!tabs[0]) return console.warn("No active tab");
            chrome.tabs.sendMessage(tabs[0].id, { action: "get_selected_text" }, (response) => {
                console.log("Response from content script:", response?.selectedText);
            });
        });
    }
});
