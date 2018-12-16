# microservice_design
validate mobile numbers from large csv file input using backend microservices with object oriented coding principle

PhoneNumber Lookup API  
This API checks if a valid number is provided, in the most basic sense. The only input that is needed is an international number or a national number with the country code. The lookup API will tell you if the number has an unknown format (HTTP status 400) or if it is correct (200, \o/). When the number is correct, it will provide you with a JSON object with additional information; country-code, country-prefix, type and the phone number formatted in four different ways.  
