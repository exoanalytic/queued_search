import logging

from django.conf import settings
from haystack import site
from celery.decorators import task
from queued_search import utils

logger = logging.getLogger(__name__)

@task(ignore_result=True)
def add_to_index(obj_identifier, **kwargs):
    object_path, pk = utils.split_obj_identifier(obj_identifier)
    model_class = utils.get_model_class(object_path)
    instance = model_class.objects.get(pk=pk)

    index = site.get_index(model_class)

    try:
        import xapian
        # work around the single-writer issue in Xapian
        try:
            index.backend.update(index, [instance])
        except xapian.DatabaseLockError, e:
            retries_remaining = add_to_index.max_retries - kwargs['task_retries']
            logger.warn("Got DatabaseLockError, will retry %s times", retries_remaining)
            add_to_index.retry(exc=e)

    except ImportError:
        index.backend.update(index, [instance])

@task(ignore_result=True)
def delete_from_index(obj_identifier, **kwargs):
    object_path, pk = utils.split_obj_identifier(obj_identifier)
    model_class = utils.get_model_class(object_path)

    index = site.get_index(model_class)
    index.remove_object(obj_identifier)
