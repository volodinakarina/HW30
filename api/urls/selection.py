from django.urls import path

from api.views import selection

urlpatterns = [
    path('selection/', selection.SelectionListView.as_view()),
    path('selection/<int:pk>/', selection.SelectionDetailView.as_view()),
    path('selection/create/', selection.SelectionCreateView.as_view()),
    path('selection/<int:pk>/update/', selection.SelectionUpdateView.as_view()),
    path('selection/<int:pk>/delete/', selection.SelectionDeleteView.as_view()),
]