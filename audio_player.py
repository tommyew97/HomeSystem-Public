import simpleaudio as sa
from random import randint
#from pi_hat import PiHat
import time
import os
import webbrowser
import pyautogui

class AudioPlayer:

    def __init__(self):
        self.stations = {"p1": "https://onlineradiobox.com/no/?cs=no.nrkp1&played=1", "p3": "https://onlineradiobox.com/search?cs=no.nrkp3&played=1&q=p3",
                          "p4": "https://onlineradiobox.com/no/?cs=no.p4&played=1&p=0", "nrj": "https://onlineradiobox.com/search?cs=no.nrj&played=1&q=nrj"}


    def play(self, track):
        wave_obj = sa.WaveObject.from_wave_file("audio/" + track)
        play_obj = wave_obj.play()
        play_obj.wait_done()


    def play_random(self):
        tracks = self.get_track_names()
        random_num = randint(0, len(tracks)-1)
        self.play(tracks[random_num])

    def get_random_track(self):
        tracks = self.get_track_names()
        random_num = randint(0, len(tracks) - 1)
        return tracks[random_num]

    def get_track_names(self):
        tracks = []
        f = open("save_files/track_names.txt", "r")
        for x in f:
            tracks.append(x.rstrip())
        return tracks

    def play_for_duration(self, track, duration):
        wave_obj = sa.WaveObject.from_wave_file("audio/" + track)
        play_obj = wave_obj.play()
        start = time.time()
        #hat = PiHat()
        while True:
            #if hat.buttonPress() == "middle":
                #play_obj.stop()
                #return
            if (time.time() - start) >= duration:
                play_obj.stop()
                return
            time.sleep(1)

    def play_radio(self, station, duration):
        webbrowser.open("https://vg.no")
        time.sleep(1)
        pyautogui.click(100, 100)
        time.sleep(1)
        url = ""
        if station == "P1":
            url = self.stations["p1"]
        elif station == "NRJ":
            url = self.stations["nrj"]
        elif station == "P3":
            url = self.stations["p3"]
        elif station == "P4":
            url = self.stations["p4"]
        elif station == "random":
            url = self.get_random_station()
        else:
            print("Wrong radio station.")
        webbrowser.open(url)

        if duration:
            time.sleep(duration)
            os.system("pkill chromium")

    def get_random_station(self):
        stations = []
        for station in self.stations:
            stations.append(self.stations[station])
        random_num = randint(0, len(stations) - 1)
        return stations[random_num]

    def add_track_name(self, track_name):
        f = open("save_files/track_names.txt", "a")
        f.write("\n")
        f.write(track_name)
        f.close()

    def delete_track_name(self, track):
        tracks = []
        f = open("save_files/track_names.txt", "r")
        for x in f:
            if x.rstrip() != track:
                tracks.append(x.rstrip())
        f.close()

        f = open("save_files/track_names.txt", "w")
        counter = 0
        for x in tracks:
            counter += 1
            if counter == len(tracks):
                f.write(x)
            else:
                f.write(x + "\n")

    def music_then_radio(self, track, duration1, duration2, station):
        if track == "random":
            track = self.get_random_track()
        self.play_for_duration(track, duration1)
        self.play_radio(station, duration2)

    def audio_handler(self, command):
        print(command)
        if command == "play_random":
            self.play_for_duration("J Cole - No Role Models (2014 Forest Hills Drive) LYRIC VIDEO.wav", 11)
        elif command == "music_then_radio_random":
            self.music_then_radio("random", 10, 10, "random")
