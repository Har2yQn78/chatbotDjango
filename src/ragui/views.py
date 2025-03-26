from django.shortcuts import render
from django.views.generic import FormView
from django.http import JsonResponse
from .forms import QueryForm
from .utils import get_query_engine, process_query
from .rag_initializer import ensure_rag_initialized

class IndexView(FormView):
    template_name = 'ragui/index.html'
    form_class = QueryForm
    success_url = '/'
    
    @ensure_rag_initialized
    def form_valid(self, form):
        query = form.cleaned_data['query']

        try:
            query_engine = get_query_engine()
            response, debug_info = process_query(query_engine, query)
            response_data = {
                'response': response.response,
                'source_nodes': [node.node.text for node in response.source_nodes] if hasattr(response, 'source_nodes') else [],
                'debug_info': debug_info
            }

            if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse(response_data)
 
            return render(self.request, self.template_name, {
                'form': form,
                **response_data
            })
        
        except Exception as e:
            error_message = str(e)
            if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'error': error_message
                }, status=500)
            
            return render(self.request, self.template_name, {
                'form': form,
                'error': error_message
            })