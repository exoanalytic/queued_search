from django.db.models.loading import get_model

def split_obj_identifier(obj_identifier):
    """
    Break down the identifier representing the instance.
    
    Converts 'notes.note.23' into ('notes.note', 23).
    """
    bits = obj_identifier.split('.')
    
    if len(bits) < 2:
        return (None, None)
    
    pk = bits[-1]
    # In case Django ever handles full paths...
    object_path = '.'.join(bits[:-1])
    return (object_path, pk)

def get_model_class(object_path):
    """Fetch the model's class in a standarized way."""
    bits = object_path.split('.')
    app_name = '.'.join(bits[:-1])
    classname = bits[-1]
    model_class = get_model(app_name, classname)
    
    return model_class
