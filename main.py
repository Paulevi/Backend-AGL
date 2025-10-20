from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
import jwt
from passlib.context import CryptContext
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

app = FastAPI()

# Database setup
DATABASE_URL = "postgresql://user:password@localhost/rh_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Authentication setup
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

# Database Models
class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    role = Column(String)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    schedules = relationship("Schedule", back_populates="employee")
    leave_requests = relationship("LeaveRequest", back_populates="employee")

class Schedule(Base):
    __tablename__ = "schedules"
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    employee = relationship("Employee", back_populates="schedules")

class LeaveRequest(Base):
    __tablename__ = "leave_requests"
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    approved = Column(Boolean, default=False)
    employee = relationship("Employee", back_populates="leave_requests")

Base.metadata.create_all(bind=engine)

# Pydantic Models
class EmployeeCreate(BaseModel):
    name: str
    role: str
    email: str
    password: str

class EmployeeResponse(BaseModel):
    id: int
    name: str
    role: str
    email: str

class LoginRequest(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class ScheduleCreate(BaseModel):
    employee_id: int
    start_time: datetime
    end_time: datetime

class ScheduleResponse(BaseModel):
    id: int
    employee_id: int
    start_time: datetime
    end_time: datetime

class LeaveRequestCreate(BaseModel):
    employee_id: int
    start_date: datetime
    end_date: datetime

class LeaveRequestResponse(BaseModel):
    id: int
    employee_id: int
    start_date: datetime
    end_date: datetime
    approved: bool

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Authentication functions
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict):
    to_encode = data.copy()
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: SessionLocal = Depends(get_db)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    user = db.query(Employee).filter(Employee.email == email).first()
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    return user

# API Endpoints
@app.post("/register", response_model=EmployeeResponse)
def register(employee: EmployeeCreate, db: SessionLocal = Depends(get_db)):
    db_employee = db.query(Employee).filter(Employee.email == employee.email).first()
    if db_employee:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(employee.password)
    db_employee = Employee(name=employee.name, role=employee.role, email=employee.email, hashed_password=hashed_password)
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

@app.post("/login", response_model=TokenResponse)
def login(login_request: LoginRequest, db: SessionLocal = Depends(get_db)):
    user = db.query(Employee).filter(Employee.email == login_request.email).first()
    if not user or not verify_password(login_request.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/employees/", response_model=EmployeeResponse)
def create_employee(employee: EmployeeCreate, current_user: Employee = Depends(get_current_user), db: SessionLocal = Depends(get_db)):
    if current_user.role != "Manager du magasin":
        raise HTTPException(status_code=403, detail="Not authorized")
    hashed_password = get_password_hash(employee.password)
    db_employee = Employee(name=employee.name, role=employee.role, email=employee.email, hashed_password=hashed_password)
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

@app.get("/employees/", response_model=List[EmployeeResponse])
def read_employees(current_user: Employee = Depends(get_current_user), skip: int = 0, limit: int = 100, db: SessionLocal = Depends(get_db)):
    employees = db.query(Employee).offset(skip).limit(limit).all()
    return employees

@app.get("/employees/{employee_id}", response_model=EmployeeResponse)
def read_employee(employee_id: int, current_user: Employee = Depends(get_current_user), db: SessionLocal = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

@app.post("/schedules/", response_model=ScheduleResponse)
def create_schedule(schedule: ScheduleCreate, current_user: Employee = Depends(get_current_user), db: SessionLocal = Depends(get_db)):
    if current_user.role not in ["Manager du magasin", "Responsable de rayon"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    db_schedule = Schedule(employee_id=schedule.employee_id, start_time=schedule.start_time, end_time=schedule.end_time)
    db.add(db_schedule)
    db.commit()
    db.refresh(db_schedule)
    return db_schedule

@app.get("/schedules/", response_model=List[ScheduleResponse])
def read_schedules(current_user: Employee = Depends(get_current_user), skip: int = 0, limit: int = 100, db: SessionLocal = Depends(get_db)):
    schedules = db.query(Schedule).offset(skip).limit(limit).all()
    return schedules

@app.post("/leave-requests/", response_model=LeaveRequestResponse)
def create_leave_request(leave_request: LeaveRequestCreate, current_user: Employee = Depends(get_current_user), db: SessionLocal = Depends(get_db)):
    if leave_request.employee_id != current_user.id and current_user.role != "Manager du magasin":
        raise HTTPException(status_code=403, detail="Not authorized")
    db_leave_request = LeaveRequest(employee_id=leave_request.employee_id, start_date=leave_request.start_date, end_date=leave_request.end_date)
    db.add(db_leave_request)
    db.commit()
    db.refresh(db_leave_request)
    return db_leave_request

@app.get("/leave-requests/", response_model=List[LeaveRequestResponse])
def read_leave_requests(current_user: Employee = Depends(get_current_user), skip: int = 0, limit: int = 100, db: SessionLocal = Depends(get_db)):
    if current_user.role == "Manager du magasin":
        leave_requests = db.query(LeaveRequest).offset(skip).limit(limit).all()
    else:
        leave_requests = db.query(LeaveRequest).filter(LeaveRequest.employee_id == current_user.id).offset(skip).limit(limit).all()
    return leave_requests

@app.put("/leave-requests/{request_id}/approve")
def approve_leave_request(request_id: int, current_user: Employee = Depends(get_current_user), db: SessionLocal = Depends(get_db)):
    if current_user.role != "Manager du magasin":
        raise HTTPException(status_code=403, detail="Not authorized")
    leave_request = db.query(LeaveRequest).filter(LeaveRequest.id == request_id).first()
    if leave_request is None:
        raise HTTPException(status_code=404, detail="Leave request not found")
    leave_request.approved = True
    db.commit()
    return {"message": "Leave request approved"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)