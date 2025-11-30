from django.contrib import admin
from django.urls import include, path

from codex.views import PlayerSearchView

urlpatterns = [
    path('', PlayerSearchView.as_view(), name='player-search'),
    path('admin/', admin.site.urls),
    path('api/codex/', include('codex.urls')),
]
