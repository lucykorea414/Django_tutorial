from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseNotAllowed
from django.utils import timezone
from .models import Question, Answer
from .forms import QuestionForm, AnswerForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

def index(request):
    page = request.GET.get('page', '1') #페이지
    question_list = Question.objects.order_by('-create_date')
    paginator = Paginator(question_list, 10) #페이지당 10개씩 보여주기

    page_obj = paginator.get_page(page)
    context = {'question_list': page_obj}
    return render(request, 'pybo/question_list.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {'question' : question}
    return render(request, 'pybo/question_detail.html', context)

@login_required(login_url='common:login')
def answer_create(request, question_id):
    """
    pybo 답변등록
    """
    question = get_object_or_404(Question, pk=question_id)
    if(request.method == 'POST'):
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user #author 속성에 로그인 계정 저장
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        return HttpResponseNotAllowed('Only POST is possible.')
    context = {'question': question, 'form': form}
    return render(request, 'pybo/question_detail.html', context)
    # question_create와 같은 방법으로 AnswerForm을 이용하도록 변경했다. 하지만 답변 등록은 POST 방식만 사용되기 때문에 GET 방식으로 요청할 경우에는 HttpResponseNotAllowed 오류가 발생하도록 했다.

@login_required(login_url='common:login')
def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid(): #폼이 유효하다면
            question = form.save(commit=False) #임시저장하여 question 객체를 리턴받는다.
            question.author = request.user #author 속성에 로그인 계정 저장
            question.create_date = timezone.now() #실제 저장을 위해 작성일지를 설정한다.
            question.save() #데이터를 실제로 저장한다.
            return redirect('pybo:index')
    else:
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'pybo/question_form.html', {'form': form})
