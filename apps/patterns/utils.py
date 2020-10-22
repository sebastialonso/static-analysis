import arrow


def epoch_to_date_string(epoch: int) -> str:
    return arrow.get(epoch).format('YYYY-MM-DD')


def epoch_to_datetime_string(epoch: int) -> str:
    return arrow.get(epoch).format('YYYY-MM-DD HH:mm:SS')