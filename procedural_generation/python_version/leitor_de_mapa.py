def import_csv_layout(path):
    terrain_map = []
    path = 'map2.csv'
    with open(path) as level_map:
        print(level_map)
        for linha in level_map:
            linha  = linha.split(',')
            
            print(linha)



import_csv_layout('dsadfas')