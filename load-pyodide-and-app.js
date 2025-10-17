// Global variable for the Pyodide instance
let pyodideInstance = null;

async function initializePyodideAndApp() {
    // Ensure the browser has finished loading before attempting to load Pyodide
    // The Pyodide files will be pulled from the Service Worker cache if available.
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

        // --- PLACE YOUR MAIN APPLICATION LOGIC HERE ---
        // Example: Run a setup function or display your UI
        // pyodideInstance.runPython('import numpy');
        // document.getElementById('py-status').textContent = 'Python Ready';

    } catch (error) {
        console.error("Failed to load Pyodide:", error);
    }
}

// Start the loading process
window.addEventListener('DOMContentLoaded', initializePyodideAndApp);