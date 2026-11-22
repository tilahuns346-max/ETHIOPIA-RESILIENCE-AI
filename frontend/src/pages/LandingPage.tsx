import React from 'react';

export const LandingPage: React.FC = () => {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col">
      <main className="flex-1 max-w-7xl mx-auto px-6 py-12">
        <div className="text-center py-16">
          <span className="inline-block px-3 py-1 bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 rounded-full text-xs font-semibold mb-4">
            የኢትዮጵያ አደጋ ስጋት ስራ አመራር ኮሚሽን (EDRMC)
          </span>
          <h1 className="text-5xl font-extrabold tracking-tight text-white mb-6">
            ETHIOPIA RESILIENCE AI
          </h1>
          <p className="text-xl text-slate-300 max-w-3xl mx-auto mb-8">
            ብሔራዊ የአደጋ ቅድመ ማስጠንቀቂያ፣ የማህበረሰብ ሪፖርት እና የአደጋ ጊዜ ፈጣን ምላሽ ቅንጅት ቴክኖሎጂ
          </p>
        </div>
      </main>
    </div>
  );
};
