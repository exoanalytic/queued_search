from haystack import site
from celery.decorators import task
from queued_search import utils

@task(ignore_result=True)
def add_to_index(obj_identifier, **kwargs):
    object_path, pk = utils.split_obj_identifier(obj_identifier)
    model_class = utils.get_model_class(object_path)
    instance = model_class.objects.get(pk=pk)

    index = site.get_index(model_class)
    index.backend.update(index, [instance])

@task(ignore_result=True)
def delete_from_index(obj_identifier, **kwargs):
    object_path, pk = utils.split_obj_identifier(obj_identifier)
    model_class = utils.get_model_class(object_path)

    index = site.get_index(model_class)
    index.remove_object(obj_identifier)
