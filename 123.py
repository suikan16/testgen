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
def timealg(sortf, original_arr, runs=100):
    total_time = 0
    for _ in range(runs):
        arr_copy = original_arr.copy() 
        
        start_cpu = time.perf_counter()
        sortf(arr_copy)
        end_cpu = time.perf_counter()
        
        total_time += (end_cpu - start_cpu) * 10**6
        
    return total_time / runs
def genarr(n):
    sort_arr = [x for x in range(1,n+1)]

    random_arr = sort_arr.copy()
    random.shuffle(random_arr)

    rev_arr = sort_arr[::-1]
    return random_arr, sort_arr, rev_arr

def compl(arr1, arr2, n1, n2):
    t1 = timealg(shellsort, arr1, runs=1000)
    t2 = timealg(shellsort, arr2, runs=1000)
    return math.log(t2/t1)/math.log(n2/n1)
n1 = int(input())
n2 = int(input())
RandArr1, SortArr1, RevArr1 = genarr(n1)
RandArr2, SortArr2, RevArr2 = genarr(n2)

pow_rand = compl(RandArr1, RandArr2, n1, n2)
pow_sort = compl(SortArr1, SortArr2, n1, n2)
pow_rev = compl(RevArr1, RevArr2, n1, n2)
print(f'Теоретическая сложность алгоримта в лучшем: O(n^{pow_sort})')
print(f'Теоретическая сложность алгоримта в среднем: O(n^{pow_rand})')
print(f'Теоретическая сложность алгоримта в худшем: O(n^{pow_rev})')

