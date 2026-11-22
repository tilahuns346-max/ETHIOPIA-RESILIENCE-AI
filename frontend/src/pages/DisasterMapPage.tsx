import React from 'react';

export const DisasterMapPage: React.FC = () => {
  return (
    <div className="p-6 bg-slate-950 min-h-screen text-slate-100 flex flex-col">
      <h2 className="text-2xl font-bold mb-4">የኢትዮጵያ አደጋ ስጋት ካርታ (Disaster Risk Map)</h2>
      <div className="flex-1 bg-slate-900 border border-slate-800 rounded-xl relative overflow-hidden flex items-center justify-center min-h-[500px]">
        <div className="text-center p-8">
          <p className="text-lg font-semibold text-slate-300">🗺️ የኢትዮጵያ የካርታ ንብርብሮች (GIS Layers Loaded)</p>
          <p className="text-sm text-slate-500 mt-2">ጎፋ (Kencho Shacha) • ቦረና (ያቤሎ) • አዋሽ ፈንታሌ • መርካቶ</p>
        </div>
      </div>
    </div>
  );
};
