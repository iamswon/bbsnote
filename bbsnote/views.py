from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Board, Comment
from .forms import BoardForm
from django.utils import timezone

def index(request):
    board_list = Board.objects.order_by('-create_date')
    context = {'board_list': board_list}
    return render(request, 'bbsnote/board_list.html', context)

def detail(request, board_id):
    board = Board.objects.get(id=board_id)
    context = {'board': board}
    return render(request, 'bbsnote/board_detail.html', context)

def comment_create(request, board_id):
    board = Board.objects.get(id=board_id)
    #comment = Comment(board=board, content=request.POST.get('content'), create_date=timezone.now())
    #comment.save()
    board.comment_set.create(content=request.POST.get('content'), create_date=timezone.now())
    return redirect('bbsnote:detail', board_id=board.id)

def board_create(request):
    if request.method=='POST':
        form = BoardForm(request.POST) 
        if form.is_valid():
            board = form.save(commit=False)
            board.create_date = timezone.now()
            board.save()
            return redirect('bbsnote:index')
    else:
        form =BoardForm()
    return render(request,'bbsnote/board_form.html',{'form':form})