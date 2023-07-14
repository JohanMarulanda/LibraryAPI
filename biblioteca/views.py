from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Book
from django.db.models import Q
from .serializers import BookSerializer
import requests


@api_view(['GET'])
def search_book(request):
    query = request.GET.get('query')
    print("Este es el query que estoy buscando")
    print(query)
    # Buscar en la base de datos interna
    books = Book.objects.filter(
        Q(title__icontains=query) |
        Q(subtitle__icontains=query) |
        Q(authors__icontains=query) |
        Q(categories__icontains=query) |
        Q(description__icontains=query)
    )
    
    if not books:
        print("Entre a no encontrar el libro en la base de datos interna")
        # Si no se encontraron resultados en la base de datos interna,
        # realizar la búsqueda en la API de Google
        google_results = search_google_books(query)
        # Crear instancias de libros en la base de datos interna utilizando
        # los resultados obtenidos de la API de Google
        create_books_from_google_results(google_results)
        # Recuperar los libros nuevamente de la base de datos interna
        books = Book.objects.filter(
            Q(title__icontains=query) |
            Q(subtitle__icontains=query) |
            Q(authors__icontains=query) |
            Q(categories__icontains=query) |
            Q(description__icontains=query)
        )

    serializer = BookSerializer(books, many=True)
    
    response = {
        'source': 'db interna' if books else 'google',
        'results': serializer.data
    }

    return Response(response)


@api_view(['POST'])
def register_book(request):
    serializer = BookSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        response = {
            'message': 'Libro registrado correctamente',
            'book_id': serializer.data['id'],
            'source': 'db interna'
        }
        return Response(response)

    return Response(serializer.errors, status=400)


@api_view(['DELETE'])
def delete_book(request, book_id):
    try:
        # Eliminar el libro de la base de datos interna
        book = Book.objects.get(id=book_id)
        
        if book:
            book.delete()

        response = {
            'message': 'Libro eliminado correctamente'
        }

    except Book.DoesNotExist:
        response = {
            'error': 'No se encontró un libro con el ID proporcionado'
        }
        return Response(response, status=404)

    return Response(response)


def search_google_books(query):
    print("Entre a la funcion que busca en la api de google")
    url = 'https://www.googleapis.com/books/v1/volumes'
    params = {
        'q': query
    }

    response = requests.get(url, params=params)

    data = response.json()

    if 'items' in data:
        return data['items']

    return []


def create_books_from_google_results(results):
    for result in results:
        volume_info = result.get('volumeInfo')

        title = volume_info.get('title')
        subtitle = volume_info.get('subtitle')
        authors = ', '.join(volume_info.get('authors', []))
        categories = ', '.join(volume_info.get('categories', []))
        publication_date = volume_info.get('publishedDate')
        editor = volume_info.get('publisher')
        description = volume_info.get('description')
        image = volume_info.get('imageLinks', {}).get('thumbnail')

        data = {
            'title': title,
            'subtitle': subtitle,
            'authors': authors,
            'categories': categories,
            'publication_date': publication_date,
            'editor': editor,
            'description': description,
            'image': image
        }

        serializer = BookSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors)

def serialize_books(books):
    serialized_books = []

    for book in books:
        serialized_books.append({
            'id': book.id,
            'title': book.title,
            'subtitle': book.subtitle,
            'authors': book.authors,
            'categories': book.categories,
            'publication_date': book.publication_date,
            'editor': book.editor,
            'description': book.description,
            'image': book.image
        })

    return serialized_books