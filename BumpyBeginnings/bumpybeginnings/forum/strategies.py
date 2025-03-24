from .models import Comment, Post, Forum, Vote
from hypothesis.strategies import text, composite, integers, booleans, characters
from hypothesis import strategies as st
from users.strategies import user_strategy
from django.db import IntegrityError
from hypothesis import  assume
from notifications.models import Notification
import string


@composite
def unique_username_strategy(draw):
    # start with a non-empty/none null string
    base = draw(text(characters(blacklist_characters='\x00'), min_size=1, max_size=10))
    # append a unique integer to the base string
    unique_int = draw(integers(min_value=0, max_value=100000))
    return f"{base}_{unique_int}"

@composite
def unique_forum_name_strategy(draw):
    # start with a non-empty/none null string
    base = draw(text(characters(blacklist_characters='\x00'), min_size=1, max_size=10))
    # can be longer than the username due to the length diffrences
    unique_int = draw(integers(min_value=0, max_value=10**6))
    return f"{base}_{unique_int}"

# strategy for creating forum examples
@composite
def forum_strategy(draw):
    forum_name = draw(unique_forum_name_strategy())
    description = draw(
        text(characters(blacklist_characters='\x00'), min_size=1, max_size=500)
    )
    is_live = draw(booleans())
    try:
        return Forum.objects.create(
            forumName=forum_name,
            description=description,
            isLive=is_live
        )
    except IntegrityError:
        assume(False) 

# strategy for creating post examples
@composite
def post_strategy(draw, forum=None, poster=None):
    if forum is None:
        forum = draw(forum_strategy())
    if poster is None:
        poster = draw(user_strategy)
    post_title = draw(
        text(characters(blacklist_characters='\x00'), min_size=1, max_size=255)
    )
    post_text = draw(
        text(characters(blacklist_characters='\x00'), min_size=1, max_size=500)
    )
    is_active = draw(st.booleans())
    return Post.objects.create(
        forum=forum,
        poster=poster,
        postTitle=post_title,
        postText=post_text,
        isActive=is_active
    )

# strategy for creating comment examples
@composite
def comment_strategy(draw, post=None, commenter=None):
    if post is None:
        post = draw(post_strategy())
    if commenter is None:
        commenter = draw(user_strategy)
    comment_text = draw(
        text(characters(blacklist_characters='\x00'), min_size=1, max_size=500)
    )
    score = draw(st.integers(min_value=-10, max_value=10))
    return Comment.objects.create(
        post=post,
        commenter=commenter,
        commentText=comment_text,
        score=score
    )



# strategy for creating Votes
@composite
def vote_strategy(draw, user=None, comment=None):
    if user is None:
        user = draw(user_strategy)
    if comment is None:
        comment = draw(comment_strategy())
    vote_type = draw(st.sampled_from(["upvote", "downvote"]))
    return Vote.objects.create(
        user=user,
        comment=comment,
        vote_type=vote_type
    )

# strategy for creating a Notifications
@composite
def notification_strategy(draw, recipient=None):
    if recipient is None:
        recipient = draw(user_strategy())
    notification_message = draw(st.text())
    is_read = draw(st.booleans())
    return Notification.objects.create(
        recipient=recipient,
        notification_message=notification_message,
        is_read=is_read
    )




# helper functions.
# used to quickly generate a forum (i.e. creating a post needs a forum for it to be in)
def create_unique_forum(description="Test Forum", isLive=True):
    forum_name = unique_forum_name_strategy()
    return Forum.objects.create(forumName=forum_name, description=description, isLive=isLive)

def create_post(forum, poster, postTitle="Test Title", postText="Test Text", isActive=True):
    return Post.objects.create(
        forum=forum,
        poster=poster,
        postTitle=postTitle,
        postText=postText,
        isActive=isActive
    )

def create_comment(post, commenter, commentText="Test Comment", score=0):
    return Comment.objects.create(
        post=post,
        commenter=commenter,
        commentText=commentText,
        score=score
    )

description_strategy = text(
    alphabet=string.printable,
    min_size=0,
    max_size=255
)
