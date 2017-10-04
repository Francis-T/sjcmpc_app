"""
    @filename   models.py
    @author     Francis T
    
    This file contains the data models for the underlying database
    used by the program. It is used by SQLAlchemy's ORM to simplify
    database interactions.

"""
import enum

from sqlalchemy import Column, Enum, Date, Time, Integer, String
from sqlalchemy import ARRAY, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class SeasonType(enum.Enum):
    REGULAR = "REG"
    PEAK = "PEAK"
    LEAN = "LEAN"

class TimesheetRecord(Base):
    __tablename__ = "t_timesheet"

    ## Table Columns ##
    id = Column(Integer, primary_key=True)
    date = Column(Date)
    badge_id = Column(Integer, ForeignKey('t_employee_badges.id'))
    badge = relationship("EmployeeBadges", back_populates="records")
    job_id = Column(Integer, ForeignKey('t_jobs.id'))
    job = relationship("Jobs", back_populates="records")
    time_started = Column(Time)
    time_finished = Column(Time)
    workday_offset = Column(Time)
    season_type = Column(Enum(SeasonType))

    def __repr__(self):
        return "<{}(id={}, date='{}', badge_id={}, job_id={}, time_started='{}', time_finished='{}', workday_offset='{}', season_type='{}'>".format(
                    "TimesheetRecords",
                    self.id,
                    self.date,
                    self.badge_id,
                    self.job_id,
                    self.time_started,
                    self.time_finished,
                    self.workday_offset,
                    self.season_type )


class PayTypes(enum.Enum):
    DAILY = "DY"
    PIECE_RATE = "PR"

class EmployeeBadges(Base):
    __tablename__ = "t_employee_badges"

    ## Table Columns ##
    id = Column(Integer, primary_key=True)
    serial_no = Column(Integer)
    employee_id = Column(Integer, ForeignKey('t_employees.id'))
    employee = relationship("Employees", back_populates="badges")
    pay_type = Column(Enum(PayTypes))
    records = relationship("TimesheetRecord", order_by=TimesheetRecord.id, back_populates="badge")

    def __repr__(self):
        return "<{}(id={}, serial_no={}, employee_id={}, pay_type='{}'>".format(
                    "EmployeeBadges",
                    self.id,
                    self.serial_no,
                    self.employee_id,
                    self.pay_type )


class Employees(Base):
    __tablename__ = "t_employees"

    ## Table Columns ##
    id = Column(Integer, primary_key=True)
    last_name = Column(String(255))
    first_name = Column(String(255))
    middle_name = Column(String(255))
    dept_id = Column(Integer, ForeignKey('t_departments.id'))
    dept = relationship("Departments", back_populates="members")
    sex = Column(String(255))
    birth_date = Column(Date)
    location = Column(String(255))
    hire_date = Column(Date)
    tel_no = Column(String(255))
    mobile_no = Column(String(255))
    badges = relationship("EmployeeBadges", order_by=EmployeeBadges.id, back_populates="employee")

    def __repr__(self):
        return "<{}(id={}, last_name='{}', first_name='{}', middle_name='{}', dept_id={}, sex='{}', birth_date='{}', location='{}', hire_date='{}', tel_no='{}', mobile_no='{}'>".format(
                    "Employees",
                    self.id,
                    self.last_name,
                    self.first_name,
                    self.middle_name,
                    self.dept_id,
                    self.sex,
                    self.birth_date,
                    self.location,
                    self.hire_date,
                    self.tel_no,
                    self.mobile_no )

class Jobs(Base):
    __tablename__ = "t_jobs"

    ## Table Columns ##
    id = Column(Integer, primary_key=True)
    job_name = Column(String(255))
    desc = Column(String(255))
    dept_id = Column(Integer, ForeignKey('t_departments.id'))
    dept = relationship("Departments", back_populates="roles")
    records = relationship("TimesheetRecord", order_by=TimesheetRecord.id, back_populates="job")

    def __repr__(self):
        return "<{}(id={}, job_name='{}', desc='{}', dept_id={}>".format(
                    "Jobs",
                    self.id,
                    self.job_name,
                    self.desc,
                    self.dept_id )

class Departments(Base):
    __tablename__ = "t_departments"

    ## Table Columns ##
    id = Column(Integer, primary_key=True)
    dept_name = Column(String(255))
    desc = Column(String(255))
    members = relationship("Employees", order_by=Employees.id, back_populates="dept")
    roles = relationship("Jobs", order_by=Jobs.id, back_populates="dept")

    def __repr__(self):
        return "<{}(id={}, name='{}', desc='{}'>".format(
                    "Departments",
                    self.id,
                    self.dept_name,
                    self.desc )






