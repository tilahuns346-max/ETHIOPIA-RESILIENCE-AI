class PushNotificationDispatcher:
    def send_emergency_siren(self, woreda_code: str, alert_title: str) -> dict:
        return {
            "priority": "HIGH",
            "sound": "emergency_siren_alarm.wav",
            "vibrate": [1000, 500, 1000, 500],
            "channel": "EDRMC_CRITICAL_ALERTS",
            "title": alert_title,
            "target_woreda": woreda_code
        }

push_dispatcher = PushNotificationDispatcher()
