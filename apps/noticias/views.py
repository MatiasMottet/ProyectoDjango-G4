from django.shortcuts import render, redirect, get_object_or_404

from django.contrib import messages

from django.contrib.auth.decorators import login_required

from .models import Noticia, Categoria, Comentario

from django.urls import reverse_lazy

def Listar_Noticias(request):
	contexto = {}

	id_categoria = request.GET.get('id',None)

	if id_categoria:
		n = Noticia.objects.filter(categoria_noticia = id_categoria)
	else:
		n = Noticia.objects.all() #RETORNA UNA LISTA DE OBJETOS

	contexto['noticias'] = n

	cat = Categoria.objects.all().order_by('nombre')
	contexto['categorias'] = cat

	return render(request, 'noticias/listar.html', contexto)

def Detalle_Noticias(request, pk):
	contexto = {}

	n = Noticia.objects.get(pk = pk) #RETORNA SOLO UN OBEJTO
	contexto['noticia'] = n

	c = Comentario.objects.filter(noticia = n)
	contexto['comentarios'] = c

	return render(request, 'noticias/detalle.html',contexto)


@login_required
def Comentar_Noticia(request):

	com = request.POST.get('comentario',None)
	usu = request.user
	noti = request.POST.get('id_noticia', None)# OBTENGO LA PK
	noticia = Noticia.objects.get(pk = noti) #BUSCO LA NOTICIA CON ESA PK
	coment = Comentario.objects.create(usuario = usu, noticia = noticia, texto = com)

	return redirect(reverse_lazy('noticias:detalle', kwargs={'pk': noti}))

@login_required
def Eliminar_Comentario(request, pk):
    # Obtener el comentario o lanzar un error 404 si no existe
    comentario = get_object_or_404(Comentario, pk=pk, usuario=request.user)
    
    # Guardar el ID de la noticia antes de eliminar el comentario
    noticia_id = comentario.noticia.pk

    # Asegurarse de que solo el autor pueda eliminar su comentario
    if comentario.usuario == request.user:
        comentario.delete()
        messages.success(request, "Comentario eliminado correctamente.")
    else:
        messages.error(request, "No tienes permiso para eliminar este comentario.")

    # Redirigir a la página de detalles de la noticia
    return redirect(reverse_lazy('noticias:detalle', kwargs={'pk': noticia_id}))

#{'nombre':'name', 'apellido':'last name', 'edad':23}
#EN EL TEMPLATE SE RECIBE UNA VARIABLE SEPARADA POR CADA CLAVE VALOR
# nombre
# apellido
# edad

'''
ORM

CLASE.objects.get(pk = ____)
CLASE.objects.filter(campos = ____)
CLASE.objects.all() ---> SELECT * FROM CLASE

'''