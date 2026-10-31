/* Leaflet maps: home (departures), trip detail (route), publication (point picker). */
const TILE = "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png";
const ATTR = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>';

function baseMap(id, lat, lng, zoom) {
  const el = document.getElementById(id);
  if (!el || typeof L === "undefined") return null;
  const map = L.map(el, { scrollWheelZoom: false }).setView([lat, lng], zoom);
  L.tileLayer(TILE, { attribution: ATTR, maxZoom: 19 }).addTo(map);
  return map;
}

function dotIcon(color) {
  return L.divIcon({ className: "", iconSize: [18, 18], iconAnchor: [9, 9],
    html: `<span style="display:block;width:18px;height:18px;border-radius:50%;background:${color};border:3px solid #fff;box-shadow:0 1px 4px rgba(0,0,0,.4)"></span>` });
}
const ICON_A = () => dotIcon("#12573f"), ICON_B = () => dotIcon("#e8742c");

function initHomeMap(id, lat, lng) {
  const map = baseMap(id, lat, lng, 12);
  if (!map) return;
  L.marker([lat, lng], { icon: ICON_B() }).addTo(map).bindPopup("<b>IFRI</b><br>Université d'Abomey-Calavi");
  const data = document.getElementById("home-points");
  const points = data ? JSON.parse(data.textContent) : [];
  points.forEach(p => L.marker([p.lat, p.lng], { icon: ICON_A() }).addTo(map)
    .bindPopup(`<a href="${p.url}">${p.titre}</a>`));
  const fit = () => {
    map.invalidateSize();
    if (points.length) map.fitBounds(L.latLngBounds([[lat, lng], ...points.map(p => [p.lat, p.lng])]).pad(0.2));
  };
  fit();
  window.addEventListener("load", fit);   // layout may change once fonts/styles are applied
}

function initTripMap(id, a, b) {
  const map = baseMap(id, a[0], a[1], 13);
  if (!map) return;
  L.marker(a, { icon: ICON_A() }).addTo(map).bindTooltip("Départ");
  L.marker(b, { icon: ICON_B() }).addTo(map).bindTooltip("Arrivée");
  L.polyline([a, b], { color: "#12573f", weight: 4, dashArray: "8 8", opacity: .8 }).addTo(map);
  const fit = () => { map.invalidateSize(); map.fitBounds(L.latLngBounds([a, b]).pad(0.3)); };
  fit();
  window.addEventListener("load", fit);
}

function initPickerMap(id, ifriLat, ifriLng) {
  const map = baseMap(id, ifriLat, ifriLng, 12);
  if (!map) return;
  map.scrollWheelZoom.enable();
  const f = n => document.getElementById("id_" + n);
  const markers = {};
  let mode = "depart";

  function place(which, latlng) {
    const icon = which === "depart" ? ICON_A() : ICON_B();
    if (markers[which]) markers[which].setLatLng(latlng);
    else {
      markers[which] = L.marker(latlng, { icon, draggable: true }).addTo(map);
      markers[which].on("dragend", e => write(which, e.target.getLatLng()));
    }
    write(which, latlng);
  }
  function write(which, ll) {
    f("lat_" + which).value = ll.lat.toFixed(6);
    f("lng_" + which).value = ll.lng.toFixed(6);
  }

  // existing values (edit form or redisplay after error)
  ["depart", "arrivee"].forEach(w => {
    const la = parseFloat((f("lat_" + w).value || "").replace(",", "."));
    const lo = parseFloat((f("lng_" + w).value || "").replace(",", "."));
    if (!isNaN(la) && !isNaN(lo)) place(w, L.latLng(la, lo));
  });
  const pts = Object.values(markers).map(m => m.getLatLng());
  if (pts.length === 2) map.fitBounds(L.latLngBounds(pts).pad(0.3));

  document.querySelectorAll(".chip[data-mode]").forEach(btn => btn.addEventListener("click", () => {
    mode = btn.dataset.mode;
    document.querySelectorAll(".chip[data-mode]").forEach(b => b.classList.toggle("active", b === btn));
  }));
  document.getElementById("btn-ifri")?.addEventListener("click", () => {
    place("arrivee", L.latLng(ifriLat, ifriLng));
    if (!f("lieu_arrivee").value) f("lieu_arrivee").value = "IFRI — UAC Abomey-Calavi";
  });
  map.on("click", e => {
    place(mode, e.latlng);
    if (mode === "depart") document.querySelector('.chip[data-mode="arrivee"]').click();
  });
}
