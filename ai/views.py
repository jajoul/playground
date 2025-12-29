from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from django.http import HttpResponse
from .utils import generate_ai_response
from .models import AiChat, ChatMessage
import io
from xhtml2pdf import pisa
from django.template.loader import get_template

# Create your views here.
def home(request):
    return render(request,'ai/home.html')


class AiChatView(View):
    def get(self,request, chat_id=None):
        chats = AiChat.objects.all()
        conversation = []
        current_chat = None
        subject = None
        first_bot_name = None
        second_bot_name = None

        if chat_id:
            current_chat = get_object_or_404(AiChat, pk=chat_id)
            conversation = ChatMessage.objects.filter(aichat=current_chat).order_by('created_at')
            subject = current_chat.subject
            first_bot_name = current_chat.first_bot_name
            second_bot_name = current_chat.second_bot_name

        return render(request,'ai/aichat.html', {
            'chats': chats, 
            'conversation': conversation, 
            'current_chat': current_chat,
            'subject': subject,
            'first_bot_name': first_bot_name,
            'second_bot_name': second_bot_name
        })
    
    def post(self,request):
        subject=request.POST.get('subject')
        first_bot_name=request.POST.get('first_bot_name')
        second_bot_name=request.POST.get('second_bot_name')
        
        if first_bot_name==second_bot_name:
            chats = AiChat.objects.all()
            return render(request,'ai/aichat.html',{'error':'Bot names cannot be the same', 'chats': chats})
        
        ai_chat = AiChat.objects.create(subject=subject, first_bot_name=first_bot_name, second_bot_name=second_bot_name)
        
        conversation_history = []
        
        # Simulating a few turns of conversation
        for i in range(5): # Generate 5 turns (10 messages total, 5 from each bot)
            # Bot 1 speaks
            bot_one_response = generate_ai_response(
                subject=subject,
                bot_name=first_bot_name,
                colleague_name=second_bot_name,
                history=conversation_history
            )
            ChatMessage.objects.create(aichat=ai_chat, role=first_bot_name, content=bot_one_response)
            conversation_history.append({'role': first_bot_name, 'content': bot_one_response})
            
            # Bot 2 speaks (responding to Bot 1's last message)
            bot_two_response = generate_ai_response(
                subject=subject,
                bot_name=second_bot_name,
                colleague_name=first_bot_name,
                history=conversation_history
            )
            ChatMessage.objects.create(aichat=ai_chat, role=second_bot_name, content=bot_two_response)
            conversation_history.append({'role': second_bot_name, 'content': bot_two_response})

        # Generate PDF from the conversation
        conversation_messages = ChatMessage.objects.filter(aichat=ai_chat).order_by('created_at')
        
        template = get_template('ai/chat_pdf_template.html')
        context = {
            'subject': subject,
            'first_bot_name': first_bot_name,
            'second_bot_name': second_bot_name,
            'conversation_messages': conversation_messages,
        }
        html = template.render(context)
        result_file = io.BytesIO()
        pisa_status = pisa.CreatePDF(
            html,                # the HTML to convert
            dest=result_file)    # file handle to receive result

        if pisa_status.err:
            return HttpResponse('We had some errors <pre>%s</pre>' % html)
        
        response = HttpResponse(result_file.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="chat_{ai_chat.id}.pdf"'
        return response


def download_pdf(request, chat_id):
    current_chat = get_object_or_404(AiChat, pk=chat_id)
    conversation_messages = ChatMessage.objects.filter(aichat=current_chat).order_by('created_at')
    
    template = get_template('ai/chat_pdf_template.html')
    context = {
        'subject': current_chat.subject,
        'first_bot_name': current_chat.first_bot_name,
        'second_bot_name': current_chat.second_bot_name,
        'conversation_messages': conversation_messages,
    }
    html = template.render(context)
    result_file = io.BytesIO()
    pisa_status = pisa.CreatePDF(
        html,                # the HTML to convert
        dest=result_file)    # file handle to receive result

    if pisa_status.err:
        return HttpResponse('We had some errors <pre>%s</pre>' % html)
    
    response = HttpResponse(result_file.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="chat_{current_chat.id}.pdf"'
    return response