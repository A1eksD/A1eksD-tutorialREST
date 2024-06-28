from django.http import Http404  # Importiert Http404 Ausnahme für Fehlerbehandlung
from rest_framework import status  # Importiert Statusmodule für HTTP-Antwortcodes
from rest_framework.decorators import api_view  # Importiert Dekorator für funktionsbasierte Views
from rest_framework.response import Response  # Importiert Response-Klasse für HTTP-Antworten
from snippets.models import Snippet  # Importiert das Snippet-Modell
from snippets.serializers import SnippetSerializer, UserSerializer  # Importiert die Serializer-Klassen
from rest_framework.views import APIView  # Importiert APIView-Klasse für klassenbasierte Views
from rest_framework import generics  # Importiert generische Views
from django.contrib.auth.models import User  # Importiert das User-Modell
from rest_framework import permissions  # Importiert das Berechtigungsmodul
from snippets.permissions import IsOwnerOrReadOnly  # Importiert benutzerdefinierte Berechtigungen
from rest_framework.reverse import reverse  # Importiert reverse-Funktion für URL-Umkehrung
from rest_framework import renderers  # Importiert Renderer für benutzerdefinierte Darstellungen
from rest_framework.decorators import action  # Importiert Action-Dekorator für ViewSets
from rest_framework import viewsets  # Importiert ViewSet-Klassen

@api_view(['GET'])  # Dekorator, der diese Funktion als API-View deklariert und nur GET-Anfragen zulässt
def api_root(request, format=None):
    """
    Diese View stellt die Wurzel der API bereit und enthält Links zu den Benutzer- und Snippet-Endpunkten.
    """
    return Response({
        'users': reverse('user-list', request=request, format=format),  # Rückgabe des Links zur Benutzerliste
        'snippets': reverse('snippet-list', request=request, format=format)  # Rückgabe des Links zur Snippet-Liste
    })
    
class SnippetHighlight(generics.GenericAPIView):  # Definition einer generischen APIView für Snippet-Highlights
    """
    Diese View wird verwendet, um ein Snippet hervorzuheben und es im HTML-Format darzustellen.
    """
    queryset = Snippet.objects.all()  # Setzt das Queryset auf alle Snippet-Objekte
    renderer_classes = [renderers.StaticHTMLRenderer]  # Setzt den Renderer auf StaticHTMLRenderer

    def get(self, request, *args, **kwargs):  # Definiert die GET-Methode
        snippet = self.get_object()  # Holt das aktuelle Snippet-Objekt
        return Response(snippet.highlighted)  # Gibt das hervorgehobene Snippet zurück
    
#---------------------------- Aktuelle Version Überarbeitet ------------------------------
class SnippetViewSet(viewsets.ModelViewSet):  # Definition eines ModelViewSets für Snippets
    """
    Dieses ViewSet stellt automatisch `list`, `create`, `retrieve`,
    `update` und `destroy` Aktionen bereit.

    Zusätzlich bieten wir eine `highlight` Aktion an.
    """
    queryset = Snippet.objects.all()  # Setzt das Queryset auf alle Snippet-Objekte
    serializer_class = SnippetSerializer  # Setzt den Serializer auf SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,  # Nur authentifizierte Benutzer können Daten ändern
                          IsOwnerOrReadOnly]  # Benutzer können nur ihre eigenen Snippets ändern

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])  # Definiert eine benutzerdefinierte Aktion
    def highlight(self, request, *args, **kwargs):
        """
        Benutzerdefinierte Aktion zum Hervorheben eines Snippets.
        """
        snippet = self.get_object()  # Holt das aktuelle Snippet-Objekt
        return Response(snippet.highlighted)  # Gibt das hervorgehobene Snippet zurück

    def perform_create(self, serializer):  # Überschreibt die Standarderstellungsfunktion
        """
        Überschreibt das Standardverhalten der Erstellung, um das Snippet mit dem aktuellen Benutzer zu verknüpfen.
        """
        serializer.save(owner=self.request.user)  # Speichert das Snippet und setzt den Eigentümer auf den aktuellen Benutzer
        
class UserViewSet(viewsets.ReadOnlyModelViewSet):  # Definition eines ReadOnlyModelViewSets für Benutzer
    """
    Dieses ViewSet stellt automatisch `list` und `retrieve` Aktionen für Benutzer bereit.
    """
    queryset = User.objects.all()  # Setzt das Queryset auf alle Benutzer
    serializer_class = UserSerializer  # Setzt den Serializer auf UserSerializer


#---------------------------- Aktuelle version ------------------------------
# class SnippetList(generics.ListCreateAPIView):
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly,
#                         IsOwnerOrReadOnly]
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer


# class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly,
#                         IsOwnerOrReadOnly]
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer


# class UserList(generics.ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


# class UserDetail(generics.RetrieveAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

#---------------------------- Ältere SnippetList version ------------------------------

# class SnippetDetail(mixins.RetrieveModelMixin,
#                     mixins.UpdateModelMixin,
#                     mixins.DestroyModelMixin,
#                     generics.GenericAPIView):
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)

#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)

#---------------------------- Alte SnippetList version ------------------------------
# class SnippetList(APIView):
#     """
#     List all snippets, or create a new snippet.
#     """
#     def get(self, request, format=None):
#         snippets = Snippet.objects.all()
#         serializer = SnippetSerializer(snippets, many=True)
#         return Response(serializer.data)

#     def post(self, request, format=None):
#         serializer = SnippetSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class SnippetDetail(APIView):
#     """
#     Retrieve, update or delete a snippet instance.
#     """
#     def get_object(self, pk):
#         try:
#             return Snippet.objects.get(pk=pk)
#         except Snippet.DoesNotExist:
#             raise Http404

#     def get(self, request, pk, format=None):
#         snippet = self.get_object(pk)
#         serializer = SnippetSerializer(snippet)
#         return Response(serializer.data)

#     def put(self, request, pk, format=None):
#         snippet = self.get_object(pk)
#         serializer = SnippetSerializer(snippet, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk, format=None):
#         snippet = self.get_object(pk)
#         snippet.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)