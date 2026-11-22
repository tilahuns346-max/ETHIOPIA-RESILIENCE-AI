const CACHE_NAME = 'resilience-ai-cache-v1';
self.addEventListener('install', (e) => {
  e.waitUntil(caches.open(CACHE_NAME).then((cache) => cache.addAll(['/'])));
});
