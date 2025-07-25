"""User repository."""

from sqlmodel import Session, select

from src.databae.models import Buyer, Farmer, User
from src.schemas import UserResponseSchema, UserSchema


class UserRepository:
    """Repository for user-related database operations."""

    def __init__(self, session: Session):
        self.session = session

    def _exists(self, phone_number: str) -> bool:
        """Check if a user with the given phone number already exists."""
        return (
            self.session.exec(
                select(User).filter(User.phone_number == phone_number)
            ).first()
            is not None
        )

    def create_user(self, user_data: UserSchema) -> UserSchema:
        """Create a new user in the database."""
        if self._exists(user_data.phone_number):
            return {
                "error": "User with this phone number already exists.",
                "status": "failed",
            }

        user = User(
            name=user_data.name,
            phone_number=str(user_data.phone_number),
        )

        self.session.add(user)
        self.session.commit()
        if user_data.is_farmer:
            farmer = Farmer(
                user_id=user.id,
                region=user_data.region or "Unknown",
                latitude=user_data.latitude or 0.0,
                longitude=user_data.longitude or 0.0,
            )
            self.session.add(farmer)
        else:
            buyer = Buyer(user_id=user.id)
            self.session.add(buyer)
        self.session.commit()
        return UserResponseSchema(
            id=user.id,
            name=user.name,
            phone_number=user.phone_number,
            is_farmer=user_data.is_farmer,
            region=user_data.region,
            latitude=user_data.latitude,
            longitude=user_data.longitude,
        )
