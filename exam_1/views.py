from django.shortcuts import render, render_to_response
from .forms import RegistrationForm, QuestionForm
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponse
from django.template import RequestContext
from django.contrib.auth.models import User
from django.views import generic
from django.views.generic.base import View
from .models import Question, Choice, Quiz, UserSession, UserAnswer
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


class IndexView(generic.ListView):
    template_name = 'exam_1/main_page.html'
    context_object_name = 'list_of_quizzes'

    def get_queryset(self):
        """Return the last five published questions."""
        # return Question.objects.order_by('-pub_date')[:5]
        return Quiz.objects.all().order_by('created_date')


def old_index(request):
    list_of_quizzes = Quiz.objects.all().order_by('created_date')
    # ~ return render_to_response(
    # ~ 'polls/main_page.html',
    # ~ list_of_quizzes
    # ~ )
    return render(
        request,
        'exam_1/main_page.html', {'list_of_quizzes': list_of_quizzes})


class QuizDetail(View):
    def get(self, request, pk):
        # <view logic>
        test = Question.objects.filter(quiz=pk)

        print(test)
        form_dic = {}
        for num, test_form in enumerate(test):
            # ~ form = QuestionForm(instance=test)
            choices = Choice.objects.filter(question=test_form.id)
            form_dic['form_' + str(test_form.id)] = [QuestionForm(
                instance=test_form), choices]
        # ~ return HttpResponse('test %s'%pk)
        return render(request, 'exam_1/quiz_detail.html', {
            'form_dic': form_dic})

    def post(self, request, pk):
        quiz = get_object_or_404(Quiz, pk=pk)
        test = Question.objects.filter(quiz=pk)

        for items in test:
            my_key = 'form_' + str(items.id)
            if my_key in request.POST:
                obj_user_session = UserSession.objects.create(
                    user=request.user,
                    quiz=quiz,
                    question=items,
                    # user_answer=Choice.objects.get(id=request.POST[my_key]),
                    # user_score=100
                )

                UserAnswer.objects.create(
                    session=obj_user_session,
                    user_answer=Choice.objects.get(id=request.POST[my_key])
                )
                print "nag save!!"
        return redirect('results', pk=pk)


def old_quiz_detail(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    test = Question.objects.filter(quiz=pk)
    # print request['form_1'], "may laman ba"
    if request.method == 'POST':

        for items in test:
            my_key = 'form_' + str(items.id)
            if my_key in request.POST:
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
        form_dic['form_' + str(test_form.id)] = [QuestionForm(
            instance=test_form), choices]
    # ~ return HttpResponse('test %s'%pk)
    return render(request, 'exam_1/quiz_detail.html', {'form_dic': form_dic})


class ResultsView(generic.DetailView):
    model = Question
    context_object_name = 'list_of_users_info'
    template_name = 'exam_1/results.html'

    def get_context_data(self, **kwargs):
        data = super(ResultsView, self).get_context_data(**kwargs)
        question_list = Question.objects.filter(quiz=self.kwargs['pk'])

        list_of_obj_user_answer = UserAnswer.objects.filter(
            session__quiz=self.kwargs['pk'],

        )

        new_data = []
        for obj_user_answer in list_of_obj_user_answer:
            x=[
                obj_user_answer.session.question.question_text,
                obj_user_answer.user_answer.choice_text,
                obj_user_answer.user_answer.is_correct,

                ]
            if x not in new_data:
                new_data.append(x)
            print obj_user_answer.session.question.question_text
        print new_data, "eto ang data",len(new_data)
     
        # list_of_users_info = []
        # for question_item in question_list:
        #     list_of_users_info.append(UserSession.objects.filter(
        #         user=self.request.user,
        #         question=question_item))

        # data['list_of_users_info'] = list_of_users_info
        data['new_data'] = new_data
        return data
    # def get_queryset(self):
    #     question_list = Question.objects.filter(quiz=self.kwargs['pk'])
    #     list_of_users_info = []
    #     for question_item in question_list:
    #         list_of_users_info.append(UserSession.objects.filter(user=self.request.user,question=question_item))

    #     return list_of_users_info


def oldresults(request, pk):
    question_list = Question.objects.filter(quiz=pk)
    list_of_users_info = []
    for question_item in question_list:
        list_of_users_info.append(UserSession.objects.filter(
            user=request.user, question=question_item))

    return render(request, 'exam_1/results.html', {
        'list_of_users_info': list_of_users_info})
