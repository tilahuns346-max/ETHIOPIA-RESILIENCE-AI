import os
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from backend.app.router import Router

router = Router()

# Import all route modules so they register with the router
import backend.app.routes.auth
import backend.app.routes.users
import backend.app.routes.incidents
import backend.app.routes.incidents_list
import backend.app.routes.incident_detail
import backend.app.routes.sync
import backend.app.routes.verification
import backend.app.routes.alerts
import backend.app.routes.broadcast
import backend.app.routes.teams
import backend.app.routes.dispatch
import backend.app.routes.analytics
import backend.app.routes.events
import backend.app.routes.gis
import backend.app.routes.health
import backend.app.routes.ai_predictions

DASHBOARD_HTML = """<!DOCTYPE html>
<html lang="am">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ETHIOPIA RESILIENCE AI — ብሔራዊ የአደጋ መቆጣጠሪያ ማዕከል</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Ethiopic:wght@400;600;700;800&family=Inter:wght@400;600;700&display=swap');
        body { font-family: 'Inter', 'Noto Sans Ethiopic', sans-serif; }
    </style>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen flex flex-col">

    <!-- Top Navigation Bar -->
    <header class="bg-slate-900 border-b border-slate-800 px-6 py-4 flex flex-wrap justify-between items-center shadow-lg sticky top-0 z-50">
        <div class="flex items-center space-x-3">
            <span class="text-3xl">🇪🇹</span>
            <div>
                <div class="flex items-center space-x-2">
                    <h1 class="text-xl font-bold tracking-tight text-white">ETHIOPIA RESILIENCE AI</h1>
                    <span class="px-2 py-0.5 text-xs font-semibold bg-emerald-500/20 text-emerald-400 border border-emerald-500/40 rounded-full">v2.4.0-PROD</span>
                </div>
                <p class="text-xs text-slate-400">የኢትዮጵያ አደጋ ቅድመ ማስጠንቀቂያ፣ የማህበረሰብ ሪፖርት እና የአደጋ ጊዜ ምላሽ ቅንጅት መድረክ</p>
            </div>
        </div>
        <div class="flex items-center space-x-4 mt-2 sm:mt-0">
            <span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-red-950 text-red-400 border border-red-800 animate-pulse">
                ● EDRMC LIVE COMMAND ACTIVE
            </span>
            <button onclick="toggleReportModal()" class="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg text-sm font-semibold transition shadow-md">
                + አደጋ ሪፖርት አድርግ (Report)
            </button>
        </div>
    </header>

    <!-- Main Content Grid -->
    <main class="flex-1 max-w-7xl w-full mx-auto p-6 space-y-6">

        <!-- KPI Status Cards -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <div class="bg-slate-900/90 border border-slate-800 rounded-xl p-5 shadow-sm">
                <p class="text-xs font-semibold text-slate-400 uppercase tracking-wider">የቀረቡ ሪፖርቶች (Total Reports)</p>
                <p class="text-3xl font-extrabold text-blue-400 mt-2" id="kpi-incidents">1,248</p>
                <p class="text-xs text-slate-500 mt-1">ከ 14 ክልሎችና አስተዳደሮች</p>
            </div>
            <div class="bg-slate-900/90 border border-slate-800 rounded-xl p-5 shadow-sm">
                <p class="text-xs font-semibold text-slate-400 uppercase tracking-wider">በወረዳ የተረጋገጡ (Verified)</p>
                <p class="text-3xl font-extrabold text-amber-400 mt-2" id="kpi-verified">89</p>
                <p class="text-xs text-slate-500 mt-1">በአካባቢው የመስክ መርማሪዎች</p>
            </div>
            <div class="bg-slate-900/90 border border-slate-800 rounded-xl p-5 shadow-sm">
                <p class="text-xs font-semibold text-slate-400 uppercase tracking-wider">ንቁ ማስጠንቀቂያዎች (Active Alerts)</p>
                <p class="text-3xl font-extrabold text-red-500 mt-2" id="kpi-alerts">4</p>
                <p class="text-xs text-slate-500 mt-1">ደረጃ 4 እና 3 አደጋዎች</p>
            </div>
            <div class="bg-slate-900/90 border border-slate-800 rounded-xl p-5 shadow-sm">
                <p class="text-xs font-semibold text-slate-400 uppercase tracking-wider">የተሰማሩ ቡድኖች (Response Teams)</p>
                <p class="text-3xl font-extrabold text-emerald-400 mt-2" id="kpi-teams">24</p>
                <p class="text-xs text-slate-500 mt-1">ቀይ መስቀል እና ማዳን</p>
            </div>
        </div>

        <!-- Interactive Map & Live Feed Section -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
            
            <!-- Map Container (2 Columns) -->
            <div class="lg:col-span-2 bg-slate-900 border border-slate-800 rounded-xl overflow-hidden flex flex-col shadow-lg">
                <div class="px-5 py-3 border-b border-slate-800 flex justify-between items-center bg-slate-900/50">
                    <h3 class="font-bold text-sm text-slate-200">🗺️ የኢትዮጵያ የቀጥታ አደጋ ስጋት ካርታ (Live Hazard Map)</h3>
                    <span class="text-xs text-slate-400">PostGIS EPSG:4326</span>
                </div>
                <div id="map" style="height: 480px; width: 100%;"></div>
            </div>

            <!-- Live Incident Stream (1 Column) -->
            <div class="bg-slate-900 border border-slate-800 rounded-xl flex flex-col shadow-lg overflow-hidden">
                <div class="px-5 py-3 border-b border-slate-800 flex justify-between items-center bg-slate-900/50">
                    <h3 class="font-bold text-sm text-slate-200">🚨 የቀጥታ አደጋዎች ዝርዝር (Live Feed)</h3>
                    <button onclick="loadIncidents()" class="text-xs text-emerald-400 hover:underline">አድስ (Refresh)</button>
                </div>
                <div id="incidents-container" class="flex-1 p-4 space-y-3 overflow-y-auto max-h-[480px]">
                    <div class="text-center py-10 text-slate-500 text-sm">ሪፖርቶች እየተጫኑ ነው...</div>
                </div>
            </div>
        </div>

        <!-- API Links and System Endpoints -->
        <div class="bg-slate-900/60 border border-slate-800 rounded-xl p-4">
            <h4 class="text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">ፈጣን የ REST API ሊንኮች (Direct API Endpoints)</h4>
            <div class="flex flex-wrap gap-2 text-xs">
                <a href="/api/v1/health/" target="_blank" class="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded border border-slate-700 font-mono">/api/v1/health/</a>
                <a href="/api/v1/incidents/" target="_blank" class="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded border border-slate-700 font-mono">/api/v1/incidents/</a>
                <a href="/api/v1/analytics/overview/" target="_blank" class="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded border border-slate-700 font-mono">/api/v1/analytics/overview/</a>
                <a href="/api/v1/teams/" target="_blank" class="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded border border-slate-700 font-mono">/api/v1/teams/</a>
                <a href="/api/v1/gis/boundaries/" target="_blank" class="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded border border-slate-700 font-mono">/api/v1/gis/boundaries/</a>
                <a href="https://github.com/tilahuns346-max/ETHIOPIA-RESILIENCE-AI" target="_blank" class="px-3 py-1.5 bg-emerald-950/80 hover:bg-emerald-900 text-emerald-300 rounded border border-emerald-700 font-medium ml-auto">GitHub Repository (105 Commits) ➔</a>
            </div>
        </div>

    </main>

    <!-- Incident Submission Modal -->
    <div id="report-modal" class="fixed inset-0 bg-black/70 backdrop-blur-sm hidden items-center justify-center p-4 z-50">
        <div class="bg-slate-900 border border-slate-800 rounded-2xl max-w-lg w-full p-6 shadow-2xl">
            <div class="flex justify-between items-center mb-4">
                <h3 class="text-lg font-bold text-white">አዲስ አደጋ ሪፖርት ማድረጊያ (Submit Hazard Report)</h3>
                <button onclick="toggleReportModal()" class="text-slate-400 hover:text-white text-xl">&times;</button>
            </div>
            <form id="incident-form" onsubmit="submitIncident(event)" class="space-y-4">
                <div>
                    <label class="block text-xs font-semibold text-slate-400 mb-1">የአደጋው አይነት (Hazard Type)</label>
                    <select id="hazard-type" class="w-full bg-slate-800 border border-slate-700 rounded-lg p-2.5 text-white text-sm">
                        <option value="HAZ-LANDSLIDE">የመሬት መንሸራተት / ናዳ (Debris Flow & Landslide)</option>
                        <option value="HAZ-FLASH-FLOOD">የወንዝ ሙላት / ድንገተኛ ጎርፍ (Riverine & Flash Flood)</option>
                        <option value="HAZ-DROUGHT">የተራዘመ የድርቅ አደጋ (Pastoral Drought)</option>
                        <option value="HAZ-WILDFIRE">የደንና ሰደድ እሳት (Wildfire)</option>
                        <option value="HAZ-URBAN-FIRE">የከተማ ከፍተኛ እሳት (Urban Fire - Mercato)</option>
                    </select>
                </div>
                <div>
                    <label class="block text-xs font-semibold text-slate-400 mb-1">ቦታ (Location Coordinates [Lat, Lon])</label>
                    <div class="grid grid-cols-2 gap-2">
                        <input type="number" step="any" id="lat" value="6.2241" placeholder="Latitude" class="bg-slate-800 border border-slate-700 rounded-lg p-2 text-white text-sm" required>
                        <input type="number" step="any" id="lon" value="36.9214" placeholder="Longitude" class="bg-slate-800 border border-slate-700 rounded-lg p-2 text-white text-sm" required>
                    </div>
                    <span class="text-[11px] text-slate-500">ነባሪ ቦታ፡ ጎፋ (Kencho Shacha, Gofa Zone)</span>
                </div>
                <div>
                    <label class="block text-xs font-semibold text-slate-400 mb-1">ዝርዝር መግለጫ (Description in Amharic / English)</label>
                    <textarea id="desc" rows="3" class="w-full bg-slate-800 border border-slate-700 rounded-lg p-2.5 text-white text-sm" placeholder="በከባድ ዝናብ ሳቢያ የተከሰተውን አደጋ ይግለጹ..." required></textarea>
                </div>
                <div>
                    <label class="block text-xs font-semibold text-slate-400 mb-1">የተጎጂዎች ግምት (Estimated Affected People)</label>
                    <input type="number" id="affected" value="150" class="w-full bg-slate-800 border border-slate-700 rounded-lg p-2 text-white text-sm">
                </div>
                <div class="flex justify-end space-x-3 pt-2">
                    <button type="button" onclick="toggleReportModal()" class="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-lg text-sm font-semibold">ይቅር (Cancel)</button>
                    <button type="submit" class="px-5 py-2 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg text-sm font-semibold shadow-md">ሪፖርት ላክ (Submit)</button>
                </div>
            </form>
        </div>
    </div>

    <!-- Script to Initialize Map and Data -->
    <script>
        // Initialize Leaflet Map centered on Ethiopia
        const map = L.map('map').setView([9.0, 39.5], 6);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 18,
            attribution: '© OpenStreetMap | EDRMC'
        }).addTo(map);

        // Pre-loaded high-risk zones
        const highRiskZones = [
            { name: "ገዜ ጎፋ (Geze Gofa - Kencho Shacha)", lat: 6.2241, lon: 36.9214, type: "የመሬት መንሸራተት / ናዳ", color: "#dc2626" },
            { name: "አዋሽ ፈንታሌ (Awash Fentale - Afar)", lat: 8.9833, lon: 40.0167, type: "የወንዝ ሙላትና ጎርፍ", color: "#0284c7" },
            { name: "ያቤሎ (Yabello - Borana Pastoral)", lat: 4.8833, lon: 38.0833, type: "የተራዘመ የድርቅ አደጋ", color: "#f59e0b" },
            { name: "መርካቶ (Mercato Central - Addis Ababa)", lat: 9.0300, lon: 38.7400, type: "የንግድ ማዕከል እሳት", color: "#ea580c" }
        ];

        highRiskZones.forEach(zone => {
            const circle = L.circle([zone.lat, zone.lon], {
                color: zone.color,
                fillColor: zone.color,
                fillOpacity: 0.4,
                radius: 25000
            }).addTo(map);
            circle.bindPopup(`<b>${zone.name}</b><br>የአደጋ አይነት፡ ${zone.type}`);
        });

        function toggleReportModal() {
            const modal = document.getElementById('report-modal');
            modal.classList.toggle('hidden');
            modal.classList.toggle('flex');
        }

        async function loadIncidents() {
            try {
                const res = await fetch('/api/v1/incidents/');
                const data = await res.json();
                const container = document.getElementById('incidents-container');
                
                if (data.data && data.data.length > 0) {
                    container.innerHTML = data.data.map(inc => `
                        <div class="bg-slate-800/80 border border-slate-700/60 p-3 rounded-lg text-xs space-y-1 hover:border-slate-600 transition">
                            <div class="flex justify-between items-center">
                                <span class="font-bold text-slate-200">${inc.incident_number}</span>
                                <span class="px-2 py-0.5 rounded text-[10px] font-bold ${inc.status === 'VERIFIED' ? 'bg-emerald-950 text-emerald-400 border border-emerald-700' : 'bg-amber-950 text-amber-400 border border-amber-700'}">${inc.status}</span>
                            </div>
                            <p class="font-semibold text-slate-300">${inc.title_am || inc.title_en}</p>
                            <p class="text-slate-400 line-clamp-2">${inc.description_raw}</p>
                            <div class="text-[10px] text-slate-500 pt-1 flex justify-between">
                                <span>📍 ${inc.latitude.toFixed(4)}, ${inc.longitude.toFixed(4)}</span>
                                <span>👥 ~${inc.estimated_affected_people || 0} ተጎጂዎች</span>
                            </div>
                        </div>
                    `).join('');
                }
            } catch (e) {
                console.error("Failed to load incidents", e);
            }
        }

        async function submitIncident(e) {
            e.preventDefault();
            const payload = {
                hazard_type_code: document.getElementById('hazard-type').value,
                location: {
                    type: "Point",
                    coordinates: [parseFloat(document.getElementById('lon').value), parseFloat(document.getElementById('lat').value)]
                },
                title_am: document.getElementById('desc').value.slice(0, 30),
                description_raw: document.getElementById('desc').value,
                estimated_affected_people: parseInt(document.getElementById('affected').value) || 0,
                detected_language: "am"
            };

            const res = await fetch('/api/v1/incidents/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            if (res.ok) {
                alert("አደጋው በተሳካ ሁኔታ ተመዝግቧል! (Incident Submitted Successfully)");
                toggleReportModal();
                loadIncidents();
            } else {
                alert("ሪፖርት ማድረግ አልተሳካም። እባክዎ እንደገና ይሞክሩ።");
            }
        }

        // Initial fetch
        loadIncidents();
    </script>
</body>
</html>
"""

@router.get("/")
def get_dashboard_root(req: dict):
    return 200, DASHBOARD_HTML

@router.get("/dashboard/")
def get_dashboard_page(req: dict):
    return 200, DASHBOARD_HTML

class ResilienceRequestHandler(BaseHTTPRequestHandler):
    def _set_cors_headers(self, is_html=False):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PATCH, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization, Idempotency-Key, X-Sync-Batch-ID")
        if is_html:
            self.send_header("Content-Type", "text/html; charset=utf-8")
        else:
            self.send_header("Content-Type", "application/json; charset=utf-8")

    def do_OPTIONS(self):
        self.send_response(204)
        self._set_cors_headers()
        self.end_headers()

    def handle_request(self, method: str):
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        if path.endswith("/") and len(path) > 1:
            pass
        elif not path.endswith("/") and "." not in path:
            path = path + "/"
            
        query_params = {k: v[0] if len(v) == 1 else v for k, v in parse_qs(parsed_url.query).items()}
        
        handler, path_params = router.resolve(method, path)
        if not handler and not path.endswith("/"):
            handler, path_params = router.resolve(method, path + "/")
            
        if not handler:
            self.send_response(404)
            self._set_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ERROR", "message": f"Endpoint not found: {method} {path}"}).encode("utf-8"))
            return

        body = None
        content_length = int(self.headers.get("Content-Length", 0))
        if content_length > 0:
            raw_body = self.rfile.read(content_length).decode("utf-8")
            try:
                body = json.loads(raw_body)
            except Exception:
                body = raw_body

        req = {
            "method": method,
            "path": path,
            "path_params": path_params,
            "query_params": query_params,
            "headers": dict(self.headers),
            "body": body
        }

        try:
            status_code, resp_body = handler(req)
            is_html = isinstance(resp_body, str) and (resp_body.strip().startswith("<!DOCTYPE") or "<html" in resp_body)
            self.send_response(status_code)
            self._set_cors_headers(is_html=is_html)
            self.end_headers()
            
            if is_html:
                self.wfile.write(resp_body.encode("utf-8"))
            else:
                self.wfile.write(json.dumps(resp_body, default=str).encode("utf-8"))
        except Exception as e:
            self.send_response(500)
            self._set_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps({"status": "INTERNAL_SERVER_ERROR", "error": str(e)}).encode("utf-8"))

    def do_GET(self):
        self.handle_request("GET")

    def do_POST(self):
        self.handle_request("POST")

    def do_PATCH(self):
        self.handle_request("PATCH")

    def do_DELETE(self):
        self.handle_request("DELETE")

def run_server(host="0.0.0.0", port=8000):
    server = HTTPServer((host, port), ResilienceRequestHandler)
    print(f"Ethiopia Resilience AI Backend running on http://{host}:{port}")
    server.serve_forever()

if __name__ == "__main__":
    run_server()
