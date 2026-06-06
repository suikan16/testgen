import random, time, math
def gengaps(length):    
    gaps = [1, 4, 10, 23, 57, 132, 301, 701, 1750]
    
    if length <= gaps[-1]:
        return [g for g in gaps if g < length]
        
    while True:
        next_gap = int(gaps[-1] * 2.25 + 0.5)
        if next_gap >= length:
            break
        gaps.append(next_gap)
        
    return gaps
def shellsort(arr):
    l = len(arr)  
    gaps = gengaps(l)
    
    g = len(gaps) - 1
    while g >= 0 and gaps[g] >= l:
        g -= 1

    while g >= 0:
        gap = gaps[g]
        
        for i in range(gap, l):
            t = arr[i]
            j = i
            while j >= gap and arr[j - gap] > t:
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = t
            
        g -= 1 
        
    return arr
def timealg(sortf, arr):
    start_cpu = time.perf_counter()
    sortf(arr)
    end_cpu = time.perf_counter()
    el = (end_cpu-start_cpu)*10**6
    return el
n1 = int(input())
RandomArr1 = [x for x in range(1, n1+1)]
random.shuffle(RandomArr1)

n2 = int(input())
RandomArr2 = [x for x in range(1, n2+1)]
random.shuffle(RandomArr2)

t1 = timealg(shellsort, RandomArr1)
t2 = timealg(shellsort, RandomArr2)

#Доказательство сложности Алгоритма Шелл Сорт Циура
#T1 = N1^x   T2/T1 = (N2/N1)^x ln(T2/T1) = ln(N2/N1)^x  
#T2 = N2^x   ln(T2/T1) = xln(N2/N1) x = ln(T2/T1)/ln(N2/N1)
pow = math.log(t2/t1)/math.log(n2/n1)
print(f'Теоретическая сложность алгоримта: O(n^{pow})')
print(4/3)
