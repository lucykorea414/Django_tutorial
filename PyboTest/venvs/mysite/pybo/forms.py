import py_compile
from django import forms
from pybo.models import Question, Answer, Comment

#폼은 쉽게 말해 페이지 요청시 전달되는 파라미터들을 쉽게 관리하기 위해 사용하는 클래스이다. 
#폼은 필수 파라미터의 값이 누락되지 않았는지, 파라미터의 형식은 적절한지 등을 검증할 목적으로 사용한다. 
#이 외에도 HTML을 자동으로 생성하거나 폼에 연결된 모델을 이용하여 데이터를 저장하는 기능도 있다.


#QuestionForm은 Question 모델과 연결된 폼이고 속성으로 Question 모델의 subject와 content를 사용한다고 정의한 것이다.
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question #사용할 모델
        fields = ['subject', 'content'] #QuestionForm에서 사용할 Question 모델의 속성
        labels = {
            'subject': '제목',
            'content': '내용',
        }

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        labels = {
            'content': '답변내용'
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'content': '댓글내용',
        }