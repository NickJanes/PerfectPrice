from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .forms import RegistrationForm

def register(request):
  form = RegistrationForm(request.POST or None)
  if form.is_valid():
    form.save()
    return redirect('profile')
  return render(request, "users/register.html", {"form": form})