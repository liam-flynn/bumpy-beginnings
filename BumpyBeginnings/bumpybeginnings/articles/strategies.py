from .models import Article
from hypothesis import given, strategies as st
from hypothesis.extra.django import from_model
from hypothesis.strategies import none, just


# strategy to create test instances of articles
article_strategy = from_model(
    Article,
    # generate text atleast 1-255 charactors long and is not null 
    title=st.text(min_size=1, max_size=255)
            .filter(lambda x: x.strip() != '' and '\0' not in x),
    # subtitle can be empty but not null
    subtitle=st.text(min_size=0, max_size=255)
              .filter(lambda x: x is not None and '\0' not in x),
    # text needs to be between 1-2000. If it is only whitespaces, replace it with valid text
    text=st.text(min_size=1, max_size=2000)
        .map(lambda s: "Valid article text" if not s.strip() else s)
        .filter(lambda x: x.strip() != '' and '\0' not in x),
    source=st.one_of(none(), just("")).filter(lambda x: x is None or '\0' not in x),
    related_week=st.one_of(st.integers(min_value=1, max_value=40), none()),
    image=none(),
)