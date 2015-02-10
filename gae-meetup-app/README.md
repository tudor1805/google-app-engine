# gae-meetup-app

This repository contains a Social Web application designed for the [Google App Engine] platform.

### gae-meetup-app

This project shows how to build an Android social application that leverages off the App Engine platform as a backend service.

The application requires the user to have a Google+ account. It will connect to the Google+ service on behalf of the user, and extract the user's contacts. It will, then show the users found in close proximity to the user on a map.
Each user can select to be invisible to other friends.

Some of the things you may learn by diving into it:
  - Connecting to Google+ service from an Android app in order to extract user contacts
  - Using the Google Maps API in an Android app
  - Interacting with the Datastore, for holding persistent data
  - Performing geolocation queries using the Google App Engine platform

### Details

The communication between the Android Client and the App Engine service is done using [Google Cloud Endpoints].

The support for geolocation queries is done through the awesome [Geomodel] python library.

### Documentation
The official [App Engine Documentation] is probably the best place to start

The [Cloud Playground] is an awesome tool that allows testing various features in the browser, without the need install the SDK on your computer.

### Known issues

In order to succeed with deploying the application, you need to perform at least three authentications:

1. Android app authentication with Google Maps service
2. Android app authentication with Google Plus service
3. Android app authentication with Google Cloud Endpoint service

Unfortunately, at this stage a fresh deployment will be painful, as you will need to generate at least a Client ID and two API keys in the App Engine console, to get everything to work successfully.

### Development

1. Create a Google App Engine account
2. Go to your [Cloud Console], and create a new project
4. Enable from the console the following APIs:
 1. Google Maps v.2 Api
 2. Google Cloud Endpoints Api
 3. Google+ Api
 4. [possibly 1-2 more]
5. Generate Authentication Keys and Client IDs
 1. Generate a new Client ID for Cloud Endpoints
 2. Generate a new Client ID for Google Play Services/ Google +
 3. Generate an API key for Google Maps API
6. Clone this repository

    ```sh
    $ git clone https://github.com/tudor1805/google-app-engine.git
    ```
    
6. Edit the app.yaml file, and replace your-app-id, with the id of the project (you can find it in the [Cloud Console] of the project)

    ```sh
    $ cd google-app-engine
    $ sed -i 's/your-app-id/my-app-id/g' gae-meetup-app/app.yaml
    ```

7. Upload your application (you may need to wait a while)

    ```sh
    $ appcfg.py update gae-meetup-app/
    ```

6. Open your browser, and point it to the following address (my-app-id is the actual id of the project)

    ```sh
    http://my-app-id.appspot.com/
    ```
7. Open The Android App project, clean & build it

8. Deploy the .apk file to an android device

### Debugging

1. Uploading the application

    ```sh
    $ appcfg.py update gae-meetup-app/
    ```
2. Running the application (local server)

    ```sh
    $ dev_appserver.py gae-meetup-app/
    ```

3. Clean and update indexes

    ```sh
    $ appcfg.py vacuum_indexes gae-meetup-app/
    $ appcfg.py update_indexes gae-meetup-app/
    ```

4. Open your browser
 
    ```sh
    http://localhost:8080/           -> Your deployed site
    http://localhost:8000/instances  -> Application console
    http://localhost:8080/_ah/api    -> Test Endpoints API
    ```

### Todo's

 - The communication protocol between the client and server is resource-intensive, as it is poll-based. Replace it with WebSockets implementation.
 - Implement capability to set up meetings
 - Investigate newly added support for Geolocation queries in App Engine, see if it can replace Geomodel
 
### Version
1.0

##License
GPL v.2

[Google App Engine]:https://cloud.google.com/appengine/
[Google Cloud Endpoints]: https://cloud.google.com/endpoints/
[App Engine Documentation]: https://cloud.google.com/appengine/docs
[Cloud Playground]: https://code.google.com/p/cloud-playground/
[Geomodel]: https://code.google.com/p/geomodel/
[Cloud Console]: https://cloud.google.com/
[WebSockets]: https://www.websocket.org/
