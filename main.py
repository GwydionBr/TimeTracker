import wx
import wx.adv
import datetime as dt

TRAY_TOOLTIP = "Time-Tracker"
TRAY_ICON = "clock_icon.png"

def create_menu_item(menu, label, func):
    item = wx.MenuItem(menu, -1, label)
    menu.Bind(wx.EVT_MENU, func, id=item.GetId())
    menu.Append(item)
    return item

def convert_seconds_to_time(sec):
    seconds = sec % 60
    minutes = sec // 60
    hours = minutes // 60
    minutes = minutes % 60

    return f"hours: {hours}, minutes: {minutes}, seconds:{seconds}"

class TaskBarIcon(wx.adv.TaskBarIcon):
    def __init__(self, frame):
        wx.adv.TaskBarIcon.__init__(self)
        self.myapp_frame = frame
        self.set_icon(TRAY_ICON)
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.on_left_down)

    def CreatePopupMenu(self):
        menu = wx.Menu()
        create_menu_item(menu, "Pause Timer", self.pause_timer)
        menu.AppendSeparator()
        create_menu_item(menu, "Continue Timer", self.continue_timer)
        menu.AppendSeparator()
        create_menu_item(menu, "End Timer", self.stop_timer)
        menu.AppendSeparator()
        create_menu_item(menu, "Close Timer App", self.on_exit)
        return menu

    def set_icon(self, path):
        icon = wx.Icon(wx.Bitmap(path))
        self.SetIcon(icon, TRAY_TOOLTIP)

    # Left klick on Icon asks for Project-name and starts timer
    def on_left_down(self, event):
        dlg = wx.TextEntryDialog(None, "Enter your text:", "Text Input", "")
        if dlg.ShowModal() == wx.ID_OK:
            self.timer_name = dlg.GetValue()
            print("Entered text:", self.timer_name)
        dlg.Destroy()
        self.start_timer()

    def start_timer(self):
        self.start_time = wx.DateTime.GetTimeNow()
        self.times = []
        print("Timer started")

    def pause_timer(self, event):
        self.end_time = wx.DateTime.GetTimeNow()
        self.times.append(self.end_time - self.start_time)
        print("Timer paused")

    def continue_timer(self, event):
        self.start_time = wx.DateTime.GetTimeNow()
        print("Timer continued")

    def stop_timer(self, event):
        self.end_time = wx.DateTime.GetTimeNow()
        seconds = 0
        for time in self.times:
            seconds += time
        seconds += self.end_time - self.start_time
        time = convert_seconds_to_time(seconds)
        with open("data.txt", "a") as file:
            file.write(f"{dt.datetime.now().strftime("%d.%m.%Y")} / Project: {self.timer_name} / Time: {time}\n")
        print(f"Timer stopped with that time: {time}")

    def on_exit(self, event):
        self.myapp_frame.Close()

class My_Application(wx.Frame):

    #----------------------------------------------------------------------
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "Time-Tracker")
        panel = wx.Panel(self)
        self.myapp = TaskBarIcon(self)
        self.Bind(wx.EVT_CLOSE, self.onClose)

    #----------------------------------------------------------------------
    def onClose(self, evt):
        """
        Destroy the taskbar icon and the frame
        """
        self.myapp.RemoveIcon()
        self.myapp.Destroy()
        self.Destroy()


if __name__ == "__main__":
    MyApp = wx.App()
    My_Application()
    MyApp.MainLoop()
    def __init__(self, app, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, (-1, -1), (290, 280))
        self.Centre()



