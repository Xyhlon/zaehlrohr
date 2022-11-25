from labtool_ex2 import Project
from sympy import exp, pi
import numpy as np
import os


def test_zaehlrohr_protokoll():
    # zLuft / cps zPapier / cps zKunststoff / cps zAlu0_8 / cps zAlu1_5 / cps
    gm = {
        "zLuft": r"z_{\mathrm{Luft}}",
        "zPapier": r"z_{\mathrm{Papier}}",
        "zCd": r"z_{\mathrm{CD}}",
        "zKunststoff": r"z_{\mathrm{Lineal}}",
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
        "A": r"A",
        "mu": r"\mu",
        "sig": r"\sigma",
        "k": r"k",
        "m": r"m",
        "b": r"b",
        "l": r"l_{\mathrm{Quelle}}",
        "E": r"E_{\mathrm{kin}}",
    }
    gv = {
        "zLuft": r"\si{\cps}",
        "zPapier": r"\si{\cps}",
        "zCd": r"\si{\cps}",
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
        "A": r"\si{1}",
        "mu": r"\si{\mega\electronvolt}",
        "sig": r"\si{\mega\electronvolt}",
        "k": r"\si{\cm\squared}",
        "m": r"\si{\per\volt}",
        "b": r"\si{1}",
        "l": r"\si{\cm}",
        "I": r"\si{\cm}",
        "E": r"\si{\mega\electronvolt}",
    }

    P = Project("Zaehlrohr", global_variables=gv, global_mapping=gm, font=13)
    P.output_dir = "./"
    P.figure.set_size_inches((8, 6))
    ax = P.figure.add_subplot()

    # A1 qualitative Absorption Untersuchung mit und ohne Abschirmung
    filepath = os.path.join(os.path.dirname(__file__), "../data/absorbtion.csv")
    P.load_data(filepath, loadnew=True)
    P.data["dzLuft"] = 0
    P.data["dzPapier"] = 0
    P.data["dzKunststoff"] = 0
    P.data["dzCd"] = 0
    P.data["dzAlu0_4"] = 0
    P.data["dzAlu0_8"] = 0
    P.data["dzAlu1_5"] = 0
    P.data["dzAlu4"] = 0
    P.print_table(
        zLuft,
        zPapier,
        zCd,
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
        style="#1cb2f5",
        errors=True,
    )
    P.data = P.data[P.data["z"] > 160]
    z = m * U + b
    P.print_expr(z)
    P.plot_fit(
        axes=ax,
        x=U,
        y=z,
        eqn=z,
        style=r"#1cb2f5",
        label="Linear",
        offset=[40, 10],
        use_all_known=False,
        guess={"m": 0.01, "b": 185},
        bounds=[
            {"name": "m", "min": 0, "max": 1},
            {"name": "b", "min": 100, "max": 200},
        ],
        add_fit_params=True,
        granularity=10000,
        # gof=True,
        # scale_covar=True,
    )
    ax.set_title(f"Zählrohrcharakteristik mit Na-22")
    P.ax_legend_all(loc=4)
    ax = P.savefig(f"charakteristik.pdf")

    # A3 Darstellung der Zählstatistik
    P.vload()
    filepath = os.path.join(os.path.dirname(__file__), "../data/stat.csv")
    P.load_data(filepath, loadnew=True)

    P.data["dt"] = 0
    P.data["dn"] = 0

    P.print_table(t, n, name="statistik_raw", inline_units=True)
    bins = (int)(n.data.max() - n.data.min()) // 10
    P.plot_histo(axes=ax, x=n, label="Histogramm", bins=bins, offset=(70, 20))
    ax.set_title(f"Statischtische Verteilung der Zählrate")
    P.ax_legend_all(loc=1)
    ax = P.savefig(f"10statistik.pdf")
    bins = (int)(n.data.max() - n.data.min()) // 5
    P.plot_histo(axes=ax, x=n, label="Histogramm", bins=bins, offset=(70, 20))
    ax.set_title(f"Statischtische Verteilung der Zählrate")
    P.ax_legend_all(loc=1)
    ax = P.savefig(f"5statistik.pdf")

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
        style="#1cb2f5",
        errors=True,
    )
    P.vload()
    z = k / l**2
    P.plot_fit(
        axes=ax,
        x=l,
        y=z,
        eqn=z,
        style=r"#1cb2f5",
        label="Abstandsgesetz",
        offset=[60, 10],
        use_all_known=False,
        guess={"k": 1500},
        bounds=[
            {"name": "k", "min": 1000, "max": 2000},
        ],
        add_fit_params=True,
        granularity=10000,
        # gof=True,
        # scale_covar=True,
    )
    ax.set_title(f"Abstandsgesetz mit Sr-90")
    P.ax_legend_all(loc=1)
    ax = P.savefig(f"abstandsgesetz.pdf")

    # A6 Magnetspektrometer Na22
    P.vload()
    filepath = os.path.join(os.path.dirname(__file__), "../data/magnetspektro.csv")
    P.load_data(filepath, loadnew=True)

    P.data["dB"] = 0.2
    P.data["dn"] = 1
    P.data["r"] = 0.05
    P.data["dr"] = 0.003
    P.print_table(B, n, name="magneto_raw", inline_units=True)
    P.data["dn"] = 0.01
    m_0 = 0.511  # MeV
    p = 299.792456 * B / 1000 * r  # radius
    P.print_expr(p)
    E = m_0 * (((p / m_0) ** 2 + 1) ** 0.5 - 1)
    P.print_expr(E)
    n_background = 23  # Hintergrundstrahlung
    P.data["n"] = n.data - n_background
    P.resolve(E)
    P.resolve(p)
    P.print_table(E, p, name="magneto_E_p", inline_units=True)
    P.plot_data(
        ax,
        E,
        n,
        label="Gemessene Daten",
        style="#9a30f0",
        errors=True,
    )
    P.plot_data(
        ax,
        p,
        n,
        label="Gemessene Daten",
        style="#ca5f46",
        errors=True,
    )
    P.vload()
    n = A * exp(-((E - mu) ** 2) / (2 * sig**2)) / (2 * pi * sig**2) ** 0.5
    P.print_expr(n)
    P.plot_fit(
        axes=ax,
        x=E,
        y=n,
        eqn=n,
        style=r"#9a30f0",
        label="Normalverteilung",
        offset=[30, -10],
        use_all_known=False,
        guess={"mu": 0.3, "sig": 0.1, "A": 300},
        bounds=[
            {"name": "A", "min": 0, "max": 350},
            {"name": "mu", "min": 0.1, "max": 0.4},
            {"name": "sig", "min": 0.01, "max": 0.9},
        ],
        add_fit_params=True,
        granularity=10000,
        # gof=True,
        scale_covar=True,
    )
    P.vload()
    n = A * exp(-((p - mu) ** 2) / (2 * sig**2)) / (2 * pi * sig**2) ** 0.5
    P.print_expr(n)
    P.plot_fit(
        axes=ax,
        x=p,
        y=n,
        eqn=n,
        style=r"#ca5f46",
        label="Normalverteilung",
        offset=[60, -10],
        use_all_known=False,
        guess={"mu": 0.5, "sig": 0.5, "A": 350},
        bounds=[
            {"name": "A", "min": 100, "max": 700},
            {"name": "mu", "min": 0.4, "max": 0.6},
            {"name": "sig", "min": 0.1, "max": 2},
        ],
        add_fit_params=True,
        granularity=10000,
        # gof=True,
        scale_covar=True,
    )
    ax.set_title(f"Energie Spektrum von Na-22")
    P.ax_legend_all(loc=1)
    ax = P.savefig(f"energiespektrum.pdf")

    # A5 Ra226 Aluminiumabsorbtion
    filepath = os.path.join(os.path.dirname(__file__), "../data/aluminium.csv")
    P.vload()
    P.load_data(filepath, loadnew=True)
    P.data["dD"] = 0
    P.data["dz1"] = 0
    P.data["dz2"] = 0
    P.data["dz3"] = 0
    P.print_table(D, z1, z2, z3, name="alu_absorbtion", inline_units=True)

    # A5 Ra226 C137 und Ra226 Bilder sind schon vorhanden und im figures folder DONE
    # filepath = os.path.join(os.path.dirname(__file__), "../data/aluminium.csv")
    # P.load_data(filepath,loadnew=True)
    # Szintillator


if __name__ == "__main__":
    test_zaehlrohr_protokoll()
