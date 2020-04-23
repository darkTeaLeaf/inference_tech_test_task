from rest_framework import routers

from chat.views import UserViewSet, MessageViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'users/(?P<user_id>\d+)/messages', MessageViewSet, basename='User')

urlpatterns = router.urls
