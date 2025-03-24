from .models import DevelopmentMilestone
from hypothesis import strategies as st


# strategy for creating development milestone instances
@st.composite
def development_milestone_strategy(draw):
    stage = draw(st.sampled_from(['prenatal', 'postnatal']))
    description = draw(st.text(min_size=1, max_size=200))
    if stage == 'prenatal':
        week = draw(st.integers(min_value=1, max_value=40))
        return DevelopmentMilestone(
            stage=stage,
            week=week,
            start_age_months=None,
            end_age_months=None,
            description=description,
            image=None
        )
    else:
        start_age_months = draw(st.integers(min_value=0, max_value=36))
        end_age_months = draw(st.integers(min_value=start_age_months + 1, max_value=48))
        return DevelopmentMilestone(
            stage=stage,
            week=None,
            start_age_months=start_age_months,
            end_age_months=end_age_months,
            description=description,
            image=None
        )