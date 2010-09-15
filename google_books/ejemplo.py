from gdata.books.service import BookService
servicio = BookService()

busqueda = raw_input('Ingresa el ISBN que quieres buscar:')

resultado = servicio.search('ISBN' + busqueda)
if resultado.entry:
    datos = resultado.entry[0].to_dict()
    print 'Datos del libro:'
    print 'Titulo:', datos['title']
    print 'Tapa:', datos['thumbnail']
    print 'Fecha:', datos['date']
    print 'Genero:', ', '.join(datos['subjects'])
    print 'Autores:', ', '.join(datos['authors'])
    print 'Descripcion:'
    print datos['description']
else:
    print 'No encotre ese ISBN :('

