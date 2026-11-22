export function useAlertSound() {
  const playSiren = () => {
    if (typeof window !== 'undefined') {
      const audio = new Audio('/sounds/emergency_siren.mp3');
      audio.play().catch(() => {});
    }
  };
  return { playSiren };
}
