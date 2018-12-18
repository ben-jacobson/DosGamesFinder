from django.views.generic import ListView, DetailView
from dosgamesfinder.models import DosGame, Publisher, Genre
from dosgamesfinder.serializers import DosGameSerializer, PublisherSerializer, GenreSerializer
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination

MAX_DOSGAME_RESULTS_LISTVIEW = 18 # max number of results in DosgamesListView
MAX_PUBLISHER_RESULTS_LISTVIEW = 20 # max number of publishers in PublisherListView 

class DosGameListView(ListView): 
    template_name = 'dosgame_listview.html'
    context_object_name = 'dosgames_list'
    paginate_by = MAX_DOSGAME_RESULTS_LISTVIEW      # pleasantly surprised that pagination is already built in to ListView
    queryset = DosGame.objects.all()   

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  
        context['page_title'] = 'Games List A-Z'
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


# old API views to be removed

# our pagination mixin classes - This is how you cusomize the page_sizes for pagination styles

class DosGamesPageNumberPagination(PageNumberPagination):
    page_size = 18
    max_page_size = page_size
    #page_size_query_param = 'page_size'    

class PublisherPageNumberPagination(PageNumberPagination):
    page_size = 20
    max_page_size = page_size

class DosGameList(generics.ListAPIView):
    pagination_class = DosGamesPageNumberPagination     # see how you can set pagination styles,    
    serializer_class = DosGameSerializer
    
    def get_queryset(self):
        genre_query_string = self.request.query_params.get('genre', None)
        publisher_query_string = self.request.query_params.get('publisher', None)
        query_obj = {}

        if publisher_query_string is not None:
            query_obj['publisher'] = Publisher.objects.get(slug__iexact=publisher_query_string)
 
        if genre_query_string is not None:
            query_obj['genre'] = Genre.objects.get(slug__iexact=genre_query_string)

        return DosGame.objects.filter(**query_obj)      # this is how we can use a dictionary to define our filter
        #return DosGame.objects.all()                   # DosGame.objects.filter(**{}) is the same as DosGame.objects.all()

class PublisherList(generics.ListAPIView):
    pagination_class = PublisherPageNumberPagination
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer

class GenreList(generics.ListAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

# Detail Views

class DosGameDetail(generics.RetrieveAPIView):
    lookup_field = 'slug'
    queryset = DosGame.objects.all()        # I was skeptical too of using objects.all() but I can see in 3 separate posts that this is the correct way to do it..
    serializer_class = DosGameSerializer

class PublisherDetail(generics.RetrieveAPIView):
    lookup_field = 'slug'
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer    

class GenreDetail(generics.RetrieveAPIView):
    lookup_field = 'slug'
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer



