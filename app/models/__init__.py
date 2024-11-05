from .auth_user import *
from .course import *
from .instructor import *
from .notifications import *
from .payment import *
from .student import *
from .enrollment import *
from .profile import *

from ..database.main import engine

course.Base.metadata.create_all(bind=engine)
instructor.Base.metadata.create_all(bind=engine)
auth_user.Base.metadata.create_all(bind=engine)
notifications.Base.metadata.create_all(bind=engine)
payment.Base.metadata.create_all(bind=engine)
student.Base.metadata.create_all(bind=engine)
enrollment.Base.metadata.create_all(bind=engine)
profile.Base.metadata.create_all(bind=engine)