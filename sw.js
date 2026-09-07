/* Service worker do Caderno MF Imports.
   Faz o app abrir mesmo sem internet. Ao publicar uma versão nova do
   index.html, troque o número em CACHE para forçar a atualização. */

const CACHE = "mf-imports-v3";

const ESSENCIAIS = [
  "./",
  "./index.html",
  "./manifest.webmanifest",
  "./icon-192.png",
  "./icon-512.png",
  "./apple-touch-icon.png",
  "./favicon.png"
];

self.addEventListener("install", e => {
  e.waitUntil(
    caches.open(CACHE)
      .then(c => c.addAll(ESSENCIAIS))
      .then(() => self.skipWaiting())
      .catch(() => self.skipWaiting())
  );
});

self.addEventListener("activate", e => {
  e.waitUntil(
    caches.keys()
      .then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

function guardar(req, resp){
  if (resp && (resp.ok || resp.type === "opaque")) {
    const copia = resp.clone();
    caches.open(CACHE).then(c => c.put(req, copia)).catch(() => {});
  }
  return resp;
}

self.addEventListener("fetch", e => {
  const req = e.request;
  if (req.method !== "GET") return;

  /* A página em si: rede primeiro, para receber atualizações;
     cache como rede de segurança quando está offline. */
  if (req.mode === "navigate") {
    e.respondWith(
      fetch(req)
        .then(r => guardar(new Request("./index.html"), r))
        .catch(() => caches.match("./index.html").then(hit => hit || caches.match("./")))
    );
    return;
  }

  /* Ícones e fontes: cache primeiro, é o que faz abrir rápido e offline. */
  e.respondWith(
    caches.match(req).then(hit => {
      if (hit) return hit;
      return fetch(req).then(r => guardar(req, r)).catch(() => hit);
    })
  );
});
