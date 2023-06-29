import pandas as pd

file = open("./rezultat.txt",'r')
rez = open("./rezultat_analiza.txt", 'w', encoding='utf-8')

# Lista ta de domenii blocate
domenii_blocate = []

for line in file:
    domain = line.strip().split()
    domenii_blocate.insert(-1,domain[2][2:-2])

data_frame = pd.DataFrame({'Domeniu': domenii_blocate, 'Sursă': ''})

for index, row in data_frame.iterrows():
    if 'google' in row['Domeniu']:
        data_frame.at[index, 'Sursă'] = 'Google'
    elif 'facebook' in row['Domeniu']:
        data_frame.at[index, 'Sursă'] = 'Facebook'
    else:
        data_frame.at[index, 'Sursă'] = 'Altele'

total_google = data_frame[data_frame['Sursă'] == 'Google'].shape[0]
total_facebook = data_frame[data_frame['Sursă'] == 'Facebook'].shape[0]
total_altele = data_frame[data_frame['Sursă'] == 'Altele'].shape[0]

rez.write(f"Numărul de domenii de la Google:{total_google}\n")
rez.write(f"Numărul de domenii de la Facebook:{total_facebook}\n")
rez.write(f"Numărul de domenii de la alte surse:{total_altele}\n\n")

data_frame['Companie'] = data_frame['Domeniu'].str.split('.').str[-2]
frecventa_companii = data_frame['Companie'].value_counts()
cele_mai_frecvente_companii = frecventa_companii.head(5)

rez.write("Cele mai frecvente companii blocate:\n")
for companie, frecventa in cele_mai_frecvente_companii.items():
    rez.write(f"{companie} -> {frecventa}\n")

rez.flush()
rez.close()
file.close()