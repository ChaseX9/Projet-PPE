"""API endpoints for CapInvest Academy training system."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime, date, timedelta

from ..database.database import get_db
from ..database.models import Module, Lesson, Question, UserLessonProgress, UserTrainingStats, User
from ..auth.dependencies import get_current_user

router = APIRouter(prefix="/api/training", tags=["Training"])

# ============================================================================
# RESPONSE MODELS
# ============================================================================

class ModuleListItem(BaseModel):
    id: int
    title: str
    description: str
    level: str
    order: int
    icon: str
    lesson_count: int
    completed_lessons: int
    progress_percentage: int
    is_locked: bool = False
    lock_reason: Optional[str] = None

class LessonListItem(BaseModel):
    id: int
    title: str
    order: int
    estimated_minutes: int
    xp_reward: int
    status: str  # not_started, in_progress, completed
    score: Optional[int]

class ModuleDetail(BaseModel):
    id: int
    title: str
    description: str
    level: str
    icon: str
    lessons: List[LessonListItem]
    is_locked: bool = False
    lock_reason: Optional[str] = None

class QuestionData(BaseModel):
    id: int
    type: str
    prompt: str
    choices: Optional[List[str]]
    order: int

class LessonDetail(BaseModel):
    id: int
    module_id: int
    title: str
    content: str
    example: Optional[str]
    estimated_minutes: int
    xp_reward: int
    questions: List[QuestionData]

class SubmitAnswersRequest(BaseModel):
    answers: Dict[int, str]  # question_id -> user_answer

class QuestionResult(BaseModel):
    question_id: int
    correct: bool
    user_answer: str
    correct_answer: str
    explanation: str

class SubmitAnswersResponse(BaseModel):
    score: int
    total_questions: int
    percentage: int
    xp_earned: int
    results: List[QuestionResult]
    lesson_completed: bool

class ProgressResponse(BaseModel):
    total_xp: int
    completed_lessons_count: int
    total_lessons: int
    total_minutes: int
    current_streak: int
    longest_streak: int
    last_activity_date: Optional[date]
    daily_modules: Dict[str, Optional[int]] = {}
    daily_session_titles: Dict[str, Optional[str]] = {}
    daily_session_progress: Dict[str, int] = {}

# ============================================================================
# ENDPOINTS
# ============================================================================

@router.get("/modules", response_model=List[ModuleListItem])
def get_modules(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get all modules with user progress and locking status."""
    modules = db.query(Module).order_by(Module.order).all()
    stats = db.query(UserTrainingStats).filter(UserTrainingStats.user_id == current_user.id).first()
    
    # Refresh daily modules if first time today
    today = date.today()
    daily_modules = {}
    if stats:
        if stats.last_activity_date:
            # Safely handle potential mixed types from DB
            try:
                if hasattr(stats.last_activity_date, 'date'):
                    last_date = stats.last_activity_date.date()
                elif isinstance(stats.last_activity_date, (str, bytes)):
                    date_str = stats.last_activity_date.decode() if isinstance(stats.last_activity_date, bytes) else stats.last_activity_date
                    last_date = datetime.fromisoformat(date_str).date()
                else:
                    last_date = stats.last_activity_date
                
                if last_date < today:
                    stats.daily_modules = {}
                    db.commit()
            except Exception as e:
                print(f"Error checking last_activity_date in get_modules: {e}")
        
        daily_modules = stats.daily_modules if isinstance(stats.daily_modules, dict) else {}

    # Get all modules to check global sequence
    all_modules = db.query(Module).order_by(Module.order).all()
    
    # Calculate progress for each once to avoid N+1 issues
    results = []
    # Track locking per level
    level_locked_status = {
        "beginner": False,
        "intermediate": False,
        "advanced": False
    }

    for module in all_modules:
        lesson_count = len(module.lessons)
        completed_lessons = db.query(UserLessonProgress).join(Lesson).filter(
            Lesson.module_id == module.id,
            UserLessonProgress.user_id == current_user.id,
            UserLessonProgress.status == "completed"
        ).count()
        
        progress = int((completed_lessons / lesson_count) * 100) if lesson_count > 0 else 0
        
        # Determine if locked
        is_locked = False
        lock_reason = None
        
        if level_locked_status.get(module.level, False):
            is_locked = True
            lock_reason = "Terminez les modules précédents pour débloquer celui-ci."
        
        # 2. Daily Lock: 1 module per level per day (Global)
        if not is_locked and progress < 100:
            active_daily_for_level = daily_modules.get(module.level)
            if active_daily_for_level is not None and active_daily_for_level != module.id:
                is_locked = True
                lock_reason = "Vous avez déjà commencé un autre module dans cette catégorie aujourd'hui. Revenez demain pour débloquer !"

        # Update level-specific sequential flag: if this one is NOT 100%, subsequent ones IN THIS LEVEL are locked
        if progress < 100:
            level_locked_status[module.level] = True

        results.append(ModuleListItem(
            id=module.id,
            title=module.title,
            description=module.description,
            level=module.level,
            order=module.order,
            icon=module.icon,
            lesson_count=lesson_count,
            completed_lessons=completed_lessons,
            progress_percentage=progress,
            is_locked=is_locked,
            lock_reason=lock_reason
        ))
    
    return results


@router.get("/modules/{module_id}", response_model=ModuleDetail)
def get_module(module_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get module details with lesson list and locking status."""
    module = db.query(Module).filter(Module.id == module_id).first()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    
    stats = db.query(UserTrainingStats).filter(UserTrainingStats.user_id == current_user.id).first()
    today = date.today()
    
    # Calculate progress for locking logic
    lesson_count = len(module.lessons)
    completed_count = db.query(UserLessonProgress).join(Lesson).filter(
        Lesson.module_id == module.id,
        UserLessonProgress.user_id == current_user.id,
        UserLessonProgress.status == "completed"
    ).count()
    progress_percentage = int((completed_count / lesson_count * 100)) if lesson_count > 0 else 0

    is_locked = False
    lock_reason = None
    
    if stats:
        # Enforce lock
        if progress_percentage < 100:
            stats_daily = stats.daily_modules if isinstance(stats.daily_modules, dict) else {}
            active_daily_for_level = stats_daily.get(module.level)
            if active_daily_for_level is not None and active_daily_for_level != module.id:
                is_locked = True
                lock_reason = "Vous avez déjà commencé un autre module de ce niveau aujourd'hui. Revenez demain !"

    lessons_data = []
    for lesson in sorted(module.lessons, key=lambda x: x.order):
        progress = db.query(UserLessonProgress).filter(
            UserLessonProgress.user_id == current_user.id,
            UserLessonProgress.lesson_id == lesson.id
        ).first()
        
        # If module is locked, lessons are visually locked too
        status = progress.status if progress else "not_started"
        if is_locked and status != "completed":
            status = "locked"

        lessons_data.append(LessonListItem(
            id=lesson.id,
            title=lesson.title,
            order=lesson.order,
            estimated_minutes=lesson.estimated_minutes,
            xp_reward=lesson.xp_reward,
            status=status,
            score=progress.score if progress else None
        ))
    
    return ModuleDetail(
        id=module.id,
        title=module.title,
        description=module.description,
        level=module.level,
        icon=module.icon,
        lessons=lessons_data,
        is_locked=is_locked,
        lock_reason=lock_reason
    )


@router.get("/lessons/{lesson_id}", response_model=LessonDetail)
def get_lesson(lesson_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get lesson content and questions (without answers)."""
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    
    # Early Lock: If this is the first lesson accessed today, lock in the module!
    stats = db.query(UserTrainingStats).filter(UserTrainingStats.user_id == current_user.id).first()
    if stats:
        today = date.today()
        # Reset if new day
        if stats.last_activity_date:
            try:
                if hasattr(stats.last_activity_date, 'date'):
                    last_date = stats.last_activity_date.date()
                elif isinstance(stats.last_activity_date, (str, bytes)):
                    date_str = stats.last_activity_date.decode() if isinstance(stats.last_activity_date, bytes) else stats.last_activity_date
                    last_date = datetime.fromisoformat(date_str).date()
                else:
                    last_date = stats.last_activity_date
                
                if last_date < today:
                    stats.daily_modules = {}
                    db.commit()
            except Exception:
                pass
            
        daily_modules = dict(stats.daily_modules) if isinstance(stats.daily_modules, dict) else {}
        if daily_modules.get(lesson.module.level) is None:
            # Check if module is already done
            lesson_count = db.query(Lesson).filter(Lesson.module_id == lesson.module_id).count()
            completed_count = db.query(UserLessonProgress).join(Lesson).filter(
                Lesson.module_id == lesson.module_id,
                UserLessonProgress.user_id == current_user.id,
                UserLessonProgress.status == "completed"
            ).count()
            
            if completed_count < lesson_count:
                daily_modules[lesson.module.level] = lesson.module_id
                stats.daily_modules = daily_modules
                from sqlalchemy.orm.attributes import flag_modified
                flag_modified(stats, "daily_modules")
                stats.last_activity_date = datetime.utcnow()
                db.commit()
    
    # Mark as in_progress if not started
    progress = db.query(UserLessonProgress).filter(
        UserLessonProgress.user_id == current_user.id,
        UserLessonProgress.lesson_id == lesson_id
    ).first()
    
    if not progress:
        # Check daily limit BEFORE starting a new lesson
        stats = db.query(UserTrainingStats).filter(UserTrainingStats.user_id == current_user.id).first()
        today = date.today()
        
        if stats:
            # Refresh for today
            if stats.last_activity_date:
                try:
                    if hasattr(stats.last_activity_date, 'date'):
                        last_date = stats.last_activity_date.date()
                    elif isinstance(stats.last_activity_date, (str, bytes)):
                        date_str = stats.last_activity_date.decode() if isinstance(stats.last_activity_date, bytes) else stats.last_activity_date
                        last_date = datetime.fromisoformat(date_str).date()
                    else:
                        last_date = stats.last_activity_date
                    
                    if last_date < today:
                        stats.daily_modules = {}
                        db.commit()
                except Exception:
                    pass
            
            daily_modules = dict(stats.daily_modules) if isinstance(stats.daily_modules, dict) else {}
            active_daily_for_level = daily_modules.get(lesson.module.level)
            
            # Module check
            if active_daily_for_level is not None and active_daily_for_level != lesson.module_id:
                # Is the current module already done?
                completed_count = db.query(UserLessonProgress).join(Lesson).filter(
                    Lesson.module_id == active_daily_for_level,
                    UserLessonProgress.user_id == current_user.id,
                    UserLessonProgress.status == "completed"
                ).count()
                total_in_module = db.query(Lesson).filter(Lesson.module_id == active_daily_for_level).count()
                
                if completed_count < total_in_module:
                    raise HTTPException(status_code=403, detail="Vous avez déjà commencé un autre module de ce niveau aujourd'hui.")
                else:
                    raise HTTPException(status_code=403, detail="Session quotidienne pour ce niveau terminée. Revenez demain !")

            # Lock in the module for today if not already set
            if active_daily_for_level is None:
                daily_modules[lesson.module.level] = lesson.module_id
                stats.daily_modules = daily_modules
                from sqlalchemy.orm.attributes import flag_modified
                flag_modified(stats, "daily_modules")
                stats.last_activity_date = datetime.utcnow()
                db.commit()

        progress = UserLessonProgress(
            user_id=current_user.id,
            lesson_id=lesson_id,
            status="in_progress"
        )
        db.add(progress)
        db.commit()
    elif progress.status == "not_started":
        progress.status = "in_progress"
        db.commit()
    
    questions_data = []
    for q in sorted(lesson.questions, key=lambda x: x.order):
        questions_data.append(QuestionData(
            id=q.id,
            type=q.type,
            prompt=q.prompt,
            choices=q.choices,
            order=q.order
        ))
    
    return LessonDetail(
        id=lesson.id,
        module_id=lesson.module_id,
        title=lesson.title,
        content=lesson.content,
        example=lesson.example,
        estimated_minutes=lesson.estimated_minutes,
        xp_reward=lesson.xp_reward,
        questions=questions_data
    )


@router.post("/lessons/{lesson_id}/submit", response_model=SubmitAnswersResponse)
def submit_lesson(
    lesson_id: int,
    submission: SubmitAnswersRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Submit lesson answers and get results."""
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    
    # Get all questions
    questions = {q.id: q for q in lesson.questions}
    
    # Evaluate answers
    results = []
    correct_count = 0
    
    for q_id, user_answer in submission.answers.items():
        question = questions.get(q_id)
        if not question:
            continue
        
        is_correct = user_answer.lower().strip() == question.correct_answer.lower().strip()
        if is_correct:
            correct_count += 1
        
        results.append(QuestionResult(
            question_id=q_id,
            correct=is_correct,
            user_answer=user_answer,
            correct_answer=question.correct_answer,
            explanation=question.explanation
        ))
    
    total_questions = len(questions)
    percentage = int((correct_count / total_questions * 100)) if total_questions > 0 else 0
    
    # Update progress
    progress = db.query(UserLessonProgress).filter(
        UserLessonProgress.user_id == current_user.id,
        UserLessonProgress.lesson_id == lesson_id
    ).first()
    
    if not progress:
        progress = UserLessonProgress(user_id=current_user.id, lesson_id=lesson_id)
        db.add(progress)
    
    progress.score = percentage
    progress.attempts += 1
    progress.last_done_at = datetime.utcnow()
    
    # Mark as completed if score >= 70%
    lesson_completed = percentage >= 70
    if lesson_completed and progress.status != "completed":
        progress.status = "completed"
        
        # Update user stats
        stats = db.query(UserTrainingStats).filter(UserTrainingStats.user_id == current_user.id).first()
        if not stats:
            stats = UserTrainingStats(
                user_id=current_user.id,
                total_xp=0,
                completed_lessons_count=0,
                current_streak=0,
                longest_streak=0
            )
            db.add(stats)
            db.flush()  # Get the ID before using it
        
        stats.total_xp += lesson.xp_reward
        stats.completed_lessons_count += 1
        
        # Update streak
        today = date.today()
        if stats.last_activity_date == today - timedelta(days=1):
            stats.current_streak += 1
        elif stats.last_activity_date != today:
            stats.current_streak = 1
        
        if stats.current_streak > stats.longest_streak:
            stats.longest_streak = stats.current_streak
        
        stats.last_activity_date = today
        stats.updated_at = datetime.utcnow()
    
    db.commit()
    
    xp_earned = lesson.xp_reward if lesson_completed and progress.attempts == 1 else 0
    
    return SubmitAnswersResponse(
        score=correct_count,
        total_questions=total_questions,
        percentage=percentage,
        xp_earned=xp_earned,
        results=results,
        lesson_completed=lesson_completed
    )


@router.get("/progress", response_model=ProgressResponse)
def get_progress(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get user's overall training statistics."""
    stats = db.query(UserTrainingStats).filter(UserTrainingStats.user_id == current_user.id).first()
    total_lessons = db.query(Lesson).count()
    # Time spent = estimated_minutes of lessons the user has completed
    total_minutes = db.query(func.sum(Lesson.estimated_minutes))\
        .join(UserLessonProgress, UserLessonProgress.lesson_id == Lesson.id)\
        .filter(
            UserLessonProgress.user_id == current_user.id,
            UserLessonProgress.status == "completed"
        ).scalar() or 0
    
    if not stats:
        return ProgressResponse(
            total_xp=0,
            completed_lessons_count=0,
            total_lessons=total_lessons,
            total_minutes=total_minutes,
            current_streak=0,
            longest_streak=0,
            last_activity_date=None
        )
    
    daily_session_titles = {}
    daily_session_progress = {}
    
    if stats:
        stats_daily = stats.daily_modules if isinstance(stats.daily_modules, dict) else {}
        for level, module_id in stats_daily.items():
            if module_id:
                module = db.query(Module).filter(Module.id == module_id).first()
                if module:
                    daily_session_titles[level] = module.title
                    
                    # Calculate progress for this module
                    lesson_count = len(module.lessons)
                    completed_count = db.query(UserLessonProgress).join(Lesson).filter(
                        Lesson.module_id == module.id,
                        UserLessonProgress.user_id == current_user.id,
                        UserLessonProgress.status == "completed"
                    ).count()
                    daily_session_progress[level] = int((completed_count / lesson_count * 100)) if lesson_count > 0 else 0
            
    # Safe date conversion
    last_act_date = None
    if stats and stats.last_activity_date:
        try:
            if hasattr(stats.last_activity_date, 'date'):
                last_act_date = stats.last_activity_date.date()
            elif isinstance(stats.last_activity_date, (str, bytes)):
                date_str = stats.last_activity_date.decode() if isinstance(stats.last_activity_date, bytes) else stats.last_activity_date
                last_act_date = datetime.fromisoformat(date_str).date()
            else:
                last_act_date = stats.last_activity_date
        except:
            pass

    return ProgressResponse(
        total_xp=stats.total_xp if stats else 0,
        completed_lessons_count=stats.completed_lessons_count if stats else 0,
        total_lessons=total_lessons,
        total_minutes=total_minutes,
        current_streak=stats.current_streak if stats else 0,
        longest_streak=stats.longest_streak if stats else 0,
        last_activity_date=last_act_date,
        daily_modules=stats.daily_modules if stats and isinstance(stats.daily_modules, dict) else {},
        daily_session_titles=daily_session_titles,
        daily_session_progress=daily_session_progress
    )
