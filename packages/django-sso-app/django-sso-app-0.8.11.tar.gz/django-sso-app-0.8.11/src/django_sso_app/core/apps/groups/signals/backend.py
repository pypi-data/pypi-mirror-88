import logging

from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver

from .... import app_settings
from ....permissions import is_django_staff
from ...profiles.models import Profile
from ..models import Group

logger = logging.getLogger('django_sso_app.core.apps.groups.signals')


@receiver(m2m_changed, sender=Profile.groups.through)
def signal_handler_when_user_profile_is_added_or_removed_from_group(action, instance, pk_set, **kwargs):
    """
    Update sso_rev when user enter/exit groups
    """

    profile = instance
    user = profile.user

    logger.debug('Groups signal')

    is_loaddata = getattr(user, '__dssoa__loaddata', False)
    is_creating = getattr(user, '__dssoa__creating', False)
    is_entering_incomplete_group = getattr(user, '__dssoa__enter_incomplete_group', False)
    is_exiting_incomplete_group = getattr(user, '__dssoa__exit_incomplete_group', False)

    must_update_rev = (not is_loaddata) and \
                      (not is_creating) and \
                      (not is_entering_incomplete_group) and \
                      (not is_exiting_incomplete_group) and \
                      (not is_django_staff(user))

    groups_updated = False

    if action == 'pre_add':
        groups_updated = True
        for pk in pk_set:
            group = Group.objects.get(id=pk)
            logger.info('Profile "{}" entered group "{}"'.format(profile, group))

    elif action == 'pre_remove':
        groups_updated = True
        for pk in pk_set:
            group = Group.objects.get(id=pk)
            logger.info('Profile "{}" exited from group "{}"'.format(profile, group))

    # updating rev

    if groups_updated and must_update_rev:
        profile.update_rev(True)


@receiver(post_save, sender=Profile)
def user_profile_updated(sender, instance, created, **kwargs):
    """
    Profile model has been updated, check user profile completeness
    """
    profile = instance
    user = profile.user

    if kwargs['raw']:
        # https://github.com/django/django/commit/18a2fb19074ce6789639b62710c279a711dabf97
        return

    if not is_django_staff(user):
        should_manage_groups = app_settings.BACKEND_ENABLED or app_settings.REPLICATE_PROFILE

        if should_manage_groups:
            if created:  # if instance.pk:
                if profile.is_incomplete:
                    logger.debug('Profile model has been created incomplete, entering "incomplete" group')

                    setattr(profile.user, '__dssoa__enter_incomplete_group', True)

                    group, _created = Group.objects.get_or_create(name='incomplete')

                    profile.groups.add(group)
            else:
                if not profile.is_incomplete:
                    group, _created = Group.objects.get_or_create(name='incomplete')

                    if profile.groups.filter(name=group.name).count() > 0:
                        logger.debug('Profile model has been completed, exiting "incomplete" group')

                        setattr(profile.user, '__dssoa__exit_incomplete_group', True)

                        profile.groups.remove(group)

            # check profile groups
            user_object_profile = getattr(profile.user, '__dssoa__profile__object', None)

            if user_object_profile is not None:
                group_names = user_object_profile.get('groups', [])

                for group_name in group_names:
                    group, _created = Group.objects.get_or_create(name=group_name)

                    if profile.groups.filter(name=group.name).count() == 0:
                        profile.groups.add(group)
