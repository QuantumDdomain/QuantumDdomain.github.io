// service-worker.js

const CACHE_NAME = 'numerical-app-v1';
const FILES_TO_CACHE = [
  '/',                            // main index.html
  '/index.html',                   // root index.html
  '/README.md',
  '/requirements.txt',
  
  // Pyodide core files (from CDN)
  'https://cdn.jsdelivr.net/pyodide/v0.25.1/full/pyodide.js',
  'https://cdn.jsdelivr.net/pyodide/v0.25.1/full/pyodide.asm.wasm',
  'https://cdn.jsdelivr.net/pyodide/v0.25.1/full/packages.json',
  'https://cdn.jsdelivr.net/pyodide/v0.25.1/full/numpy.js',
  'https://cdn.jsdelivr.net/pyodide/v0.25.1/full/numpy.data',
  'https://cdn.jsdelivr.net/pyodide/v0.25.1/full/numpy.wasm',
  
  // Pre-caching important .html files
  '/curve_fitting/index.html',
  '/derivatives/index.html',
  '/integration/index.html',
  '/interpolation/index.html',
  '/linear_solver/index.html',
  '/matrixlab/index.html',
  '/ode_solver/index.html',
  '/root_finding/index.html',

  // Pre-caching specific .html files for algorithms
  '/interpolation/lagrange.html',
  '/interpolation/spline.html',
  '/ode_solver/plot.html',
  '/ode_solver/multivariable_rk.html',
  '/ode_solver/runge_kutta.html',
  '/matrixlab/inverse_matrix.html',
  '/matrixlab/matrixeigen.html',
  '/matrixlab/matrix_multiply.html',
  
  // Pre-caching Python files (modify as needed)
  '/derivatives/point_5_first_derivative.py',
  '/derivatives/second_derivative.py',
  '/integration/simpson.py',
  '/interpolation/web_lagrange_interpolation.py',
  '/interpolation/web_spline_interpolation.py',
  '/linear_solver/web_linear_solver.py',
  '/ode_solver/runge_kutta_multivariable.py',
  '/ode_solver/runge_kutta_method.py',
  '/root_finding/web_muller.py',
];

// During install, open cache and add files
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(FILES_TO_CACHE);
    })
  );
});

// Fetch event listener to serve files from cache if available
self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request).then((cachedResponse) => {
      // Return cached response if found, else fetch from the network
      return cachedResponse || fetch(event.request);
    })
  );
});

// Clear old caches (optional)
self.addEventListener('activate', (event) => {
  const cacheWhitelist = [CACHE_NAME];
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (!cacheWhitelist.includes(cacheName)) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});