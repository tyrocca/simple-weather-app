from django.shortcuts import render
from django.http import HttpResponse

from .forms import EmailForm
from .models import Subscriber

# Create your views here.
def index(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = EmailForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # ideally you would make sure the user validates their email
            # with a "magic link"
            subscriber, created = Subscriber.objects.update_or_create(
                email=form.cleaned_data["email"],
                defaults={
                    "is_valid": form.is_valid(),
                    "city": form.cleaned_data["city"],
                    "state": form.cleaned_data["city"].state,
                }
            )
            # display correct message if successful
            if created:
                return HttpResponse("Success, your subscription has been created!")
            else:
                return HttpResponse("Success, your subscription has been updated!")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = EmailForm()

    return render(request, 'emails/index.html', {'form': form})
