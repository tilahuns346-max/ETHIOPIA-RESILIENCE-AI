import React from 'react';

export const AlertManagementPage: React.FC = () => {
  return (
    <div className="p-8 bg-slate-950 min-h-screen text-slate-100">
      <h2 className="text-2xl font-bold mb-2">የቅድመ ማስጠንቀቂያ ማጽደቂያ ኮንሶል (Early Warning Approval)</h2>
      <p className="text-sm text-red-400 mb-6 font-semibold">⚠️ SAFETY INVARIANT: የመንግስት አዛዥ ዲጂታል ፊርማ ብቻ ማስጠንቀቂያን ያጸድቃል።</p>
      <div className="bg-slate-900 border border-slate-800 p-6 rounded-xl">
        <p className="text-sm text-slate-300">ማስጠንቀቂያዎችን በይፋ ለማሰራጨት የኮሚሽነሩን ዲጂታል ፊርማ ያስገቡ።</p>
      </div>
    </div>
  );
};
