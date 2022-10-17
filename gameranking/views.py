from django.shortcuts import render
from django.views.generic import TemplateView
from controller.models import *
from django.core.paginator import Paginator

class RankingPageView(TemplateView):

    template_name = "ranking.html"
    paginate_by = 10

    def get(self, request):
        rank = dict()
        rankusr = HistUsersCurrent.objects.order_by('-reputation')
        return render(request, self.template_name, {'context': rankusr})


def rank_paginator(request):
	usrs_rank = HistUsersCurrent.objects.order_by('-reputation')
	paginator = Paginator(usrs_rank, 20)
	page = request.GET.get('page')
	rank_list = paginator.get_page(page)
	tot = len(usrs_rank)

	return render(request, 'ranking.html', {'rank_list': rank_list, 'tot':range(tot)})