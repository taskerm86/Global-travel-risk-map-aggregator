import { useEffect, useState } from "react";
import { MapContainer, TileLayer, GeoJSON } from "react-leaflet";
import "leaflet/dist/leaflet.css";

const LEVEL_COLORS = { 1: "#2ecc71", 2: "#f39c12", 3: "#e67e22", 4: "#e74c3c" };
const LEVEL_LABELS = { 1: "Low Risk", 2: "Some Risk", 3: "High Risk", 4: "Do Not Travel" };

export default function App() {
  const [advisories, setAdvisories] = useState([]);
  const [geoData, setGeoData] = useState(null);
  const [selected, setSelected] = useState(null);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/advisories")
      .then(r => r.json())
      .then(data => { console.log("Loaded advisories:", data); setAdvisories(data); })
      .catch(e => console.error("API error:", e));
    fetch("https://raw.githubusercontent.com/datasets/geo-countries/master/data/countries.geojson")
      .then(r => r.json())
      .then(setGeoData);
  }, []);

  function findMatch(name) {
    return advisories.find(a => (a.name || "").toLowerCase() === (name || "").toLowerCase());
  }

  function getColor(feature) {
    const name = feature?.properties?.name;
    const match = findMatch(name);
    return match ? (LEVEL_COLORS[match.level] || "#cccccc") : "#cccccc";
  }

  function onEachFeature(feature, layer) {
    const name = feature?.properties?.name;
    layer.on({
      click: () => {
        const match = findMatch(name);
        setSelected(match || { name, level: "No data", alert: "No advisory data available" });
      },
      mouseover: (e) => { e.target.setStyle({ fillOpacity: 0.9, weight: 2 }); },
      mouseout: (e) => { e.target.setStyle({ fillOpacity: 0.7, weight: 1 }); }
    });
  }

  return (
    <div style={{ height: "100vh", width: "100vw", position: "relative" }}>
      <div style={{ position: "absolute", top: 0, left: 0, right: 0, zIndex: 1000, background: "#1a1a2e", color: "white", padding: "10px 20px", display: "flex", alignItems: "center" }}>
        <h1 style={{ margin: 0, fontSize: 18 }}>🗺️ Global Travel Risk Map</h1>
        <span style={{ marginLeft: 20, fontSize: 12, color: "#aaa" }}>Source: FCDO</span>
      </div>
      <MapContainer center={[20, 0]} zoom={2} style={{ height: "100%", width: "100%", paddingTop: 40 }}>
        <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
        {geoData && advisories.length > 0 && (
          <GeoJSON
            key={advisories.length}
            data={geoData}
            style={f => ({ fillColor: getColor(f), weight: 1, color: "white", fillOpacity: 0.7 })}
            onEachFeature={onEachFeature}
          />
        )}
      </MapContainer>
      {selected && (
        <div style={{ position: "absolute", bottom: 30, left: 30, zIndex: 1000, background: "white", padding: 20, borderRadius: 8, boxShadow: "0 2px 10px rgba(0,0,0,0.3)", minWidth: 280 }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
            <h3 style={{ margin: 0 }}>{selected.name}</h3>
            <button onClick={() => setSelected(null)} style={{ border: "none", background: "none", cursor: "pointer", fontSize: 18 }}>×</button>
          </div>
          <div style={{ marginTop: 10, padding: "8px 12px", borderRadius: 4, background: LEVEL_COLORS[selected.level] || "#eee", color: "white", fontWeight: "bold" }}>
            {LEVEL_LABELS[selected.level] || selected.level}
          </div>
          <p style={{ margin: "10px 0 0", color: "#666", fontSize: 12 }}>{selected.alert}</p>
          {selected.url && <a href={selected.url} target="_blank" rel="noreferrer" style={{ display: "block", marginTop: 10, color: "#0066cc" }}>View FCDO advice →</a>}
        </div>
      )}
      <div style={{ position: "absolute", top: 50, right: 10, zIndex: 1000, background: "white", padding: 15, borderRadius: 8, boxShadow: "0 2px 10px rgba(0,0,0,0.3)" }}>
        <strong style={{ fontSize: 13 }}>Risk Level</strong>
        {Object.entries(LEVEL_COLORS).map(([l, c]) => (
          <div key={l} style={{ display: "flex", alignItems: "center", marginTop: 6 }}>
            <div style={{ width: 16, height: 16, background: c, marginRight: 8, borderRadius: 2 }} />
            <span style={{ fontSize: 12 }}>{LEVEL_LABELS[l]}</span>
          </div>
        ))}
        <div style={{ display: "flex", alignItems: "center", marginTop: 6 }}>
          <div style={{ width: 16, height: 16, background: "#cccccc", marginRight: 8, borderRadius: 2 }} />
          <span style={{ fontSize: 12 }}>No data</span>
        </div>
      </div>
    </div>
  );
}