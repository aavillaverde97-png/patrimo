import * as THREE from 'https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.module.min.js';
import { OrbitControls } from 'https://unpkg.com/three@0.128.0/examples/jsm/controls/OrbitControls.js';
import { IFCLoader } from 'https://unpkg.com/web-ifc-three@0.0.134/IFCLoader.js';

const API = 'http://localhost:8000';

// ── Renderer ──────────────────────────────────────────────────────────────────
const canvas = document.getElementById('canvas');
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
renderer.setPixelRatio(devicePixelRatio);
renderer.setSize(canvas.clientWidth, canvas.clientHeight);

// ── Scene ─────────────────────────────────────────────────────────────────────
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0a0a0f);

// ── Camera ────────────────────────────────────────────────────────────────────
const camera = new THREE.PerspectiveCamera(
  45,
  canvas.clientWidth / canvas.clientHeight,
  0.01,
  500
);
camera.position.set(10, 8, 12);

// ── Controls ──────────────────────────────────────────────────────────────────
const controls = new OrbitControls(camera, canvas);
controls.enableDamping = true;

// ── Lights ────────────────────────────────────────────────────────────────────
scene.add(new THREE.AmbientLight(0xffffff, 0.5));
const sun = new THREE.DirectionalLight(0xffffff, 1);
sun.position.set(10, 20, 10);
scene.add(sun);
scene.add(new THREE.GridHelper(30, 30, 0x222233, 0x111122));

// ── IFC Loader ────────────────────────────────────────────────────────────────
const loader = new IFCLoader();
loader.ifcManager.setWasmPath('https://unpkg.com/web-ifc@0.0.57/');

let model = null;
const raycaster = new THREE.Raycaster();
raycaster.firstHitOnly = true;
const mouse = new THREE.Vector2();

// Material highlight selección
const MAT_SELECTED = new THREE.MeshLambertMaterial({
  color: 0xe8c96a,
  transparent: true,
  opacity: 0.85,
  side: THREE.DoubleSide,
});

// ── Cargar IFC ────────────────────────────────────────────────────────────────
export async function cargarIFC(url) {
  setStatus('Cargando modelo IFC...');
  model = await loader.loadAsync(url, (p) => {
    const pct = Math.round((p.loaded / p.total) * 100);
    setStatus(`Cargando... ${pct}%`);
  });
  scene.add(model);

  // Centrar cámara al modelo
  const box    = new THREE.Box3().setFromObject(model);
  const size   = box.getSize(new THREE.Vector3());
  const center = box.getCenter(new THREE.Vector3());
  const maxDim = Math.max(size.x, size.y, size.z);
  camera.position.set(
    center.x + maxDim,
    center.y + maxDim * 0.7,
    center.z + maxDim
  );
  controls.target.copy(center);
  controls.update();

  setStatus('Modelo listo — click para seleccionar elemento');
}

// ── Selección por click ───────────────────────────────────────────────────────
canvas.addEventListener('click', async (e) => {
  if (!model) return;

  const rect = canvas.getBoundingClientRect();
  mouse.x =  ((e.clientX - rect.left) / rect.width)  * 2 - 1;
  mouse.y = -((e.clientY - rect.top)  / rect.height) * 2 + 1;

  raycaster.setFromCamera(mouse, camera);
  const hits = raycaster.intersectObjects(model.children, true);
  if (!hits.length) return;

  const hit       = hits[0];
  const faceIndex = hit.face?.a;
  if (faceIndex == null) return;

  const expressId = await loader.ifcManager.getExpressId(
    hit.object.geometry,
    faceIndex
  );

  await seleccionarElemento(expressId);
});

// ── Highlight + datos ─────────────────────────────────────────────────────────
async function seleccionarElemento(expressId) {
  // Highlight
  loader.ifcManager.createSubset({
    modelID: 0,
    ids: [expressId],
    material: MAT_SELECTED,
    scene,
    removePrevious: true,
  });

  // Propiedades IFC locales
  const props = await loader.ifcManager.getItemProperties(0, expressId, true);
  mostrarPropiedades(props, expressId);

  // Datos financieros desde backend
  await cargarFinanciero(expressId);
}

function mostrarPropiedades(props, expressId) {
  const panel = document.getElementById('panel-propiedades');
  const guid  = props?.GlobalId?.value ?? '—';
  const items = [
    ['Express ID', expressId],
    ['Tipo',       props?.constructor?.name ?? '—'],
    ['Nombre',     props?.Name?.value ?? '—'],
    ['GUID',       guid.substring(0, 20) + '...'],
  ];
  panel.innerHTML = items
    .map(([k, v]) =>
      `<div class="kv"><span class="k">${k}</span><span class="v">${v}</span></div>`
    )
    .join('');
}

async function cargarFinanciero(expressId) {
  const panel = document.getElementById('panel-financiero');
  panel.innerHTML = '<div class="loading">Consultando backend...</div>';
  try {
    const r    = await fetch(`${API}/ifc-element/${expressId}`);
    const data = await r.json();
    renderFinanciero(data);
  } catch {
    panel.innerHTML = '<div class="error">Backend no disponible</div>';
  }
}

function renderFinanciero(data) {
  const panel = document.getElementById('panel-financiero');
  const f = data.financiero;
  if (!f) {
    panel.innerHTML = '<div class="muted">Elemento sin datos financieros asociados</div>';
    return;
  }
  panel.innerHTML = `
    <div class="kv"><span class="k">Propietario</span><span class="v">${f.nombre}</span></div>
    <div class="kv"><span class="k">NOI mensual</span><span class="v g">$${f.noi_mensual.toLocaleString('es-AR')}</span></div>
    <div class="kv"><span class="k">NOI anual</span><span class="v g">$${f.noi_anual.toLocaleString('es-AR')}</span></div>
    <div class="kv"><span class="k">Valor cap ARS</span><span class="v y">$${f.valor_capitalizacion_ars.toLocaleString('es-AR')}</span></div>
    <div class="kv"><span class="k">Valor cap USD</span><span class="v y">USD ${f.valor_capitalizacion_usd.toLocaleString('es-AR')}</span></div>
    <div class="kv"><span class="k">Valor DCF USD</span><span class="v">USD ${f.valor_descuento_flujos_usd.toLocaleString('es-AR')}</span></div>
    <div class="kv"><span class="k">Dólar blue</span><span class="v">$${f.dolar_blue}</span></div>
  `;
}

// ── Utilidades ────────────────────────────────────────────────────────────────
function setStatus(msg) {
  const el = document.getElementById('status');
  if (el) el.textContent = msg;
}

// ── Resize ────────────────────────────────────────────────────────────────────
window.addEventListener('resize', () => {
  const w = canvas.clientWidth;
  const h = canvas.clientHeight;
  renderer.setSize(w, h);
  camera.aspect = w / h;
  camera.updateProjectionMatrix();
});

// ── Loop ──────────────────────────────────────────────────────────────────────
(function animate() {
  requestAnimationFrame(animate);
  controls.update();
  renderer.render(scene, camera);
})();
