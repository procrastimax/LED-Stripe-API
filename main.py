#!/usr/bin/python3

from bottle import run, get, BaseResponse, request
import pigpio

RED_CHANNEL_PIN: int = 21
GREEN_CHANNEL_PIN: int = 16
BLUE_CHANNEL_PIN: int = 20

# these represent the duty cycles for PWM
red_channel_value: int = 0
green_channel_value: int = 0
blue_channel_value: int = 0
brightness_value : int = 100

pi = pigpio.pi()


def setup_GPIO():
    print("Setting up GPIO...")
    pi.set_PWM_dutycycle(RED_CHANNEL_PIN, red_channel_value)
    pi.set_PWM_dutycycle(GREEN_CHANNEL_PIN, green_channel_value)
    pi.set_PWM_dutycycle(BLUE_CHANNEL_PIN, blue_channel_value)


def close_GPIO():
    print("Closing all GPIO...")
    pi.stop()


def set_red(value):
    pi.set_PWM_dutycycle(RED_CHANNEL_PIN, value)


def set_green(value):
    pi.set_PWM_dutycycle(GREEN_CHANNEL_PIN, value)


def set_blue(value):
    pi.set_PWM_dutycycle(BLUE_CHANNEL_PIN, value)

def set_brightness(value) -> str:
    global brightness_value
    brightness_value = value
    
    red_value = round(float(red_channel_value) * (float(brightness_value) / 100.0))
    green_value = round(float(green_channel_value) * (float(brightness_value) / 100.0))
    blue_value = round(float(blue_channel_value) * (float(brightness_value) / 100.0))

    # update all channels
    set_red(red_value)
    set_green(green_value)
    set_blue(blue_value)
    return f"{red_value},{green_value},{blue_value},{brightness_value}"

@get("/alive")
@get("/test")
@get("/ping")
@get("/health")
def health_check():
    return "I am alive!"

@get("/brightness/<value:int>")
def set_brightness_value(value):
    if (_check_relative_value(value)):
        return set_brightness(value)
    else:
        return BaseResponse(
            body="Unvalid value! Set a value between 0 and 100!", status=400)
        
@get("/brightness")
def get_brightness_value():
    return f"{brightness_value}"

@get("/r/<value:int>")
@get("/red/<value:int>")
def set_red_channel(value):
    if (_check_value(value)):
        global red_channel_value
        red_channel_value = round(float(value) * (float(brightness_value) / 100.0))
        set_red(red_channel_value)
        return f"{red_channel_value}"
    else:
        return BaseResponse(
            body="Unvalid value! Set a value between 0 and 255!", status=400)


@get("/r")
@get("/red")
def get_red_channel():
    return f"{red_channel_value}"


@get("/g/<value:int>")
@get("/green/<value:int>")
def set_green_channel(value):
    if (_check_value(value)):
        global green_channel_value
        green_channel_value = round(float(value) * (float(brightness_value) / 100.0))
        set_green(green_channel_value)
        return f"{green_channel_value}"
    else:
        return BaseResponse(
            body="Unvalid value! Set a value between 0 and 255!", status=400)


@get("/g")
@get("/green")
def get_green_channel():
    return f"{green_channel_value}"


@get("/b/<value:int>")
@get("/blue/<value:int>")
def set_blue_channel(value):
    if (_check_value(value)):
        global blue_channel_value
        blue_channel_value = round(float(value) * (float(brightness_value) / 100.0))
        set_blue(blue_channel_value)
        return f"{blue_channel_value}"
    else:
        return BaseResponse(
            body="Unvalid value! Set a value between 0 and 255!", status=400)


@get("/b")
@get("/blue")
def get_blue_channel():
    return f"{blue_channel_value}"


@get("/setValues")
def set_all_values():
    """
        This query is able to set all channels with HTTP Query variables
        This is the preferred method to set the channels.
        An example query could look like: .../setChannels?r=VALUE&g=VALUE&b=VALUE&brightness=VALUE
    """

    redVal = request.query.r
    greenVal = request.query.g
    blueVal = request.query.b
    brightness = request.query.brightness

    if not redVal:
        redVal = -1

    if not greenVal:
        greenVal = -1

    if not blueVal:
        blueVal = -1

    if not brightness:
        brightness = -1

    # we dont know if the passed parameters are valid int, so we try to convert them
    # if one of the parameters is not a valid int, the complete query is
    # invalid, this is why we only use one try/except construct
    try:
        redVal = int(redVal)
        greenVal = int(greenVal)
        blueVal = int(blueVal)
        brightness = int(brightness)
    except ValueError:
        return BaseResponse(
            body=f"Unvalid value(s)! Query {request.query_string} does not contain valid integer query parameter!", status=400
        )

    if _check_value(redVal) and isinstance(redVal, int):
        global red_channel_value
        red_channel_value = round(float(redVal) * (float(brightness_value) / 100.0))

    if _check_value(greenVal) and isinstance(greenVal, int):
        global green_channel_value
        green_channel_value = round(float(greenVal) * (float(brightness_value) / 100.0))

    if _check_value(blueVal) and isinstance(blueVal, int):
        global blue_channel_value
        blue_channel_value = round(float(blueVal) * (float(brightness_value) / 100.0))
        
    # brightness should be set as last, since it modified the previous values
    if _check_relative_value(brightness) and isinstance(brightness, int):
        set_brightness(brightness)

    return f"{red_channel_value},{green_channel_value},{blue_channel_value},{brightness_value}"


@get("/getValues")
def get_current_values():
    return f"{red_channel_value},{green_channel_value},{blue_channel_value},{brightness_value}"


@get("/off")
def turn_off_all():
    set_brightness(0)
    return f"{red_channel_value},{green_channel_value},{blue_channel_value},{brightness_value}"


@get("/help")
@get("/h")
def get_help():
    help_text: str = """
    <h1>Help - Supported functions</h1>
    <b>/help</b> - shows this help page</br>
    <b>/brightness/VALUE</b> - sets brightness to VALUE (0-100)</br>
    <b>/brightness</b> - gets brightness value</br>
    <b>/(r/red)/VALUE</b> - sets red channel to VALUE (0-255)</br>
    <b>/(g/green)/VALUE</b> - sets green channel to VALUE (0-255)</br>
    <b>/(b/blue)/VALUE</b> - sets blue channel to VALUE (0-255)</br>
    <b>/(r/red)</b> - gets red channel</br>
    <b>/(g/green)</b> - gets green channel</br>
    <b>/(b/blue)</b> - gets blue channel</br>
    <b>/setValues?r=VALUE&g=VALUE&b=VALUE</b> - sets the r,g,b and brightness values via HTTP Query variables</br>
    <b>/getValues</b> - gets the r,g,b and brightness values as csv</br>
    <b>/off</b> - turns all channel off (0)</br>
    """
    return help_text


def _check_value(val: int) -> bool:
    return val in range(0, 256)

def _check_relative_value(val: int) -> bool:
    return val in range(0, 101)

def main():
    print("Starting server...")
    setup_GPIO()
    run(host="0.0.0.0", port=8000, quiet=True)

    print("Turning off all channels...")
    turn_off_all()
    close_GPIO()


if __name__ == "__main__":
    main()
