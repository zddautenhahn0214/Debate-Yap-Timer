import win32gui
import win32ui
import win32con
import ctypes
from ctypes import wintypes

def capture_window(hwnd):
    # Get the window's device context
    window_dc = win32gui.GetWindowDC(hwnd)
    mfc_dc = win32ui.CreateDCFromHandle(window_dc)
    save_dc = mfc_dc.CreateCompatibleDC()
    
    # Get the window's dimensions
    left, top, right, bot = win32gui.GetClientRect(hwnd)
    width = right - left
    height = bot - top
    
    # Create a bitmap object
    bitmap = win32ui.CreateBitmap()
    bitmap.CreateCompatibleBitmap(mfc_dc, width, height)
    save_dc.SelectObject(bitmap)
    
    # Copy the window's device context to the bitmap object
    save_dc.BitBlt((0, 0), (width, height), mfc_dc, (0, 0), win32con.SRCCOPY)
    
    # Get the bitmap data
    bmpinfo = bitmap.GetInfo()
    bmpstr = bitmap.GetBitmapBits(True)
    
    # Convert the raw data to a PIL image
    import PIL.Image
    img = PIL.Image.frombuffer(
        'RGB',
        (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
        bmpstr, 'raw', 'BGRX', 0, 1
    )
    
    # Clean up
    win32gui.DeleteObject(bitmap.GetHandle())
    save_dc.DeleteDC()
    mfc_dc.DeleteDC()
    win32gui.ReleaseDC(hwnd, window_dc)
    
    return img

def list_windows():
    def _enum_windows_proc(hwnd, results):
        if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd):
            results.append(hwnd)
    results = []
    win32gui.EnumWindows(_enum_windows_proc, results)
    return results

def main():
    windows = list_windows()
    for hwnd in windows:
        window_title = win32gui.GetWindowText(hwnd)
        img = capture_window(hwnd)
        img.show(title=window_title)  # Display or save the image

if __name__ == "__main__":
    main()
