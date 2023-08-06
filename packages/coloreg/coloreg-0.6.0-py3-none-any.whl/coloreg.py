'''
Style, sheet, theme - simple coloring for python standard `logging` module

*Currently works only for '{'-style formatting*
'''


import logging
import sys
import string
import enum
from typing import Iterator, Optional, Union

import colorama


colorama.init(wrap=False)
ANSI_STREAM_HANDLER = colorama.AnsiToWin32(sys.stderr).stream


CRITICAL = logging.CRITICAL
ERROR    = logging.ERROR
WARNING  = logging.WARNING
INFO     = logging.INFO
DEBUG    = logging.DEBUG


class FG(enum.Enum):
    BLACK   = 30
    RED     = 31
    GREEN   = 32
    YELLOW  = 33
    BLUE    = 34
    MAGENTA = 35
    CYAN    = 36
    WHITE   = 37
    BRIGHT_BLACK   = 90
    BRIGHT_RED     = 91
    BRIGHT_GREEN   = 92
    BRIGHT_YELLOW  = 93
    BRIGHT_BLUE    = 94
    BRIGHT_MAGENTA = 95
    BRIGHT_CYAN    = 96
    BRIGHT_WHITE   = 97

class BG(enum.Enum):
    BLACK   = 40
    RED     = 41
    GREEN   = 42
    YELLOW  = 43
    BLUE    = 44
    MAGENTA = 45
    CYAN    = 46
    WHITE   = 47
    BRIGHT_BLACK   = 100
    BRIGHT_RED     = 101
    BRIGHT_GREEN   = 102
    BRIGHT_YELLOW  = 103
    BRIGHT_BLUE    = 104
    BRIGHT_MAGENTA = 105
    BRIGHT_CYAN    = 106
    BRIGHT_WHITE   = 107



class Style():

    def __init__(self, fg: FG = FG.BRIGHT_BLACK, bg: BG = BG.BLACK, bold: bool = False, pattern: str = '{}'):
        self._pattern = f"\033[{';'.join(map(str, [fg.value, bg.value, 1 if bold else 22]))}m{pattern}"

    @property
    def pattern(self) -> str:
        return self._pattern

    def copy(self) -> 'Style':
        stl = Style()
        stl._pattern = self._pattern
        return stl


class Sheet():

    default_format = '{asctime} {levelname:3.3}: {message}'
    
    def __init__(self, fmt: str = None, indent: int = 13, default_style: Style = None):
        self._attrs = {}
        self.indent = indent
        self.default_style = default_style
        self.setFormat(fmt)

    def getAttr(self, attrname: str) -> Style:
        style = self._attrs.get(attrname)
        if not style:
            style = self._default_style.copy()
            self.setAttr(attrname, style)
        return style

    def setAttr(self, attrname: str, style: Style):
        if isinstance(attrname, list):
            for item in attrname:
                self._attrs[item] = style.copy()
        else:
            self._attrs[attrname] = style.copy()
        self._format = None

    @property
    def default_style(self) -> Style:
        return self._default_style

    @default_style.setter
    def default_style(self, style: Style) -> None:
        self._default_style = style.copy() if style else Style()
        self._format = None

    def getFormat(self, ansi=True) -> str:
        if not ansi:
            return self._raw
        if not self._format:
            self._format = self._formatRaw()
        return self._format

    def setFormat(self, fmt: str):
        self._raw = fmt or Sheet.default_format
        self._format = None

    def _formatRaw(self) -> str:
        formatter = string.Formatter()
        arr = formatter.parse(self._raw)
        result = []
        for txt, field, spec, conv in arr:
            if txt:
                result.append(self._default_style.pattern.format(txt))
            if field:
                fmt_field = f"{{{field}{'!'+conv if conv else ''}{':'+spec if spec else ''}}}"
                result.append( self.getAttr(field).pattern.format(fmt_field))
        return ''.join(result)+'\033[0m'

    def copy(self) -> 'Sheet':
        sheet = Sheet()
        sheet.indent = self.indent
        sheet._raw = self._raw
        sheet._format = None
        sheet._default_style = self._default_style.copy()
        sheet._attrs = {k: v.copy() for k,v in self._attrs.items()}
        return sheet


class Theme():

    def __init__(self, default_sheet: Sheet = None, datefmt: str = '%H:%M:%S', msecs: int = 3):
        self._levels = {}
        self.datefmt = datefmt
        self.msecs = msecs
        self.default_sheet = default_sheet

    def setSheet(self, level: int, sheet: Sheet):
        self._levels[level] = sheet

    def getSheet(self, level: int) -> Sheet:
        sheet = self._levels.get(level)
        if not sheet:
            sheet = self._default_sheet.copy()
            self.setSheet(level, sheet)
        return sheet

    @property
    def default_sheet(self) -> Sheet:
        return self._default_sheet

    @default_sheet.setter
    def default_sheet(self, sheet: Sheet) -> None:
        self._default_sheet = sheet.copy() if sheet else Sheet()

    def setFormat(self, fmt: str, level: Optional[int] = None) -> None:
        for sheet in self._getSheets(level):
            sheet.setFormat(fmt)

    def setIndent(self, indent: int, level: Optional[int] = None) -> None:
        for sheet in self._getSheets(level):
            sheet.indent = indent

    def setAttr(self, attrname: str, style: Style, level: Optional[int] = None) -> None:
        for sheet in self._getSheets(level):
            sheet.setAttr(attrname, style)

    def setDefaultStyle(self, style: Style, level: Optional[int] = None) -> None:
        for sheet in self._getSheets(level):
            sheet.setDefault(style)

    def _getSheets(self, level: Optional[int] = None) -> Iterator[Sheet]:
        if level is None:
            for sheet in self._levels.values():
                yield sheet
            yield self._default_sheet
        else:
            yield self.getSheet(level)



class Formatter(logging.Formatter):

    def __init__(
            self,
            theme: Theme,
            ansi: bool = True):
        
        self.theme = theme
        self.ansi = ansi
        self.default_time_format = theme.datefmt
        self.default_msec_format = f'%s.%0{theme.msecs}d' if theme.msecs>0 else '%s'
        super().__init__(fmt=None, datefmt=None, style='{')

    def format(self, record: logging.LogRecord, *args, **kwargs):
        sheet = self.theme.getSheet(record.levelno)
        self._style._fmt = sheet.getFormat(self.ansi)
        result = super().format(record, *args, **kwargs)
        if sheet.indent:
            return ('\n' + ' '*sheet.indent).join(result.splitlines())
        return result



#----------------------------------------------------------------------------------------------#
#
#   helpers
#

def getThemeDefault() -> Theme:
    return Theme()
    

def getThemeSingle() -> Theme:
    theme = Theme()
    
    FORMAT_ERR = '{asctime} {levelname:3.3}: {message}\n'
    indent = 18

    sheet_cri = Sheet(FORMAT_ERR, indent=indent, default_style=Style(fg=FG.RED))
    sheet_cri.setAttr('levelname', Style(fg=FG.WHITE, bg=BG.RED, bold=True))
    sheet_cri.setAttr('message', Style(fg=FG.RED, bold=True))
    theme.setSheet(CRITICAL, sheet_cri)

    sheet_err = Sheet(FORMAT_ERR, indent=indent)
    sheet_err.setAttr('levelname', Style(fg=FG.BRIGHT_RED, bold=True))
    sheet_err.setAttr('message', Style(fg=FG.RED, bold=True))
    theme.setSheet(ERROR, sheet_err)

    FORMAT_LOG = '{asctime} {levelname:3.3}: {message}'

    sheet_war = Sheet(FORMAT_LOG, indent=indent)
    sheet_war.setAttr('levelname', Style(fg=FG.YELLOW, bold=True))
    sheet_war.setAttr('message', Style(fg=FG.YELLOW))
    theme.setSheet(WARNING, sheet_war)

    sheet_inf = Sheet(FORMAT_LOG, indent=indent)
    sheet_inf.setAttr('message', Style(fg=FG.WHITE))
    theme.setSheet(INFO, sheet_inf)

    sheet_deb = Sheet(FORMAT_LOG, indent=indent)
    theme.setSheet(DEBUG, sheet_deb)

    return theme


def getThemeDouble() -> Theme:
    theme = Theme()

    FORMAT = '{asctime} {levelname:3.3} [{threadName}] {name} ({funcName}):\n{message}'
    theme.setFormat(FORMAT)
    theme.setIndent(17)

    sheet = theme.getSheet(DEBUG)
    sheet.setAttr("message", Style(fg=FG.WHITE))
    
    sheet = theme.getSheet(INFO)
    sheet.setAttr("message", Style(fg=FG.BRIGHT_GREEN))

    sheet = theme.getSheet(WARNING)
    sheet.setAttr("message", Style(fg=FG.BRIGHT_YELLOW))
    sheet.setAttr(["threadName", "name", "funcName", "levelname"], Style(fg=FG.YELLOW))

    sheet = theme.getSheet(ERROR)
    sheet.setAttr("message", Style(fg=FG.BRIGHT_RED))
    sheet.setAttr(["threadName", "name", "funcName", "levelname"], Style(fg=FG.RED))
    
    sheet = theme.getSheet(CRITICAL)
    sheet.setAttr("message", Style(fg=FG.BRIGHT_RED))
    sheet.setAttr(["threadName", "name", "funcName"], Style(fg=FG.RED))
    sheet.setAttr("levelname", Style(fg=FG.WHITE, bg=BG.RED, bold=True))
    
    return theme



THEMES = {
    'single': getThemeSingle(),
    'double': getThemeDouble()
}


def getTheme(name: Optional[str] = None) -> Theme:
    return THEMES.get(name, getThemeDefault())


def getStreamHandler() -> logging.Handler:
    return logging.StreamHandler(stream=ANSI_STREAM_HANDLER)


def getFormatter(theme: Theme, ansi: bool = True) -> logging.Formatter:
    return Formatter(theme=theme, ansi=ansi)


def configHandler(
        theme: Union[Theme, str, None] = None,
        ansi: bool = True) -> logging.Handler:
    
    if not isinstance(theme, Theme):
        theme = getTheme(theme)

    formatter = getFormatter(theme=theme, ansi=ansi)
    handler = getStreamHandler()
    handler.setFormatter(formatter)
    return handler


def configLogger(
        name: str = None,
        level: int = DEBUG,
        theme: Union[Theme, str, None] = None,
        ansi: bool = True) -> logging.Logger:
    
    hdlr = configHandler(
            theme=theme,
            ansi=ansi)

    lg = getLogger(name, level)
    lg.addHandler(hdlr)
    return lg


def getLogger(name: str = None, level: Optional[int] = None) -> logging.Logger:
    lg = logging.getLogger(name)
    if level is not None:
        lg.setLevel(level)
    return lg



