from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
# import matplotlib.pyplot as plt
import io

# def generate_graphs(final_dict):
#     fig, axes = plt.subplots(len(final_dict)//2, 2, figsize=(10, 10))
#     labels = ['Tempo de Operação', 'Tempo Ocioso']

#     for i, (key, value) in enumerate(final_dict.items()):
#             # Obter o índice da linha e da coluna do eixo atual
#             row = i // 2
#             col = i % 2
#             # Obter os valores relativos do dicionário
#             try:
#                 data = list(value['Relativos'].values())
#             except Exception as e:
#                 print(value)
#                 print(type(value))
#             # Plotar o gráfico de pizza no eixo atual
#             axes[row, col].pie(data, labels=labels, autopct='%.2f%%', shadow=True)
#             # Adicionar o título do eixo com a chave do dicionário
#             axes[row, col].set_title(key)

#     buf = io.BytesIO()
#     plt.savefig(buf, format="png")
    
#     image = UploadFile(filename="graph.png",file=buf)
#     return FileResponse(image.file, media_type="image/png")

def total_production(aux_dict):
    def classify_piece(red, aux_dict, count): 
        if i == red:
            for j in aux_dict[i]:
                if j[1] == 1 or j[1] == True:
                    count += 1
        return count
    
    TotalProd = {}
    count_red, count_black, count_metal = 0,0,0

    for i in aux_dict:
        # TODO ajustar as tags para as tags de acordo com o objeto certo
        count_red, count_black, count_metal = classify_piece('G1',aux_dict,count_red), classify_piece('G2', aux_dict, count_black), classify_piece('G3', aux_dict, count_metal)

    TotalProd['Vermelha'] = count_red
    TotalProd['Preta'] = count_black
    TotalProd['Metalica'] = count_metal
    TotalProd['Total'] = count_metal + count_black + count_red

    return TotalProd

def failures(aux_dict):
    count = 0
    cf = 0
    TotalFails = {}
    for i in aux_dict['M_STOP']:
        if i[1] == True:
            count += 1
        if i[1] == False:
            print(i)
            cf += 1
    TotalFails['Fails'] = count
    TotalFails['Normal'] = cf
    return TotalFails
