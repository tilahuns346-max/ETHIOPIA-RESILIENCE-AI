import React, { useState } from 'react';

export const LoginPage: React.FC<{ onLoginSuccess: (token: string, user: any) => void }> = ({ onLoginSuccess }) => {
  const [phone, setPhone] = useState("+251911000002");
  const [password, setPassword] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onLoginSuccess("mock_token", { full_name: "Dr. Senait Hailemariam", role: "NATIONAL_EDRMC_OFFICER" });
  };

  return (
    <div className="min-h-screen bg-slate-900 flex items-center justify-center p-6">
      <div className="bg-slate-800 border border-slate-700 rounded-xl p-8 max-w-md w-full shadow-2xl">
        <h2 className="text-2xl font-bold text-white mb-2 text-center">መግቢያ (Officer Login)</h2>
        <form onSubmit={handleSubmit} className="space-y-4 mt-6">
          <div>
            <label className="block text-xs font-medium text-slate-400 mb-1">ስልክ ቁጥር (Phone)</label>
            <input type="text" value={phone} onChange={e => setPhone(e.target.value)} className="w-full bg-slate-900 border border-slate-700 rounded-lg p-2.5 text-white" />
          </div>
          <div>
            <label className="block text-xs font-medium text-slate-400 mb-1">የይለፍ ቃል (Password)</label>
            <input type="password" value={password} onChange={e => setPassword(e.target.value)} className="w-full bg-slate-900 border border-slate-700 rounded-lg p-2.5 text-white" />
          </div>
          <button type="submit" className="w-full py-3 bg-emerald-600 hover:bg-emerald-700 text-white font-semibold rounded-lg">ይግቡ</button>
        </form>
      </div>
    </div>
  );
};
