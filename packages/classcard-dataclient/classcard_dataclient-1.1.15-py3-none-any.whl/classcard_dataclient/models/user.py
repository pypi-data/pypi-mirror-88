from ..models.base import BaseModel
from ..utils.code import b64decode


class GenderSet(object):
    MALE = 'M'
    FEMALE = "F"

    MESSAGE = {
        MALE: "男",
        FEMALE: "女"
    }


class Teacher(BaseModel):

    def __init__(self, *args, **kwargs):
        self.uid = None
        self.number = None
        self.password = None
        self.name = None
        self.description = None
        self.birthday = None
        self.ecard = None
        self.email = None
        self.gender = GenderSet.MALE
        self.phone = None
        self.school = None
        super(Teacher, self).__init__(*args, **kwargs)

    @property
    def sso_data(self):
        data = {"birthday": self.birthday,
                "description": self.description,
                "ecard": self.ecard,
                "email": self.email,
                "gender": self.gender,
                "name": self.name,
                "number": self.number,
                "phone": self.phone,
                "password": self.password,
                "school": self.school
                }
        return data


class Student(BaseModel):

    def __init__(self, *args, **kwargs):
        self.uid = None
        self.number = None
        self.password = "MTIzNDU2"  # base64
        self.name = None
        self.description = None
        self.birthday = None
        self.ecard = None
        self.email = None
        self.gender = GenderSet.MALE
        self.phone = None
        self.classof = None
        self.graduateat = None
        self.class_name = None
        self.section = None
        self.school = None
        super(Student, self).__init__(*args, **kwargs)
        self.class_id = None

    @property
    def sso_data(self):
        data = {"birthday": self.birthday,
                "description": self.description,
                "ecard": self.ecard,
                "email": self.email,
                "gender": self.gender,
                "name": self.name,
                "number": self.number,
                "phone": self.phone,
                "password": self.password,
                "classof": self.classof,
                "graduateat": self.graduateat,
                "section": self.class_id or self.section}
        return data


class EduOrgUser(BaseModel):

    def __init__(self, *args, **kwargs):
        self.uid = None
        self.number = None
        self.password = None
        self.name = None
        self.description = None
        self.birthday = None
        self.outer_id = None
        self.email = None
        self.gender = GenderSet.MALE
        self.phone = None
        self.job = None
        super(EduOrgUser, self).__init__(*args, **kwargs)

    @property
    def sso_data(self):
        data = {"birthday": self.birthday,
                "description": self.description,
                "outer_id": self.outer_id,
                "email": self.email,
                "gender": self.gender,
                "name": self.name,
                "number": self.number,
                "phone": self.phone,
                "password": self.password,
                "job": self.job
                }
        return data
