import random
import string

from django.utils.text import slugify
from rest_framework.pagination import PageNumberPagination


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_slug_generator(instance, new_slug=None):
    """
    This is for a Django project and it assumes your instance
    has a model with a slug field and a title character (char) field.

    slug_name = None
    if instance.name:
        slug_name = instance.name
    elif instance.title:
        slug_name = instance.title
    elif instance.first_name:
        slug_name = instance.first_name
    elif instance.title1:
        slug_name = instance.title1
    """
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
            slug=slug,
            randstr=random_string_generator(size=7)
        )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug


def unique_slug_question_generator(instance, new_slug=None):
    """
    This is for a Django project and it assumes your instance
    has a model with a slug field and a title character (char) field.
    """
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.question.slug)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
            slug=slug,
            randstr=random_string_generator(size=7)
        )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug


def unique_slug_generator_user_profile(instance, new_slug=None):

    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.user.slug)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
            slug=slug,
            randstr=random_string_generator(size=7)
        )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug


def unique_slug_generator_invention(instance, new_slug=None):
    """
    This is for a Django project and it assumes your instance
    has a model with a slug field and a title character (char) field.
    """
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.project_title)
        new_slugger = "{slug}-{randstr}".format(
            slug=slug,
            randstr=random_string_generator(size=7)
        )
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=new_slugger).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
            slug=new_slugger,
            randstr=random_string_generator(size=7)
        )
        return unique_slug_generator(instance, new_slug=new_slug)
    return new_slugger


def unique_slug_generator_invention_slug(instance, new_slug=None):
    """
    This is for a Django project and it assumes your instance
    has a model with a slug field and a title character (char) field.
    """
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.invention.slug)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
            slug=slug,
            randstr=random_string_generator(size=7)
        )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 10000
    page_size_query_param = 'page_size'
    max_page_size = 100000


class SmallResultsSetPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = 16


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 10000
