from slackclient import SlackClient
import json
import time
from audio_player import AudioPlayer
from weather import Weather
from alarm import Alarm
from datetime import datetime
from prices import Prices

sent = False


def main():
    prices = Prices()
    weather = Weather()

    def wake_up_routine(number):
        if number == 1:
            w1 = Weather()
            send_message = "God morgen Tommy! I dag kan du forvente følgende temperaturer " + w1.min_max_weather()
            channel = "raspberry-pi"
            slack_client.api_call("chat.postMessage", channel=channel, text=send_message)
            audio = AudioPlayer()
            audio.music_then_radio("random", 10, 300, "random")

    def send_bitcoin_price(channel):
        price_bit = prices.get_bitcoin_price()
        send_msg_bit = "Den nåværende prisen for Bitcoin er: " + price_bit[0]
        returns_msg_bit = "Din nåværende avkastning på Bitcoin er: " + price_bit[1]
        slack_client.api_call("chat.postMessage", channel=channel, text=send_msg_bit)
        slack_client.api_call("chat.postMessage", channel=channel, text=returns_msg_bit)

    def send_dogecoin_price(channel):
        price_dog = prices.get_dogecoin_price()
        send_msg_dog = "Den nåværende prisen for Dogecoin er: " + price_dog[0]
        # returns_msg_dog = "Din nåværende avkastning på Bitcoin er: " + price_dog[1]
        slack_client.api_call("chat.postMessage", channel=channel, text=send_msg_dog)
        # slack_client.api_call("chat.postMessage", channel=channel, text=returns_msg_dog)

    def send_litecoin_price(channel):
        price_ltc = prices.get_litecoin_price()
        send_msg_ltc = "Den nåværende prisen for Litecoin er: " + price_ltc[0]
        returns_msg_ltc = "Din nåværende avkastning på Litecoin er: " + price_ltc[1]
        slack_client.api_call("chat.postMessage", channel=channel, text=send_msg_ltc)
        slack_client.api_call("chat.postMessage", channel=channel, text=returns_msg_ltc)

    def morning_messages():
        time = datetime.now().time()
        hour = str(time)[0:2]
        global sent
        if hour == "09" and not sent:
            morning_prices()
            morning_weather()
            sent = True
        if hour == "10" and sent:
            sent = False

    def morning_weather():
        curr_weather = weather.min_max_weather().split()
        minimum = curr_weather[0]
        maximum = curr_weather[1]
        send_message = f"I dag kan du forvente temperaturer mellom {minimum} og {maximum}."
        channel = "raspberry-pi"
        slack_client.api_call("chat.postMessage", channel=channel, text=send_message)

    def morning_prices():
        channel = "raspberry-pi"
        good_morning_msg = "God morgen Tommy! Håper du får en fin dag :)"
        slack_client.api_call("chat.postMessage", channel=channel, text=good_morning_msg)
        send_bitcoin_price(channel)
        send_dogecoin_price(channel)
        send_litecoin_price(channel)

    tokens = {}
    with open('configs.json') as json_data:
        tokens = json.load(json_data)
    slack_client = SlackClient(tokens.get("slack_bot_token"))
    alarm = Alarm()
    if slack_client.rtm_connect(auto_reconnect=True):
        print("Connected!")
        while True:
            morning_messages()
            try:
                messages = slack_client.rtm_read()
            except:
                print("Disconnected.")
                print("Reconnecting...")
                time.sleep(20)
                slack_client.rtm_connect()
                messages = slack_client.rtm_read()
            if alarm.alarm_active():
                if alarm.check_alarm():
                    wake_up_routine(1)
            # print(messages)
            if messages:
                for message in messages:
                    if message.get("subtype") is None and message.get('user') is not None and message.get(
                            'text') is not None and "BOT TEST" in message.get('text'):
                        channel = message["channel"]
                        send_message = "Responding to `BOT TEST` message sent by user <@%s>" % message["user"]
                        slack_client.api_call("chat.postMessage", channel=channel, text=send_message)

                    if message.get("subtype") is None and message.get('user') is not None and message.get(
                            'text') is not None and "audio" in message.get('text'):
                        command = message.get('text')
                        command_lst = command.split()
                        command = " ".join(command_lst[1:])
                        au1 = AudioPlayer()
                        au1.audio_handler(command)

                    if message.get("subtype") is None and message.get('user') is not None and message.get(
                            'text') is not None and "weather_now" in message.get('text'):
                        command = message.get('text')
                        command_lst = command.split()
                        command = " ".join(command_lst[1:])
                        weather = Weather()
                        send_message = weather.weather_handler(command)
                        channel = message["channel"]
                        slack_client.api_call("chat.postMessage", channel=channel, text=send_message)

                    if message.get("subtype") is None and message.get('user') is not None and message.get(
                            'text') is not None and "weather_min_max" in message.get('text'):
                        weather = Weather()
                        send_message = weather.min_max_weather()
                        channel = message["channel"]
                        slack_client.api_call("chat.postMessage", channel=channel, text=send_message)

                    if message.get("subtype") is None and message.get('user') is not None and message.get(
                            'text') is not None and "set_alarm" in message.get('text'):
                        command = message.get('text')
                        command_lst = command.split()
                        alarm.set_alarm(int(command_lst[1]), int(command_lst[2]), int(command_lst[3]),
                                        int(command_lst[4]))

                    if message.get("subtype") is None and message.get('user') is not None and message.get(
                            'text') is not None and "get_bitcoin_price" in message.get('text'):
                        send_bitcoin_price(message["channel"])

                    if message.get("subtype") is None and message.get('user') is not None and message.get(
                            'text') is not None and "get_dogecoin_price" in message.get('text'):
                        send_dogecoin_price(message["channel"])

                    if message.get("subtype") is None and message.get('user') is not None and message.get(
                            'text') is not None and "get_litecoin_price" in message.get('text'):
                        send_litecoin_price(message["channel"])

                    if message.get("subtype") is None and message.get('user') is not None and message.get(
                            'text') is not None and "get_crypto_price" in message.get('text'):
                        channel = message["channel"]
                        send_bitcoin_price(channel)
                        send_dogecoin_price(channel)
                        send_litecoin_price(channel)

            time.sleep(4)
    else:
        print("Connection Failed")


if __name__ == "__main__":
    main()
