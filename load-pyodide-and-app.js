// Global variable for the Pyodide instance
let pyodideInstance = null;

async function initializePyodideAndApp() {
    // Ensure the browser has finished loading before attempting to load Pyodide
    if (typeof loadPyodide === 'undefined') {
        console.error("Pyodide loader (loadPyodide) not found. Check your HTML script tags.");
        return;
    }
    
    try {
        const pyodide = await loadPyodide({
            // Must use the same full URL as defined in the service worker
            indexURL: "https://cdn.jsdelivr.net/pyodide/v0.25.1/full/" 
        });

        pyodideInstance = pyodide;
        console.log("Pyodide is fully initialized and ready.");
        
        // Load required packages after Pyodide is ready
        await pyodide.loadPackage(["numpy", "sympy"]);

        // Call the main application initialization function from index.html (if it exists)
        if (typeof initializeAppLogic === 'function') {
             initializeAppLogic(pyodideInstance);
        } else {
             document.getElementById("output").textContent = "Pyodide Loaded. Ready to input and solve!";
        }

    } catch (error) {
        console.error("Failed to load Pyodide:", error);
        document.getElementById("output").textContent = `❌ Failed to load Pyodide: ${error.message}`;
    }
}

// Start the loading process
window.addEventListener('DOMContentLoaded', initializePyodideAndApp);
