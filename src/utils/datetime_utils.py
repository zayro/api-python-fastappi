from datetime import datetime, timedelta
from datetime import datetime, timedelta
from email.utils import formatdate

# Example
# timedelta(days=270, hours=9, minutes=18)


def formatdate_timestime_now():
    """Devuelve la fecha y hora actuales en formato RFC 2822."""
    return formatdate(timeval=None, localtime=False, usegmt=True)


def time_to_miliseconds(**kwargs):
    """Convertir un tiempo en milisegundos."""
    set_time = timedelta(**kwargs)
    return round(set_time.total_seconds() * 1000)


def time_print():
    """Imprimir la fecha y hora actuales."""
    current_date_and_time = datetime.now()
    print(
        "The current year is ", current_date_and_time.year
    )  # Output: The current year is  2022
    print(
        "The current month is ", current_date_and_time.month
    )  # Output: The current month is  3
    print(
        "The current day is ", current_date_and_time.day
    )  # Output: The current day is  19
    print(
        "The current hour is ", current_date_and_time.hour
    )  # Output: The current hour is  10
    print(
        "The current minute is ", current_date_and_time.minute
    )  # Output: The current minute is  49
    print(
        "The current second is ", current_date_and_time.second
    )  # Output: The current second is  18


# convert from datetime to timestamp
# rs = datetime.timestamp(datetime.now())

# convert the timestamp to a datetime object in the local timezone
# dt_object = datetime.fromtimestamp(timestamp)


def convert_timestamp_to_date(sec: int):
    """Convertir un valor de tiempo en segundos a una cadena de tiempo en formato HH:MM:SS."""
    sec = sec % (24 * 3600)
    hour = sec // 3600
    sec %= 3600
    min = sec // 60
    sec %= 60
    print("seconds value in hours:", hour)
    print("seconds value in minutes:", min)
    return "%02d:%02d:%02d" % (hour, min, sec)


def get_difference_in_minutes(start_date, end_date):
    """
    Esta función devuelve la diferencia en minutos entre dos fechas.

    Args:
      start_date: La fecha de inicio.
      end_date: La fecha de finalización.

    Returns:
      La diferencia en minutos entre las dos fechas.
    """

    # Obtenga la diferencia en segundos entre las dos fechas.
    difference_in_seconds = (end_date - start_date).total_seconds()

    # Devuelva la diferencia en minutos.
    return difference_in_seconds // 60


def current_utc_time() -> datetime:
    """Devuelve el tiempo actual en UTC."""
    return datetime.now()


def add_timedelta_to_current_time(hours: int) -> datetime:
    """Agrega un número específico de horas al tiempo actual UTC."""
    return current_utc_time() + timedelta(hours=hours)
