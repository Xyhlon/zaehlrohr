from labtool_ex2 import Project
from scipy.constants import e
import numpy as np
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
        "r": r"r",
        "l": r"l_{\mathrm{Quelle}}",
        "E": r"E_{\mathrm{kin}}",
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
        "z": r"\si{1}",
        "t": r"\si{\second}",
        "U": r"\si{\volt}",
        "B": r"\si{\milli\tesla}",
        "d": r"\si{\micro\meter}",
        "n": r"1",
        "p": r"\si{\mega\electronvolt}",
        "r": r"\si{\m}",
        "l": r"\si{\cm}",
        "I": r"\si{\cm}",
        "E": r"\si{\mega\electronvolt}",
    }
    P = Project("Zaehlrohr", global_variables=gv, global_mapping=gm, font=13)
    P.output_dir = "./figures/"
    ax = P.figure.add_subplot()
    # A1 qualitative Absorption Untersuchung mit und ohne Abschirmung
    filepath = os.path.join(os.path.dirname(__file__), "../data/absorbtion.csv")
    P.load_data(filepath, loadnew=True)
    # A2 Daten besorgen Untersuchung der Zählrohrcharakteristik Na22
    filepath = os.path.join(os.path.dirname(__file__), "../data/charakter.csv")
    P.load_data(filepath, loadnew=True)
    print(P.data)
    P.data["z"] = P.data[["z1", "z2", "z3"]].mean(axis=1)
    P.data["dz"] = P.data[["z1", "z2", "z3"]].sem(axis=1)

    P.plot_data(
        ax,
        U,
        z,
        label="Gemessene Daten",
        style="r",
        errors=True,
    )
    ax.set_title(f"Zählrohrcharakteristik mit Na-22")
    P.ax_legend_all(loc=1)
    ax = P.savefig(f"charakteristik.pdf")
    # A3 Darstellung der Zählstatistik
    P.vload()
    filepath = os.path.join(os.path.dirname(__file__), "../data/stat.csv")
    P.load_data(filepath, loadnew=True)
    bins = (int)(n.data.max() - n.data.min()) // 10
    P.histoofseries(n.data, bins=bins, name="statistik")
    bins = (int)(n.data.max() - n.data.min()) // 5
    P.histoofseries(n.data, bins=bins, name="atistik")
    # A4 Aufnahme des Abstandsgesetz
    filepath = os.path.join(os.path.dirname(__file__), "../data/abstandsgesetzt.csv")
    P.load_data(filepath, loadnew=True)
    # delta l = 0.5cm mit Sr90
    P.data["dl"] = 0.2
    P.data["z"] = P.data[["z1", "z2", "z3"]].mean(axis=1)
    P.data["dz"] = P.data[["z1", "z2", "z3"]].sem(axis=1)
    P.plot_data(
        ax,
        l,
        z,
        label="Gemessene Daten",
        style="r",
        errors=True,
    )
    ax.set_title(f"Abstandsgesetz mit Sr-90")
    P.ax_legend_all(loc=1)
    ax = P.savefig(f"abstandsgesetz.pdf")

    # A6 Magnetspektrometer Na22
    P.vload()
    filepath = os.path.join(os.path.dirname(__file__), "../data/magnetspektro.csv")
    P.load_data(filepath, loadnew=True)
    # print(e)
    # print(B.data)
    # print(n.data)

    P.data["dB"] = 0.1
    P.data["dn"] = 4
    P.data["r"] = 0.05
    P.data["dr"] = 0.003
    m_0 = 0.511  # MeV
    p = 299.792456 * B / 1000 * r  # radius
    E = m_0 * (((p / m_0) ** 2 + 1) ** 0.5 - 1)
    P.resolve(E)
    P.resolve(p)
    print(p.data)
    print(E.data)
    P.plot_data(
        ax,
        E,
        n,
        label="Gemessene Daten",
        style="r",
        errors=True,
    )
    P.plot_data(
        ax,
        p,
        n,
        label="Gemessene Daten",
        style="b",
        errors=True,
    )
    ax.set_title(f"Energie Spektrum von Na-22")
    P.ax_legend_all(loc=1)
    ax = P.savefig(f"energiespektrum.pdf")

    # A6 Ra226 C137 und Ra226 Bilder sind schon vorhanden und im figures folder DONE
    # filepath = os.path.join(os.path.dirname(__file__), "../data/aluminium.csv")
    # P.load_data(filepath)
    # Szintillator


if __name__ == "__main__":
    test_zaehlrohr_protokoll()
