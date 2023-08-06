import logging

# import pyximport
# pyximport.install()

from ...permissions import is_django_staff
from ... import app_settings
from .models import Profile as Profile

logger = logging.getLogger('django_sso_app.core.apps.profiles')


def update_profile(profile, update_object, commit=True):
    logger.info('Updating profile fields for "{}"'.format(profile))

    for f in app_settings.PROFILE_FIELDS + ('sso_rev', 'meta'):
        if hasattr(profile, f):
            new_val = update_object.get(f, None)
            if new_val is not None:
                setattr(profile, f, new_val)
                logger.debug('profile field updated "{}":"{}"'.format(f, new_val if f != 'password' else '*'))

    if commit:
        profile.save()

    return profile


def get_or_create_user_profile(user, initials=None, commit=True):
    logger.debug('get or create user profile')

    try:
        profile = user.sso_app_profile

    except Profile.DoesNotExist:
        logger.info('User "{}" has no profile, creating one'.format(user))

        profile = Profile(user=user, django_user_email=user.email, django_user_username=user.username)

        sso_id = getattr(user, '__dssoa__profile__sso_id', None)
        if sso_id is not None:
            sso_rev = getattr(user, '__dssoa__profile__sso_rev', 0)
            profile.sso_id = sso_id
            profile.sso_rev = sso_rev
        else:
            # django staff users sso_id equals username
            if is_django_staff(user):
                profile.sso_id = user.username
                profile.sso_rev = 0

                setattr(user, '__dssoa__creating', True)

                profile.save()

        profile_initials = initials or getattr(user, '__dssoa__profile__object', None)

        if profile_initials is not None:
            logger.debug('Got profile initials "{}"'.format(profile_initials))
            profile = update_profile(profile, profile_initials, commit=False)
        else:
            logger.debug('No profile initials')

        if commit:
            profile.save()

    # force user sso_app_profile object field
    setattr(user, 'sso_app_profile', profile)

    return profile
