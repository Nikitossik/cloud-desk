from __future__ import annotations

from pathlib import Path
import platform

try:
    import win32api
    import win32con
    import win32gui
    import win32ui
except Exception:
    win32api = None
    win32con = None
    win32gui = None
    win32ui = None

try:
    from PIL import Image
except Exception:
    Image = None

from app.config import BASE_DIR

APP_ICONS_DIR = BASE_DIR / "static" / "app-icons"
APP_ICONS_SUBDIR = "app-icons"


def get_app_icon_key(app_id: str) -> str:
    return f"{APP_ICONS_SUBDIR}/{app_id}.png"


def get_app_icon_abs_path(icon_key: str) -> Path:
    return BASE_DIR / "static" / icon_key


def save_application_icon(app_id: str, exe_path: str | None) -> str | None:
    if platform.system() != "Windows":
        return None

    if not all([win32api, win32con, win32gui, win32ui, Image]):
        return None

    if not exe_path:
        return None

    exe_file = Path(exe_path)
    if not exe_file.exists():
        return None

    APP_ICONS_DIR.mkdir(parents=True, exist_ok=True)
    icon_key = get_app_icon_key(app_id)
    output_path = get_app_icon_abs_path(icon_key)

    if output_path.exists():
        return icon_key

    extracted = _extract_icon_to_png(exe_file, output_path)
    if not extracted:
        return None

    return icon_key


def _extract_icon_to_png(exe_path: Path, output_path: Path) -> bool:
    large_icons: list[int] = []
    small_icons: list[int] = []
    hdc_screen = None
    hdc_mem = None
    h_bitmap = None

    try:
        large_icons, small_icons = win32gui.ExtractIconEx(str(exe_path), 0)
        if not large_icons and not small_icons:
            return False

        h_icon = large_icons[0] if large_icons else small_icons[0]

        icon_width = win32api.GetSystemMetrics(win32con.SM_CXICON)
        icon_height = win32api.GetSystemMetrics(win32con.SM_CYICON)

        hdc_screen = win32ui.CreateDCFromHandle(win32gui.GetDC(0))
        hdc_mem = hdc_screen.CreateCompatibleDC()

        h_bitmap = win32ui.CreateBitmap()
        h_bitmap.CreateCompatibleBitmap(hdc_screen, icon_width, icon_height)
        hdc_mem.SelectObject(h_bitmap)

        hdc_mem.FillSolidRect((0, 0, icon_width, icon_height), 0)
        win32gui.DrawIconEx(
            hdc_mem.GetSafeHdc(),
            0,
            0,
            h_icon,
            icon_width,
            icon_height,
            0,
            None,
            win32con.DI_NORMAL,
        )

        bmp_info = h_bitmap.GetInfo()
        bmp_bits = h_bitmap.GetBitmapBits(True)

        image = Image.frombuffer(
            "RGBA",
            (bmp_info["bmWidth"], bmp_info["bmHeight"]),
            bmp_bits,
            "raw",
            "BGRA",
            0,
            1,
        )
        image.save(output_path, "PNG")
        return True
    except Exception:
        return False
    finally:
        for icon_handle in large_icons + small_icons:
            try:
                win32gui.DestroyIcon(icon_handle)
            except Exception:
                pass

        if h_bitmap is not None:
            try:
                win32gui.DeleteObject(h_bitmap.GetHandle())
            except Exception:
                pass

        if hdc_mem is not None:
            try:
                hdc_mem.DeleteDC()
            except Exception:
                pass

        if hdc_screen is not None:
            try:
                hdc_screen.DeleteDC()
            except Exception:
                pass
