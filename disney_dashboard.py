import tkinter as tk
import tkinter.font as tkfont
from waits import get_wait_time
from stream import get_youtube_url
import time
import os

try:
    import vlc
except ImportError:
    vlc = None

class DisneyDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Disney Parks Live")
        self.root.configure(bg='#000000')

        # Use Quicksand if available, otherwise fallback to a standard font
        self.custom_font = ('Quicksand', 16, 'bold') if 'Quicksand' in tkfont.families() else ('Helvetica', 16, 'bold')
        self.ride_font = self.custom_font
        self.time_font = self.custom_font

        self.main_frame = tk.Frame(root, bg='#000000')
        self.main_frame.pack(expand=True, fill='both')

        self.video_frame = tk.Frame(self.main_frame, bg='#000000')
        self.video_frame.pack(expand=True, fill='both')

        self.overlay_frame = tk.Frame(
            self.main_frame,
            bg='#1A1A1A',
            highlightbackground='#2A2A2A',
            highlightthickness=2,
            bd=8,
            relief='ridge'
        )
        self.overlay_frame.place(relx=0.75, rely=0.15, relwidth=0.23, relheight=0.7)

        content_frame = tk.Frame(self.overlay_frame, bg='#1A1A1A')
        content_frame.pack(fill='both', expand=True, padx=25, pady=50)

        header = tk.Label(
            content_frame,
            text="Disneyland",
            font=('Quicksand', 20, 'bold'),
            bg='#1A1A1A',
            fg='#FFFFFF'
        )
        header.pack(pady=(0, 20))

        tk.Label(
            content_frame,
            text="CURRENT WAIT TIMES",
            font=('Quicksand', 14, 'bold'),
            bg='#1A1A1A',
            fg='#AAAAAA'
        ).pack(pady=(0, 30))

        self.rides_container = tk.Frame(content_frame, bg='#1A1A1A')
        self.rides_container.pack(fill='x')

        self.wait_labels = {}
        self.rides = {
            '🏰  Haunted Mansion': '/en-US/parks/16/rides/13958',
            '🚀  Space Mountain': '/en-US/parks/16/rides/284',
            '⛵  Pirates': '/en-US/parks/16/rides/285',
            '🗻  Matterhorn Bobsleds': '/en-US/parks/16/rides/279',
            '✈️  Peter Pan': '/en-US/parks/16/rides/281',
            '🎩  Indiana Jones': '/en-US/parks/16/rides/326',
            '⭐  Rise of Resistance': '/en-US/parks/16/rides/6340'
        }

        for ride_name, href in self.rides.items():
            card = tk.Frame(self.rides_container, bg='#1A1A1A', padx=20, pady=10)
            card.pack(fill='x', pady=5)

            emoji, name = ride_name.split('  ')

            tk.Label(card, text=emoji, font=self.ride_font, bg='#1A1A1A', fg='#DDDDDD', width=2, anchor='w').pack(side='left')
            tk.Label(card, text=name, font=self.ride_font, bg='#1A1A1A', fg='#DDDDDD', padx=5).pack(side='left')

            label = tk.Label(card, text="--", font=self.time_font, bg='#1A1A1A', fg='#AAAAAA')
            label.pack(side='right', padx=10)
            self.wait_labels[href] = label

        self.status_label = tk.Label(content_frame,
                                     text="🟢 Live Updates",
                                     font=('QuicksandRegular', 12),
                                     bg='#1A1A1A',
                                     fg='#888888')
        self.status_label.pack(side='bottom', pady=30)

        self.start_stream()
        self.update_wait_times()

    def get_time_color(self, wait_time):
        try:
            minutes = int(wait_time.split()[0])
            if minutes <= 25:
                return "#8dd577"
            elif minutes <= 70:
                return "#e8ea65"
            else:
                return "#c75252"
        except:
            return "#888888"

    def update_wait_times(self):
        current_time = time.strftime("%I:%M %p")
        self.status_label.config(text=f"🟢 Last Update: {current_time}")

        for href, label in self.wait_labels.items():
            wait_time = get_wait_time(href)
            label.config(text=wait_time, fg=self.get_time_color(wait_time))

        self.root.after(60000, self.update_wait_times)

    def start_stream(self):
        if vlc is None:
            print("VLC module not found. Please install python-vlc.")
            return

        url = get_youtube_url()
        if url:
            try:
                instance = vlc.Instance()
                self.player = instance.media_player_new()
                media = instance.media_new(url)
                self.player.set_media(media)

                if hasattr(self.video_frame, 'winfo_id'):
                    self.player.set_hwnd(self.video_frame.winfo_id())

                self.player.play()
            except Exception as e:
                print(f"Failed to start VLC stream: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    root.attributes('-fullscreen', True)
    app = DisneyDashboard(root)
    root.mainloop()
