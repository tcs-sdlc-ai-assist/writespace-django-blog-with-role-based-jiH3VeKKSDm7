from django import template
from django.utils.html import format_html

register = template.Library()


@register.simple_tag
def render_avatar(user, size="md"):
    size_classes = {
        "sm": "w-8 h-8 text-sm",
        "md": "w-10 h-10 text-base",
        "lg": "w-14 h-14 text-xl",
    }

    classes = size_classes.get(size, size_classes["md"])

    if user.is_staff:
        emoji = "👑"
        bg_classes = "bg-purple-100 text-purple-700 border-purple-300"
    else:
        emoji = "📖"
        bg_classes = "bg-blue-100 text-blue-700 border-blue-300"

    return format_html(
        '<span class="{} {} inline-flex items-center justify-center '
        'rounded-full border-2 flex-shrink-0" title="{}">'
        '{}</span>',
        classes,
        bg_classes,
        user.get_full_name() or user.username,
        emoji,
    )