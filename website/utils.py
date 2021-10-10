from flask import flash
from .db_config import CharLimits


def validate_post(given_title, given_body):
    post_is_validated = True

    title_limits = CharLimits.post["title"]
    body_limits = CharLimits.post["body"]

    if (len(given_title) < title_limits["min"] or len(given_title) > title_limits["max"]):
        flash(f"Title must be between {title_limits['min']} and {title_limits['max']} characters long.",
            category="error")
        post_is_validated = False

    elif (len(given_body) < body_limits["min"] or len(given_body) > body_limits["max"]):
        flash(f"Body must be between {body_limits['min']} and {body_limits['max']} characters long.",
            category="error")
        post_is_validated = False

    return post_is_validated
