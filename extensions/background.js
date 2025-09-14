// background.js
chrome.commands.onCommand.addListener((command) => {
    console.log("Command triggered:", command);
    if (command === "send_selected_text") {
        chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
            if (!tabs[0]) return console.warn("No active tab");
            chrome.tabs.sendMessage(
                tabs[0].id,
                { action: "get_selected_text" },
                (response) => {
                    console.log("Response from content script:", response?.selectedText);
                }
            );
        });
    }
});


/*

making chrome extension. background js reads when the shortcut has been pressed. 
content js gets the selected text and sends it to main.py. 
main.py calls a function in AI.py to generate the ai response. 
I want to create a pop up with that ai response. how?

*/