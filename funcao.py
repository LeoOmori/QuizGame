
def comparaString(a,b):

    string1 = a
    string2 = b
   

    size_a = len(string1) + 1
    size_b = len(string2) + 1

    matrix = [[0 for i in range(size_b+1)] for j in range(size_a+1)]



    for i in range(size_a):
        matrix[i][0] = i

    for j in range(size_b):
        matrix[0][j] = j


    for i in range(1, size_a):
    
    
     for j in range(1, size_b):
        
        
        if string1[i-1] == string2[j-1]:
            matrix[i][j] = min(matrix[i-1][j-1], matrix[i-1][j] + 1, matrix[i][j-1] + 1)

        
        else:
            matrix[i][j] = min(matrix[i-1][j]+1, matrix[i-1][j-1]+1, matrix[i] [j-1]+1)

    print(matrix)
    print('')
    diferenca = (matrix[size_a-1][size_b-1])

    if diferenca == 0:
        print('Sao iguais')
    elif diferenca <= 2:
        print('Sao parecidos')
    else:
        print("Sao diferentes")



    print('Distancia entre {}  e {} é {}.'.format(string1, string2, matrix[size_a - 1][size_b - 1]))
    print('')

    return matrix[size_a - 1][size_b - 1]
comparaString("avengers", "avengar")