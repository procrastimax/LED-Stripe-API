# LED Stripe API

A simple REST-API to control a RGB-LED stripe with a Raspberry Pi.

## Commands


| Type        | REQUEST        | RESPONSE      | Codes             | Description
| ------------|:--------------:| -------------:|-------------------|------------
| GET         | /health        | "I am alive   | 200 OK            | Checks if the API is available
| GET         | /brightness    | INT (0-100)   | 200 OK, 400 ERR   | Returns the value of the brightness value
| GET         | /r             | INT (0-255)   | 200 OK, 400 ERR   | Returns the value of the red channel
| GET         | /g             | INT (0-255)   | 200 OK, 400 ERR   | Returns the value of the green channel
| GET         | /b             | INT (0-255)   | 200 OK, 400 ERR   | Returns the value of the blue channel
| GET         | /brightness/VAL| INT (0-100)   | 200 OK, 400 ERR   | Sets the value of the brightness value - all other channels get updated accordingly.
| GET         | /r/VAL         | INT (0-255)   | 200 OK, 400 ERR   | Sets the value of the red channel, returns red value after trying to set it.
| GET         | /g/VAL         | INT (0-255)   | 200 OK, 400 ERR   | Sets the value of the green channel, returns green value after trying to set it.
| GET         | /b/VAL         | INT (0-255)   | 200 OK, 400 ERR   | Sets the value of the blue channel, returns red value after trying to set it.
| GET         | /setValues?r=VAL1&g=VA2L&b=VAL3&brightness=VAL4    | INT,INT,INT (0-255), INT (0-100)   | 200 OK, 400 ERR   | Sets all values r,g,b and brightness with query parameters, returns RGB values and brightness in CSV format
| GET         | /getValues     | INT,INT,INT (0-255), INT (0-100)   | 200 OK, 400 ERR   | Returns RGB values and brightness in CSV format
| GET         | /help          | String                | 200 OK            | Returns a short HTML-Text to show API functions
| GET         | /off           | INT,INT,INT (0-255)   | 200 OK, 400 ERR   | Sets all channel values to 0, returns values in CSV after trying to set them to 0.


