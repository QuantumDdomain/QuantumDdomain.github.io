const CACHE_NAME = 'app-only-cache-v2'; // Incrementing cache version again to force re-install
const PYODIDE_VERSION = 'v0.25.1'; // Keeping this variable, but not using it for caching
const PYODIDE_BASE_URL = `https://cdn.jsdelivr.net/pyodide/${PYODIDE_VERSION}/full/`;

// List of only the local application files.
// We are REMOVING the root path '/' which can sometimes cause fetch failures.
const CACHE_URLS = [
  // --- Local Application Files ---
  '/index.html',            // Root index.html
  '/service-worker-setup.js',
  '/load-pyodide-and-app.js',
];

// 1. Installation: Open cache and store only local files
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      console.log('Pre-caching ONLY local application files to bypass path errors.');
      // This will now only fail if one of the local files is missing (which they shouldn't be).
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
      // Otherwise, fetch from the network (Pyodide CDN files will be fetched here)
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
