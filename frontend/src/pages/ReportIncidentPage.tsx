import React, { useState } from 'react';

export const ReportIncidentPage: React.FC = () => {
  const [hazard, setHazard] = useState("HAZ-LANDSLIDE");
  const [desc, setDesc] = useState("");

  return (
    <div className="max-w-3xl mx-auto p-8 bg-slate-950 text-slate-100">
      <h2 className="text-2xl font-bold mb-4">አደጋ ሪፖርት ማድረጊያ (Community Hazard Report)</h2>
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-4">
        <div>
          <label className="block text-sm font-medium mb-1">የአደጋው አይነት (Hazard Type)</label>
          <select value={hazard} onChange={e => setHazard(e.target.value)} className="w-full bg-slate-800 border border-slate-700 rounded-lg p-2.5">
            <option value="HAZ-LANDSLIDE">የመሬት መንሸራተት / ናዳ (Landslide)</option>
            <option value="HAZ-FLASH-FLOOD">ድንገተኛ ጎርፍ (Flash Flood)</option>
            <option value="HAZ-DROUGHT">ድርቅ (Drought)</option>
          </select>
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">ዝርዝር ማብራሪያ (Description)</label>
          <textarea rows={4} value={desc} onChange={e => setDesc(e.target.value)} className="w-full bg-slate-800 border border-slate-700 rounded-lg p-2.5" />
        </div>
        <button className="w-full py-3 bg-emerald-600 hover:bg-emerald-700 text-white font-bold rounded-lg">ሪፖርት ላክ (Submit)</button>
      </div>
    </div>
  );
};
