from flask_apscheduler import APScheduler

class SchedulerConfig:
    def __init__(self, wa):
        self.scheduler = APScheduler()
        self.wa = wa

        # Agendar a tarefa de envio de resumos diários
        self.scheduler.add_job(
            func=self.send_daily_summaries,
            trigger='interval',
            seconds=60,  # Ajuste conforme necessário
            id='send_daily_summaries',
            replace_existing=True,
        )

    def init_app(self, app):
        self.scheduler.init_app(app)
        self.scheduler.start()

    def send_daily_summaries(self):
        pass