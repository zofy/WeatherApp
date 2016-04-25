from celery.schedules import crontab
from celery.task import periodic_task
from celery.utils.log import get_task_logger

from weatherAnalyzer.analyzer import Analyzer
from weatherAnalyzer.models import User, Location
from weatherAnalyzer.sender import MailManager

logger = get_task_logger(__name__)


@periodic_task(run_every=(crontab(minute='*/1')), name="send_forecast", ignore_result=True)
def send_forecast():
    logger.info("Sending forecast to ...")
    users = User.objects.all()
    for user in users:
        email = user.email
        location = Location.objects.get(user=user)
        a = Analyzer(location.loc_dict)
        w_data = a.get_data()
        m = MailManager(str(email), str(w_data))
        m.login_to_server()
        m.send_mail()


