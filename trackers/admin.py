from django.contrib import admin

#from users.models import User
from trackers.models import Tracker
from employees.models import Employee


admin.site.register(Tracker)

admin.site.register(Employee)

#admin.site.register(User)