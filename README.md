# Catalog Project

## Running under Win10

To run this project you will need 
[Git Bash](https://git-scm.com/), 
[Python 3](https://www.python.org/)& 
[Vagrant](https://www.vagrantup.com/) 
instled on your machine.

Copy files into your local vagrant folder.

## Description:
   A web application that lists items within various categories, using a Google OAuth2.0 login system. Registered users can add, edit and delete items.
   The app also has a JSON endpoint to export all categories with their items in the JSON format.

#### How to run it:

   1.Install virtualbox and vagrant first.
   
   2.cd into the folder named vagrant.
   
   3.Run "vagrant up" and "vagrant ssh" to log into the virtual environment.
   
   4.Load database file 
   ```bash
   python /vagrant/catalog/database_setup.py
   ```
   5.Load basic database 
   ```bash
   python /vagrant/catalog/add_items.py
   ```
   6.Run web application
   ```bash
   python /vagrant/catalog/application.py
   ```
   7.Visit [http://localhost:8000/catalog/index](http://localhost:8000/catalog/index) in the browser.
   
   8.Use your Google account to log into the website.
   
   9.Add new items from the "Add Item" option on the home page.
   
   10.Click each item to see its description.
   
   11.Edit and delete your own items in each item's description page.
   
   12.Visit [http://localhost:8000/catalog/JSON](http://localhost:8000/catalog/JSON) to access the JSON endpoint.
   
   
#### Credits:

   Part of this application's code uses components from Udacity's Nanodegree course in Full Stack Web Developement.
