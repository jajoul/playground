#urls:
from django.urls import path
from .views import home, AiChatView, download_pdf

#patterns
urlpatterns=[
    path('',home,name='home'),
    path('chat/', AiChatView.as_view(), name='ai_chat'),
    path('chat/<int:chat_id>/', AiChatView.as_view(), name='ai_chat_detail'),
    path('chat/<int:chat_id>/download/', download_pdf, name='download_pdf'),
]