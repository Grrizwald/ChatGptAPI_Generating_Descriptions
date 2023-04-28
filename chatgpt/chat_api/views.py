from django.shortcuts import render, redirect
from django.contrib import messages
import openai
from .models import Past
from django.core.paginator import Paginator

def home(request):
    if request.method == "POST":
        question = request.POST['question']
        past_responses = request.POST['past_responses']

        # Check if question already exists in database
        if Past.objects.filter(question=question).exists():
            past_responses = Past.objects.get(question=question).answer
            messages.warning(request, f'Odpowiedź na pytanie "{question}" została już udzielona.')

        else:
            openai.api_key="#CHAT_GPT_API_KEY"
            openai.Model.list()
            try:
                response = openai.Completion.create(
                    model="text-davinci-003",
                    prompt=question,
                    temperature=0,
                    max_tokens=450,
                    top_p=1.0,
                    frequency_penalty=0.0,
                    presence_penalty=0.0
                )
                response = (response["choices"][0]["text"]).strip()
                if "1new1" in past_responses:
                    past_responses = f"<span style='color: green;'>[Dodano Nowy Rekord]</span><br/><br/>{response}"
                else:
                    past_responses = f"{past_responses}<br/><br/>{response[:500]}"

                record = Past(question=question, answer=response)
                record.save()

                return render(request, 'home.html', {"question":question, "response":response, "past_responses":past_responses})
            except Exception as e:
                return render(request, 'home.html', {"question":question, "response":e, "past_responses":past_responses})
        
        return render(request, 'home.html', {"question":question, "response":past_responses, "past_responses":past_responses})
    
    return render(request, 'home.html', {})

def past(request):
    p = Paginator(Past.objects.all(),5)
    page = request.GET.get('page')
    pages = p.get_page(page)

    past = Past.objects.all()

    nums = "a" * pages.paginator.num_pages

    return render(request, 'past.html', {"past":past,"pages":pages,"nums":nums}) 



def delete_past(request, Past_id):
    past = Past.objects.get(pk=Past_id)
    past.delete()
    messages.success(request, "Delete ANS and QUE done!")
    return redirect('past')
