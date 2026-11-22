import React from 'react';

export const ResponseTeamPage: React.FC = () => {
  return (
    <div className="p-8 bg-slate-950 min-h-screen text-slate-100">
      <h2 className="text-2xl font-bold mb-4">የአደጋ ምላሽ ሰጪ ቡድኖች ስምሪት (Emergency Response Logistics)</h2>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-slate-900 border border-slate-800 p-4 rounded-xl">
          <h4 className="font-bold text-emerald-400">የኢትዮጵያ ቀይ መስቀል ማህበር</h4>
          <p className="text-xs text-slate-400 mt-1">የህክምና እና የድንገተኛ ረዳት ቡድን</p>
        </div>
      </div>
    </div>
  );
};
