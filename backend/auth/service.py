from sqlalchemy.orm import Session
from passlib.context import CryptContext
from backend.auth.models import User, ChatHistory
from backend.db import get_session


pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

class AuthService:
    def __init__(self):
        self.Session = get_session()

    def get_password_hash(self, password):
        return pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    def signup(self, full_name, email, password):
        session = self.Session()
        try:
            existing_user = session.query(User).filter(User.email == email).first()
            if existing_user:
                return None, "Email already registered."

            new_user = User(
                full_name=full_name,
                email=email,
                password_hash=self.get_password_hash(password)
            )
            session.add(new_user)
            session.commit()
            print(f"User created: {new_user.id}") # Debug
            return new_user, None
        except Exception as e:
            session.rollback()
            return None, str(e)
        finally:
            session.close()

    def login(self, email, password):
        session = self.Session()
        try:
            user = session.query(User).filter(User.email == email).first()
            if not user:
                return None, "Invalid email or password."
            
            if not self.verify_password(password, user.password_hash):
                return None, "Invalid email or password."
            
            return user, None
        finally:
            session.close()

    def save_message(self, user_id, role, content):
        session = self.Session()
        try:
            msg = ChatHistory(user_id=user_id, role=role, content=content)
            session.add(msg)
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Error saving message: {e}")
        finally:
            session.close()

    def get_chat_history(self, user_id, limit=None):
        session = self.Session()
        try:
            # Fetch messages
            query = session.query(ChatHistory)\
                .filter(ChatHistory.user_id == user_id)\
                .order_by(ChatHistory.timestamp.desc())
            
            if limit:
                query = query.limit(limit)
            
            messages = query.all()
            # Return reversed so they are chronologically ascending
            return messages[::-1]
        finally:
            session.close()
