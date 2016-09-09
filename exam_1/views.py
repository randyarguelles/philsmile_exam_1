from django.shortcuts import render, render_to_response
from .forms import RegistrationForm, QuizForm, QuestionForm, UserInfoForm
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponse
from django.template import RequestContext
from django.contrib.auth.models import User
from .models import Question, Choice, Quiz, UserSession
from django.contrib.auth import logout
# Create your views here.


def logout_page(request):
    logout(request)
    return redirect('/')


def register_page(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            print('pumasok dito')
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email']
            )
            return redirect('/register/success/')
        else:
            return HttpResponse("<p>error here</p>")
        print('asas dito')
    else:
        form = RegistrationForm()
        variables = RequestContext(request, {
            'form': form
        })

        return render_to_response(
            'registration/register.html',
            variables
        )


def index(request):
    list_of_quizzes = Quiz.objects.all().order_by('created_date')
    print(list_of_quizzes)
    # ~ return render_to_response(
    # ~ 'polls/main_page.html',
    # ~ list_of_quizzes
    # ~ )
    return render(
        request,
        'exam_1/main_page.html', {'list_of_quizzes': list_of_quizzes})


def quiz_detail(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    test = Question.objects.filter(quiz=pk)
    # print request['form_1'], "may laman ba"
    if request.method == 'POST':

        for items in test:
            my_key = 'form_' + str(items.id)
            print items.id,"items hahs"
            if my_key in request.POST:
                print my_key ,"ANSWER" ,request.POST[my_key]

                UserSession.objects.create(
                    user=request.user, 
                    quiz=quiz, 
                    question=items,
                    user_answer=Choice.objects.get(id=request.POST[my_key]),
                    user_score=100)
                print "nag save!!"
        return redirect('results', pk=pk)

    quiz = get_object_or_404(Quiz, pk=pk)
    test = Question.objects.filter(quiz=pk)

    print(test)
    form_dic = {}
    for num, test_form in enumerate(test):
        # ~ form = QuestionForm(instance=test)
        choices = Choice.objects.filter(question=test_form.id)
        print choices,'id ng test_form'
        form_dic['form_' + str(test_form.id)] = [QuestionForm(instance=test_form), choices]
    # ~ return HttpResponse('test %s'%pk)
    print(form_dic)
    return render(request, 'exam_1/quiz_detail.html', {'form_dic': form_dic})

def results(request, pk):
    question_list = Question.objects.filter(quiz=pk)
    list_of_users_info = []
    for question_item in question_list:
        list_of_users_info.append(UserSession.objects.filter(user=request.user,question=question_item))


    return render(request, 'exam_1/results.html',{'list_of_users_info': list_of_users_info})
