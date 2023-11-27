from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Question, Answer, Comment, Vote
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import QuestionForm, AnswerForm
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
# Create your views here.

def home(request):
    q=request.GET.get('q') 
    orderby=request.GET.get('orderby')
    if q != None:
        questions = Question.objects.filter(topic=q)#.order_by(f'-{orderby}')
    else:
        questions = Question.objects.all()#.order_by(f'-{orderby}')
    tags = Question.objects.values_list('topic', flat=True).distinct()
    context = {'questions': questions, 'tags': tags, 'orderby': orderby}
    return render(request, 'CodeIt/home.html', context)

    
def questionPage(request,pk):
    questions=Question.objects.get(id=pk)
    answers=questions.answer_set.all()
    comments = Comment.objects.filter(answer__in=answers)
    context={'questions':questions, 'answers':answers, 'comments':comments}
    return render(request, 'CodeIt/question_page.html', context)


@login_required(login_url='login')
def questionSubmit(request):
    form=QuestionForm()
    if request.method=="POST":
        form=QuestionForm(request.POST)
        form.instance.user=request.user
        #form.user=request.user
        if form.is_valid():
            form.save()
            return redirect('home')
    context={'form':form}
    return render(request, 'CodeIt/question_form.html', context)


@login_required(login_url='login')
def answerSubmit(request, pk):
    form=AnswerForm()
    questions=Question.objects.get(id=pk)
    if request.method=="POST":
        form=AnswerForm(request.POST)
        form.instance.user=request.user
        form.instance.question=questions
        if form.is_valid():
            form.save()
            return redirect('home')
    context={'form':form, 'questions':questions}
    return render(request, 'CodeIt/answer_form.html', context)

@login_required(login_url='login')
def commentSubmit(request, pk):
    answers=Answer.objects.get(id=pk)
    question_id=answers.question.id
    if request.method=="POST":
        comment=Comment.objects.create(
            user=request.user,
            answer=answers,
            body=request.POST.get('body')
        )
        redirect_url = reverse('question-page', args=[question_id])
        return redirect(redirect_url)
    context={'obj':"", 'answer':answers}
    return render(request, 'CodeIt/comment_form.html', context)
        

def loginPage(request):
    page='login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method=="POST":
        username=request.POST.get('username').lower()
        password=request.POST.get('password')
        try:
            user=User.objects.get(username=username)
        except:
            messages.error(request, 'user does not exist')
        
        user=authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'username or password does not exist')
    context={'page':page}
    return render(request, 'CodeIt/login_register.html', context)


def logoutPage(request):
    logout(request)
    return redirect('home')

      
def registerPage(request):
    page='register'
    form=UserCreationForm()
    if request.method=="POST":
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'something went wrong with the registration process')
    return render(request, 'CodeIt/login_register.html', {'form':form})

@login_required(login_url='login')
def updateQuestion(request, pk):
    question=Question.objects.get(id=pk)
    form=QuestionForm(instance=question)
    if request.user != question.user:
        return HttpResponse('you have no power here')
    if request.method=="POST":
        form=QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            return HttpResponse('something went wrong')
    context={'form':form}
    return render(request, 'CodeIt/question_form.html', context)

@login_required(login_url='login')
def updateAnswer(request, pk):
    answer=Answer.objects.get(id=pk)
    question_id=answer.question.id
    form=AnswerForm(instance=answer)
    if request.user != answer.user:
        return HttpResponse("You do not have permission to perform this action")
    if request.method=="POST":
        form=AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            form.save()
            redirect_url = reverse('question-page', args=[question_id])
            return redirect(redirect_url)
        else:
            return HttpResponse("something went wrong")
    context={'form':form}
    return render(request, 'CodeIt/answer_form.html', context)

@login_required(login_url='login')
def updateComment(request, pk):
    comment=Comment.objects.get(id=pk)
    question_id=comment.answer.question.id
    if request.user != comment.user:
        return HttpResponse("You do not have permission to perform this action")
    if request.method=="POST":
        comment.body=request.POST.get('body')
        comment.save()
        redirect_url = reverse('question-page', args=[question_id])
        return redirect(redirect_url)
    context={'comment':comment}
    return render(request, 'CodeIt/comment_form.html', context)

@login_required(login_url='login')
def deleteQuestion(request, pk):
    question=Question.objects.get(id=pk)
    if request.user != question.user:
        return HttpResponse('you have no authority here')
    if request.method=="POST":
        question.delete()
        return redirect('home')
    return render(request, 'CodeIt/delete.html', {'obj':question})

@login_required(login_url='login')
def deleteAnswer(request, pk):
    answer=Answer.objects.get(id=pk)
    question_id=answer.question.id
    if request.user != answer.user:
        return HttpResponse("you are not HIM")
    if request.method=="POST":
        answer.delete()
        redirect_url = reverse('question-page', args=[question_id])
        return redirect(redirect_url)
    return render(request, 'CodeIt/delete.html', {'obj':answer})

@login_required(login_url='login')
def deleteComment(request, pk):
    comment=Comment.objects.get(id=pk)
    question_id=comment.answer.question.id
    if request.user != comment.user:
        return HttpResponse("not your comment")
    if request.method=="POST":
        comment.delete()
        redirect_url = reverse('question-page', args=[question_id])
        return redirect(redirect_url)
    return render(request, 'CodeIt/delete.html', {'obj':comment})
        

def questionVote(request, pk, value):
    question=Question.objects.get(id=pk)
    user=request.user
    value=int(value)
    vote='upvote'
    if value < 0:
        vote='downvote'

    if not Vote.objects.filter(user=user, question=question).exists():
        Vote.objects.create(user=user, question=question, vote=vote)
        question.votes += value
        question.save()
    elif Vote.objects.filter(user=user, question=question).exists():
        temp=Vote.objects.get(user=user, question=question)
        if temp.vote == vote:
            Vote.objects.filter(user=user, question=question, vote=vote).delete()
            question.votes -= value
            question.save()
        else:
            Vote.objects.filter(user=user, question=question).delete()
            Vote.objects.create(user=user, question=question, vote=vote)
            value *= 2
            question.votes += value
            question.save()            

    return redirect(request.META['HTTP_REFERER'])
        

def answerVote(request, pk, value):
    answer=Answer.objects.get(id=pk)
    user=request.user
    value=int(value)
    vote='upvote'
    if value < 0:
        vote='downvote'

    if not Vote.objects.filter(user=user, answer=answer).exists():
        Vote.objects.create(user=user, answer=answer, vote=vote)
        answer.votes += value
        answer.save()
    elif Vote.objects.filter(user=user, answer=answer).exists():
        temp=Vote.objects.get(user=user, answer=answer)
        if temp.vote == vote:
            Vote.objects.filter(user=user, answer=answer, vote=vote).delete()
            answer.votes -= value
            answer.save()
        else:
            Vote.objects.filter(user=user, answer=answer).delete()
            Vote.objects.create(user=user, answer=answer, vote=vote)
            value *= 2
            answer.votes += value
            answer.save()            

    return redirect(request.META['HTTP_REFERER'])

        
def commentVote(request, pk, value):
    comment=Comment.objects.get(id=pk)
    user=request.user
    value=int(value)
    vote='upvote'
    if value < 0:
        vote='downvote'

    if not Vote.objects.filter(user=user, comment=comment).exists():
        Vote.objects.create(user=user, comment=comment, vote=vote)
        comment.votes += value
        comment.save()
    elif Vote.objects.filter(user=user, comment=comment).exists():
        temp=Vote.objects.get(user=user, comment=comment)
        if temp.vote == vote:
            Vote.objects.filter(user=user, comment=comment, vote=vote).delete()
            comment.votes -= value
            comment.save()
        else:
            Vote.objects.filter(user=user, comment=comment).delete()
            Vote.objects.create(user=user, comment=comment, vote=vote)
            value *= 2
            comment.votes += value
            comment.save()            

    return redirect(request.META['HTTP_REFERER'])
