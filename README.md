# Week 3 Varsity | Uploads & SocketIO

### Check out the [resources](https://github.com/flask-django-independent-study/varsity/blob/master/Resources/Week-3.md) then complete the TODOs in the project

## The Project

This week we will be building a voting app using Flask, Flask-Uploads, Flask-SocketIO, SQLAlchemy, and WTForms. You will be able to vote for someone, see the results live, and save the results to a database. You will be able to add new candidates by filling out a form along with an image of the candidate.

**Watch demo.mov to see what the finished result should look like.**

#### From the Flask-Uploads Docs

> Flask-Uploads allows your application to flexibly and efficiently handle file uploading and serving the uploaded files. You can create different sets of uploads - one for document attachments, one for photos, etc. - and the application can be configured to save them all in different places and to generate different URLs for them.

#### From the Flask-SocketIO Docs

> Flask-SocketIO gives Flask applications access to low latency bi-directional communications between the clients and the server.

**Please note we will be using Flask-Reuploaded instead of Flask-Uploads. The maintainer for Flask-Uploads stopped updating the library and there are now bugs when trying to integrate with other more up-to-date packages. Flask-Reuploaded is still being actively maintained.**


## Stretch Challenges

* When adding a new candidate, the votes don't go with them. The candidate either, moves from the left side to non-exsistent, or moves from the right side to the left side. In either case, the votes aren't correlated with the candidate. Fix this.
* Add a default picture for candidate1 and candidate2.
* Figure out how to resize images to 1000x1000 before we save them to the file system so that there won't be large pictures taking up excessive space.
* Add a loading animation to display in between the time we submit a new candidate and that candidate is rendered on screen. (Note: this delay may not be very long depending on the file size of the uploaded image)

If you you have any questions, feel free to contact Starlight or Sid via Slack.

If you find a typo, or other issue with the repository, please add an issue so that we can address it!

Thank you for your feedback!
