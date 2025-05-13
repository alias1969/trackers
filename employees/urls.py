from rest_framework.routers import DefaultRouter
from django.conf.urls.static import static

from config import settings

from employees.apps import EmployeesConfig
from employees.views import EmployeeViewSet

app_name = EmployeesConfig.name

router = DefaultRouter()
router.register("", EmployeeViewSet, basename="employee")

urlpatterns = []

urlpatterns += router.urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
