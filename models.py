import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Integer, Enum, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID, JSONB, ARRAY
from sqlalchemy.orm import relationship
import enum
from database import Base

class RoleEnum(str, enum.Enum):
    buyer = "buyer"
    seller = "seller"
    admin = "admin"

class FuelTypeEnum(str, enum.Enum):
    petrol = "petrol"
    diesel = "diesel"
    cng = "cng"
    electric = "electric"

class TransmissionEnum(str, enum.Enum):
    manual = "manual"
    automatic = "automatic"

class ListingStatusEnum(str, enum.Enum):
    under_review = "under_review"
    active = "active"
    sold = "sold"
    expired = "expired"
    removed = "removed"

class TransactionStatusEnum(str, enum.Enum):
    created = "created"
    paid = "paid"
    failed = "failed"

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    phone = Column(String(15), unique=True, nullable=True) # made nullable for email/google users
    email = Column(String(100), unique=True, nullable=True)
    hashed_password = Column(String(255), nullable=True)
    google_provider_id = Column(String(100), unique=True, nullable=True)
    name = Column(String(100), nullable=True)
    city = Column(String(100), nullable=True)
    role = Column(Enum(RoleEnum), nullable=False, default=RoleEnum.buyer)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    # Relationships
    dealer_profile = relationship("DealerProfile", back_populates="user", uselist=False)
    listings = relationship("Listing", back_populates="seller")

class DealerProfile(Base):
    __tablename__ = "dealer_profiles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), unique=True)
    dealership_name = Column(String(200), nullable=False)
    logo_url = Column(Text, nullable=True)
    address = Column(Text, nullable=True)
    city = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    user = relationship("User", back_populates="dealer_profile")

class Listing(Base):
    __tablename__ = "listings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    seller_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    make = Column(String(100), nullable=False)
    model = Column(String(100), nullable=False)
    variant = Column(String(100), nullable=True)
    year = Column(Integer, nullable=False)
    mileage_km = Column(Integer, nullable=False)
    fuel_type = Column(Enum(FuelTypeEnum), nullable=False)
    transmission = Column(Enum(TransmissionEnum), nullable=False)
    ownership_count = Column(Integer, default=1)
    color = Column(String(50), nullable=True)
    asking_price = Column(Integer, nullable=False)
    is_negotiable = Column(Boolean, default=True)
    city = Column(String(100), nullable=False)
    locality = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)
    features = Column(JSONB, nullable=True)
    photos = Column(ARRAY(Text), nullable=True)
    status = Column(Enum(ListingStatusEnum), default=ListingStatusEnum.under_review)
    view_count = Column(Integer, default=0)
    enquiry_count = Column(Integer, default=0)
    expires_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    seller = relationship("User", back_populates="listings")
    enquiries = relationship("Enquiry", back_populates="listing")

class Enquiry(Base):
    __tablename__ = "enquiries"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    listing_id = Column(UUID(as_uuid=True), ForeignKey("listings.id"))
    buyer_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    seller_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    message = Column(Text, nullable=False)
    sent_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    listing = relationship("Listing", back_populates="enquiries")
    buyer = relationship("User", foreign_keys=[buyer_id])
    seller = relationship("User", foreign_keys=[seller_id])

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    listing_id = Column(UUID(as_uuid=True), ForeignKey("listings.id"), nullable=True)
    seller_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    amount = Column(Integer, nullable=False)
    razorpay_order_id = Column(String(100), unique=True, nullable=True)
    razorpay_payment_id = Column(String(100), nullable=True)
    status = Column(Enum(TransactionStatusEnum), nullable=False, default=TransactionStatusEnum.created)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

class SavedListing(Base):
    __tablename__ = "saved_listings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    listing_id = Column(UUID(as_uuid=True), ForeignKey("listings.id"))
    saved_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    __table_args__ = (UniqueConstraint('user_id', 'listing_id', name='uix_user_listing_saved'),)

class ReportedListing(Base):
    __tablename__ = "reported_listings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    listing_id = Column(UUID(as_uuid=True), ForeignKey("listings.id"))
    reported_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    reason = Column(Text, nullable=False)
    resolved = Column(Boolean, default=False)
    reported_at = Column(DateTime(timezone=True), default=datetime.utcnow)
