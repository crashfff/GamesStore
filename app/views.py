from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from django.http import HttpResponseNotFound

from .forms import RegisterUserForm, SellForm
from .models import *


class AppMain(ListView, LoginRequiredMixin):
    model = Name_of_game
    template_name = 'main_page.html'
    context_object_name = 'games'

    def get_queryset(self):
        queryset = Name_of_game.objects.all()
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['queryset1'] = Name_of_game.objects.order_by('quantity_purchased').reverse
        return context


@login_required
def profile_view(request):
    return render(request, 'profile.html')


def logout_user(request):
    logout(request)

    return redirect('main_page')


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        return dict(list(context.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('profile')


class GamePage(ListView):
    model = Name_of_game

    def get_queryset(self, game_name=None):
        queryset = Name_of_game.objects.get(game_name=game_name)
        return queryset

    def get(self, request, game_name=None, name_of_game_id=None, *args, **kwargs):
        all_products_game = Name_of_game.objects.get(game_name=game_name).game_account_set.all()
        one_name_game = Name_of_game.objects.get(game_name=game_name)
        if one_name_game:
            return render(request, 'game.html', context={'game': one_name_game,
                                                                        'products': all_products_game})
        return HttpResponseNotFound('Page not found =(')

class SellGame(CreateView, SellForm, LoginRequiredMixin):
    form_class = SellForm
    template_name = 'sell.html'
    model = Game_account
    success_url = reverse_lazy('profile')

    def get_context_data(self, **kwargs):
        kwargs['form'] = SellForm
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)