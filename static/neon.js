// Initialize the Ace editor
const editor = ace.edit("editor");
editor.setTheme("ace/theme/monokai");
editor.session.setMode("ace/mode/python"); // Default to Python

editor.setValue("# Write your Python code here\n", -1); // Default content
editor.clearSelection();

// Editor settings
editor.setOptions({
    fontSize: "14px",
    showLineNumbers: true,
    tabSize: 2,
    useSoftTabs: true,
    wrap: true, // Enable line wrapping
    enableBasicAutocompletion: true,
    enableSnippets: true,
    enableLiveAutocompletion: true,
});

// Example code for different languages
const exampleCode = {
    python: "# Write your Python code here\nprint('Hello, Python!')",
    java: "// Write your Java code here\nclass Main {\n    public static void main(String[] args) {\n        System.out.println(\"Hello, Java!\");\n    }\n}",
    cpp: "// Write your C++ code here\n#include <iostream>\nusing namespace std;\nint main() {\n    cout << \"Hello, C++!\" << endl;\n    return 0;\n}",
    c: "// Write your C code here\n#include <stdio.h>\nint main() {\n    printf(\"Hello, C!\\n\");\n    return 0;\n}"
};

// Keep track of the current language
let currentLanguage = 'python';

// Function to update the editor mode and example code
function setEditorMode(language) {
    const modeMap = {
        python: "ace/mode/python",
        java: "ace/mode/java",
        cpp: "ace/mode/c_cpp",
        c: "ace/mode/c_cpp",
    };

    currentLanguage = language; // Store the current language
    const mode = modeMap[language] || "ace/mode/plain_text";
    editor.session.setMode(mode);
    editor.setValue(exampleCode[language] || "// Write your code here", -1);
    editor.clearSelection();

    // Update the current language display
    document.getElementById("current-language").textContent = `Selected Language: ${language.charAt(0).toUpperCase() + language.slice(1)}`;
    console.log(`Editor mode set to: ${mode}`);
}

// Add click event listeners to language icons
document.querySelectorAll(".language-icon").forEach((icon) => {
    icon.addEventListener("click", () => {
        const selectedLang = icon.getAttribute("data-lang");
        setEditorMode(selectedLang);
    });
});

// Function to copy code from the editor to the clipboard
function copyToClipboard() {
    const code = editor.getValue();
    navigator.clipboard.writeText(code)
        .then(() => {
            console.log("Code copied to clipboard!");
        })
        .catch((err) => {
            console.error("Failed to copy text: ", err);
        });
}

// Add click event listener to the "cpy" button
document.querySelector(".cpy").addEventListener("click", copyToClipboard);

// Function to save the editor content as a file
function saveToFile() {
    const code = editor.getValue();

    // Use the currentLanguage variable to determine the correct extension
    const extensionMap = {
        python: ".py",
        java: ".java",
        cpp: ".cpp",
        c: ".c"  // Separate extension for C files
    };

    const fileExtension = extensionMap[currentLanguage] || ".txt";
    const fileName = `code${fileExtension}`;

    // Create a Blob with the code content
    const fileBlob = new Blob([code], { type: "text/plain" });

    // Create a temporary download link
    const downloadLink = document.createElement("a");
    downloadLink.href = URL.createObjectURL(fileBlob);
    downloadLink.download = fileName;

    // Append the link to the document, click it, and remove it
    document.body.appendChild(downloadLink);
    downloadLink.click();
    document.body.removeChild(downloadLink);

    // Provide user feedback
    alert(`Your code has been saved as ${fileName}.`);
}

// Add click event listener to the "save" button
document.querySelector(".save").addEventListener("click", saveToFile);