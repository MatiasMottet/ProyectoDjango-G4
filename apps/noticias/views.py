from django.shortcuts import render, redirect, get_object_or_404

from django.contrib import messages

from django.contrib.auth.decorators import login_required

from django.core.exceptions import PermissionDenied

from .forms import NoticiaForm

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

@login_required
def Crear_Noticia(request):
    if request.method == 'POST':
        form = NoticiaForm(request.POST, request.FILES)
        if form.is_valid():
            noticia = form.save(commit=False)
            noticia.usuario = request.user
            noticia.save()
            messages.success(request, "Noticia creada correctamente.")
            return redirect('noticias:listar')
        else:
            print(form.errors)
            messages.error(request, "Error al crear la noticia. Revisa el formulario.")
    else:
        form = NoticiaForm()

    return render(request, 'noticias/crear.html', {'form': form})

@login_required
def Eliminar_Noticia(request, pk):
    n = get_object_or_404(Noticia, pk=pk)

    if request.user == n.usuario or request.user.is_staff:
        n.delete()
        return redirect('noticias:listar')
    else:
        raise PermissionDenied("No tienes permiso para eliminar esta noticia.")

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
    comentario = get_object_or_404(Comentario, pk=pk, usuario=request.user)

    noticia_id = comentario.noticia.pk

    if comentario.usuario == request.user:
        comentario.delete()
        messages.success(request, "Comentario eliminado correctamente.")
    else:
        messages.error(request, "No tienes permiso para eliminar este comentario.")

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