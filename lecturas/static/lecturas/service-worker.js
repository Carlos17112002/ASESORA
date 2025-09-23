self.addEventListener('install', e => {
    e.waitUntil(
        caches.open('lecturas-cache').then(cache => {
            return cache.addAll(['/', '/lecturas/app/', '/static/lecturas/app.js']);
        })
    );
});

self.addEventListener('fetch', e => {
    e.respondWith(
        caches.match(e.request).then(response => response || fetch(e.request))
    );
});
