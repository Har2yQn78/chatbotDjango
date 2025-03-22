from django.shortcuts import render
from django.views.generic import TemplateView, FormView
from django.http import JsonResponse
from .forms import QueryForm
from .utils import get_query_engine, process_query
import re

class IndexView(FormView):
    template_name = 'ragui/index.html'
    form_class = QueryForm
    success_url = '/'
    
    def form_valid(self, form):
        query = form.cleaned_data['query']

        query_engine = get_query_engine()
        response, debug_info = process_query(query_engine, query)

        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'response': response.response,
                'source_nodes': [node.node.text for node in response.source_nodes] if hasattr(response, 'source_nodes') else [],
                'debug_info': debug_info
            })
        
        return render(self.request, self.template_name, {
            'form': form,
            'response': response.response,
            'source_nodes': response.source_nodes if hasattr(response, 'source_nodes') else [],
            'debug_info': debug_info
        })

class TopPostsView(TemplateView):
    template_name = 'ragui/results.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query_engine = get_query_engine()
        most_viewed_response, most_viewed_debug = process_query(
            query_engine, 
            "What are the top 5 most viewed blog posts? What keywords do their content have?"
        )
        context['most_viewed'] = most_viewed_response.response
        context['most_viewed_debug'] = most_viewed_debug
        least_viewed_response, least_viewed_debug = process_query(
            query_engine, 
            "What are the top 5 least viewed blog posts?"
        )
        context['least_viewed'] = least_viewed_response.response
        context['least_viewed_debug'] = least_viewed_debug
        
        return context