from email.mime import image
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import *

# View for gallery 
def gallery(request):
    # Display category, none in the html file means all photos
    category = request.GET.get('category')
    # Filter the photos from the database for each user
    if category is None:
        photos = Photo.objects.filter(category__user=request.user)
    else:
        photos = Photo.objects.filter(category__name=category,category__user=request.user)
        
    categories = Category.objects.filter(user=request.user)
    context = {'categories':categories, 'photos':photos}
    return render(request, 'gallery_app/gallery.html', context)
# View for a single photo, filter photos for eatch user is done in the gallery view
def viewPhoto(request, pk):
    photo = Photo.objects.get(id=pk)
    context = {'photo':photo}
    return render(request, 'gallery_app/photo.html', context)
# View for adding a new photo
def addPhoto(request):
    # Get all the user categories, each user have is own categories
    categories = Category.objects.filter(user=request.user)
    # Handle the POST request
    if request.method == 'POST':
        data = request.POST
        images = request.FILES.getlist('images')
        
        if data['category'] != 'none':
            category = Category.objects.get(id=data['category'])
        elif data['category_new'] != '':
            category, created = Category.objects.get_or_create(name=data['category_new'], user=request.user)
        else:
            messages.info(request, "Please select a category from the list, or create a new one")
            return redirect('add')
        # Create objects for each uploaded photo (can upload multiple photos)
        for image in images:
            photo = Photo.objects.create(
                category = category,
                discription = data['discription'],
                image = image
                )

        return redirect('gallery')

    context = {'categories':categories}
    return render(request, 'gallery_app/add.html', context)

# A class view to delete a photo
class PhotoDelete(LoginRequiredMixin, DeleteView):
    model = Photo
    # You have to use reverse_lazy() instead of reverse(),
    # as the urls are not loaded when the file is imported.
    success_url = reverse_lazy('gallery')
