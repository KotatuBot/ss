from prompt_toolkit.application import Application
from prompt_toolkit.layout.margins import ScrollbarMargin
from prompt_toolkit.filters import IsDone
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import Window
from prompt_toolkit.layout.containers import ConditionalContainer
from prompt_toolkit.layout.containers import ScrollOffsets
from prompt_toolkit.layout.containers import HSplit
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.dimension import LayoutDimension as D
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.mouse_events import MouseEventType
from prompt_toolkit.styles import Style
from prompt_toolkit.styles import pygments_token_to_classname
from prompt_toolkit.styles.pygments import style_from_pygments_dict
from pygments.token import Token
# add 
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl
from prompt_toolkit.key_binding.bindings.scroll import scroll_half_page_down, scroll_half_page_up
import subprocess



class InquirerControl(FormattedTextControl):
    selected_option_index = 0
    answered = False

    def __init__(self, choices, **kwargs):
        self.choices = choices
        super(InquirerControl, self).__init__(self._get_choice_tokens, **kwargs)


    @property
    def choice_count(self):
        return len(self.choices)

    def _get_choice_tokens(self):
        tokens = []
        T = Token

        def append(index, label):
            selected = (index == self.selected_option_index)

            def select_item(app, mouse_event):
                self.selected_option_index = index
                self.answered = True

            token = T.Selected if selected else T
            tokens.append((T.Selected if selected else T, ' > ' if selected else '   '))
            if selected:
                tokens.append((Token.SetCursorPosition, ''))
            tokens.append((T.Selected if selected else T, '%-24s' % label, select_item))
            tokens.append((T, '\n'))

        for i, choice in enumerate(self.choices):
            append(i, choice)
        tokens.pop()
        return [('class:'+pygments_token_to_classname(x[0]), str(x[1])) for x in tokens]

    def get_selection(self):
        return self.choices[self.selected_option_index]


class Terminal():

    def __init__(self,ic):
        self.ic = ic

    def selected_item(self,text):
        command = "vim "+text
        res = subprocess.call(command.split())
        print(res)


    def get_prompt_tokens(self):
        string_query = 'SELECT your file path\n'
        inst = '=========================================='
        tokens = []
        T = Token
        tokens.append((Token.QuestionMark, '?'))
        tokens.append((Token.Question, string_query))
        if self.ic.answered:
            tokens.append((Token.Answer, ' ' + self.ic.get_selection()))
            self.selected_item(self.ic.get_selection())
        else:
            tokens.append((Token.Instruction, inst))
        return [('class:'+pygments_token_to_classname(x[0]), str(x[1])) for x in tokens]

    def apps_m(self):
        buffer1 = Buffer()
        HSContainer = HSplit([
            Window(height=D.exact(1),
                   content=FormattedTextControl(self.get_prompt_tokens)),
            Window(content=BufferControl(buffer=buffer1)),
            ConditionalContainer(
                Window(
                self.ic,
                width=D.exact(43),
                height=D(min=3),
                scroll_offsets=ScrollOffsets(top=1, bottom=1)
                ),
                filter=~IsDone())])
        layout = Layout(HSContainer)


        kb = KeyBindings()

        @kb.add('q', eager=True)
        def _(event):
            event.app.exit(None)
        @kb.add('j', eager=True)
        def move_cursor_down(event):
            self.ic.selected_option_index = (
                (self.ic.selected_option_index + 1) % self.ic.choice_count)
        @kb.add('k', eager=True)
        def move_cursor_up(event):
            self.ic.selected_option_index = (
                (self.ic.selected_option_index - 1) % self.ic.choice_count)
        @kb.add('space', eager=True)
        def set_answer(event):
            self.ic.answered = True
            event.app.exit(None)


        inquirer_style = style_from_pygments_dict({
            Token.QuestionMark: '#5F819D',
            Token.Selected: '#FF9D00',
            Token.Instruction: '',
            Token.Answer: '#FF9D00 bold',
            Token.Question: 'bold'
        })


        app = Application(
            layout=layout,
            key_bindings=kb,
            mouse_support=False,
            style=inquirer_style
        )
        app.run()

