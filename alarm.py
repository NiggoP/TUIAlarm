#!/bin/python3

from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Button, Static
from textual.reactive import reactive
import myNumbers

import subprocess
import datetime
import sys

class Number(Static):
    """Render a number"""

    numberArray = [myNumbers.zero, myNumbers.one, myNumbers.two, myNumbers.three, myNumbers.four, myNumbers.five, myNumbers.six, myNumbers.seven, myNumbers.eight, myNumbers.nine]
    decimalNumber = reactive(-1)
    maxValue = 0
    value = 0

    def __init__(self, *args, **kwargs):
        self.maxValue=kwargs.pop('maxValue')
        super(Number, self).__init__(*args, **kwargs)

    def on_mount(self) -> None:
        self.display_number()

    def increase(self) -> None:
        if self.value < self.maxValue:
            self.value += 1
            self.display_number()
    
    def decrease(self) -> None:
        if self.value > 0:
            self.value -= 1
            self.display_number()

    def watch_decimalNumber(self, dec) -> None:
        if dec < 0:
            return  #abort if dec wasn't changed -> this is not a number that is affected

        if dec > 1:
            self.maxValue = 3
        else:
            self.maxValue = 9

        if self.value > self.maxValue:
            self.value = self.maxValue
            self.display_number()

    def display_number(self) -> None:
        if self.value <= len(self.numberArray):
            self.update(f"{self.numberArray[self.value]}")

class TUIAlarmApp(App):
    CSS_PATH = "style.css"

    def compose(self) -> ComposeResult:
        yield Horizontal(
            Vertical(
                Horizontal(
                    Vertical(
                        Number(maxValue=2, id="hourFirst_Number"),
                        Button(myNumbers.arrow_up, id="hourFirst_increase"),
                        Button(myNumbers.arrow_down, id="hourFirst_decrease")
                    ),
                    Vertical(
                        Number(maxValue=9, id="hourSecond_Number"),
                        Button(myNumbers.arrow_up, id="hourSecond_increase"),
                        Button(myNumbers.arrow_down, id="hourSecond_decrease")
                    ),
                    Static(f"{myNumbers.doubleDot}", id="doubleDot"),
                    Vertical(
                        Number(maxValue=5, id="minuteFirst_Number"),
                        Button(myNumbers.arrow_up, id="minuteFirst_increase"),
                        Button(myNumbers.arrow_down, id="minuteFirst_decrease")
                    ),
                    Vertical(
                        Number(maxValue=9, id="minuteSecond_Number"),
                        Button(myNumbers.arrow_up, id="minuteSecond_increase"),
                        Button(myNumbers.arrow_down, id="minuteSecond_decrease")
                    ),
                    id="time-mod"
                ),
                id="time-seg"
            ),
            Vertical(
                Button(myNumbers.stopSymbol, id="stop"),
                Button(myNumbers.sleepSymbol, id="sleep"),
                id="btn-seg"
            ),
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "sleep":
            timeToSleep = 0
            currtime = str(datetime.datetime.now().time()).split(":")[:2]
            #currtime = ['hours', 'minutes']
            curr_minutes = int(currtime[0])*60 + int(currtime[1])

            minutes_set = (self.query_one("#hourFirst_Number").value * 10 + self.query_one("#hourSecond_Number").value)*60 + self.query_one("#minuteFirst_Number").value * 10 + self.query_one("#minuteSecond_Number").value
            if curr_minutes < minutes_set:
                timeToSleep = minutes_set - curr_minutes
            else:
                timeToSleep = minutes_set + 1440-curr_minutes
            
            subprocess.Popen(['./wakeupCommand.sh', str(timeToSleep*60)])
        elif event.button.id == "stop":
            subprocess.Popen('./stopCommand.sh')
        elif event.button.id == "hourFirst_increase":
            self.query_one("#hourFirst_Number").increase()
        elif event.button.id == "hourSecond_increase":
            self.query_one("#hourSecond_Number").increase()
        elif event.button.id == "minuteFirst_increase":
            self.query_one("#minuteFirst_Number").increase()
        elif event.button.id == "minuteSecond_increase":
            self.query_one("#minuteSecond_Number").increase()
        elif event.button.id == "hourFirst_decrease":
            self.query_one("#hourFirst_Number").decrease()
        elif event.button.id == "hourSecond_decrease":
            self.query_one("#hourSecond_Number").decrease()
        elif event.button.id == "minuteFirst_decrease":
            self.query_one("#minuteFirst_Number").decrease()
        elif event.button.id == "minuteSecond_decrease":
            self.query_one("#minuteSecond_Number").decrease()

        self.query_one("#hourSecond_Number").decimalNumber = self.query_one("#hourFirst_Number").value


if __name__ == "__main__":
    app = TUIAlarmApp()
    sys.stdout.write("\x1b]2;TUIAlarm\x07")
    print(app.run())