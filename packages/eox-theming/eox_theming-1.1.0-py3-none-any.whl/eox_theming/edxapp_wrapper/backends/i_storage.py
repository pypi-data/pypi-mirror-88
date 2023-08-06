"""
Simple backend that returns the platform's SiteTheme model
"""
from openedx.core.djangoapps.theming.storage import (  # pylint: disable=import-error
    ThemeCachedFilesMixin,
    ThemePipelineMixin,
    ThemeStorage,
)
from openedx.core.storage import PipelineForgivingStorage  # pylint: disable=import-error
from require.storage import OptimizedFilesMixin  # pylint: disable=import-error


def get_theme_storage():
    """Return the ThemeStorage class when called during runtime"""
    return ThemeStorage


def get_themecached_mixin():
    """Return the ThemeCached mixin when called during runtime"""
    return ThemeCachedFilesMixin


def get_themepipeline_mixin():
    """Return the Theme pipeline mixin when called during runtime"""
    return ThemePipelineMixin


def get_pipeline_forgiving_storage():
    """Return PipelineForgivingStorage when called during runtime"""
    return PipelineForgivingStorage


class ProductionMixinI(
        PipelineForgivingStorage,
        OptimizedFilesMixin,
        ThemeCachedFilesMixin,
):
    """
    This class offers support for Ironwood version.

    Combines several mixins that provide additional functionality.
    We use this version on production.
    """


def get_production_mixin():
    """Return ProductionMixin when called during runtime"""
    return ProductionMixinI
