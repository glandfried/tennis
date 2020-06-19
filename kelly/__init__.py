
def static_bets(n=1000,initial=20,max_bet=1,odd=1.5,p=0.6,comision=0.05):
    """
    plt.plot(static_bets(initial=20))
    """
    odd2=1/((1-(1/odd))+comision/2)
    odd1=1/((1/odd)+(comision/2))
    temporal = [initial]
    for i in range(n):
        if temporal[-1] <= max_bet:
            bet=temporal[-1]/2
        else:
            bet = max_bet
        r = np.random.random()
        if r <= p :
            res = 0
        else:
            res = bet*odd2
        temporal.append(temporal[-1]+(res-bet))
    return temporal


def show_static_bets(m=33,n=350,initial=2,max_bet=0.1,p_odd=0.85,p=0.8,comision=0.05):
    """
    res = show_static_bets(m=330,n=1000,max_bet=0.05,p_odd=0.99,p=0.94,initial=6)
    sum(list(map(lambda x: 1 if x[350]<6 else 0,res)))
    """
    odd = 1/p_odd
    res = []
    odd2=1/((1-(1/odd))+comision/2)
    for i in range(m):
        res.append(static_bets(n,initial,max_bet,odd,p,comision))
        plt.plot(res[-1])
    expected = p*(0)+(1-p)*(max_bet*odd2 )
    plt.plot([0,n],[initial,initial+n*(expected-max_bet)])
    plt.plot(np.mean(res,axis=0),color="black")
    return res
    
def set_bet(w,max_bet):
    if w <= max_bet:
        bet=w/2
    else:
        bet = max_bet
    return bet

def add_comision(odd,comision):
    return 1/((1/odd)+(comision/2))

def decide(odd0,odd1,p0):
    expected = [p0*(odd0)+(1-p0)*(0),
                p0*(0)+(1-p0)*(odd1 )]
    decision = [expected[0]>1 and expected[0]>=expected[1],
                expected[1]>1 and expected[0]<expected[1]]  
    return decision, expected

def bet(w=6,max_bet=0.1,p0_odd=0.6,p0=0.6,p0_real=0.6,comision=-0.05):
    """
    bet(p0_odd=)
    """
    odd1=add_comision(1/(1-p0_odd),comision) 
    odd0=add_comision(1/p0_odd,comision)
    decision, expected = decide(odd0,odd1,p0)
    bet = set_bet(w,max_bet)  
   
    gana0 = int(np.random.random() < p0_real)
    
    res = gana0*decision[0]*bet*odd0 + (1-gana0)*decision[0]*bet*odd1
    
    return res

