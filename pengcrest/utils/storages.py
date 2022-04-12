import os
from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings
from django.template.defaultfilters import slugify


class StaticRootS3Boto3Storage(S3Boto3Storage):
    location = "static"
    default_acl = "public-read"


class MediaRootS3Boto3Storage(S3Boto3Storage):
    location = "media"
    file_overwrite = False


def get_show_upload_folder(instance, pathname):
    "A standardized pathname for uploaded files and images."
    root, ext = os.path.splitext(pathname)
    return "{0}/podcasts/{1}/{2}{3}".format(
        settings.PODCASTING_IMG_PATH, instance.slug, slugify(root), ext
    )

def get_radio_upload_folder(instance, pathname):
    "A standardized pathname for uploaded files and images."
    root, ext = os.path.splitext(pathname)
    return f"{settings.PODCASTING_IMG_PATH}/radios/{instance.slug}/{slugify(root)}{ext}"



def get_episode_upload_folder(instance, pathname):
    "A standardized pathname for uploaded files and images."
    root, ext = os.path.splitext(pathname)
    if instance.podcast:
        return f"podcasts/{instance.podcast.slug}/episodes/{slugify(root)}{ext}"
    else:
        return f"podcasts/episodes/{instance.slug}/{slugify(root)}{ext}"

def get_hi_audio_upload_folder(instance, pathname):
    "A standardized pathname for uploaded files and images."
    root, ext = os.path.splitext(pathname)
    return f"podcasts/episodes/hi/{instance.slug}/{slugify(root)}{ext}"

def get_norm_audio_upload_folder(instance, pathname):
    "A standardized pathname for uploaded files and images."
    root, ext = os.path.splitext(pathname)
    return f"podcasts/episodes/norm/{instance.slug}/{slugify(root)}{ext}"

def get_lo_audio_upload_folder(instance, pathname):
    "A standardized pathname for uploaded files and images."
    root, ext = os.path.splitext(pathname)
    return f"podcasts/episodes/lo/{instance.slug}/{slugify(root)}{ext}" #{slugify(root)}{ext}
