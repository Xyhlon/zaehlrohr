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
        "zAlu0_4": r"z_{\mathrm{Alu \num{0.4}}}",
        "zAlu0_8": r"z_{\mathrm{Alu \num{0.8}}}",
        "zAlu4": r"z_{\mathrm{Alu \num{4}}}",
        "z1": r"z_{1}",
        "z2": r"z_{2}",
        "z3": r"z_{3}",
        "z4": r"z_{4}",
        "z": r"z",
        "t": r"t",
        "U": r"U",
        "B": r"B",
        "D": r"D",
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
        "zAlu0_4": r"\si{\cps}",
        "zAlu0_8": r"\si{\cps}",
        "zAlu4": r"\si{\cps}",
        "z1": r"\si{\cps}",
        "z2": r"\si{\cps}",
        "z3": r"\si{\cps}",
        "z4": r"\si{\cps}",
        "z": r"\si{1}",
        "t": r"\si{\second}",
        "U": r"\si{\volt}",
        "B": r"\si{\milli\tesla}",
        "D": r"\si{\micro\meter}",
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
    P.data["dzLuft"] = 0
    P.data["dzPapier"] = 0
    P.data["dzKunststoff"] = 0
    P.data["dzAlu0_4"] = 0
    P.data["dzAlu0_8"] = 0
    P.data["dzAlu1_5"] = 0
    P.data["dzAlu4"] = 0
    P.print_table(
        zLuft,
        zPapier,
        zKunststoff,
        zAlu0_4,
        zAlu0_8,
        zAlu4,
        name="absorption_qal_raw",
        inline_units=True,
    )
    # A2 Daten besorgen Untersuchung der Zählrohrcharakteristik Na22
    filepath = os.path.join(os.path.dirname(__file__), "../data/charakter.csv")
    P.load_data(filepath, loadnew=True)
    P.data["dU"] = 0
    P.data["dz1"] = 0
    P.data["dz2"] = 0
    P.data["dz3"] = 0
    P.print_table(U, z1, z2, z3, name="charakter_raw", inline_units=True)
    P.data["z"] = P.data[["z1", "z2", "z3"]].mean(axis=1)
    P.data["dz"] = P.data[["z1", "z2", "z3"]].sem(axis=1)
    P.print_table(z, name="charakter_z_bar", split=True, inline_units=True)

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

    P.data["dt"] = 0
    P.data["dn"] = 0

    P.print_table(t, n, name="statistik_raw", inline_units=True)
    bins = (int)(n.data.max() - n.data.min()) // 10
    P.histoofseries(n.data, bins=bins, name="statistik")
    bins = (int)(n.data.max() - n.data.min()) // 5
    P.histoofseries(n.data, bins=bins, name="atistik")
    # A4 Aufnahme des Abstandsgesetz
    filepath = os.path.join(os.path.dirname(__file__), "../data/abstandsgesetzt.csv")
    P.load_data(filepath, loadnew=True)
    # delta l = 0.5cm mit Sr90
    P.data["dl"] = 0.2
    P.data["dz1"] = 0
    P.data["dz2"] = 0
    P.data["dz3"] = 0
    P.print_table(l, z1, z2, z3, name="abstand_raw", inline_units=True)
    P.data["z"] = P.data[["z1", "z2", "z3"]].mean(axis=1)
    P.data["dz"] = P.data[["z1", "z2", "z3"]].sem(axis=1)
    P.print_table(z, name="abstand_z_bar", inline_units=True)
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
    P.print_table(B, n, name="magneto_raw", inline_units=True)
    m_0 = 0.511  # MeV
    p = 299.792456 * B / 1000 * r  # radius
    E = m_0 * (((p / m_0) ** 2 + 1) ** 0.5 - 1)
    n_background = 23  # Hintergrundstrahlung
    P.data["n"] = n.data - n_background
    P.resolve(E)
    P.resolve(p)
    print(p.data)
    print(E.data)
    P.print_table(E, p, name="magneto_E_p", inline_units=True)
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

    # A5 Ra226 Aluminiumabsorbtion
    filepath = os.path.join(os.path.dirname(__file__), "../data/aluminium.csv")
    P.vload()
    P.load_data(filepath)
    P.data["dD"] = 0
    P.data["dz1"] = 0
    P.data["dz2"] = 0
    P.data["dz3"] = 0
    P.print_table(D, z1, z2, z3, name="alu_absorbtion", inline_units=True)

    # A5 Ra226 C137 und Ra226 Bilder sind schon vorhanden und im figures folder DONE
    # filepath = os.path.join(os.path.dirname(__file__), "../data/aluminium.csv")
    # P.load_data(filepath)
    # Szintillator


if __name__ == "__main__":
    test_zaehlrohr_protokoll()
