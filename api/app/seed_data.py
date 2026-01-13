"""Seed database with mock data."""

from sqlalchemy import Engine
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from .models import User, UserRole, TeacherStudent, ClassSession, MusicalPiece, Task, TaskType, TaskStatus
from .auth.jwt import get_password_hash


def seed_database(engine: Engine):
    """Seed database with mock users and data."""
    session = Session(bind=engine)
    
    # Check if data already exists
    existing_users = session.query(User).count()
    if existing_users > 0:
        session.close()
        return
    
    print("Seeding database with mock data...")
    
    # Create users
    admin = User(
        username="admin",
        password_hash=get_password_hash("admin"),
        name="RIAM Administrator",
        email="admin@riam.ie",
        role=UserRole.ADMIN
    )
    
    teacher1 = User(
        username="teacher",
        password_hash=get_password_hash("teacher"),
        name="Dr. Sarah Murphy",
        email="sarah.murphy@riam.ie",
        role=UserRole.TEACHER
    )
    
    teacher2 = User(
        username="teacher2",
        password_hash=get_password_hash("teacher2"),
        name="Prof. Michael O'Brien",
        email="michael.obrien@riam.ie",
        role=UserRole.TEACHER
    )
    
    student1 = User(
        username="student",
        password_hash=get_password_hash("student"),
        name="Emma Walsh",
        email="emma.walsh@student.riam.ie",
        role=UserRole.STUDENT
    )
    
    student2 = User(
        username="student2",
        password_hash=get_password_hash("student2"),
        name="Liam Kelly",
        email="liam.kelly@student.riam.ie",
        role=UserRole.STUDENT
    )
    
    student3 = User(
        username="student3",
        password_hash=get_password_hash("student3"),
        name="Aoife Brennan",
        email="aoife.brennan@student.riam.ie",
        role=UserRole.STUDENT
    )
    
    session.add_all([admin, teacher1, teacher2, student1, student2, student3])
    session.commit()
    
    # Create teacher-student relationships
    rel1 = TeacherStudent(teacher_id=teacher1.id, student_id=student1.id)
    rel2 = TeacherStudent(teacher_id=teacher1.id, student_id=student2.id)
    rel3 = TeacherStudent(teacher_id=teacher2.id, student_id=student3.id)
    
    session.add_all([rel1, rel2, rel3])
    session.commit()
    
    # Create musical pieces
    piece1 = MusicalPiece(
        title="Piano Sonata No. 16 in C major, K. 545",
        composer="Wolfgang Amadeus Mozart",
        description="A famous piano sonata by Mozart, often called 'Sonata facile' or 'Sonata semplice'.",
        audio_url="https://example.com/mozart-k545.mp3"
    )
    
    piece2 = MusicalPiece(
        title="Clair de Lune",
        composer="Claude Debussy",
        description="The third movement from Suite bergamasque by Debussy.",
        audio_url="https://example.com/debussy-clair-de-lune.mp3"
    )
    
    piece3 = MusicalPiece(
        title="The Four Seasons - Spring",
        composer="Antonio Vivaldi",
        description="The first concerto from Vivaldi's famous Four Seasons.",
        audio_url="https://example.com/vivaldi-spring.mp3"
    )
    
    piece4 = MusicalPiece(
        title="Nocturne in E-flat major, Op. 9, No. 2",
        composer="Frédéric Chopin",
        description="One of Chopin's most famous nocturnes.",
        audio_url="https://example.com/chopin-nocturne-op9-2.mp3"
    )
    
    session.add_all([piece1, piece2, piece3, piece4])
    session.commit()
    
    # Create class sessions
    class1 = ClassSession(
        teacher_id=teacher1.id,
        student_id=student1.id,
        date=datetime.utcnow() - timedelta(days=7),
        notes="Excellent progress on Mozart's Sonata. Emma demonstrated strong technical skills and musicality.",
        improvement_points="Work on maintaining consistent tempo in the development section. Pay attention to dynamic contrasts.",
        actions="Practice scales in C major (hands together). Focus on the challenging passage in measures 45-52."
    )
    
    class2 = ClassSession(
        teacher_id=teacher1.id,
        student_id=student2.id,
        date=datetime.utcnow() - timedelta(days=5),
        notes="Liam showed improvement in sight-reading. Good understanding of harmonic progressions.",
        improvement_points="Need to work on finger independence. Some hesitation in transitions between positions.",
        actions="Practice Hanon exercises daily. Record practice sessions for self-assessment."
    )
    
    class3 = ClassSession(
        teacher_id=teacher2.id,
        student_id=student3.id,
        date=datetime.utcnow() - timedelta(days=3),
        notes="Aoife displayed excellent interpretation of Chopin. Beautiful phrasing and emotional depth.",
        improvement_points="Minor timing issues in the rubato sections. Hand coordination needs attention.",
        actions="Listen to recordings by Rubinstein and Pollini. Practice with metronome at slower tempo."
    )
    
    session.add_all([class1, class2, class3])
    session.commit()
    
    # Create tasks
    task1 = Task(
        student_id=student1.id,
        teacher_id=teacher1.id,
        type=TaskType.PRACTICE,
        title="Practice Mozart Sonata - Development Section",
        description="Focus on measures 45-52. Work on tempo consistency and dynamic contrasts.",
        musical_piece_id=piece1.id,
        status=TaskStatus.IN_PROGRESS,
        due_date=datetime.utcnow() + timedelta(days=7)
    )
    
    task2 = Task(
        student_id=student1.id,
        teacher_id=teacher1.id,
        type=TaskType.LISTENING,
        title="Listen to Debussy's Clair de Lune",
        description="Listen to three different interpretations and compare their approaches to tempo and dynamics.",
        musical_piece_id=piece2.id,
        status=TaskStatus.ASSIGNED,
        due_date=datetime.utcnow() + timedelta(days=10)
    )
    
    task3 = Task(
        student_id=student2.id,
        teacher_id=teacher1.id,
        type=TaskType.PRACTICE,
        title="Hanon Exercises - Finger Independence",
        description="Practice exercises 1-5 from Hanon. Focus on finger independence and evenness of tone.",
        status=TaskStatus.IN_PROGRESS,
        due_date=datetime.utcnow() + timedelta(days=5)
    )
    
    task4 = Task(
        student_id=student3.id,
        teacher_id=teacher2.id,
        type=TaskType.LISTENING,
        title="Analyze Vivaldi's Four Seasons - Spring",
        description="Listen and identify the programmatic elements. Pay attention to the use of ritornello form.",
        musical_piece_id=piece3.id,
        status=TaskStatus.COMPLETED,
        due_date=datetime.utcnow() - timedelta(days=2)
    )
    
    task5 = Task(
        student_id=student3.id,
        teacher_id=teacher2.id,
        type=TaskType.PRACTICE,
        title="Chopin Nocturne - Rubato Practice",
        description="Practice the nocturne with metronome at 70% tempo. Focus on maintaining the underlying pulse while applying rubato.",
        musical_piece_id=piece4.id,
        status=TaskStatus.IN_PROGRESS,
        due_date=datetime.utcnow() + timedelta(days=14)
    )
    
    session.add_all([task1, task2, task3, task4, task5])
    session.commit()
    
    print(f"Database seeded successfully!")
    print(f"  - Created {session.query(User).count()} users")
    print(f"  - Created {session.query(TeacherStudent).count()} teacher-student relationships")
    print(f"  - Created {session.query(MusicalPiece).count()} musical pieces")
    print(f"  - Created {session.query(ClassSession).count()} class sessions")
    print(f"  - Created {session.query(Task).count()} tasks")
    print("\nMock credentials:")
    print("  - admin/admin (Admin)")
    print("  - teacher/teacher (Dr. Sarah Murphy)")
    print("  - teacher2/teacher2 (Prof. Michael O'Brien)")
    print("  - student/student (Emma Walsh)")
    print("  - student2/student2 (Liam Kelly)")
    print("  - student3/student3 (Aoife Brennan)")
    
    session.close()
