'''
@author: Tudor Cornea
@contact: tudor.cornea@gmail.com
'''

import webapp2
import jinja2
import urllib

import os
import logging

from google.appengine.api import memcache
from google.appengine.api import users
from google.appengine.api import images
from google.appengine.ext import ndb
from google.appengine.ext import db

from PIL import Image
from pprint import pprint

from models.photo_upload import *

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), '../')),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

'''
  For now, we consider that we have only one photo album
  All the user's photos will be placed in it
'''
DEFAULT_PHOTO_ALBUM = 'default_album'

class Contact(webapp2.RequestHandler):
    '''
        Return a page with help info
    '''
    def get(self):
        user = users.get_current_user()
        if user:
           auth_url = users.create_logout_url(self.request.uri)
        else:
           auth_url = users.create_login_url(self.request.uri)

        template = JINJA_ENVIRONMENT.get_template('/views/contact.html')
        self.response.write(
            template.render({
                'auth_url': auth_url,
                'user' : user 
        }))

class Gallery(webapp2.RequestHandler):
    '''
        Render a page that displays all the images of the current user
    '''
    def get(self):
        # Retrieve parameters
        album_name = self.request.get('album_name', DEFAULT_PHOTO_ALBUM)

        # Generate login/logout url
        user = users.get_current_user()
        if user:
           auth_url = users.create_logout_url(self.request.uri)
        else:
           auth_url = users.create_login_url(self.request.uri)

        # Retrieve the photos corresponding to the current user
        # Ancestor queries are guarranteed to be strongly consistent !
        photos_query = PhotoUpload.query(
                          ancestor = album_key(album_name)).filter(
                              PhotoUpload.upload_user == user).order(
                                   PhotoUpload.date)
        photos = photos_query.fetch()

        # Render the gallery page
        template = JINJA_ENVIRONMENT.get_template('/views/index.html')
        self.response.write(
            template.render({
                'album_name': urllib.quote_plus(album_name),
                'photos': photos,
                'num_photos_per_line': 5,
                'auth_url': auth_url,
                'user': user,
        }))

class Upload(webapp2.RequestHandler):
    '''
        The POST request will trigger the creation of a new upload image object
    '''
    def post(self):
        # Retrieve parameters
        album_name = self.request.get('album_name', DEFAULT_PHOTO_ALBUM)
        upload_image = self.request.get('upload_photo')
        upload_description = self.request.get('description', '')

        user = users.get_current_user()

        # Create & populate upload object
        photo = PhotoUpload(parent=album_key(album_name))
        photo.upload_user = user
        photo.description = upload_description
        photo.image = db.Blob(upload_image)
        photo.put()

        # Redirect to the view that displays the same form
        return self.redirect('/upload')

    '''
        The GET request will return a form which will be used to upload images
    '''
    def get(self):
        user = users.get_current_user()

        template = JINJA_ENVIRONMENT.get_template('/views/upload.html')
        self.response.write(
            template.render({
                'user' : user,
        }))

class ImageHandler(webapp2.RequestHandler):
    '''
        Creates a thumbnail, which will be used for showing images in the gallery
        Uses PIL library for resize operations
    '''
    def _create_thumbnail(self, src_image, img_width, img_height):
        orig_image = images.Image(src_image)
        orig_image.resize(width = img_width, height = img_height)
        orig_image.im_feeling_lucky()
        thumbnail_img = orig_image.execute_transforms(output_encoding=images.PNG)
        return thumbnail_img

    '''
        Retrieve an image based on desired resolution
        We consider that the high resolution version of the image,
        is the original image as stored in the Datastore
    '''
    def _process_image(self, src_image, img_resolution):
        if   img_resolution == "high":
            dst_image = src_image 
        elif img_resolution == "medium":
            dst_image = self._create_thumbnail(src_image, 300, 300)
        elif img_resolution == "low":
            dst_image = self._create_thumbnail(src_image, 150, 150)
        else:
            # Default to showing the full image
            dst_image = src_image
        return dst_image

    '''
        Retrieves an image. Looks into the cache first.
        If an image already exists, it returns it.
        Otherwise it gets it from the Datastore, and adds it to the cache
    '''
    def _get_photo(self, album_name, img_resolution, img_id):
        memcache_id='%s_%s_%s' % (album_name, img_resolution, img_id)

        thumbnail_img = memcache.get(memcache_id)
        if thumbnail_img is None:
            # Cache miss
            photo = PhotoUpload.get_by_id(
                            int(img_id), parent=album_key(album_name))
            if photo.image:
                thumbnail_img = self._process_image(photo.image, img_resolution)
                if thumbnail_img:
                    memcache.set(memcache_id, thumbnail_img, 10)
        return thumbnail_img

    def get(self):
        # Retrieve parameters
        album_name = self.request.get('album_name', DEFAULT_PHOTO_ALBUM)
        img_resolution = self.request.get('resolution', 'high')
        img_id = self.request.get('img_id')

        thumbnail_img = self._get_photo(album_name, img_resolution, img_id)
        if thumbnail_img:
            self.response.headers['Content-Type'] = 'image/png'
            self.response.out.write(thumbnail_img)
        else:
            self.error(404)

class Slideshow(webapp2.RequestHandler):
    '''
        Display a slideshow with the images
        Only one image will be shown at once
    '''
    def get(self):
        # Retrieve parameters
        album_name = self.request.get('album_name', DEFAULT_PHOTO_ALBUM)
        img_id=self.request.get('img_id')
        action=self.request.get('action')

        user = users.get_current_user()

        curr_photo = PhotoUpload.get_by_id(
                         int(img_id), parent=album_key(album_name))
        photo = curr_photo
        if not curr_photo:
            return self.abort(404)

        if action == "prev":
            photo = PhotoUpload.query(
                        ancestor = album_key(album_name)).filter(
                            PhotoUpload.upload_user == user,
                            PhotoUpload.date < curr_photo.date).order(
                                -PhotoUpload.date).get()
        elif action == "next":
            photo = PhotoUpload.query(
                        ancestor = album_key(album_name)).filter(
                            PhotoUpload.upload_user == user,
                            PhotoUpload.date > curr_photo.date).get()

        # No action selected. Stick with the current photo
        if not photo:
            photo = curr_photo

        template = JINJA_ENVIRONMENT.get_template('/views/slideshow.html')
        self.response.write(
            template.render({
                'user':  user,
                'photo': photo,
        }))

