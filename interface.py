import PySimpleGUI as sg

sg.theme('DarkAmber')


def make_cubeConstr_list(cubeConstr_list):
    cubeConstr_list_print = []
    for it in range(0, len(cubeConstr_list)):
        string = str(cubeConstr_list[it][0]) + " ≤  x" + \
            str(it+1) + "  ≤ " + str(cubeConstr_list[it][1])
        cubeConstr_list_print.append(string)
    return cubeConstr_list_print


objFun_list = ["(x1-2)^2 + (x2-2)^2",
               "(x1-2)^2 + (x2-2)^2 + (x3-2)^2", "(x1-2)^2 + (x1-x2^2)^2", "x1^4+x2^4-x1^2-x2^2"]
objFun_layout = [
    [sg.Text("f_min = "),
     sg.Combo(objFun_list, default_value=objFun_list[0], size=(55, 1), key='combo-objFun')]]

objFun = sg.Frame(
    "Funkcja celu", layout=objFun_layout)


cubeConstr_list_print = []
cubeConstr_layout = [
    [sg.InputText(size=(5, 0), key="LowerConstr", default_text="-5"), sg.Text("≤ xi ≤",
                                                                              font=("Arial", 15)), sg.InputText(size=(5, 0), key="UpperConstr", default_text="5")],
    [sg.Submit("Dodaj", key="Dodaj-kostka"), sg.Push(),
     sg.Submit("Usuń", key="Usun-kostka")],
    [sg.Listbox([], no_scrollbar=False,  s=(20, 5), key='List-kostka')]]


cubeConstraints = sg.Frame(
    "Ograniczenia kostki", layout=cubeConstr_layout)

constraintFun_layout = [
    [sg.InputText(size=(20), key='-funConstr-', default_text='x1^2-x2'),
     sg.Push(), sg.Text("≤ 0", font=("Arial", 15))],
    [sg.Submit("Dodaj", key="Dodaj-funkcja"),
     sg.Submit("Usuń", key="Usun-funkcja")],
    [sg.Listbox([],  enable_events=True, no_scrollbar=False,  s=(20, 5), key='List-funkcje'), sg.Text("≤ 0", font=("Arial", 15))]]

constraintsFun = sg.Frame("Ograniczenia funkcyjne",
                          layout=constraintFun_layout)
# sg.HSeparator()
algorithm_layout = [
    [sg.Text("Epsilon", size=(10, 1)), sg.InputText(
        size=(10), key='-epsilon-', default_text="0.001")],
    [sg.Text("Max. iteracji", size=(10, 1)),  sg.InputText(
        size=(10), key='-max-it-', default_text="5000")],
    [sg.Submit("Uruchom")]]

algorithm = sg.Frame("Parametry algorytmu",
                     layout=algorithm_layout, size=(200, 100))

logs_layout = [
    [sg.Output(size=(50, 10), key='logi')],
    [sg.Submit("Wyczyść", key="Wyczysc-logi")]]

logs = sg.Frame(
    "Komunikaty", layout=logs_layout)

chart_sett_layout = [
    [sg.Text("Oś X: od", size=(7, 0)), sg.InputText(size=(5, 0), key="xmin"),
     sg.Text("do", size=(2, 0)), sg.InputText(size=(5, 0), key="xmax")],
    [sg.Text("Oś Y: od", size=(7, 0)), sg.InputText(size=(5, 0), key="ymin"), sg.Text("do", size=(2, 0)), sg.InputText(size=(5, 0), key="ymax")]]

chart_sett = sg.Frame(
    "Ustawienia wykresu", layout=chart_sett_layout)

matplotlib_layout = [
    [sg.Canvas(size=(200, 200), key='-PLOT_CANV-')]]

matplotlib_ = sg.Frame(
    "Wykres", matplotlib_layout)

matplotlib_sett_layout = [
    [sg.Text('Liczba kroków:'), sg.Text('', key='-kroki-')],
    [sg.Text('Wyświetlany krok:'), sg.Text('', key='-wys-krok-')],
    [sg.Slider((0, 0), orientation='h', key="slider-kroki", size=(50, 20), enable_events=True)]]

matplotlib_sett = sg.Frame(
    "Przeglądanie kroków", matplotlib_sett_layout)

Column1_1 = [[cubeConstraints], [algorithm]]
Column1_2 = [[constraintsFun], [chart_sett]]
Column1 = [[objFun], [sg.Column(Column1_1), sg.Column(Column1_2)], [logs]]
Column2 = [[matplotlib_], [matplotlib_sett]]

#Column1 = [[objFun], [cubeConstraints, constraintsFun], [algorithm, chart_sett], [logs]]
#Column2 = [[matplotlib_], [matplotlib_sett]]

layout = [[sg.Column(Column1, size=(500, 600)), sg.Column(Column2)]]

# Create the Window
window = sg.Window('Metoda Complex', layout)
