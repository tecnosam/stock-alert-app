const CACHE_NAME = 'static-cache';

const FILES_TO_CACHE = ["/static/", "/templates", "/", "/signup.html", "/login.html", "/basse.html"]

self.addEventListener('install', (evt) => {
  console.log('[ServiceWorker] Install');
  evt.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log('[ServiceWorker] Pre-caching offline page');
      return cache.addAll(FILES_TO_CACHE);
    })
  );

  self.skipWaiting();
});

self.addEventListener('activate', (evt) => {
  console.log('[ServiceWorker] Activate');
  evt.waitUntil(
    caches.keys().then((keyList) => {
      return Promise.all(keyList.map((key) => {
        if (key !== CACHE_NAME) {
          console.log('[ServiceWorker] Removing old cache', key);
          return caches.delete(key);
        }
      }));
    })
  );
  self.clients.claim();
});

self.addEventListener('push', function(event) {
  console.log('[Service Worker] Push Received.');

  const title = 'Tweedler';
  const options = {
    body: event.data.text()
  };

  event.waitUntil(self.registration.showNotification(title, options));
});

// self.addEventListener('sync', function(event) {
//   if (event.tag == 'example-tag') {
//     event.waitUntil(
//     // Actions to be performed go here.
//     );
//   }
// });

self.addEventListener('fetch', (evt) => {
  if (evt.request.mode !== 'navigate') {
    return;
  }
  evt.respondWith(fetch(evt.request).catch(() => {
      return caches.open(CACHE_NAME).then((cache) => {
        return cache.match('base.html');
      });
    })
  );
});

var checkResponse = function(request){
  return new Promise(function(fulfill, reject) {
    fetch(request).then(function(response){
      if(response.status !== 404) {
        fulfill(response);
      } else {
        reject();
      }
    }, reject);
  });
};

var addToCache = function(request){
  return caches.open("offline").then(function (cache) {
    return fetch(request).then(function (response) {
      console.log(response.url + " was cached");
      return cache.put(request, response);
    });
  });
};

var returnFromCache = function(request){
  return caches.open("offline").then(function (cache) {
    return cache.match(request).then(function (matching) {
     if(!matching || matching.status == 404) {
       return cache.match("base.html");
     } else {
       return matching;
     }
    });
  });
};