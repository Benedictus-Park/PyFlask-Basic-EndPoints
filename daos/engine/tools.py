from datetime import datetime, timedelta, timezone

def now(after_days:int = None) -> datetime:
    KST = timezone(timedelta(hours=9))
    if after_days == None:
        return datetime.now(tz=KST)
    else:
        return datetime.now(tz=KST) + timedelta(days=after_days)