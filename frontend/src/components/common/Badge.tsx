import React from 'react';

export const Badge: React.FC<{ label: string; severity?: string }> = ({ label, severity = 'low' }) => {
  const styles: Record<string, string> = {
    LEVEL_4_CRITICAL: "bg-red-100 text-red-800 border-red-300",
    LEVEL_3_HIGH: "bg-orange-100 text-orange-800 border-orange-300",
    LEVEL_2_MODERATE: "bg-amber-100 text-amber-800 border-amber-300",
    LEVEL_1_LOW: "bg-emerald-100 text-emerald-800 border-emerald-300"
  };
  return (
    <span className={`px-2.5 py-0.5 rounded-full text-xs font-semibold border ${styles[severity] || styles.LEVEL_1_LOW}`}>
      {label}
    </span>
  );
};
