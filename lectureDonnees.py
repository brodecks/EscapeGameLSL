import pyxdf

cheminFichier = r'C:\Users\rapha\OneDrive\Documents\CurrentStudy\sub-P001\ses-S001\eeg\sub-P001_ses-S001_task-Default_run-001_eeg.xdf'

#chargemnt du fichier
data, header = pyxdf.load_xdf(cheminFichier)

for donnee in data:
    nom_flux = donnee['info']['name'][0]

    if nom_flux == 'HeartSim':
        #extraction des tableaux de donnees
        bpm_raw = donnee['time_series']
        timestamps_raw = donnee['time_stamps']

        #temps commence a zero
        temps_zero = timestamps_raw - timestamps_raw[0]

        print(f"--- Analyse de {nom_flux} terminée ---")
        print(f"Le joueur a commencé à {bpm_raw[0]} BPM")
        print(f"Le joueur a fini à {bpm_raw[-1]} BPM")
        print(f"Durée totale : {temps_zero[-1]:.0f} secondes")#.0f permet de ne pas garder les chiffres apres la virgule
