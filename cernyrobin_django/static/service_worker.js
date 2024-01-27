console.log("Service worker loaded")

importScripts('https://storage.googleapis.com/workbox-cdn/releases/6.4.1/workbox-sw.js');
  
workbox.routing.registerRoute(
    ({request}) => request.destination === 'image',
    new workbox.strategies.CasheFirst()
    /* new workbox.strategies.NetworkFirst() if it performs like shit*/
)