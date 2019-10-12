from pathlib import Path
from prompt_toolkit.application import Application
from prompt_toolkit.application.current import get_app
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.document import Document
from prompt_toolkit.filters import has_focus, Condition, is_searching
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.key_binding.bindings import search
from prompt_toolkit.key_binding.bindings.focus import focus_next, focus_previous
from prompt_toolkit.key_binding.bindings.scroll import (
    scroll_half_page_down,
    scroll_half_page_up,
)
from prompt_toolkit.keys import Keys
from prompt_toolkit.layout.containers import VSplit, HSplit, Window
from prompt_toolkit.layout.controls import BufferControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.layout.processors import (
    ConditionalProcessor,
    DisplayMultipleCursors,
    HighlightIncrementalSearchProcessor,
    HighlightSearchProcessor,
    HighlightSelectionProcessor,
)
from prompt_toolkit.styles import Style
from prompt_toolkit.widgets import FormattedTextToolbar
from prompt_toolkit.widgets.toolbars import SearchToolbar
import subprocess


class FileReader:
    def __init__(self,file_list):
        self.file_list = file_list

    def get_path(self, idx):
        return Path(self.file_list[idx][1]).absolute()

    def get_relative_path(self,idx):
        return Path(self.file_list[idx][0])

    def read_text(self, idx):
        return Path(self.file_list[idx][1]).read_text()

    def get_list_text(self):
        return "\n".join([f[0] for f in self.file_list])


class BufferCache:

    def __init__(self):
        self._current_buffer_index = 0
        self._buffers = [Buffer(read_only=True)]

    @property
    def current_buffer(self):
        return self._buffers[self._current_buffer_index]

    @property
    def current_buffer_name(self):
        return self.current_buffer.name

    def move_current_index_previous(self):
        if self._current_buffer_index == 0:
            self._current_buffer_index = len(self._buffers) - 1
        else:
            self._current_buffer_index -= 1

    def move_current_index_next(self):
        if self._current_buffer_index == len(self._buffers) - 1:
            self._current_buffer_index = 0
        else:
            self._current_buffer_index += 1

    def get_or_append_buffer(self, buf_name, document_text):
        for i, b in enumerate(self._buffers):
            if b.name == buf_name:
                # get
                self._current_buffer_index = i
                return b

        buf = Buffer(name=buf_name, read_only=True, document=Document(document_text))
        self._buffers.append(buf)
        self._current_buffer_index += 1
        return buf


class TerminalView():
    def __init__(self):
        pass

    def main(self,data):
        fr = FileReader(data)
        bc = BufferCache()

        all_input_processors = [
            ConditionalProcessor(HighlightSearchProcessor(), ~is_searching),
            HighlightIncrementalSearchProcessor(),
            HighlightSelectionProcessor(),
            DisplayMultipleCursors(),
        ]

        search_toolbar = SearchToolbar(vi_mode=True)

        lst_window = Window(
            BufferControl(
                Buffer(
                    name="file_list",
                    document=Document(fr.get_list_text(), cursor_position=0),
                    read_only=True,
                ),
                search_buffer_control=search_toolbar.control,
                preview_search=True,
                include_default_input_processors=False,
                input_processors=all_input_processors,
            ),
            cursorline=True,
        )


        txt_window = Window(
            BufferControl(
                bc.current_buffer,
                search_buffer_control=search_toolbar.control,
                preview_search=True,
                include_default_input_processors=False,
                input_processors=all_input_processors,
            ),
            wrap_lines=False,
        )

        toolbar = FormattedTextToolbar(text="hello world!", style="class:buf_name")
        
        body = HSplit(
            [lst_window]
        )
        # Key bind
        kb = KeyBindings()
        kb.add(Keys.ControlD)(scroll_half_page_down)
        kb.add(Keys.ControlU)(scroll_half_page_up)

        @kb.add(Keys.ControlQ)
        def _(event):
            event.app.exit()

        @kb.add(Keys.Enter, filter=has_focus("file_list"))
        def _(event):
            idx = event.current_buffer.document.cursor_position_row
            path = str(fr.get_path(idx))
            origin_data = str(fr.get_relative_path(idx))
            origin_data2 = origin_data.split("->")[0]
            number = origin_data2.split(":")[-1]
            command = "vim "+"+"+number+" "+path
            res = subprocess.call(command.split())

        @kb.add("k")
        def _(event):
            event.current_buffer.cursor_up()
            idx = event.current_buffer.document.cursor_position_row
            path = str(fr.get_relative_path(idx))
            try:
               set_buffer_txt_window(bc.get_or_append_buffer(path, "AAAAA"))
               set_text_toolbar(bc.current_buffer_name)
            except:
               pass


        @kb.add("j")
        def _(event):
            event.current_buffer.cursor_down()
            idx = event.current_buffer.document.cursor_position_row
            path = str(fr.get_relative_path(idx))
            set_buffer_txt_window(bc.get_or_append_buffer(path, "AAAAA"))
            set_text_toolbar(bc.current_buffer_name)


        def set_buffer_txt_window(buf):
            txt_window.content.buffer = buf

        def set_text_toolbar(text):
            toolbar.content.text = text

        @Condition
        def search_buffer_is_empty():
            return get_app().current_buffer.text == ""

        style = Style(
            [
                ("buf_name", "fg:#dddddd bg:#8a2be2"),
                ("incsearch", "fg:ansibrightyellow reverse"),
            ]
        )

        app = Application(
            layout=Layout(body), key_bindings=kb, full_screen=True, style=style
        )

        app.run()

