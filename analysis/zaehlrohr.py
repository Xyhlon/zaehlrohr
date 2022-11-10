from labtool_ex2 import Project
import os


def test_zaehlrohr_protokoll():
    # zLuft / cps zPapier / cps zKunststoff / cps zAlu0_8 / cps zAlu1_5 / cps
    gm = {
        "zLuft": r"z_{\mathrm{Luft}}",
        "zPapier": r"z_{\mathrm{Papier}}",
        "zKunststoff": r"z_{\mathrm{Kunststoff}}",
        "zAlu0_8": r"z_{\mathrm{Alu \num{0.8}}}",
        "zAlu1_5": r"z_{\mathrm{Alu \num{1.5}}}",
        "z1": r"z_{1}",
        "z2": r"z_{2}",
        "z3": r"z_{3}",
        "z4": r"z_{4}",
        "z": r"z",
        "t": r"t",
        "U": r"U",
        "B": r"B",
        "d": r"d",
        "n": r"n",
        "p": r"p",
        "l": r"l_{\mathrm{Quelle}}",
    }
    gv = {
        "zLuft": r"\si{\cps}",
        "zPapier": r"\si{\cps}",
        "zKunststoff": r"\si{\cps}",
        "zAlu0_8": r"\si{\cps}",
        "zAlu1_5": r"\si{\cps}",
        "z1": r"\si{\cps}",
        "z2": r"\si{\cps}",
        "z3": r"\si{\cps}",
        "z4": r"\si{\cps}",
        "z": r"\si{\cps}",
        "t": r"\si{\second}",
        "U": r"\si{\volt}",
        "B": r"\si{\milli\tesla}",
        "d": r"\si{\micro\meter}",
        "n": r"1",
        "p": r"\si{\mega\electronvolt}",
        "l": r"\si{\cm}",
        "I": r"\si{\cm}",
    }
    P = Project("Zaehlrohr", global_variables=gv, global_mapping=gm, font=13)
    # qualitative Absorption Untersuchung mit und ohne Abschirmung
    filepath = os.path.join(os.path.dirname(__file__), "../data/absorbtion.csv")
    P.load_data(filepath)
    # Untersuchung der Zählrohrcharakteristik
    filepath = os.path.join(os.path.dirname(__file__), "../data/charakter.csv")
    P.load_data(filepath)
    # Darstellung der Zählstatistik
    filepath = os.path.join(os.path.dirname(__file__), "../data/statistik.csv")
    P.load_data(filepath)
    # Aufnahme des Abstandsgesetz
    filepath = os.path.join(os.path.dirname(__file__), "../data/abstandsgesetzt.csv")
    P.load_data(filepath)
    filepath = os.path.join(os.path.dirname(__file__), "../data/magnetspektro.csv")
    P.load_data(filepath)
    filepath = os.path.join(os.path.dirname(__file__), "../data/aluminium.csv")
    P.load_data(filepath)
    # Szintillator


if __name__ == "__main__":
    test_zaehlrohr_protokoll()
