# Conexões para desenhar a mão manualmente
HAND_CONNECTIONS = [
    (0, 1), (1, 2), #conexão do pulso no polegar
    (0, 5), #conexão do pulso com indicador
    (0, 9), #conexão do pulso com o dedo médio
    (0, 13), #conexão do pulso com o anelar
    (0, 17), #conexão do pulso com o mindinho

    (2, 5), #Conexão entre o polegar e o indicador
    (5, 9), #Conexao entre o indicador e o dedo médio
    (9, 13), #Conexao entre o dedo médio com anelar
    (13, 17), #Conexão entre o anelar com mindinho

    (2, 3), (3, 4), #polegar
    (5, 6), (6, 7), (7, 8), #indicador
    (9, 10), (10, 11), (11, 12), #dedo médio
    (13, 14), (14, 15), (15, 16), #anelar
    (17, 18), (18, 19), (19, 20), #mindinho
]

FINGER_TIPS = [8, 12, 16, 20] #ponta dos dedos
THUMB_TIP = 4 #ponta do polegar