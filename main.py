import os
import base64
import logging
import simplejson
import wsgiref.handlers
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api.images import Image

logging.getLogger().setLevel(logging.DEBUG)

class BaseHandler(webapp.RequestHandler):

    def get(self):
        path = os.path.join(os.path.dirname(__file__), self.template)
        self.response.out.write(template.render(path, {}))
    
    def render(self, image=None, data={}):
        json = self.request.get('json', False)
        
        if json:
            data['length'] = len(image)
            data['image'] = base64.b64encode(image)
            self.response.out.write(simplejson.dumps(data))
        else:
            self.response.headers['Content-Type'] = 'image/png'
            self.response.out.write(image)

class MainHandler(BaseHandler):
    def __init__(self, *args, **kwargs):
        self.template = 'templates/index.html'
        super(MainHandler, self).__init__(*args, **kwargs)

class AboutHandler(BaseHandler):
    def __init__(self, *args, **kwargs):
        self.template = 'templates/about.html'
        super(AboutHandler, self).__init__(*args, **kwargs)

class CropHandler(BaseHandler):
    def __init__(self, *args, **kwargs):
        self.template = 'templates/crop.html'
        super(CropHandler, self).__init__(*args, **kwargs)

    def post(self):
         img = Image(self.request.get('file'))
         left_x = float(self.request.get('left_x', '90'))
         top_y = float(self.request.get('top_y', '90'))
         right_x = float(self.request.get('right_x', '90'))
         bottom_y = float(self.request.get('bottom_y', '90'))
         
         img.crop(left_x, top_y, right_x, bottom_y)
         cropped = img.execute_transforms()
         self.render(image=cropped)

class RotateHandler(BaseHandler):
    
    def __init__(self, *args, **kwargs):
        self.template = 'templates/rotate.html'
        super(RotateHandler, self).__init__(*args, **kwargs)
    
    def post(self):
         img = Image(self.request.get('file'))
         degrees = int(self.request.get('degrees', '90'))
         img.rotate(degrees)
         rotated = img.execute_transforms()
         self.render(image=rotated)
         
class HorizontalFlipHandler(BaseHandler):
    
    def __init__(self, *args, **kwargs):
        self.template = 'templates/horizontal.html'
        super(HorizontalFlipHandler, self).__init__(*args, **kwargs)
    
    def post(self):
         img = Image(self.request.get('file'))
         img.horizontal_flip()
         horizontal = img.execute_transforms()
         self.render(image=horizontal)

class VerticalFlipHandler(BaseHandler):
    def __init__(self, *args, **kwargs):
        self.template = 'templates/vertical.html'
        super(VerticalFlipHandler, self).__init__(*args, **kwargs)
    
    def post(self):
         img = Image(self.request.get('file'))
                  
         img.vertical_flip()
         vertical = img.execute_transforms()
         
         self.render(image=vertical)

class ImFeelingLuckyHandler(BaseHandler):
    
    def __init__(self, *args, **kwargs):
        self.template = 'templates/lucky.html'
        super(ImFeelingLuckyHandler, self).__init__(*args, **kwargs)
    
    def post(self):
         img = Image(self.request.get('file'))
         
         img.im_feeling_lucky()
         lucky = img.execute_transforms()
         self.render(image=lucky)

class ResizeHandler(BaseHandler):

    def __init__(self, *args, **kwargs):
        self.template = 'templates/resize.html'
        super(ResizeHandler, self).__init__(*args, **kwargs)

    def post(self):
        img = Image(self.request.get('file'))
        json = self.request.get('json', False)
        height = int(self.request.get('height', default_value='1'))
        width = int(self.request.get('width', default_value='1'))
        img.resize(width, height)
        resized = img.execute_transforms()
        self.render(image=resized, data={'height':height, 'width':width})

urls = []
urls.append(('/', MainHandler))
urls.append(('/about', AboutHandler))
urls.append(('/resize', ResizeHandler))
urls.append(('/crop', CropHandler))
urls.append(('/rotate', RotateHandler))
urls.append(('/horizontal', HorizontalFlipHandler))
urls.append(('/vertical', VerticalFlipHandler))
urls.append(('/lucky', ImFeelingLuckyHandler))

application = webapp.WSGIApplication(urls, debug=True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
  main()
