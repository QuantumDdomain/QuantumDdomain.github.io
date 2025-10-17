// Register the Service Worker on every page load
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    // Registers the service-worker.js file located at the root
    navigator.serviceWorker.register('/service-worker.js').then(registration => {
      console.log('Service Worker registered successfully.');
    }).catch(error => {
      console.error('Service Worker registration failed:', error);
    });
  });
}