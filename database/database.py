"""
    @filenam    database.py
    @author     Francis T

    This file contains the utility functions for interacting with the
    database through SQLAlchemy's ORM.

"""
import logging
import time

from collections import Iterable
from sqlalchemy import create_engine, event, and_
from sqlalchemy.orm import sessionmaker

from database.models import *
from datetime import date, time, datetime

DEFAULT_DB_NAME = "mysql+mysqldb://root:test@localhost/sjcmpc"
module_logger = logging.getLogger("main.database")

class SjcmpcDatabase:
    def __init__(self, db_name=DEFAULT_DB_NAME):
        self.engine = create_engine(db_name)

        event.listen(self.engine, 'connect', self.on_connect)
        DBSession = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)

        # Current db session
        self.db_session = DBSession()

    def close_session(self):
        try:
            self.db_session.close()
        except Exception as e:
            print(e)
            return False
        return True

    # Required in order to add foreign keys constraints
    def on_connect(self, conn, record):
        # conn.execute('pragma foreign_keys=ON')
        return

    # Executes each test case
    def tearDown(self):
        Base.metadata.drop_all(self.engine)

    ##********************************##
    ##          Utilities             ##
    ##******************************* ##
    # @desc     Adds a record
    # @return   True if successful, otherwise False
    def add(self, row):
        try:
            self.db_session.add(row)
            self.db_session.commit()
        except Exception as e:
            print(e)
            return False
        return True

    # @desc     Inserts if record non-existing, update if otherwise
    # @return   True if successful, otherwise False
    def insert_or_update(self, obj):
        try:
            self.db_session.merge(obj)
            self.db_session.commit()
        except Exception as e:
            print(e)
            return False
        return True

    # @desc     Gets a record
    # @return   True if successful, otherwise False
    def get(self, field, result):
        if result is not None:

            # If the result is already a list, we can return it immediately
            if type(result) is list:
                return result

            # If it is an iterable, transform it into a Python list
            if isinstance(result, Iterable):
                return result.all()

            # Otherwise, encapsulate it in a Python list
            return [ result ]

        print("Get: Non-existing {}.".format(field))
        return False

    # @desc     Deletes a record
    # @return   True if successful, otherwise False
    def delete(self, obj):
        try:
            self.db_session.delete(obj)
            self.db_session.commit()
        except Exception as e:
            print(e)
            return False

        return True

    ###  Departments Table Queries   ###
    def add_department(self, dept_name, desc=""):
        department = Departments(dept_name=dept_name, desc=desc)
        return self.insert_or_update(department)

    def get_departments(self, dept_id=None,
                              dept_name=None,
                              desc=None):
        query = self.db_session.query(Departments)
        if dept_id != None:
            query = query.filter(Departments.id == dept_id)
        if dept_name != None:
            query = query.filter(Departments.dept_name == dept_name)

        return self.get("Department", query)

    def remove_department(self, dept_id=None):
        match = self.get_departments(dept_id=dept_id)
        if (len(match) <= 0):
            return True

        return self.delete(match[0])

    ###  Jobs Table Queries

    def add_job(self, job_name, dept_id, desc=""):
        job = Jobs(job_name=job_name, desc=desc, dept_id=dept_id)
        return self.insert_or_update(job)

    def get_jobs(self, job_id=None,
                       job_name=None,
                       desc=None,
                       dept_id=None):
        query = self.db_session.query(Jobs)
        if job_id != None:
            query = query.filter(Jobs.id == job_id)
        if job_name != None:
            query = query.filter(Jobs.job_name == job_name)
        if dept_id != None:
            query = query.filter(Jobs.dept_id == dept_id)

        return self.get("Job", query)

    def remove_job(self, job_id=None):
        match = self.get_jobs(job_id=job_id)
        if (len(match) <= 0):
            return True

        return self.delete(match[0])

    ###  Employees Table Queries
    def add_employee(self, last_name, first_name, dept_id, sex, 
                     birth_date, location, hire_date, 
                     employee_id=None, middle_name="", 
                     tel_no="", mobile_no=""):
        employee = Employees(last_name=last_name, 
                             first_name=first_name,
                             middle_name=middle_name,
                             dept_id=dept_id,
                             sex=sex,
                             birth_date=birth_date,
                             location=location,
                             hire_date=hire_date,
                             tel_no=tel_no,
                             mobile_no=mobile_no)
        
        if employee_id != None:
            employee.id = employee_id

        return self.insert_or_update(employee)

    def get_employees(self, employee_id=None,
                            last_name=None,
                            first_name=None,
                            middle_name=None,
                            dept_id=None,
                            sex=None,
                            location=None,
                            hired_before=None,
                            hired_after=None):
        query = self.db_session.query(Employees)
        if employee_id != None:
            query = query.filter(Employees.id == employee_id)
        if last_name != None:
            query = query.filter(Employees.last_name.like("%" + last_name + "%"))
        if first_name != None:
            query = query.filter(Employees.first_name.like("%" + first_name + "%"))
        if middle_name != None:
            query = query.filter(Employees.middle_name.like("%" + middle_name + "%"))
        if dept_id != None:
            query = query.filter(Employees.dept_id == dept_id)
        if sex != None:
            query = query.filter(Employees.sex == sex)
        if location != None:
            query = query.filter(Employees.location.like("%" + location + "%"))
        if hired_before != None:
            query = query.filter(Employees.hire_date <= hired_before)
        if hired_after != None:
            query = query.filter(Employees.hire_date >= hired_after)

        return self.get("Employee", query)

    def remove_employee(self, employee_id=None):
        match = self.get_employees(employee_id=employee_id)
        if (len(match) <= 0):
            return True

        return self.delete(match[0])

    ###  Employee Badge Table Queries

    def add_badge(self, serial_no, employee_id, pay_type=PayTypes.DAILY):
        badge = EmployeeBadges(serial_no=serial_no, employee_id=employee_id, pay_type=pay_type)
        return self.insert_or_update(badge)

    def get_badges(self, badge_id=None,
                         serial_no=None,
                         employee_id=None,
                         pay_type=None):
        query = self.db_session.query(EmployeeBadges)
        if badge_id != None:
            query = query.filter(EmployeeBadges.id == badge_id)
        if serial_no != None:
            query = query.filter(EmployeeBadges.serial_no == serial_no)
        if employee_id != None:
            query = query.filter(EmployeeBadges.employee_id == employee_id)
        if pay_type != None:
            query = query.filter(EmployeeBadges.pay_type == pay_type)

        return self.get("Badge", query)

    def remove_badge(self, badge_id=None):
        match = self.get_badges(badge_id=badge_id)
        if (len(match) <= 0):
            return True

        return self.delete(match[0])

    ###  Timesheet Table Queries

    def add_record(self, badge_id, job_id, date=None, 
                   time_started=None, time_finished=None, 
                   workday_offset=None, season_type=SeasonType.REGULAR ):

        # Check if there are existing unclosed records first
        matches = self.get_records(badge_id=badge_id, job_id=job_id,
                                   time_started_blank=True, time_finished_blank=True)
        if (len(matches) > 0):
            print("Record is still open")
            return False

        matches = self.get_records(badge_id=badge_id, job_id=job_id,
                                   time_started_blank=False, time_finished_blank=True)
        if (len(matches) > 0):
            print("Record is still open")
            return False

        record = TimesheetRecord(date=date,
                                 badge_id=badge_id,
                                 job_id=job_id,
                                 time_started=time_started,
                                 time_finished=time_finished,
                                 workday_offset=workday_offset,
                                 season_type=season_type)

        # Use the current date if no date is indicated
        if date == None:
            record.date = datetime(1,1,1).today()

        # Use the current time if no time_started is indicated
        # if time_started == None:
        #     record.time_started = datetime.datetime(1,1,1).now().time()

        return self.insert_or_update(record)

    def record_time_in(self, badge_id, job_id, record_id=None, time_in=None):
        matches = self.get_records(record_id=record_id,
                                   badge_id=badge_id,
                                   job_id=job_id,
                                   time_started_blank=True)

        if (len(matches) <= 0):
            return True
        
        record = matches[0]
        record.time_started = datetime(1,1,1).now().time()

        return self.insert_or_update(record)

    def record_time_out(self, badge_id, job_id, record_id=None, time_out=None):
        matches = self.get_records(record_id=record_id,
                                   badge_id=badge_id,
                                   job_id=job_id,
                                   time_started_blank=False,
                                   time_finished_blank=True)

        if (len(matches) <= 0):
            return True
        
        record = matches[0]
        record.time_finished = datetime(1,1,1).now().time()

        return self.insert_or_update(record)

    def get_records(self, record_id=None,
                          badge_id=None,
                          job_id=None,
                          time_started_before=None,
                          time_started_after=None,
                          time_started_blank=None,
                          time_finished_before=None,
                          time_finished_after=None,
                          time_finished_blank=None,
                          season_type=None):

        query = self.db_session.query(TimesheetRecord)
        if record_id != None:
            query = query.filter(TimesheetRecord.id == record_id)
        if badge_id != None:
            query = query.filter(TimesheetRecord.badge_id == badge_id)
        if job_id != None:
            query = query.filter(TimesheetRecord.job_id == job_id)

        if (time_started_blank == False) or (time_started_blank == None):
            if time_started_before != None:
                query = query.filter(TimesheetRecord.time_started <= time_started_before)
            if time_started_after != None:
                query = query.filter(TimesheetRecord.time_started >= time_started_after)

        else:
            query = query.filter(TimesheetRecord.time_started == None)

        if (time_finished_blank == False) or (time_finished_blank == None):
            if time_finished_before != None:
                query = query.filter(TimesheetRecord.time_finished <= time_finished_before)
            if time_finished_after != None:
                query = query.filter(TimesheetRecord.time_finished >= time_finished_after)

        else:
            query = query.filter(TimesheetRecord.time_finished == None)

        if season_type != None:
            query = query.filter(TimesheetRecord.season_type == season_type)

        return self.get("Records", query)

    def remove_record(self, record_id=None):
        match = self.get_records(record_id=record_id)
        if (len(match) <= 0):
            return True

        return self.delete(match[0])

