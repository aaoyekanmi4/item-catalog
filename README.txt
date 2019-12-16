Item Catalog Project README

To Run:

Create a Google account in order to sign in.

-To View Online
Go to https://item-catalog-udacity.herokuapp.com

About:


Google Sign in is used to login to the app using a hybrid server-client OAuth2 flow.

The app was deployed to the internet using Heroku.
The Procfile and requirements.txt file exist for that purpose.

The database itself is found in the model folder along with catlog_setup.py, the SQLalchemy python code that generates the database. The file instruments.py was used to populate the database initially.

The file music_store.py is the main file used to run the program. The files in the handlers folder are the functions used in music_store.py for each page.

The client_secrets.json file contains information for the Google hybrid oauth flow.

The css, images, and js used to run the app are found in the static folder.

The templates folder contains the html pages for each view.

The Vagrantfile and .vagrant folder are used to provision and run the virtual machine for the app.

Attributions:

The information and images for the items are from amazon.com











