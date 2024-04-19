from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create-listing", views.create_listing, name="create listing"),
    path("listings/<int:listing_id>", views.detailed_listing, name="see listing"),
    path("listings/<int:listing_id><str:message>", views.detailed_listing, name="see listing"),
    path("listings/<int:listing_id><str:message>/<int:comment_error>", views.detailed_listing, name="see listing"),
    path("listings/<int:listing_id>/bid", views.bid, name="bid listing"),
    path("listings/<int:listing_id>/add-watchlist", views.add_watchlist, name="add to watchlist"),
    path("listings/<int:listing_id>/remove-watchlist", views.remove_watchlist, name="remove from watchlist"),
    path("listings/<int:listing_id>/close", views.close_auction, name="close auction"),
    path("listings/<int:listing_id>/comment", views.comment, name="post comment"),
    path("listings/<int:listing_id>/like", views.like, name="like comment"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
