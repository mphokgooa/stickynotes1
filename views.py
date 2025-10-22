from django.shortcuts import render, get_object_or_404, redirect
from .models import Note
from .forms import NoteForm
from django.contrib.auth.decorators import login_required

def index(request):
    notes = Note.objects.order_by('-updated')[:50]
    return render(request, 'notes/index.html', {'notes': notes})

@login_required
def note_create(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.owner = request.user
            note.save()
            return redirect('notes:index')
    else:
        form = NoteForm()
    return render(request, 'notes/note_form.html', {'form': form})

@login_required
def note_detail(request, pk):
    note = get_object_or_404(Note, pk=pk)
    return render(request, 'notes/note_detail.html', {'note': note})

@login_required
def note_edit(request, pk):
    note = get_object_or_404(Note, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('notes:note_detail', pk=note.pk)
    else:
        form = NoteForm(instance=note)
    return render(request, 'notes/note_form.html', {'form': form})

@login_required
def note_delete(request, pk):
    note = get_object_or_404(Note, pk=pk, owner=request.user)
    if request.method == 'POST':
        note.delete()
        return redirect('notes:index')
    return render(request, 'notes/note_confirm_delete.html', {'note': note})
