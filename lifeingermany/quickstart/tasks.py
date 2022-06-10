from quickstart.models import State
from celery import shared_task

@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)


@shared_task
def count_states():
    return State.objects.count()


@shared_task
def rename_state_with_code(state_code, name):
    s = State.objects.get(code=state_code)
    s.name = name
    s.save()