from celery.schedules import crontab
from celery.task import periodic_task
from celery.utils.log import get_task_logger

from weatherAnalyzer.analyzer import Analyzer
from weatherAnalyzer.models import User, Location
from weatherAnalyzer.sender import MailManager

logger = get_task_logger(__name__)


@periodic_task(run_every=(crontab(minute='*/1')), name="send_forecast", ignore_result=True)
def send_forecast():
    logger.info("Sending forecast to all users...")
    users = User.objects.all()
    for user in users:
        email = user.email
        location = Location.objects.get(user=user)
        a = Analyzer(location.get_dict())
        w_data = a.get_data()
        forecast = create_message(w_data)
        m = MailManager(str(email), forecast)
        m.login_to_server()
        m.send_mail()


def create_message(data):
    result = {'sunrise': data['forecast'][1]['sunrise_time'], 'sunset': data['forecast'][1]['sunset_time'],
              'min': data['forecast'][1]['temperature_min'],
              'max': data['forecast'][1]['temperature_max'],
              'wind': data['forecast'][1]['wind_gust_max'],
              'wind_gust': data['forecast'][1]['wind_speed_max'],}
    message = 'Weather for tommorow\nSunrise: %s am, Sunset: %s pm\nMin: %s C, Max: %s C\nWind: %s km/h' % (
        result['sunrise'], result['sunset'], result['min'], result['max'], result['wind'])
    return message
