from sqlalchemy.orm import Session
from app.db.factories.user_preference_factory import UserPreferenceFactory


def test_user_address_factory_create(db_session: Session, create_user):
    user = create_user()
    preference = UserPreferenceFactory.create(
        db_session,
        user_id=user.id,
        preference_type="Test Preference Type",
        preference_value="Pref Value"
    )
    assert preference.preference_type == "Test Preference Type"
    assert preference.preference_value == "Pref Value"
    assert preference.user_id == user.id


def test_user_address_factory_batch_create(db_session: Session):
    roles = UserPreferenceFactory.batch_create(
        db_session,
        size=5
    )
    assert len(roles) == 5