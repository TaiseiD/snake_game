import random
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle, Ellipse, Line, RoundedRectangle
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.anchorlayout import AnchorLayout
from kivy.properties import NumericProperty, ListProperty, StringProperty
from kivy.metrics import dp, sp

class MenuScreen(Screen):
    recent_score = NumericProperty(0)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=dp(40), spacing=dp(20))
        layout.add_widget(Label(text='SNAKE', font_size=sp(80), bold=True, color=(0, 1, 0.5, 1)))
        self.score_label = Label(text='RECENT: 0', font_size=sp(24), color=(0.7, 0.7, 0.7, 1))
        layout.add_widget(self.score_label)
        start_btn = Button(text='PLAY', size_hint_y=None, height=dp(70), background_color=(0, 0.8, 0.4, 1), font_size=sp(24), bold=True, background_normal='')
        start_btn.bind(on_release=lambda x: setattr(self.manager, 'current', 'game'))
        set_btn = Button(text='CUSTOMIZE', size_hint_y=None, height=dp(70), background_color=(0.2, 0.4, 0.8, 1), background_normal='')
        set_btn.bind(on_release=lambda x: setattr(self.manager, 'current', 'settings'))
        layout.add_widget(start_btn)
        layout.add_widget(set_btn)
        self.add_widget(layout)
    def on_recent_score(self, instance, value):
        self.score_label.text = f'RECENT: {value}'

class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.color_buttons, self.shape_buttons = [], []
        layout = BoxLayout(orientation='vertical', padding=dp(15), spacing=dp(10))
        
        preview_area = AnchorLayout(anchor_x='center', anchor_y='center', size_hint_y=None, height=dp(150))
        with preview_area.canvas.before:
            Color(0.15, 0.15, 0.15, 1)
            self.preview_bg = RoundedRectangle(pos=preview_area.pos, size=preview_area.size, radius=[20])
        preview_area.bind(pos=self._update_bg, size=self._update_bg)
        
        self.preview_widget = Widget(size_hint=(None, None), size=(dp(60), dp(60)))
        with self.preview_widget.canvas:
            self.preview_color = Color(0, 1, 0, 1)
            self.preview_instr = Rectangle(pos=self.preview_widget.pos, size=self.preview_widget.size)
        
        self.preview_widget.bind(pos=self._update_instr, size=self._update_instr)
        preview_area.add_widget(self.preview_widget)
        preview_area.add_widget(Label(font_size=sp(12), color=(0.4, 0.4, 0.4, 1), valign='top', halign='center', size_hint_y=None, height=dp(130)))
        
        layout.add_widget(preview_area)

        scroll = ScrollView(do_scroll_x=False, bar_width=dp(5))
        cont = GridLayout(cols=1, spacing=dp(20), size_hint_y=None)
        cont.bind(minimum_height=cont.setter('height'))
        
        cont.add_widget(Label(text="SELECT COLOR", font_size=sp(18), bold=True, size_hint_y=None, height=dp(30)))
        cg = GridLayout(cols=5, spacing=dp(8), size_hint_y=None, height=dp(110))
        clrs = [('GRN',(0,1,0,1)), ('BLU',(0,.5,1,1)), ('RED',(1,0,0,1)), ('YLW',(1,1,0,1)), ('PRP',(.5,0,1,1)), 
                ('ORG',(1,.5,0,1)), ('PNK',(1,0,1,1)), ('CYN',(0,1,1,1)), ('WHT',(1,1,1,1)), ('GRY',(.5,.5,.5,1))]
        for n, c in clrs:
            b = Button(text="", background_normal='', background_color=c, size_hint_y=None, height=dp(45))
            b.bind(on_release=lambda x, col=c, btn=b: self.sel_col(col, btn))
            cg.add_widget(b)
            self.color_buttons.append(b)
        cont.add_widget(cg)

        cont.add_widget(Label(text="SELECT SHAPE", font_size=sp(18), bold=True, size_hint_y=None, height=dp(30)))
        sg = GridLayout(cols=2, spacing=dp(10), size_hint_y=None, height=dp(350))
        shps = ['Square', 'Circle', 'Triangle', 'Diamond', 'Pill', 'Vertical Bar', 'Horizontal Bar', 'Dot', 'Pentagon', 'Hexagon']
        for s in shps:
            b = Button(text=s, background_normal='', background_color=(0.2, 0.2, 0.2, 1), font_size=sp(16))
            b.bind(on_release=lambda x, shp=s, btn=b: self.sel_shp(shp, btn))
            sg.add_widget(b)
            self.shape_buttons.append(b)
        cont.add_widget(sg)
        scroll.add_widget(cont)
        layout.add_widget(scroll)
        
        back = Button(text='APPLY CHANGES', size_hint_y=None, height=dp(60), background_normal='', background_color=(0, 0.6, 0.3, 1), bold=True)
        back.bind(on_release=lambda x: setattr(self.manager, 'current', 'menu'))
        layout.add_widget(back)
        self.add_widget(layout)

    def _update_bg(self, instance, value):
        self.preview_bg.pos = instance.pos
        self.preview_bg.size = instance.size

    def _update_instr(self, instance, value):
        self.preview_instr.pos = instance.pos
        self.preview_instr.size = instance.size

    def update_preview_shape(self, shape):
        self.preview_widget.canvas.remove(self.preview_instr)
        with self.preview_widget.canvas:
            if shape == 'Square': self.preview_instr = Rectangle(pos=self.preview_widget.pos, size=self.preview_widget.size)
            elif shape == 'Circle': self.preview_instr = Ellipse(pos=self.preview_widget.pos, size=self.preview_widget.size)
            elif shape == 'Triangle': self.preview_instr = Ellipse(pos=self.preview_widget.pos, size=self.preview_widget.size, segments=3)
            elif shape == 'Diamond': self.preview_instr = Ellipse(pos=self.preview_widget.pos, size=self.preview_widget.size, segments=4)
            elif shape == 'Pentagon': self.preview_instr = Ellipse(pos=self.preview_widget.pos, size=self.preview_widget.size, segments=5)
            elif shape == 'Hexagon': self.preview_instr = Ellipse(pos=self.preview_widget.pos, size=self.preview_widget.size, segments=6)
            elif shape == 'Pill': self.preview_instr = Rectangle(pos=(self.preview_widget.x, self.preview_widget.y + dp(15)), size=(dp(60), dp(30)))
            elif shape == 'Vertical Bar': self.preview_instr = Rectangle(pos=(self.preview_widget.x + dp(15), self.preview_widget.y), size=(dp(30), dp(60)))
            elif shape == 'Horizontal Bar': self.preview_instr = Rectangle(pos=(self.preview_widget.x, self.preview_widget.y + dp(20)), size=(dp(60), dp(20)))
            else: self.preview_instr = Ellipse(pos=(self.preview_widget.x + dp(15), self.preview_widget.y + dp(15)), size=(dp(30), dp(30)))

    def sel_col(self, c, b):
        self.preview_color.rgba = c
        self.manager.get_screen('game').game_widget.snake_color = c

    def sel_shp(self, s, b):
        for btn in self.shape_buttons: btn.background_color = (0.2, 0.2, 0.2, 1)
        b.background_color = (0.4, 0.4, 0.4, 1)
        self.update_preview_shape(s)
        self.manager.get_screen('game').game_widget.snake_shape = s

class SnakeGameWidget(Widget):
    score = NumericProperty(0)
    snake_color = ListProperty([0, 1, 0, 1])
    snake_shape = StringProperty('Square')
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cell_size = dp(25)
        self.reset_game()
        Window.bind(on_key_down=self._on_key_down)
        Clock.schedule_interval(self.update, 1/12)
    def reset_game(self):
        self.snake, self.direction, self.next_direction, self.food, self.score = [(5, 5), (4, 5), (3, 5)], (1, 0), (1, 0), (10, 5), 0
    def set_dir(self, d):
        if (d[0] * -1, d[1] * -1) != self.direction: self.next_direction = d
    def _on_key_down(self, i, k, s, c, m):
        dirs = {273:(0,1), 274:(0,-1), 276:(-1,0), 275:(1,0)}
        if k in dirs: self.set_dir(dirs[k])
    def update(self, dt):
        if not self.parent or not self.parent.parent or self.parent.parent.manager.current != 'game': return
        cols, rows = int(self.width / self.cell_size), int(self.height / self.cell_size)
        if cols == 0 or rows == 0: return
        self.direction = self.next_direction
        head = self.snake[0]
        new = (head[0] + self.direction[0], head[1] + self.direction[1])
        if (new[0] < 0 or new[0] >= cols or new[1] < 0 or new[1] >= rows or new in self.snake):
            self.parent.parent.manager.get_screen('menu').recent_score = self.score
            self.reset_game()
            self.parent.parent.manager.current = 'menu'
            return
        self.snake.insert(0, new)
        if new == self.food:
            self.score += 1
            while True:
                self.food = (random.randint(0, cols-1), random.randint(0, rows-1))
                if self.food not in self.snake: break
        else: self.snake.pop()
        self.canvas.clear()
        with self.canvas:
            s = self.cell_size
            for i in range(rows):
                Color(0.4, 0.7, 0.6 + (i / rows) * 0.2, 1)
                Rectangle(pos=(self.x, self.y + i*s), size=(self.width, s))
            Color(1, 1, 1, 0.1)
            for c in range(cols + 1): Line(points=[self.x + c*s, self.y, self.x + c*s, self.y + rows*s])
            for r in range(rows + 1): Line(points=[self.x, self.y + r*s, self.x + cols*s, self.y + r*s])
            Color(1, 1, 0); Ellipse(pos=(self.food[0]*s + self.x, self.food[1]*s + self.y), size=(s, s))
            Color(*self.snake_color)
            for p in self.snake:
                px, py = p[0]*s + self.x, p[1]*s + self.y
                if self.snake_shape == 'Square': Rectangle(pos=(px, py), size=(s, s))
                elif self.snake_shape == 'Circle': Ellipse(pos=(px, py), size=(s, s))
                elif self.snake_shape == 'Triangle': Ellipse(pos=(px, py), size=(s, s), segments=3)
                elif self.snake_shape == 'Diamond': Ellipse(pos=(px, py), size=(s, s), segments=4)
                elif self.snake_shape == 'Pentagon': Ellipse(pos=(px, py), size=(s, s), segments=5)
                elif self.snake_shape == 'Hexagon': Ellipse(pos=(px, py), size=(s, s), segments=6)
                elif self.snake_shape == 'Pill': Rectangle(pos=(px, py+s/4), size=(s, s/2))
                elif self.snake_shape == 'Vertical Bar': Rectangle(pos=(px+s/4, py), size=(s/2, s))
                elif self.snake_shape == 'Horizontal Bar': Rectangle(pos=(px, py+s/3), size=(s, s/3))
                else: Ellipse(pos=(px+s/4, py+s/4), size=(s/2, s/2))

class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        main = BoxLayout(orientation='vertical')
        self.score_label = Label(text='SCORE: 0', size_hint_y=None, height=dp(50), font_size=sp(24), bold=True)
        main.add_widget(self.score_label)
        self.game_widget = SnakeGameWidget()
        self.game_widget.bind(score=self.update_score)
        main.add_widget(self.game_widget)
        ctrl_box = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(220), padding=dp(10))
        with ctrl_box.canvas.before:
            Color(0.1, 0.1, 0.1, 1)
            self.rect = Rectangle(size=ctrl_box.size, pos=ctrl_box.pos)
        ctrl_box.bind(size=self._update_rect, pos=self._update_rect)
        dpad = GridLayout(cols=3, spacing=dp(10))
        btn_style = {'background_normal': '', 'background_color': (0.2, 0.2, 0.2, 1), 'font_size': sp(30), 'bold': True}
        b_u = Button(text="▲", **btn_style); b_u.bind(on_press=lambda x: self.game_widget.set_dir((0, 1)))
        b_d = Button(text="▼", **btn_style); b_d.bind(on_press=lambda x: self.game_widget.set_dir((0, -1)))
        b_l = Button(text="◀", **btn_style); b_l.bind(on_press=lambda x: self.game_widget.set_dir((-1, 0)))
        b_r = Button(text="▶", **btn_style); b_r.bind(on_press=lambda x: self.game_widget.set_dir((1, 0)))
        dpad.add_widget(Widget()); dpad.add_widget(b_u); dpad.add_widget(Widget())
        dpad.add_widget(b_l); dpad.add_widget(b_d); dpad.add_widget(b_r)
        ctrl_box.add_widget(dpad)
        main.add_widget(ctrl_box)
        self.add_widget(main)
    def _update_rect(self, instance, value):
        self.rect.pos, self.rect.size = instance.pos, instance.size
    def update_score(self, instance, value):
        self.score_label.text = f'SCORE: {value}'

class SnakeApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(SettingsScreen(name='settings'))
        sm.add_widget(GameScreen(name='game'))
        return sm

if __name__ == '__main__':
    SnakeApp().run()
