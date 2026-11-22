import React from 'react';

export const DashboardPage: React.FC = () => {
  const kpis = [
    { title: "ጠቅላላ ሪፖርቶች", count: "1,248", desc: "ከማህበረሰቡ የቀረቡ", color: "text-blue-400" },
    { title: "የተረጋገጡ አደጋዎች", count: "89", desc: "በወረዳ ባለሙያዎች የተረጋገጡ", color: "text-amber-400" },
    { title: "ንቁ ማስጠንቀቂያዎች", count: "4", desc: "ደረጃ 4 እና 3 ማንቂያዎች", color: "text-red-400" },
    { title: "የተሰማሩ ቡድኖች", count: "24", desc: "ቀይ መስቀል እና ማዳን", color: "text-emerald-400" },
  ];

  return (
    <div className="p-8 bg-slate-950 min-h-screen text-slate-100">
      <h2 className="text-3xl font-bold mb-6">ሀገራዊ የአደጋ ክትትል ማዕከል (National Operations Dashboard)</h2>
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        {kpis.map((kpi, idx) => (
          <div key={idx} className="bg-slate-900 border border-slate-800 p-6 rounded-xl">
            <h3 className="text-sm font-medium text-slate-400">{kpi.title}</h3>
            <p className={`text-4xl font-extrabold mt-2 ${kpi.color}`}>{kpi.count}</p>
            <p className="text-xs text-slate-500 mt-1">{kpi.desc}</p>
          </div>
        ))}
      </div>
    </div>
  );
};
