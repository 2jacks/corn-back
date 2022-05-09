from accounts.models import User


def user_directory_path(instance, filename):
    user = User.objects.get(id=instance.field.owner_id)
    return 'users/{0}/{1}'.format(user.username, filename)


def user_field_path(instance, filename):
    return 'users/{0}/fields/{1}/{2}'.format(instance.field_id.owner_id, instance.field_id, filename)


def user_research_path(instance, filename):
    user = User.objects.get(id=instance.field.owner_id)
    return 'users/{0}/fields/{1}/researches/{2}/{3}'.format(user.username, instance.field.id, instance.date, filename)


def user_indexes_path(instance, filename):
    research = instance.research
    user = User.objects.get(id=research.field.owner_id)
    return 'users/{0}/fields/{1}/researches/{2}/indexes/{3}'.format(user.username, research.field.id, research.date, filename)