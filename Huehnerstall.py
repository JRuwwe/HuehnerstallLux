klappenzustand = False


def alltags_sequenz():
    update_lampen_zustand()
    update_rote_lampen_zustand()

    if daemmerig_oder_heller():
        if klappenzustand:
            return
        setze_tagesanfangszeit()
        setze_klappe(True)
        return

    if not dunkel_oder_dunkler():
        return

    if not klappenzustand:
        return

    setze_tagesanfangszeit()
    setze_klappe(False)


def update_lampen_zustand():
    # TODO Lampe an oder ausschalten, je nach Bedingungen
    return


def update_rote_lampen_zustand():
    # TODO Rote Lampe an oder ausschalten, je nach Bedingungen
    return


def daemmerig_oder_heller():
    # TODO Falls es dämmerig oder heller ist → return True, sonst return False
    return True


def dunkel_oder_dunkler():
    # TODO Falls es dunkel oder dunkler ist → return True, sonst return False
    return True


def setze_klappe(p_klappenzustand):
    # TODO GPIO Pins so setzen, dass Klappe geschlossen wird
    global klappenzustand
    klappenzustand = p_klappenzustand


def setze_tagesanfangszeit():
    # TODO aktuellen Zeitpunkt als Variable tagesanfangszeit speichern

    # hilfreicher Code:

    # import datetime
    #
    # # direkt ein datetime.time-Objekt erhalten
    # zeit_nur_hms = datetime.datetime.now().time()
    #
    # # Ausgabe der neuen Variable
    # print(zeit_nur_hms)
    return


def setze_tagesendzeit():
    # TODO aktuellen Zeitpunkt als Variable tagesendzeit speichern

    # hilfreicher Code:

    # import datetime
    #
    # # direkt ein datetime.time-Objekt erhalten
    # zeit_nur_hms = datetime.datetime.now().time()
    #
    # # Ausgabe der neuen Variable
    # print(zeit_nur_hms)
    return
