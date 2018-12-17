# Phone Number validation Application

The purpose of this app is to validate phone numbers based on the user input of csv file or a single phonenumber.

## Getting Started

For a given country (e.g., South Africa), a list of telephone numbers will be given by user.
This app will be doing the below tasks -
● Consume the provided file via any of the following means eg. upload from a browser / console call / API.
● Test each number and check for correctness, attempt to correct incorrectly formed numbers
and reject numbers that are invalid. (27831234567 is the correct format for this exercise).
● Store the results appropriately to Temporary File.

## Usages
 INPUT :

  1.) A csv file with id and number fields for each entry.
  2.) Individual Phone Number verification (service availble only via RestAPI)

 OUTPUT:
1.)  Display results by the following means
```
a. Acceptable numbers
b. Corrected numbers
c. Invalid numbers
```
2.)   Validate the individual number whether or not the number is valid

### Prerequisites

pip install following packages

```
Flask==1.0.2
Flask-HTTPAuth==3.2.4
phonenumbers==8.10.2
```

### Installing

From terminal execute server.py. This will start the web service at 127.0.0.1 on port 5000.

### Accessing the Service
To access the service via use below api -
```
 curl -i -u admin:nopass -X POST localhost:5000/phnumbers/upload -F file=@data.csv.
 curl -i -u admin:nopass -X GET localhost:5000/phnumbers/file_status/valid_numbers.csv.
 curl -i -u admin:nopass -X GET localhost:5000/phnumbers/status/27717278645.
```

Using a Webbrowser type following url-
```
127.0.0.1:5000.
```

## Running the tests

status: In progress

 - test_number_validation.py


## Deployment


## Built With

* [Flask](http://flask.pocoo.org/) - The web framework
* [PhoneNumbers](https://github.com/googlei18n/libphonenumber) - Phonenember Parsing.

## Authors

* **Tanmoy Roy** - *Initial work* - [github](https://github.com/roytanmoy/identity_microservice)

## Acknowledgments

* Thanks to everyone whose code was used

