def solution(s: str) -> str:
    
    #To calculate floor(N * sqrt(2)) we will require the first
    #2*ceil(log_10(N))+1 digits of frac{sqrt(2)}.
    #For N = 10 ** 100 this is roughly 250 digits.

    #First 250 digits of {sqrt(2)} = sqrt(2) - 1
    frac_sqrt_2 =(
        "414213562373095048801688724209698078569671875376"
        + "94807317667973799073247846210703885038753432764"
        + "15727350138462309122970249248360558507372126441"
        + "21497099935831413222665927505592755799950501152"
        + "78206057147010955997160597027453459686201472851"
        + "7418640889199")

    def term(k: int) -> int:
        #Find floor(k * sqrt(2)), the kth nonzero term in the sequence
        def required_digits() -> str:
            #By truncating frac_sqrt_2 down to only the digits needed
            #for that particular summand we save on computation time
            return frac_sqrt_2[:2*len(str(k))+10]
        
        beta = required_digits()
        product = str(k * int(beta))
        decimal_pos = len(beta)
        return k + int(product[:-decimal_pos])
    
    #Solutions for 0 <= int(N) < 5
    small_sums = {0: 0, 1: 1, 2: 3, 3: 7, 4: 12}

    '''
    Fraenkel’s Partition Theorem (with offset = 0) states the natural numbers
    are partitioned by the two Beatty sequences: B(p, 0) = B(p) and B(q, 0) = B(q)
    where q is the dual exponent of p.

    The dual exponent of p = sqrt(2) is q = sqrt(2) + 2.
    Note that B(q) is an integer translation of B(p).

    Exploiting this relationship and noticing B(p) (and thus B(q)) are non-decreasing
    we arrive at a partition of the positive integers less than mx = floor(N * sqrt(2)).

    Recall that the sum of the first M natural numbers is simply M * (M + 1) / 2.
    This tells us: SUM B(p) + SUM B(q) = mx * (mx + 1) / 2.
    If we rearrange the above formula we get: SUM B(p) = mx * (mx + 1) / 2 - SUM B(q),
    this lets us change the problem to finding the sum of a different sequence, B(q).
    
    To bound the largest term in B(q): note that mx < sqrt(2)*N < 2*N so mx - N < N.
    Because the max summand in B(q) is smaller than mx, the max term in B(p),
    we have a rapidly decreasing sequence of sums that we can use to solve
    our original sum.
    '''
    
    def answer(n: int) -> int:
        
        if n < 5: #Small values are explicitly given
            return small_sums[n]
        
        #We have to partition the natural numbers under floor(N * sqrt(2))
        mx = term(n)

        #The sum of the natural numbers upto mx is: mx * (mx+1) / 2
        #Instead I will work with 5*mx**2 + 5*mx, which is 10 times
        #the desired sum. 
        sum_to_mx = str(5 * mx * (mx + 1))
        
        sum_to_mx = int(sum_to_mx[:-1]) #Truncate the last term (effectively dividing by 10)
        
        return sum_to_mx - (mx - n) * (mx - n + 1) - answer(mx - n)
    
    N = int(s) #Convert our input to an integer
    return str(answer(N))

if __name__ == "__main__":
    N = 10**100
    print(solution(str(N)))
