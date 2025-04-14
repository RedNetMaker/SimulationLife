import dearpygui.dearpygui as dpg
from model import Model
import process

run:bool = False

dpg.create_context()

initStr = " it is the best genom for this environment try to fit it "
countModels = 10
models:list[Model] = []

models = process.run(list(initStr), countModels, models, run)

def launch(sender, app_data, user_data):
    global run
    if run:
        dpg.set_item_label("launch_button", "Start")
    else:
        dpg.set_item_label("launch_button", "Stop")
    run = not run

def update():
    global models 
    models = process.run(list(initStr), countModels, models, run)
    # Очищаем старую таблицу (если она динамическая)
    for child in dpg.get_item_children("models_table", slot=1):  # slot=1 — это строки
        dpg.delete_item(child)
    
    # Заполняем таблицу новыми данными
    for i in range(len(models)):
        with dpg.table_row(parent="models_table"):
            for j in range(len(models[i].gens) + 3):
                if j > 2:
                    if models[i].gens[j - 3].correct is True:
                        dpg.add_selectable(label=models[i].gens[j - 3].letter, default_value=True, enabled=False)  # Зелёный фон
                    else:
                        dpg.add_selectable(label=models[i].gens[j - 3].letter, default_value=False, enabled=False)
                elif j == 0:
                    dpg.add_selectable(label=i + 1, default_value=False, enabled=False)
                elif j == 1:
                    dpg.add_selectable(label=models[i].count, default_value=False, enabled=False)
                elif j == 2:
                    if models[i].replicate:
                        dpg.add_selectable(label="#", default_value=False, enabled=False)
                    else:
                        dpg.add_selectable(label="", default_value=False, enabled=False)


with dpg.window(label="Example Window", width=1000, height=500, no_close=True, no_resize=True):
    with dpg.menu_bar():
        dpg.add_menu_item(label="Start", tag="launch_button", callback=launch)
        dpg.add_menu_item(label="Exit", callback=dpg.stop_dearpygui)
        dpg.add_checkbox(label="Hi")

    with dpg.table(header_row=True, tag="models_table", resizable=True):

        for i in range(len(list(initStr)) + 3):
            if i > 2:
                dpg.add_table_column(label=list(initStr)[i - 3], width=30, width_fixed=True)
            else:
                dpg.add_table_column(label=run)

        for i in range(len(models)):
            with dpg.table_row():
                for j in range(len(models[i].gens) + 3):
                    if j > 2:
                        if models[i].gens[j - 3].correct is True:
                            dpg.add_selectable(label=models[i].gens[j - 3].letter, default_value=True, enabled=False)  # Зелёный фон
                        else:
                            dpg.add_selectable(label=models[i].gens[j - 3].letter, default_value=False, enabled=False)
                    elif j == 0:
                        dpg.add_selectable(label=i + 1, default_value=False, enabled=False)
                    elif j == 1:
                        dpg.add_selectable(label=models[i].count, default_value=False, enabled=False)
                    elif j == 2:
                        if models[i].replicate:
                            dpg.add_selectable(label="#", default_value=False, enabled=False)
                        else:
                            dpg.add_selectable(label="", default_value=False, enabled=False)

with dpg.theme() as global_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_Header, (0, 255, 0), category=dpg.mvThemeCat_Core)

dpg.bind_theme(global_theme)


dpg.create_viewport(title='Custom Title')
dpg.setup_dearpygui()
dpg.show_viewport()

while dpg.is_dearpygui_running():
    if run:
        update()
    dpg.render_dearpygui_frame()

dpg.destroy_context()