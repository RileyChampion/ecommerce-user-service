from typing import List
from app.models.user_preferences import UserPreference
from sqlalchemy.orm import Session
from app.schemas.user_preference import UserPreferenceCreate, UserPreferenceUpdate


def get_all_user_preferences(db: Session):
    return db.query(UserPreference).all()


def get_user_preference(db: Session, preference_id: int) -> UserPreference:
    return db.query(UserPreference).filter(
        UserPreference.preference_id == preference_id
    ).first()


def get_user_preferences_from_user_id(db: Session, user_id: int) -> List[UserPreference]:
    return db.query(UserPreference).filter(
        UserPreference.user_id == user_id
    ).all()


def create_user_preference(db: Session, preference: UserPreferenceCreate) -> UserPreference:
    created_perference = UserPreference(
        user_id=preference.user_id,
        preference_type=preference.preference_type,
        preference_value=preference.preference_value
    )

    db.add(created_perference)
    return created_perference


def update_user_preference(db: Session, preference_id: int, pref_update: UserPreferenceUpdate) -> UserPreference:
    updating_preference = db.query(UserPreference).filter(
        UserPreference.preference_id == preference_id
    ).first()

    if not updating_preference:
        raise ValueError("Preference not found.")

    updating_preference.preference_type = pref_update.preference_type
    updating_preference.preference_value = pref_update.preference_value

    db.add(updating_preference)
    return updating_preference


def update_user_preference_with_user_id(db: Session, preference_id: int, user_id: int, pref_update: UserPreferenceUpdate) -> UserPreference:
    updating_preference = db.query(UserPreference).filter(
        UserPreference.preference_id == preference_id,
        UserPreference.user_id == user_id
    ).first()

    if not updating_preference:
        raise ValueError("Preference not found.")

    updating_preference.preference_type = pref_update.preference_type
    updating_preference.preference_value = pref_update.preference_value

    db.add(updating_preference)
    return updating_preference


def delete_user_preference(db: Session, preference_id: int) -> None:
    deleting_preference = db.query(UserPreference).filter(
        UserPreference.preference_id == preference_id
    ).first()

    if not deleting_preference:
        raise ValueError("Preference not found.")

    db.delete(deleting_preference)
