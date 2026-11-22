import React from 'react';

export const Navbar: React.FC<{ currentLang: string; onLanguageChange: (lang: string) => void }> = ({ currentLang, onLanguageChange }) => {
  return (
    <header className="bg-slate-900 text-white px-6 py-4 flex justify-between items-center shadow-md">
      <div className="flex items-center space-x-3">
        <div className="w-10 h-10 rounded-full bg-emerald-600 flex items-center justify-center font-bold text-lg">🇪🇹</div>
        <div>
          <h1 className="text-xl font-bold tracking-wide">ETHIOPIA RESILIENCE AI</h1>
          <p className="text-xs text-slate-400">የኢትዮጵያ አደጋ ቅድመ ማስጠንቀቂያና ምላሽ መድረክ</p>
        </div>
      </div>
      <div className="flex items-center space-x-4">
        <select
          value={currentLang}
          onChange={(e) => onLanguageChange(e.target.value)}
          className="bg-slate-800 border border-slate-700 rounded-md px-3 py-1.5 text-sm text-slate-200"
        >
          <option value="am">አማርኛ (Amharic)</option>
          <option value="en">English (English)</option>
          <option value="om">Afaan Oromoo</option>
          <option value="ti">ትግርኛ (Tigrinya)</option>
        </select>
        <span className="text-xs px-2.5 py-1 bg-red-900/60 border border-red-500/50 text-red-300 rounded font-mono">
          EDRMC LIVE GATEWAY
        </span>
      </div>
    </header>
  );
};
