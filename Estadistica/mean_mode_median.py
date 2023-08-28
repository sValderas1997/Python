from statistics import median

error=0
N = int (input())
X = str (input())

X = X.split()
X =[float(i) for i in X]

N_mode=[]
for i in X:
    if not (i >0 and i <=10**5) and not (N >=10 and N <=2500):
        error=1   
        print("ERROR") 
        break
    conta = 0
    for y in X:
        if i == y:
            conta += 1
            N_mode.append((i,conta))       

#print (N_mode)
if error != 1:
    
    low = 0    
    for num in N_mode:
        if low < num[1]:
            low = num[1]
            moda = num[0]
        if low == num[1]:    
            if moda > num[0]:
                moda = num[0]
                         
    mean=sum(X)/N
    mediana= median(X)
    
    print("{:.1f}".format(mean))
    print("{:.1f}".format(mediana))
    print("{:.0f}".format(moda))
        
