#!/usr/bin/env python

from database.database import SjcmpcDatabase
from database.models import *
from mfc_reader import MfcReader

class SJCMPCCore():
    def __init__(self):
        self.db = SjcmpcDatabase()
        return

    def register_employee(self, employee=None):
        result = self.db.add_employee( employee_id = employee.id,
                                       last_name   = employee.last_name,
                                       first_name  = employee.first_name,
                                       dept_id     = employee.dept_id,
                                       sex         = employee.sex,
                                       birth_date  = employee.birth_date,
                                       location    = employee.location,
                                       hire_date   = employee.hire_date,
                                       middle_name = employee.middle_name,
                                       tel_no      = employee.tel_no,
                                       mobile_no   = employee.mobile_no )
        if result == False:
            return -1

        last_added = self.db.get_employees( last_name   = employee.last_name, 
                                            first_name  = employee.first_name, 
                                            middle_name = employee.middle_name )
        if len(last_added) <= 0:
            print("Error: No employees found ")
            return -1

        return last_added[0].id

    def register_badge(self, card_uid, employee_id, pay_type):
        return self.db.add_badge(serial_no   = card_uid, 
                                 employee_id = employee_id,
                                 pay_type    = pay_type)

    def add_new_department(self, dept_name, desc):
        return self.db.add_department(dept_name, desc)

    def add_new_job(self, job_name, dept_id, desc):
        return self.db.add_job(job_name, dept_id, desc)

    def list_departments(self):
        record_list = self.db.get_departments()
        if len(record_list) <= 0:
            print("No departments found. ")
            return []

        return record_list

    def list_departments_by_name(self, dept_name):
        record_list = self.db.get_departments(dept_name=dept_name)
        if len(record_list) <= 0:
            print("No departments found. ")
            return []

        return record_list

    def list_employees(self):
        record_list = self.db.get_employees()
        if len(record_list) <= 0:
            print("No employees found. ")
            return []

        return record_list

    def list_jobs(self):
        record_list = self.db.get_jobs()
        if len(record_list) <= 0:
            print("No jobs found. ")
            return []

        return record_list

    def list_jobs_by_name(self, job_name):
        record_list = self.db.get_jobs(job_name=job_name)
        if len(record_list) <= 0:
            print("No jobs found. ")
            return []

        return record_list

    def list_records(self):
        record_list = self.db.get_records()
        if len(record_list) <= 0:
            print("No records found. ")
            return []

        return record_list

    # TODO Replace this with a varargs instead
    def list_records_by_badge(self, badge_id, time_started_blank, time_finished_blank):
        record_list = self.db.get_records(badge_id            = badge_id,
                                          time_started_blank  = time_started_blank, 
                                          time_finished_blank = time_finished_blank)

        if len(record_list) <= 0:
            print("No records found. ")
            return []

        return record_list

    def list_badges(self):
        record_list = self.db.get_badges()
        if len(record_list) <= 0:
            print("No badges found. ")
            return []

        return record_list

class SJCMPCEmployee():
    def __init__(self):
        self.id = None
        self.last_name = None
        self.first_name = None
        self.middle_name = None
        self.sex = None
        self.birth_date = None
        self.location = None
        self.hire_date = None
        self.tel_no = None
        self.mobile_no = None
        self.dept_id = None
        return


