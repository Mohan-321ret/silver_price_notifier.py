from plyer import notification
import time

notification.notify(
    title="Silver Alert Test",
    message="This is a test notification from Plyer.",
    timeout=5
)

time.sleep(5)
