import time

import apprise
import schedule
from apprise import NotifyType


def main():
    app_object = apprise.Apprise()
    notification_target = (
        "gnome://"  # see https://pypi.org/project/apprise/#desktop-notifications
    )
    app_object.add(notification_target)

    blue = NotifyType.INFO
    green = NotifyType.SUCCESS
    yellow = NotifyType.WARNING
    red = NotifyType.FAILURE

    _startup_notify(app_object, blue)

    green_times = [
        "21:00",
        "22:00",
        "22:30",
    ]
    yellow_times = [
        "23:00",
        "23:30",
        "00:00",
        "00:30",
        "00:45",
    ]
    red_times = [
        "01:00",
        "01:15",
        "01:30",
        "01:45",
        "02:00",
        "02:15",
        "02:30",
        "02:45",
        "03:00",
    ]

    for alert_time in green_times:
        schedule.every().day.at(alert_time).do(
            _time_notify, app_object=app_object, notification_type=green
        )
    for alert_time in yellow_times:
        schedule.every().day.at(alert_time).do(
            _time_notify, app_object=app_object, notification_type=yellow
        )
    for alert_time in red_times:
        schedule.every().day.at(alert_time).do(
            _time_notify, app_object=app_object, notification_type=red
        )

    while True:
        schedule.run_pending()
        time.sleep(5)


def _startup_notify(app_object: apprise.Apprise, notification_type: NotifyType):
    """Creates notification on script startup"""
    app_object.notify(
        body="happy fun bed time yeller started",
        title="start up successful",
        notify_type=notification_type,
    )


def _time_notify(app_object: apprise.Apprise, notification_type: NotifyType):
    """Creates notifications at set times with green->yellow->red urgency"""
    current_time = time.strftime("%H:%M", time.localtime())
    app_object.notify(
        body=f"it's {current_time}",
        title=f"{current_time} warning",
        notify_type=notification_type,
    )


if __name__ == "__main__":
    main()
