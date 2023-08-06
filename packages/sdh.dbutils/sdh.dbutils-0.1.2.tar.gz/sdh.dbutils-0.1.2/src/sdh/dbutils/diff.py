

def update_diff(instance, **kwargs):
    need_save = False

    for key, value in kwargs.items():
        field = getattr(instance, key)
        if field != value:
            setattr(instance, key, value)
            need_save = True

    if need_save:
        instance.save()
    return need_save
