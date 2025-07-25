"""Project schema."""

from typing import Optional

from geopy.geocoders import Nominatim
from pydantic import BaseModel, Field, model_validator
from pydantic_extra_types.phone_numbers import PhoneNumber

PhoneNumber.phone_format = "E164"
PhoneNumber.supported_regions = ["TZ"]
PhoneNumber.number_format = "E164"
PhoneNumber.default_region = "TZ"

geolocator = Nominatim(user_agent="growsmart_api")


class UserSchema(BaseModel):
    """User schema."""

    name: str = Field(default="User Name")
    phone_number: PhoneNumber
    is_farmer: bool = Field(default=True)
    region: Optional[str] = Field(default=None)
    latitude: Optional[float] = Field(default=None)
    longitude: Optional[float] = Field(default=None)

    @model_validator(mode="after")
    def set_coordinates(self) -> "UserSchema":
        """Set latitude and longitude based on region."""
        if self.region and not (self.latitude and self.longitude):
            location = geolocator.geocode(self.region)
            if location:
                self.latitude = location.latitude
                self.longitude = location.longitude
            else:
                self.latitude = 0.0
                self.longitude = 0.0
        self.phone_number = str(self.phone_number)
        return self


class UserResponseSchema(BaseModel):
    """User schema."""

    id: str
    name: str = Field(default="User Name")
    phone_number: PhoneNumber
    is_farmer: bool = Field(default=True)
    region: Optional[str] = Field(default=None)
    latitude: Optional[float] = Field(default=None)
    longitude: Optional[float] = Field(default=None)
