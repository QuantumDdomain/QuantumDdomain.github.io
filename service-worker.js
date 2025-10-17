const CACHE_NAME = 'pyodide-full-v0251-cache-1'; 
const PYODIDE_VERSION = 'v0.25.1';
const PYODIDE_BASE_URL = `https://cdn.jsdelivr.net/pyodide/${PYODIDE_VERSION}/full/`;

// List of ALL essential Pyodide files for version v0.25.1
// NOTE: This list is based on common Pyodide requests. If your app fails, 
// check the Network tab on first load to see if any .whl files are also requested.
const CACHE_URLS = [
  // Core application files
  '/',                      // The main domain root
  '/index.html',            // Root index.html
  '/service-worker-setup.js',
  '/load-pyodide-and-app.js',
  
  // --- CORE PYODIDE FILES (from CDN) ---
  `${PYODIDE_BASE_URL}pyodide.js`,
  // The WebAssembly module and its large data file (Standard Library)
  `${PYODIDE_BASE_URL}pyodide.asm.wasm`,
  `${PYODIDE_BASE_URL}pyodide.asm.data`,
  `${PYODIDE_BASE_URL}pyodide.asm.js`,
  // Package metadata index
  `${PYODIDE_BASE_URL}packages.json`,
  
  // Add other local assets (CSS, Images) if desired for full offline support
];

// 1. Installation: Open cache and store all files
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      console.log('Pre-caching FULL Pyodide files...');
      return cache.addAll(CACHE_URLS);
    })
  );
});

// 2. Fetching: Intercept network requests and serve from cache first
self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request).then(cachedResponse => {
      // If the file is in the cache, return it immediately (FAST!)
      if (cachedResponse) {
        return cachedResponse;
      }
      // Otherwise, fetch from the network
      return fetch(event.request);
    })
  );
});

// 3. Activation: Clean up old caches when the worker updates
self.addEventListener('activate', event => {
  const cacheWhitelist = [CACHE_NAME];
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (!cacheWhitelist.includes(cacheName)) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});