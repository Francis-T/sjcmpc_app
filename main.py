#!/usr/bin/env python

from database.database import SjcmpcDatabase as SDB
from database.models import *
from mfc_reader import MfcReader
from core import SJCMPCCore, SJCMPCEmployee

core = SJCMPCCore()

def register_employee(sdb):
    # Register the Employee first
    employee_id_input = input("Enter Employee ID (leave blank to autogenerate): ")
    last_name = input("Enter Last Name: ")
    first_name = input("Enter First Name: ")
    middle_name = input("Enter Middle Name: ")
    sex = input("Enter Sex: ")
    birth_date = input("Enter Birth Date: ")
    location = input("Enter Location: ")
    hire_date = input("Enter Hire Date: ")
    tel_no = input("Enter Tel No: ")
    mobile_no = input("Enter Mobile No: ")

    employee_id = None
    if employee_id_input != "":
        employee_id = int(employee_id_input)

    # dept_matches = sdb.get_departments(dept_name=dept_name)
    # if len(dept_matches) <= 0:
    #     print("Invalid department name: {}".format(dept_name))
    #     return False
    dept_id = choose_department(sdb)
    if dept_id < 0:
        print("Failed to choose a department")
        return -1

    employee = SJCMPCEmployee()
    employee.id          = employee_id
    employee.last_name   = last_name
    employee.first_name  = first_name
    employee.dept_id     = dept_id
    employee.sex         = sex
    employee.birth_date  = birth_date
    employee.location    = location
    employee.hire_date   = hire_date
    employee.middle_name = middle_name
    employee.tel_no      = tel_no
    employee.mobile_no   = mobile_no

    return core.register_employee(employee)

def choose_department(sdb):
    dept_list = core.list_departments()
    if len(dept_list) <= 0:
        print("No departments found. Please register departments first. ")
        return -1

    count = 0
    for dept in dept_list:
        print("  ({}) {}".format(count, dept.dept_name))
        count += 1
    
    dept_list_idx = -1
    try:
        dept_list_idx = int(input("Select Department: "))
    except Exception as e:
        print("Invalid department index")
        return -1

    if (dept_list_idx < 0) or (dept_list_idx >= len(dept_list)):
        print("Invalid department index")
        return -1

    return dept_list[dept_list_idx].id

def choose_job(sdb):
    job_list = core.list_jobs()
    if len(job_list) <= 0:
        print("No jobs found. Please register jobs first. ")
        return -1

    count = 0
    for job in job_list:
        print("  ({}) {}".format(count, job.job_name))
        count += 1
    
    job_list_idx = -1
    try:
        job_list_idx = int(input("Select Job: "))
    except Exception as e:
        print("Invalid job index")
        return -1

    if (job_list_idx < 0) or (job_list_idx >= len(job_list)):
        print("Invalid job index")
        return -1

    return job_list[job_list_idx].id

def choose_employee(sdb):
    employee_list = core.list_employees()
    if len(employee_list) <= 0:
        print("No employees found. Please register employees first. ")
        return -1

    count = 0
    for employee in employee_list:
        print("  ({}) {}, {}".format(count, employee.last_name, employee.first_name))
        count += 1
    
    employee_list_idx = -1
    try:
        employee_list_idx = int(input("Select Employee: "))
    except Exception as e:
        print("Invalid employee index")
        return -1

    if (employee_list_idx < 0) or (employee_list_idx >= len(employee_list)):
        print("Invalid employee index")
        return -1

    return employee_list[employee_list_idx].id


def register_badge(sdb, uid, employee_id):
    pay_type_str = input("Enter pay type [DY/PR]: ")
    pay_type = PayTypes.DAILY
    if pay_type_str == "PR":
        pay_type = PayTypes.PIECE_RATE

    return core.register_badhe(uid, employee_id, pay_type)

###  Text-based User Interface  ###
def view_timesheet():
    result = True
    print("Timesheet")
    sdb = SDB()

    record_list = core.list_records()
    count = 1
    print("----------------------------------------------------------------------------------- ---  --  -")
    for record in record_list:
        print("{} | {} | {} | {} | {} | {} | {} ".format(record.id,
                                                             record.date,
                                                             (record.badge.employee.last_name + ", " + record.badge.employee.first_name),
                                                             record.job.job_name,
                                                             record.time_started,
                                                             record.time_finished,
                                                             record.season_type))
        print("----------------------------------------------------------------------------------- ---  --  -")

    return


def view_departments():
    result = True
    print("List of Departments")
    print("-------------------")

    sdb = SDB()

    dept_list = core.list_departments()
    count = 1
    for dept in dept_list:
        print("({}) {}".format(count, dept.dept_name))
        print("    Desc: {}".format(dept.desc))
        print("    Members:")
        [ print("     - " + member.last_name + ", " + member.first_name) for member in dept.members ]
        print("    Roles:")
        [ print("     - " + role.job_name) for role in dept.roles ]
        print("")

        count += 1

    return

def view_jobs():
    result = True
    print("List of Jobs")
    print("------------")

    sdb = SDB()

    job_list = core.list_jobs()
    count = 1
    for job in job_list:
        print("({}) {}".format(count, job.job_name))
        print("    Dept: {}".format(job.dept.dept_name))
        print("    Desc: {}".format(job.desc))
        print("")

        count += 1

    return

def view_employees():
    result = True
    print("List of Employees")
    print("-----------------")

    sdb = SDB()

    employee_list = core.list_employees()
    count = 1
    for employee in employee_list:
        print("({}) {}, {} {}".format(count, employee.last_name, employee.first_name, employee.middle_name))
        print("    Dept: {}".format(employee.dept.dept_name))
        print("    Sex: {}, Birth Date: {}, Location: {}".format(employee.sex, employee.birth_date, employee.location))
        print("    Tel: {}, Mobile: {}".format(employee.tel_no, employee.mobile_no))
        print("    Hired: {}".format(employee.hire_date))
        print("    Badges: ")
        [ print("     - {} ({})".format(badge.serial_no, badge.pay_type)) for badge in employee.badges ]
        print("")

        count += 1

    return

def add_new_departments():
    result = True

    sdb = SDB()
    while True:
        print("Add a new department")
        print("--------------------")
        dept_name = input("Enter new dept name: ")
        desc = input("Enter dept description: ")

        result = core.add_new_department(dept_name, desc)
        if result == False:
            choice = input("Add Department Failed. Try again? [Y/N] ")
            if choice == "Y":
                continue
            else:
                break

        choice = input("Add more departments? [Y/N] ")
        if choice == "Y":
            continue
        else:
            break

    return


def add_new_jobs():
    result = True

    sdb = SDB()
    while True:
        print("Add a new job")
        print("-----------------")
        job_name = input("Enter new job name: ")
        desc = input("Enter job description: ")

        dept_id = choose_department(sdb)
        if dept_id < 0:
            print("Failed to choose a department")
            return

        result = core.add_new_job(job_name, dept_id, desc)
        if result == False:
            choice = input("Add Job Failed. Try again? [Y/N] ")
            if choice == "Y":
                continue
            else:
                break

        choice = input("Add more jobs? [Y/N] ")
        if choice == "Y":
            continue
        else:
            break

    return

def remove_jobs():
    result = True

    sdb = SDB()
    while True:
        print("Remove existing Jobs")
        print("--------------------")
        job_name = input("Enter job name: ")

        job_matches = core.list_jobs_by_name(job_name)
        if len(job_matches) <= 0:
            print("Job name does not exist: {}".format(job_name))
            choice = input("Remove Job Failed. Try again? [Y/N] ")
            if choice == "Y":
                continue
            else:
                break

        job_id = job_matches[0].id
        result = sdb.remove_job(job_id)
        if result == False:
            choice = input("Remove Job Failed. Try again? [Y/N] ")
            if choice == "Y":
                continue
            else:
                break

        choice = input("Remove more jobs? [Y/N] ")
        if choice == "Y":
            continue
        else:
            break

    return

def remove_departments():
    result = True

    sdb = SDB()
    while True:
        print("Remove existing Departments")
        print("---------------------------")
        dept_name = input("Enter dept name: ")

        dept_matches = core.list_departments_by_name(dept_name)
        if len(dept_matches) <= 0:
            print("Dept name does not exist: {}".format(dept_name))
            choice = input("Remove Dept Failed. Try again? [Y/N] ")
            if choice == "Y":
                continue
            else:
                break

        dept_id = dept_matches[0].id
        result = sdb.remove_department(dept_id)
        if result == False:
            choice = input("Remove Department Failed. Try again? [Y/N] ")
            if choice == "Y":
                continue
            else:
                break

        choice = input("Remove more departments? [Y/N] ")
        if choice == "Y":
            continue
        else:
            break

    return
    

def card_deactivation():
    result = True
    print("Card Deactivation")
    print("-----------------")

    sdb = SDB()
    while True:
        print("Swipe card...")
        mfcrd = MfcReader()
        uid = mfcrd.read_card()

        registered_badges = core.list_badges()
        target_badge = None
        for badge in registered_badges:
            if badge.serial_no == uid:
                print("Card found")
                target_badge = badge

        if target_badge == None:
            print("Card not found")
            choice = input("Try a different card? [Y/N] ")
            if choice == "Y":
                continue
            else:
                break

        result = sdb.remove_badge(target_badge.id)
        if result == False:
            choice = input("Deactivation Failed. Try again? [Y/N] ")
            if choice == "Y":
                continue
            else:
                break

        choice = input("Deactivate more cards? [Y/N] ")
        if choice == "Y":
            continue
        else:
            break

    return

def card_activation():
    result = True
    print("Card Activation")
    print("---------------")

    sdb = SDB()
    while True:
        print("Swipe card...")
        mfcrd = MfcReader()
        uid = mfcrd.read_card()

        registered_badges = core.list_badges()
        for badge in registered_badges:
            if badge.serial_no == uid:
                print("Error: Card already activated")
                result = False

        if result == False:
            choice = input("Try a different card? [Y/N] ")
            if choice == "Y":
                continue
            else:
                break

        employee_id = -1
        choice = input("Register to existing user? [Y/N] ")
        if choice == "N":
            employee_id = register_employee(sdb)
            if employee_id < 0:
                choice = input("Activation Failed. Try again? [Y/N] ")
                if choice == "Y":
                    continue
                else:
                    break
        else:
            employee_id = choose_employee(sdb)
            if employee_id < 0:
                choice = input("Invalid employee selection. Try again? [Y/N] ")
                if choice == "Y":
                    continue
                else:
                    break

        result = register_badge(sdb, uid, employee_id)
        if result == False:
            choice = input("Activation Failed. Try again? [Y/N] ")
            if choice == "Y":
                continue
            else:
                break

        print("Card Activated!")
        choice = input("Activate more cards? [Y/N] ")
        if choice == "Y":
            continue
        else:
            break


    return

def admin_mode():
    commands_tbl = [
        { "cmd_id" :  "1", "cmd_text" : "Activate a Card",    "func" : card_activation },
        { "cmd_id" :  "2", "cmd_text" : "Deactivate a Card",  "func" : card_deactivation },
        { "cmd_id" :  "3", "cmd_text" : "View Timesheet",     "func" : view_timesheet },
        { "cmd_id" : "20", "cmd_text" : "View Jobs",          "func" : view_jobs },
        { "cmd_id" : "21", "cmd_text" : "View Departments",   "func" : view_departments },
        { "cmd_id" : "22", "cmd_text" : "View Employees",     "func" : view_employees },
        { "cmd_id" : "40", "cmd_text" : "Add Jobs",           "func" : add_new_jobs },
        { "cmd_id" : "41", "cmd_text" : "Add Departments",    "func" : add_new_departments },
        { "cmd_id" : "42", "cmd_text" : "Remove Jobs",        "func" : remove_jobs },
        { "cmd_id" : "43", "cmd_text" : "Remove Departments", "func" : remove_departments },
        # { "cmd_id" : "44", "cmd_text" : "Remove Employees",   "func" : remove_employees },
        { "cmd_id" :  "4", "cmd_text" : "Quit",               "func" : None },
    ]

    while True:
        print("=======================")
        print("Administrator Dashboard")
        print("-----------------------")
        for cmd in commands_tbl:
            print("  ({}) {}".format(cmd['cmd_id'], cmd['cmd_text']))

        user_cmd = input("> ")
        # Cycle through all the commands in the table
        target_cmd = None
        for cmd in commands_tbl:
            if cmd['cmd_id'] == user_cmd:
                target_cmd = cmd

        if target_cmd['func'] == None:
            print("Closing Admin Dashboard.")
            break

        # Execute the command if it matches
        target_cmd['func']()
        
    return

def normal_mode():
    result = True

    while True:
        print("Swipe card...")
        mfcrd = MfcReader()
        uid = mfcrd.read_card()

        sdb = SDB()

        # Check if the card is valid
        registered_badges = core.list_badges()
        target_badge = None
        for badge in registered_badges:
            if badge.serial_no == uid:
                print("Card found")
                target_badge = badge

        if target_badge == None:
            choice = input("No badges matched. Try again? [Y/N] ")
            if choice == "Y":
                continue
            else:
                break

        # Check whether an open record still exists for this badge
        matches = core.list_records_by_badge(target_badge.id, True, True)
        if (len(matches) > 0):
            record = matches[0]
            print("Timing in for open record")
            result = sdb.record_time_in(badge_id=record.badge_id,
                                        job_id=record.job_id,
                                        record_id=record.id)
            if result == False:
                choice = input("Time in Failed. Try again? [Y/N] ")
                if choice == "Y":
                    continue
                else:
                    break

            matched_records = sdb.get_records(record_id=record.id,
                                              badge_id=record.badge_id, 
                                              job_id=record.job_id)
            record = matched_records[0]
            print("Time in successful!")
            print("{}, {} | {} | {}".format(record.badge.employee.last_name,
                                            record.badge.employee.first_name,
                                            record.time_started,
                                            record.time_finished))

            choice = input("Continue Operation? [Y/N] ")
            if choice == "Y":
                continue
            else:
                break

        matches = core.list_records_by_badge(target_badge.id, False, True)
        if (len(matches) > 0):
            record = matches[0]
            print("Timing out for open record")
            result = sdb.record_time_out(badge_id=record.badge_id,
                                         job_id=record.job_id,
                                         record_id=record.id)
            if result == False:
                choice = input("Time out Failed. Try again? [Y/N] ")
                if choice == "Y":
                    continue
                else:
                    break

            matched_records = sdb.get_records(record_id=record.id,
                                              badge_id=record.badge_id, 
                                              job_id=record.job_id)
            record = matched_records[0]
            print("Time out successful!")
            print("{}, {} | {} | {}".format(record.badge.employee.last_name,
                                            record.badge.employee.first_name,
                                            record.time_started,
                                            record.time_finished))

            choice = input("Continue Operation? [Y/N] ")
            if choice == "Y":
                continue
            else:
                break

        # job_list = sdb.get_jobs()
        # if len(job_list) <= 0:
        #     print("No jobs found. Please register jobs first. ")
        #     break

        # count = 0
        # for job in job_list:
        #     print("  ({}) {}".format(count, job.job_name))
        #     count += 1
        # 
        # job_list_idx = int(input("Select Job: "))
        job_id = choose_job(sdb)
        if job_id < 0:
            choice = input("Failed to choose a job. Try again? [Y/N] ")
            if choice == "Y":
                continue
            else:
                break

        result = sdb.add_record(badge_id=target_badge.id, job_id=job_id)
        if result == False:
            choice = input("Add Record Failed. Try again? [Y/N] ")
            if choice == "Y":
                continue
            else:
                break

        choice = input("Continue Operation? [Y/N] ")
        if choice == "Y":
            continue
        else:
            break

    return

def main():
    commands_tbl = [
        { "cmd_id" :  "1", "cmd_text" : "Admin Mode",           "func" : admin_mode },
        { "cmd_id" :  "2", "cmd_text" : "Normal Mode",          "func" : normal_mode },
        { "cmd_id" :  "3", "cmd_text" : "Quit",                 "func" : None },
    ]

    while True:
        print("=====================================")
        print("Test Program w/ Database Connectivity")
        print("-------------------------------------")
        for cmd in commands_tbl:
            print("  ({}) {}".format(cmd['cmd_id'], cmd['cmd_text']))

        user_cmd = input("> ")
        # Cycle through all the commands in the table
        target_cmd = None
        for cmd in commands_tbl:
            if cmd['cmd_id'] == user_cmd:
                target_cmd = cmd

        if target_cmd['func'] == None:
            print("Closing Program.")
            break
            
        # Execute the command if it matches
        target_cmd['func']()
        print("\n")

    return

if __name__ == "__main__":
    main()

