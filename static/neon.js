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

// Function to update the editor mode and example code
function setEditorMode(language) {
    const modeMap = {
        python: "ace/mode/python",
        java: "ace/mode/java",
        cpp: "ace/mode/c_cpp",
        c: "ace/mode/c_cpp",
    };

    const mode = modeMap[language] || "ace/mode/plain_text"; // Default to plain text if language is unknown
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