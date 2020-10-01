from slackclient import SlackClient
import json
import time
from audio_player import AudioPlayer
from weather import Weather
from alarm import Alarm

def main():

    def wake_up_routine(number):
        if number == 1:
            w1 = Weather()
            send_message = "God morgen! I dag kan du forvente følgende temperaturer " + w1.min_max_weather()
            channel = "raspberry-pi"
            slack_client.api_call("chat.postMessage", channel=channel, text=send_message)
            audio = AudioPlayer()
            audio.music_then_radio("random", 10, 300, "random")

    tokens = {}
    with open('configs.json') as json_data:
        tokens = json.load(json_data)

    slack_client = SlackClient(tokens.get("slack_bot_token"))
    alarm = Alarm()

    if slack_client.rtm_connect():
        while slack_client.server.connected is True:
            messages = slack_client.rtm_read()
            if alarm.alarm_active():
                if alarm.check_alarm():
                    wake_up_routine(1)

            print(messages)

            if messages:
                for message in messages:
                    if message.get('text') is not None and  "BOT TEST" in message.get('text'):
                        channel = message["channel"]
                        send_message = "Responding to `BOT TEST` message sent by user <@%s>" % message["user"]
                        slack_client.api_call("chat.postMessage", channel=channel, text=send_message)

                    if message.get('text') is not None and  "audio" in message.get('text'):
                        command = message.get('text')
                        command_lst = command.split()
                        command = " ".join(command_lst[1:])
                        au1 = AudioPlayer()
                        au1.audio_handler(command)

                    if message.get('text') is not None and "weather_now" in message.get('text'):
                        command = message.get('text')
                        command_lst = command.split()
                        command = " ".join(command_lst[1:])
                        weather = Weather()
                        send_message = weather.weather_handler(command)
                        channel = message["channel"]
                        slack_client.api_call("chat.postMessage", channel=channel, text=send_message)

                    if message.get('text') is not None and "weather_min_max" in message.get('text'):
                        weather = Weather()
                        send_message = weather.min_max_weather()
                        channel = message["channel"]
                        slack_client.api_call("chat.postMessage", channel=channel, text=send_message)

                    if message.get('text') is not None and "set_alarm" in message.get('text'):
                        command = message.get('text')
                        command_lst = command.split()
                        alarm.set_alarm(int(command_lst[1]), int(command_lst[2]), int(command_lst[3]), int(command_lst[4]))


            time.sleep(1)
    else:
        print("Connection Failed")


if __name__ == "__main__":
    main()
