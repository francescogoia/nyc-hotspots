import flet as ft


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        # page stuff
        self._page = page
        self._page.title = "Template application using MVC and DAO"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.LIGHT
        # controller (it is not initialized. Must be initialized in the main, after the controller is created)
        self._controller = None
        # graphical elements
        self._title = None
        self.txt_name = None
        self.btn_hello = None
        self.txt_result = None
        self.txt_container = None

    def load_interface(self):
        # title
        self._title = ft.Text("NYC HOTSPOSTS", color="blue", size=24)
        self._page.controls.append(self._title)

        #ROW with some controls
        # text field for the name
        self.txt_name = ft.TextField(
            label="name",
            width=200,
            hint_text="Insert a your name"
        )

        # button for the "hello" reply
        """self.btn_hello = ft.ElevatedButton(text="Hello", on_click=self._controller.handle_hello)
        row1 = ft.Row([self.txt_name, self.btn_hello],
                      alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row1)"""

        # row1
        self._ddProvider = ft.Dropdown(label="Provider")
        self._controller.fillDDProvider()
        self._btCreaGrafo = ft.ElevatedButton(text="Crea Grafo", on_click=self._controller.handleCreaGrafo)
        row1 = ft.Row([ft.Container(self._ddProvider, width=300), ft.Container(self._btCreaGrafo, width=300)],
                      ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row1)
        # row2
        self._txtInDistanza = ft.TextField(label="Distanza")
        self._btnAnalisiGrafo = ft.ElevatedButton(text="Analizza Grafo", on_click=self._controller.handleAnalizzaGrafo)
        row2 = ft.Row([ft.Container(self._txtInDistanza, width=300), ft.Container(self._btnAnalisiGrafo, width=300)],
                      ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row2)
        # row3
        self._txtInString = ft.TextField(label="Stringa")
        self._btnCalcolaPercorso = ft.ElevatedButton(text="Calcola Percorso", on_click=self._controller.handleCalcolaPercorso)
        row3 = ft.Row([ft.Container(self._txtInString, width=300), ft.Container(self._btnCalcolaPercorso, width=300)],
                      ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row3)
        # row4
        self._ddTarget = ft.Dropdown(label="Target")
        row4 = ft.Row([ft.Container(self._ddTarget, width=300), ft.Container(None, width=300)],
                      ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row4)


        # List View where the reply is printed
        self.txt_result = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
        self._page.controls.append(self.txt_result)
        self._page.update()

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller

    def create_alert(self, message):
        dlg = ft.AlertDialog(title=ft.Text(message))
        self._page.dialog = dlg
        dlg.open = True
        self._page.update()

    def update_page(self):
        self._page.update()
