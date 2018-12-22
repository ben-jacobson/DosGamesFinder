from django.views.generic import ListView, DetailView
from dosgamesfinder.models import DosGame, Publisher, Genre

MAX_DOSGAME_RESULTS_LISTVIEW = 18 # max number of results in DosgamesListView
MAX_PUBLISHER_RESULTS_LISTVIEW = 20 # max number of publishers in PublisherListView 

# context processor for adding the genres to the drop down menu on every page
def genre_dropdown(request):
    return {
        'genre_dropdown': Genre.objects.all()
    }

# our class based views

class DosGameListView(ListView): 
    page_title = 'Games List A-Z'                   # see how this is altered by get_queryset, then passed as context data during get_context_data
    template_name = 'dosgame_listview.html'
    context_object_name = 'dosgames_list'
    paginate_by = MAX_DOSGAME_RESULTS_LISTVIEW      # pleasantly surprised that pagination is already built in to ListView
    queryset = DosGame.objects.all()   

    def get_queryset(self):
        if self.kwargs:
            if 'genre' in self.request.path:
                genre_obj = Genre.objects.get(slug=self.kwargs['slug'])
                self.page_title = f'{genre_obj.name} Games'
                return DosGame.objects.filter(genre=genre_obj) 
            if 'publisher' in self.request.path:
                publisher_obj = Publisher.objects.get(slug=self.kwargs['slug'])
                self.page_title = f'Games by {publisher_obj.name}'
                return DosGame.objects.filter(publisher=publisher_obj) 
        else:
            self.page_title = 'Games List A-Z'
            return DosGame.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  
        context['page_title'] = self.page_title
        return context

class DosGameDetailView(DetailView):
    template_name = 'dosgame_detailview.html'
    model = DosGame
    context_object_name = 'dosgame'

class PublisherListView(ListView): 
    template_name = 'publisher_listview.html'
    context_object_name = 'publishers'
    paginate_by = MAX_PUBLISHER_RESULTS_LISTVIEW
    queryset = Publisher.objects.all()   

