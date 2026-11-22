export class OfflineSyncQueue {
  async processQueue(isOnline: boolean) {
    if (!isOnline) return { processed: 0, status: "OFFLINE" };
    return { processed: 1, status: "SYNCED" };
  }
}
