import React from 'react';

export const BroadcastModal: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 p-6 rounded-xl text-slate-100">
      <h3 className="text-lg font-bold mb-2">የብዙ-ቻናል አደጋ ስርጭት (Multi-Channel Emergency Broadcast)</h3>
      <ul className="text-sm space-y-1 text-slate-400">
        <li>• ኢትዮ ቴሌኮም SMS Cell Broadcast (Geo-fenced)</li>
        <li>• የሞባይል አደጋ ሳይረን (Mobile Siren Alarm)</li>
        <li>• የሬዲዮ እና ቴሌቪዥን ማሰራጫ ኤፒአይ (Radio Bulletin API)</li>
      </ul>
    </div>
  );
};
