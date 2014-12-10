# google-app-engine

This repository contains various applications designed for the [Google App Engine] platform.

### gae-photoshare-app

This is a simple yet useful application, that demonstrates how to build a web application, and interact with App Engine through various API-s.

Some of the things you may learn by diving into it:
  - Using a HTML template to structure a website
  - Handling HTTP requests in App Engine
  - Interacting with the Datastore, for holding persistent data
  - Using the Memcache to store frequently accessed images
  - Creating an App Engine Cron task, that will display memcache statistics

### Documentation
The official [App Engine Documentation] is probably the best place to start

The [Cloud Playground] is an awesome tool that allows testing various features in the browser, without the need install the SDK on your computer.

The HTML template is one adapted from the [Sunflower Template]

### Known issues

I recommend testing directly on the App Engine backend

The [PIL Library] does not come bundled with the SDK, so it will not work by default on the development server. You will need to install it independently of your SDK, to get it to work locally.

### Development

1. Create a Google App Engine account
2. Go to your [Cloud Console], and create a new project
3. Clone this repository
```sh
$ git clone https://github.com/tudor1805/google-app-engine.git
```
4. Edit the app.yaml file, and replace your-app-id, with the id of the project (you cand find in the [Cloud Console] of the project)
```sh
$ sed -i 's/your-app-id/my-app-id/g' gae-photoshare-app/app.yaml
```
5. Upload your application (you may need to wait a while)
```sh
$ appcfg.py update gae-photoshare-app/
```
6. Open your browser, and point it to the following address (my-app-id is the actual id of the project)
```sh
http://my-app-id.appspot.com/
```

### Debugging

1. Uploading the application
```sh
$ appcfg.py update gae-photoshare-app/
```
2. Running the application (local server)
```sh
$ dev_appserver.py gae-photoshare-app/
```
3. Clean and update indexes
```sh
$ appcfg.py vacuum_indexes gae-photoshare-app/
$ appcfg.py update_indexes gae-photoshare-app/
```
4. Open your browser
```sh
http://localhost:8080/           -> Your deployed site
http://localhost:8000/instances  -> Application console
```

### Todo's

 - The current app uses a single photo album. Extend it, so that it can use an arbitrary number of photo albums. Albums could be public/private.
 - Allow the sharing of photos with other people. (Ex: generate a unique link that holds the image, and give it to other people)
 - Implement image comments
 - Maybe make it as a service, so that it can be used by mobile apps
 - Create a mobile app that takes photos and uploads them to the user's album of choice

### Version
1.0

##License
GPL v.2

[Google App Engine]:https://cloud.google.com/appengine/
[Sunflower Template]: http://www.tooplate.com/view/2039-sunflower
[App Engine Documentation]: https://cloud.google.com/appengine/docs
[Cloud Playground]: https://code.google.com/p/cloud-playground/
[PIL Library]: http://www.pythonware.com/products/pil
[Cloud Console]: https://cloud.google.com/
