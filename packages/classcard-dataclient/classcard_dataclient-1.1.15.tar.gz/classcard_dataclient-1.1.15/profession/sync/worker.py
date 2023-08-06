import time
from sync.student import StudentSync
from sync.teacher import TeacherSync
from sync.clas import ClassSync
from sync.classroom import ClassroomSync
from sync.course2 import CourseSyncV2
from sync.course import CourseSyncV1
from sync.subject import SubjectSync
from sync.school import SchoolSync
from utils.loggerutils import logging

logger = logging.getLogger(__name__)

WALKING_MAP = {"3552": False, "3490": False}


def start_sync_v1():
    special_number = None
    special_number_list = ["3490", "3532"]
    logger.info(">>>Start profession sync")
    school_sync = SchoolSync(special_number=special_number)
    school_sync.start()
    index, total = 0, len(school_sync.school_map)
    for name, number in school_sync.school_map.items():
        index += 1
        logger.info(">>> Start Sync {} Data, Process {}/{}".format(name, index, total))
        print(">>> Start Sync {} Data, Process {}/{}".format(name, index, total))
        if special_number_list and number not in special_number_list:
            continue
        is_walking = WALKING_MAP.get(number, True)
        school_info = {"school_name": name, "school_number": number}
        teacher_sync = TeacherSync(**school_info)
        teacher_sync.start()
        class_sync = ClassSync(**school_info)
        class_sync.start()
        student_sync = StudentSync(class_entrance=class_sync.class_entrance, **school_info)
        student_sync.start()
        classroom_sync = ClassroomSync(**school_info)
        classroom_sync.is_walking = is_walking
        classroom_sync.classroom_class = class_sync.classroom_class
        classroom_sync.start()
        subject_sync = SubjectSync(**school_info)
        subject_sync.start()
        course_sync = CourseSyncV1(**school_info)
        course_sync.is_walking = is_walking
        course_sync.classroom_map = classroom_sync.id_num_map
        course_sync.start()


def start_sync_v2():
    special_number = None
    special_number_list = ["3490"]
    logger.info(">>>Start profession sync")
    school_sync = SchoolSync(special_number=special_number)
    school_sync.start()
    index, total = 0, len(school_sync.school_map)
    for name, number in school_sync.school_map.items():
        index += 1
        logger.info(">>> Start Sync {} Data, Process {}/{}".format(name, index, total))
        print(">>> Start Sync {} Data, Process {}/{}".format(name, index, total))
        if special_number_list and number not in special_number_list:
            continue
        is_walking = WALKING_MAP.get(number, True)
        school_info = {"school_name": name, "school_number": number}
        teacher_sync = TeacherSync(**school_info)
        teacher_sync.start()
        class_sync = ClassSync(**school_info)
        class_sync.start()
        student_sync = StudentSync(class_entrance=class_sync.class_entrance, **school_info)
        student_sync.start()
        classroom_sync = ClassroomSync(**school_info)
        classroom_sync.is_walking = is_walking
        classroom_sync.classroom_class = class_sync.classroom_class
        classroom_sync.start()
        subject_sync = SubjectSync(**school_info)
        subject_sync.start()
        course_sync = CourseSyncV2(**school_info)
        course_sync.is_walking = is_walking
        course_sync.classroom_map = classroom_sync.id_num_map
        course_sync.start()
        time.sleep(5)


def init_basic_data():
    special_number = None
    special_number_list = ["3550"]
    logger.info(">>>Start profession sync")
    school_sync = SchoolSync(special_number=special_number)
    school_sync.start()
    index, total = 0, len(school_sync.school_map)
    for name, number in school_sync.school_map.items():
        index += 1
        logger.info(">>> Start Sync {} Data, Process {}/{}".format(name, index, total))
        print(">>> Start Sync {} Data, Process {}/{}".format(name, index, total))
        if special_number_list and number not in special_number_list:
            continue
        is_walking = WALKING_MAP.get(number, True)
        school_info = {"school_name": name, "school_number": number}
        teacher_sync = TeacherSync(**school_info)
        teacher_sync.start()
        class_sync = ClassSync(**school_info)
        class_sync.start()
        student_sync = StudentSync(class_entrance=class_sync.class_entrance, **school_info)
        student_sync.start()
