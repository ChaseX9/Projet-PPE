"""SQLAlchemy models for persistence."""
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, JSON, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    """User account model."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    is_active = Column(Boolean, default=False)
    email_verified = Column(Boolean, default=False)
    is_test_user = Column(Boolean, default=False) # Marked for bypass/audit
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # GDPR Compliance fields
    privacy_policy_accepted_at = Column(DateTime, nullable=True)  # Timestamp when user accepted privacy policy
    cookies_consent = Column(Boolean, default=False)  # Consent for non-essential cookies
    marketing_consent = Column(Boolean, default=False)  # Consent for marketing communications
    data_retention_notified = Column(DateTime, nullable=True)  # Last notification about data retention

    # Relationships
    profiles = relationship("SavedProfile", back_populates="user")
    portfolios = relationship("SavedPortfolio", back_populates="user")


class SavedProfile(Base):
    """Model for saving user questionnaire and refined profile."""
    __tablename__ = "saved_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    # Store raw questionnaire as JSON
    questionnaire_data = Column(JSON)
    
    # Refinement results
    risk_profile = Column(String)
    risk_score = Column(Float)
    horizon_score = Column(Float)
    expertise_level = Column(String)
    confidence_score = Column(Float)
    coherence_flags = Column(JSON)
    explanation_level = Column(String)
    
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="profiles")
    portfolio = relationship("SavedPortfolio", back_populates="profile", uselist=False)

class SavedPortfolio(Base):
    """Model for saving generated portfolios."""
    __tablename__ = "saved_portfolios"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    profile_id = Column(Integer, ForeignKey("saved_profiles.id"))
    
    # Portfolio lifecycle
    status = Column(String, default="proposed")  # proposed, accepted, rejected, alternative
    parent_portfolio_id = Column(Integer, ForeignKey("saved_portfolios.id"), nullable=True)
    
    # Portfolio data
    positions = Column(JSON)  # List of dicts
    category_allocations = Column(JSON)
    expected_return = Column(Float)
    volatility = Column(Float)
    sharpe_ratio = Column(Float)
    optimization_method = Column(String)
    total_positions = Column(Integer)
    excluded_tickers = Column(JSON, nullable=True)  # Tickers excluded by user preference
    
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="portfolios")
    profile = relationship("SavedProfile", back_populates="portfolio")


# ============================================================================
# TRAINING SYSTEM MODELS (CapInvest Academy)
# ============================================================================

class Module(Base):
    """Training module (e.g., 'Les bases de l'investissement')."""
    __tablename__ = "modules"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    level = Column(String, nullable=False)  # beginner, intermediate, advanced
    order = Column(Integer, nullable=False)
    icon = Column(String, default="📚")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    lessons = relationship("Lesson", back_populates="module", cascade="all, delete-orphan")


class Lesson(Base):
    """Individual lesson within a module."""
    __tablename__ = "lessons"
    
    id = Column(Integer, primary_key=True, index=True)
    module_id = Column(Integer, ForeignKey("modules.id"), nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)  # Main educational text
    example = Column(String)  # Practical example
    order = Column(Integer, nullable=False)
    estimated_minutes = Column(Integer, default=5)
    xp_reward = Column(Integer, default=10)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    module = relationship("Module", back_populates="lessons")
    questions = relationship("Question", back_populates="lesson", cascade="all, delete-orphan")
    user_progress = relationship("UserLessonProgress", back_populates="lesson")


class Question(Base):
    """Quiz question for a lesson."""
    __tablename__ = "questions"
    
    id = Column(Integer, primary_key=True, index=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=False)
    type = Column(String, nullable=False)  # multiple_choice, true_false, numeric
    prompt = Column(String, nullable=False)  # Question text
    choices = Column(JSON)  # Array of choices for MCQ, null for others
    correct_answer = Column(String, nullable=False)
    explanation = Column(String, nullable=False)  # Why this is the answer
    order = Column(Integer, nullable=False)
    
    # Relationships
    lesson = relationship("Lesson", back_populates="questions")


class UserLessonProgress(Base):
    """Track user progress on individual lessons."""
    __tablename__ = "user_lesson_progress"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=False)
    status = Column(String, default="not_started")  # not_started, in_progress, completed
    score = Column(Integer, default=0)  # 0-100
    attempts = Column(Integer, default=0)
    last_done_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User")
    lesson = relationship("Lesson", back_populates="user_progress")


class UserTrainingStats(Base):
    """Overall training statistics for a user."""
    __tablename__ = "user_training_stats"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    total_xp = Column(Integer, default=0)
    completed_lessons_count = Column(Integer, default=0)
    current_streak = Column(Integer, default=0)
    longest_streak = Column(Integer, default=0)
    last_activity_date = Column(DateTime)
    daily_modules = Column(JSON, default=dict)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User")


class AuthToken(Base):
    """Tokens for email verification and password reset."""
    __tablename__ = "auth_tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    token = Column(String, unique=True, index=True, nullable=False)
    type = Column(String, nullable=False)  # 'verify' or 'reset'
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User")
