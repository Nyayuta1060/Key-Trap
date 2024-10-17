from pynput.keyboard import Listener, KeyCode
from pynput.mouse import Listener as MouseListener
import threading
import cv2
import ctypes
import pyautogui as pag

cap = cv2.VideoCapture(0)

pag.hotkey("win", "d")

class KeyMonitor:
    def __init__(self):
        self._stop_event = threading.Event()
        self.key_listener = None
        self.mouse_listener = None

    def start(self):
        print("キーモニタースタート")
        self.key_listener = Listener(on_press=self.on_press)
        self.mouse_listener = MouseListener(on_click=self.on_click)
        self.key_listener.start()
        self.mouse_listener.start()
        self._stop_event.clear()
        

    def stop(self):
        print("キーモニターストップ")
        if self.key_listener:
            self.key_listener.stop()
        if self.mouse_listener:
            self.mouse_listener.stop()
        self._stop_event.set()

    def on_press(self, key):
        try:
            if key == KeyCode(char='x'):
                # print("終了")
                self.stop()
                return True  
            elif key != KeyCode(char='x'):  
                # print(f"{key}が押されました")
                ret, frame = cap.read()
                cv2.imwrite("image.jpg", frame)
                cap.release()
                ctypes.windll.user32.LockWorkStation()
            
        except AttributeError:
            pass
        return False  
    
    def on_click(self, x, y, button, pressed):
        # print(f"{button}がクリックされました")
        ret, frame = cap.read()
        cv2.imwrite("image.jpg", frame)
        cap.release()
        ctypes.windll.user32.LockWorkStation()

    def join(self, timeout=None):
        self.key_listener.join(timeout)
        self.mouse_listener.join(timeout)

def main():
    monitor = KeyMonitor()
    monitor.start()
    
    try:
        while not monitor._stop_event.wait(timeout=1):
            continue
    finally:
        monitor.stop()

if __name__ == "__main__":
    main()
