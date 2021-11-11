#!/usr/bin/python3

from bottle import run, get, BaseResponse
import pigpio

RED_CHANNEL_PIN: int = 21
GREEN_CHANNEL_PIN: int = 16
BLUE_CHANNEL_PIN: int = 20

# these represent the duty cycles for PWM
red_channel_value: int = 0
green_channel_value: int = 0
blue_channel_value: int = 0

#PWM_FREQUENCY: int = 200

pi = pigpio.pi()

def setup_GPIO():
    print("Setting up GPIO...")
    pi.set_PWM_dutycycle(RED_CHANNEL_PIN, red_channel_value)
    pi.set_PWM_dutycycle(GREEN_CHANNEL_PIN, green_channel_value)
    pi.set_PWM_dutycycle(BLUE_CHANNEL_PIN, blue_channel_value)

def close_GPIO():
    print("Closing all GPIO...")
    pi.stop()

def set_red_channel(value):
    global red_channel_value, RED_PWM
    red_channel_value = value
    pi.set_PWM_dutycycle(RED_CHANNEL_PIN, red_channel_value)


def set_green_channel(value):
    global green_channel_value, GREEN_PWM
    green_channel_value = value
    pi.set_PWM_dutycycle(GREEN_CHANNEL_PIN, green_channel_value)


def set_blue_channel(value):
    global blue_channel_value, BLUE_PWM
    blue_channel_value = value
    pi.set_PWM_dutycycle(BLUE_CHANNEL_PIN, blue_channel_value)

@get("/alive")
@get("/test")
@get("/ping")
@get("/health")
def health_check():
    return "API is alive!"


@get("/r/<value:int>")
@get("/red/<value:int>")
def handle_red_change(value):
    if value >= 0 and value <= 255:
        set_red_channel(value)
        return f"Set red channel to {str(value)}"
    else:
        response = BaseResponse(
            body="Unvalid value! Set a value between 0 and 255!", status=400
        )
        return response


@get("/g/<value:int>")
@get("/green/<value:int>")
def handle_green_change(value):
    if value >= 0 and value <= 255:
        set_green_channel(value)
        return f"Set green channel to {str(value)}"
    else:
        response = BaseResponse(
            body="Unvalid value! Set a value between 0 and 255!", status=400
        )
        return response


@get("/b/<value:int>")
@get("/blue/<value:int>")
def handle_blue_change(value):
    if value >= 0 and value <= 255:
        set_blue_channel(value)
        return f"Set blue channel to {str(value)}"
    else:
        response = BaseResponse(
            body="Unvalid value! Set a value between 0 and 255!", status=400
        )
        return response


@get("/all/<red:int>,<green:int>,<blue:int>")
def handle_all_change(red, green, blue):
    if (
        red >= 0
        and red <= 255
        and green >= 0
        and green <= 255
        and blue >= 0
        and blue <= 255
    ):
        set_red_channel(red)
        set_green_channel(green)
        set_blue_channel(blue)
        return f"Set channels to: red ({red}), green ({green}), blue ({blue})"
    else:
        response = BaseResponse(
            body="Unvalid value! Set a value between 0 and 255!", status=400
        )
        return response


@get("/white")
def turn_on_all_channels():
    set_red_channel(255)
    set_green_channel(255)
    set_blue_channel(255)
    return "Set all channels on (100%)"


@get("/off")
def turn_off_all_channels():
    set_red_channel(0)
    set_green_channel(0)
    set_blue_channel(0)
    return "Set all channels off"


@get("/values")
def get_current_values():
    return f"Current brightness values: r ({red_channel_value}), g ({green_channel_value}), b({blue_channel_value})"


@get("/help")
@get("/h")
def get_help():
    help_text: str = """
    <h1>Help - Supported functions</h1>
    <b>/help</b> - shows this help page</br>
    <b>/(r/red)/VALUE</b> - sets red channel to VALUE (0-100)</br>
    <b>/(g/green)/VALUE</b> - sets green channel to VALUE (0-100)</br>
    <b>/(b/blue)/VALUE</b> - sets blue channel to VALUE (0-100)</br>
    <b>/white</b> - turns all channels on (100)</br>
    <b>/off</b> - turns all channel off (0)</br>
    <b>/values</b> - returns the current values of all channels</br>
    """
    return help_text


def main():
    print("Starting server...")
    setup_GPIO()
    run(host="0.0.0.0", port=8000)
    
    print("Turning off all channels...")
    turn_off_all_channels()
    set_red_channel(0)
    set_green_channel(0)
    set_blue_channel(0)
    close_GPIO()

    print("Turning off all channels...")
    turn_off_all_channels()
    set_red_channel(0)
    set_green_channel(0)
    set_blue_channel(0)
    close_GPIO()

if __name__ == "__main__":
    main()
