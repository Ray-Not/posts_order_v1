from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    'send-weekly-newsletter': {
        'task': 'newapp.tasks.send_weekly_articles',
        # 'schedule': crontab(minute=0, hour=0, day_of_week=0),
        'schedule': crontab(minute="*/1"),
    },
}
