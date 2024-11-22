import pytest
from app.crud.user_preference import (
    get_all_user_preferences,
    get_user_preference,
    get_user_preferences_from_user_id,
    create_user_preference,
    update_user_preference,
    update_user_preference_with_user_id,
    delete_user_preference
)
from app.models.user_preferences import UserPreference
from app.schemas.user_preference import UserPreferenceCreate, UserPreferenceUpdate


def test_get_all_user_preferences(db_session, batch_create_preferences):
    batch_create_preferences(10)

    preferences = get_all_user_preferences(db_session)

    assert len(preferences) == 10


def test_get_user_preference(db_session, create_preference):
    test_pref = create_preference(
        preference_id=150
    )

    preference = get_user_preference(db_session, test_pref.preference_id)

    assert preference.preference_id == 150


def test_get_user_preferences_from_user_id(db_session, create_user, batch_create_preferences):
    test_user = create_user(
        id=55
    )

    batch_create_preferences(
        3,
        preference_type="Pref Type",
        preference_value="Pref Val",
        user_id=test_user.id
    )

    retrieved_preferences = get_user_preferences_from_user_id(db_session, test_user.id)

    assert len(retrieved_preferences) == 3

    for pref in retrieved_preferences:
        assert pref.preference_type == "Pref Type"
        assert pref.preference_value == "Pref Val"


def test_create_user_preference(db_session, create_user):
    test_user = create_user(
        id=56
    )

    creating_pref = UserPreferenceCreate(
        user_id=test_user.id,
        preference_type="Pref Type Created",
        preference_value="Pref Type Value"
    )

    created_pref = create_user_preference(db_session, creating_pref)

    assert created_pref.user_id == test_user.id
    assert created_pref.preference_type == "Pref Type Created"
    assert created_pref.preference_value == "Pref Type Value"


def test_update_user_preference(db_session, create_preference):
    test_pref = create_preference(
        preference_id=40,
        preference_type="Replace Type",
        preference_value="Replace Val"
    )

    pref_update = UserPreferenceUpdate(
        preference_type="New Type",
        preference_value="New Val"
    )

    updated_pref = update_user_preference(db_session, test_pref.preference_id, pref_update)

    assert updated_pref.preference_type == "New Type"
    assert updated_pref.preference_value == "New Val"


def test_update_user_preference_not_found(db_session):
    pref_update = UserPreferenceUpdate(
        preference_type="New Type",
        preference_value="New Val"
    )

    with pytest.raises(ValueError) as exec_info:
        update_user_preference(db_session, 678, pref_update)
    
    assert exec_info.value.args[0] == "Preference not found."


def test_update_user_preference_with_user_id(db_session, create_user, create_preference, batch_create_preferences):
    test_user = create_user(
        id=70
    )

    batch_create_preferences(
        2,
        user_id=test_user.id
    )
    
    test_pref = create_preference(
        preference_id=68,
        user_id=test_user.id,
        preference_type="Replace Type",
        preference_value="Replace Val"
    )

    pref_update = UserPreferenceUpdate(
        preference_type="New Type",
        preference_value="New Val"
    )

    updated_pref = update_user_preference_with_user_id(db_session, test_pref.preference_id, test_user.id, pref_update)

    assert updated_pref.preference_type == "New Type"
    assert updated_pref.preference_value == "New Val"


def test_update_user_preference_with_user_id_not_found(db_session):
    pref_update = UserPreferenceUpdate(
        preference_type="New Type",
        preference_value="New Val"
    )

    with pytest.raises(ValueError) as exec_info:
        update_user_preference_with_user_id(db_session, 23, 78, pref_update)
    
    assert exec_info.value.args[0] == "Preference not found."


def test_delete_user_preference(db_session, create_preference):
    test_pref = create_preference(
        preference_id=45,
        preference_type="Deleted Type",
        preference_value="Deleted Val"
    )

    delete_user_preference(db_session, test_pref.preference_id)
    db_session.commit()

    deleted_preference = db_session.query(UserPreference).filter(
        UserPreference.preference_id == 45
    ).first()

    assert deleted_preference is None


def test_delete_user_preference_not_found(db_session):
    with pytest.raises(ValueError) as exec_info:
        delete_user_preference(db_session, 60)

    assert exec_info.value.args[0] == "Preference not found."
