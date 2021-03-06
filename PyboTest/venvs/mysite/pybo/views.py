from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.http import HttpResponseNotAllowed
from django.utils import timezone
from .models import Question, Answer
from .forms import QuestionForm, AnswerForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.db.models import Q
from django.views.generic import ListView
from itertools import chain
from django.contrib.auth.models import User
from django.db.models import F, Count
from .models import Question, Answer, Comment

def index(request):
    page = request.GET.get('page', '1') #페이지
    kw = request.GET.get('kw', '') #검색어
    question_list = Question.objects.order_by('-create_date')
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |  # 제목 검색
            Q(content__icontains=kw) |  # 내용 검색
            Q(answer__content__icontains=kw) |  # 답변 내용 검색
            Q(author__username__icontains=kw) |  # 질문 글쓴이 검색
            Q(answer__author__username__icontains=kw)  # 답변 글쓴이 검색
        ).distinct()
    paginator = Paginator(question_list, 10) #페이지당 10개씩 보여주기

    page_obj = paginator.get_page(page)
    context = {'question_list': page_obj, 'page': page, 'kw': kw}
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
            return redirect('{}#answer_{}'.format(
                resolve_url('pybo:detail', question_id=question.id), answer.id))
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

@login_required(login_url='common:login')
def question_modify(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('pybo:detail', question_id=question.id)
    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.modify_date = timezone.now()  # 수정일시 저장
            question.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        form = QuestionForm(instance=question)
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)

@login_required(login_url='common:login')
def question_delete(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '삭제 권한이 없습니다.')
        return redirect('pybo:detail', question_id=question.id)
    question.delete()
    return redirect('pybo:index')

@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('pybo:detail', question_id=answer.question.id)
    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.modify_date = timezone.now()
            answer.save()
            return redirect('{}#answer_{}'.format(
                resolve_url('pybo:detail', question_id=answer.question.id), answer.id))
    else:
        form = AnswerForm(instance=answer)
    context = {'answer': answer, 'form': form}
    return render(request, 'pybo/answer_form.html', context)

@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '삭제권한이 없습니다')
    else:
        answer.delete()
    return redirect('pybo:detail', question_id=answer.question.id)

@login_required(login_url='common:login')
def question_vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user == question.author:
        messages.error(request, '본인이 작성한 글은 추천할수 없습니다')
    else:
        question.voter.add(request.user)
    return redirect('pybo:detail', question_id=question.id)

@login_required(login_url='common:login')
def answer_vote(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user == answer.author:
        messages.error(request, '본인이 작성한 글은 추천할수 없습니다')
    else:
        answer.voter.add(request.user)
    return redirect('{}#answer_{}'.format(
                resolve_url('pybo:detail', question_id=answer.question.id), answer.id))

def profile_base(request, user_id):
    """
    프로필 기본정보
    """
    user = get_object_or_404(User, pk=user_id)
    context = {'profile_user': user, 'profile_type': 'base'}
    return render(request, 'common/profile/profile_base.html', context)


class ProfileObjectListView(ListView):
    """
    프로필 목록 추상 클래스 뷰
    """
    paginate_by = 10

    class Meta:
        abstract = True

    def get_queryset(self):
        self.profile_user = get_object_or_404(User, pk=self.kwargs['user_id'])
        self.so = self.request.GET.get('so', 'recent')  # 정렬기준
        object_list = self.model.objects.filter(author=self.profile_user)
        # 정렬
        object_list = Answer.order_by_so(object_list, self.so)
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'profile_user': self.profile_user,
            'profile_type': self.profile_type,
            'so': self.so
        })
        return context


class ProfileQuestionListView(ProfileObjectListView):
    """
    작성한 질문 목록
    """
    model = Question
    template_name = 'common/profile/profile_question.html'
    profile_type = 'question'


class ProfileVoteListView(ProfileObjectListView):
    """
    작성한 댓글 목록
    """
    template_name = 'common/profile/profile_vote.html'
    profile_type = 'vote'

    def get_queryset(self):
        self.profile_user = get_object_or_404(User, pk=self.kwargs['user_id'])
        question_list = self.profile_user.voter_question.all()
        answer_list = self.profile_user.voter_answer.annotate(category=F('question__category__description'))

        _queryset = sorted(
            chain(question_list, answer_list),
            key=lambda obj: obj.create_date,
            reverse=True,
        )
        return _queryset

    def get_context_data(self, **kwargs):
        context = ListView.get_context_data(self, **kwargs)
        context.update({
            'profile_user': self.profile_user,
            'profile_type': self.profile_type,
            # 'so': self.so
        })
        return context


class ProfileCommentListView(ProfileObjectListView):
    """
    작성한 댓글 목록
    """
    model = Comment
    template_name = 'common/profile/profile_comment.html'
    profile_type = 'comment'