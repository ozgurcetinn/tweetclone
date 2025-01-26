from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from . import models
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView

def listtweet(request):
    """View to list all tweets."""
    all_tweets = models.Tweet.objects.all()
    tweet_dict = {"tweets": all_tweets}
    return render(request, 'tweetapp/listtweet.html', context=tweet_dict)

@login_required(login_url= "/login")
def addtweet(request):
    """View to add a new tweet."""
    if request.method == "POST":
        
        message = request.POST.get("message")

        # Create a new Tweet
        models.Tweet.objects.create(username=request.user, message=message)
        return redirect(reverse('tweetapp:listtweet'))

    # If GET request, render the form
    return render(request, 'tweetapp/addtweet.html')

@login_required
def deletetweet(request, id):
   tweet = models.Tweet.objects.get(pk=id)
   if request.user == tweet.username:
      models.Tweet.objects.filter(id=id).delete()
      return redirect('tweetapp:listtweet')


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = "registration/signup.html"