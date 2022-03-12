from django.urls import path, include
from .views import Index, PostCreate, PostDelete, PostDetail, PostUpdate, PostList, Login, Logout, SignUp

app_name = 'myapp'

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('post_create/', PostCreate.as_view(), name='post_create'),
    path('post_detail/<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('post_update/<int:pk>/', PostUpdate.as_view(), name='post_update'),
    path('post_delete/<int:pk>/', PostDelete.as_view(), name='post_delete'),
    path('post_list/', PostList.as_view(), name='post_list'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('signup/', SignUp.as_view(), name='signup'),
]
