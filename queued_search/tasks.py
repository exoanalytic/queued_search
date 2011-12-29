import logging

from haystack import site
from celery.decorators import task
from queued_search import utils


logger = logging.getLogger(__name__)


@task(ignore_result=True, max_retries=2, default_retry_delay=3600)
def add_to_index(obj_identifier, **kwargs):
    object_path, pk = utils.split_obj_identifier(obj_identifier)
    model_class = utils.get_model_class(object_path)
    try:
        instance = model_class.objects.get(pk=pk)
    except model_class.DoesNotExist, exc:
        retries_remaining = add_to_index.max_retries - kwargs['task_retries']
        logger.warn("Could not find %s with pk=%s, will retry %d more times", model_class.__name__, pk,
                    retries_remaining)
        add_to_index.retry(exc=exc)

    index = site.get_index(model_class)
    index.backend.update(index, [instance])

@task(ignore_result=True)
def delete_from_index(obj_identifier, **kwargs):
    object_path, pk = utils.split_obj_identifier(obj_identifier)
    model_class = utils.get_model_class(object_path)

    index = site.get_index(model_class)
    index.remove_object(obj_identifier)
