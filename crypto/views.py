from django.shortcuts import render, redirect
from .models import records, rsa_records

# Create your views here.

import random
import math

def gcd(x,y):
    r=x%y
    while r>1:
        x=y
        y=r
        r=x%y
    if r==0:
        return y
    return 1

def fastexp(x,e,m):
    y=1
    while e!=0:
        if e%2==1:
            e=e-1
            y=(y*x)%m
        else :
            e=int(e/2)
            x=(x*x)%m
    return y

def bsgs(b,a,p):
    m=math.ceil(math.sqrt(p-1))
    rhs=[[0,1],[1,b]]
    for i in range(2,m):
        rhs.append([i,(rhs[i-1][1]*b)%p])
    lhs=[[0,a]]
    binv=fastexp(b,p-2,p)
    binv=fastexp(binv,m,p)
    for i in range(1,m):
        lhs.append([i,(lhs[i-1][1]*binv)%p])
    rhs.sort(key=lambda x: x[1])
    lhs.sort(key=lambda x: x[1])
    i,j,l=0,0,0
    while i<len(rhs) and j<len(lhs):
        if rhs[i][1]==lhs[j][1]:
            l=(rhs[i][0]+(m*lhs[j][0]))%(p-1)
            i=i+1
        elif rhs[i][1]<lhs[j][1]:
            i=i+1
        else:
            j=j+1
    return l

def miller_rabin_test(n):
    if n < 2:
        return False
    small_primes = [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61,
        67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137,
        139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199
    ]
    if n in small_primes:
        return True
    if any(n % p == 0 for p in small_primes):
        return False
    return miller_rabin(n)

def miller_rabin(n, rounds=8):
    #Miller-Rabin primality test for finding if a number is prime or composite
    if n % 2 == 0 or n < 2:
        return False
    r, m = 0, n - 1
    while m % 2 == 0:
        r += 1
        m //= 2
    for _ in range(rounds):
        base = random.randint(2,n - 2)
        x = fastexp(base, m, n)
        if x in (1, n - 1):
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def blum_blum_shub(size=10**8):
    # Generates a random series of bits resulting a complete random number
    p = generate_random_prime(size)
    while p%4!=3:
        p = generate_random_prime(size)
    q = generate_random_prime(size)
    while p==q or q%4!=3:
        q = generate_random_prime(size)
    n = p*q
    s = [ random.randint(1,size) ]
    b = [ s[0]%2 ]
    x = random.randint(1,int(math.log(size,2)))
    for i in range(x-1):
        s.append((s[-1]*s[-1])%n)
        b.append(s[-1]%2)
    ans,t=0,1
    for i in range(x-1,0,-1):
        ans+=t*b[i]
        t*=2
    return ans

def generate_random_prime(size=10**8):
    # Generates a random prime number using the Miller-Rabin test and blum blum shub method within given size
    while True:
        a = random.randint(3,size)
        if miller_rabin_test(a):
            return a

def p_minus_one(n):
    # Pollard's p-1 algorithm for factorization to find prime factor of n
    for b in range(2,int(math.sqrt(n))+1):
        if n%b==0:
            return b
        else:
            c = b
            for i in range(2,b+1):
                if miller_rabin_test(i)==False:
                    continue
                a = int(math.log(n,i))
                a = math.pow(i,a)
                c = fastexp(c,a,n)
                if c==1:
                    continue
                a = gcd(c-1,n)
                if a!=1 :
                    return a
    return n

    # a, i = 2, 2
    # while True:
    #     a = FastModExo(a, i, n)  # (a^i) mod n
    #     d = GCD(a - 1, n)
    #     if 1 < d < n:
    #         return d
    #     i += 1

def pollard_factors(n):
    #Uses Pollard's p-1 algorithm to factorize n into its prime components.
    p,q = p_minus_one(n),n
    print(p,"p", n)
    while q%p==0:
        q = q // p
    print(q,"q")
    if q==1:
        return (p,)
    if miller_rabin_test(q):
        return p, q
    return (p,)+ pollard_factors(q)

def cyclic(g):
    if g==2 or g==4:
        return True
    if g%2==0:
        g/=2
    if g%2==0:
        while g%2==0:
            g/=2
        if g==1:
            return True
        else:
            return False
    else:
        x=pollard_factors(g)
        if len(x)>1:
            return False
        else:
            return True
        
def pr(b,q,g):
    for x in q:
        if fastexp(b,x,g)==1:
            return False
    return True

def primitive_root(g):
    p=pollard_factors(g-1)
    print(p)
    q=p
    for r in p:
        x=r
        while g%x==0:
            q=q+tuple(x)
            x*=r
    p=q
    for r in p:
        for l in p:
            if l%r==0:
                continue
            q=q+(r*l,)
    q=tuple(set(q))
    while True:
        b=blum_blum_shub(g-1)
        while b==0:
            b=blum_blum_shub(g-1)
        print(b,g-1)
        if pr(b,q,g) is True:
            return b  

def phi(g):
    if g==2 or g==4:
        return g//2
    if g%2==0:
        g/=2
    p=p_minus_one(g)
    if p==g:
        return p-1
    k,q=1,p
    while g%q==0:
        q*=p
        k+=1
    return fastexp(p,k-1,g)*(k-1)

def alice_1(g):
    b=primitive_root(g)
    r=blum_blum_shub(g-1)
    while r<=1:
        r=blum_blum_shub(g-1)
    br=fastexp(b,r,g)
    return b,br,r

def bob_1(b,br,g):
    l=blum_blum_shub(g-1)
    while l<2:
        l=blum_blum_shub(g-1)
    bl=fastexp(b,l,g)
    blr=fastexp(br,l,g)
    blri=fastexp(blr,phi(g)-1,g)
    return l,bl,blri

def alice_2(g,r,bl):
    return fastexp(bl,r,g)

def alice(x,blr,g):
    y=x
    y*=blr
    y%=g
    return y

def bob(y,blri,g):
    x=y
    x*=blri
    x%=g
    return x

# class Timeout(Exception): 
#     pass 

# def try_one(func,t):
#     def timeout_handler(signum, frame):
#         raise Timeout()

#     old_handler = signal.signal(signal.SIGALRM, timeout_handler) 
#     signal.alarm(t) # triger alarm in 3 seconds

#     try: 
#         t1=time.clock()
#         func()
#         t2=time.clock()

#     except Timeout:
#         print('{} timed out after {} seconds'.format(func.__name__,t))
#         return None
#     finally:
#         signal.signal(signal.SIGALRM, old_handler) 

#     signal.alarm(0)
#     return t2-t1

# def troublesome():
#     while True:
#         pass

def eve(g,b,bl,br):
    r=bsgs(b,br,g)
    if fastexp(b,r,g)==br:
        blr=fastexp(bl,r,g)
        blri=fastexp(blr,phi(g)-1,g)
        return blri
    l=bsgs(b,bl,g)
    if fastexp(b,l,g)==bl:
        blr=fastexp(br,l,g)
        blri=fastexp(blr,phi(g)-1,g)
        return blri
    return 0

# def eve(x,blri,g):
#     y=x
#     y*=blri
#     y%=g
#     return y

def is_prime(n):
    """
    Basic primality test using trial division up to sqrt(n).
    Less efficient for large numbers.
    """
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

record1=rsa_records(id=1,n=0,p=0,q=0,phi=0,e=0,d=0,msg=0)
record1.save()

def rsab0(request):
    if request.method=='POST':
        p_=request.POST.get('p')
        q_=request.POST.get('q')
        e_=request.POST.get('e')
        print(p_,q_,e_)
        print("1")
        if len(p_)==0 or p_ is None or p_==0:
            p=generate_random_prime()
            while p<10 or p>10000:
                p=generate_random_prime()
        else:
            p=int(p_)
            if miller_rabin_test(p)==False:
                return render(request,'rbob0.html',{'x':1})
        if len(q_)==0 or p_ is None or p_==0:
            q=generate_random_prime()
            while q<10 or q>10000:
                q=generate_random_prime()
        else:
            q=int(q_)
            if miller_rabin_test(q)==False:
                return render(request,'rbob0.html',{'x':2})
        phi=(p-1)*(q-1)
        n=p*q
        if len(e_)==0 or e_ is None or e_==0:
            e=blum_blum_shub(phi)
            while e<2:
                e=blum_blum_shub(phi)
        else:
            e=int(e_)
            if e>phi:
                return render(request,'rbob0.html',{'x':3})
        d=fastexp(e,phi-1,n)
        record3=rsa_records.objects.get(id=1)
        record3.n=n
        record3.p=p
        record3.q=q
        record3.phi=phi
        record3.e=e
        record3.d=d
        record3.msg=0
        print(n,p,q,e,d,phi)
        record3.save()
        return redirect(rsab)
    else:
        return render(request,'rbob0.html',{'x':0})

def rsab(request):
    record4=rsa_records.objects.get(id=1)
    n=record4.n
    p=record4.p
    q=record4.q
    e=record4.e
    d=record4.d
    phi=record4.phi
    print("bob",record4.msg,n,p,q,e,d,phi)
    if record4.msg==0:
        msg=""
    else:
        x=record4.msg
        x*=d
        x%=n
        msg="Alice sent you: "+str(x)
    return render(request,'rbob.html',{'n':n,'p':p,'q':q,'e':e,'d':d,'phi':phi,'msg':msg})

def rsaa(request):
    record6=rsa_records.objects.get(id=1)
    n=record6.n
    e=record6.e
    x=0
    if request.method=='POST':
        record6.msg=int(request.POST.get('g'))
        print(record6.msg)
        record6.msg*=e
        record6.msg%=n
        x=1
        record6.save()
    return render(request, 'ralice.html',{'n':n,'e':e,'x':x})

def rsae(request):
    record7=rsa_records.objects.get(id=1)
    n=record7.n
    e=record7.e
    x=record7.msg
    r=pollard_factors(n)
    p=r[0]
    q=r[1]
    phi=(p-1)*(q-1)
    d=fastexp(e,phi-1,n)
    if x==0:
        return render(request, 'reve.html',{'n':n,'e':e,'p':p,'q':q,'phi':phi,'msg':x})
    x*=d
    x%=n
    return render(request, 'reve.html',{'n':n,'e':e,'p':p,'q':q,'phi':phi,'d':d,'msg':x})

def land(request):
    return render(request, 'index.html')

record2=records(id=1,g=0,b=0,l=0,r=0,bl=0,br=0,blr=0,blri=0,msg=0)
record2.save()

def alice1(request):
    if request.method=='POST':
        print("2")
        g_=request.POST.get('g')
        print("Print","(",g_,")",type(g_))
        if len(g_)==0:
            g=generate_random_prime()
        else:
            g=int(g_)
        print(g)
        if cyclic(g)==False:
            return render(request,'alice.html',{'x':0})
        else:
            b,br,r=alice_1(g)
            l,bl,blri=bob_1(b,br,g)
            x=1
            blr=alice_2(g,r,bl)
            record=records.objects.get(id=1)
            record.g=g
            record.l=l
            record.b=b
            record.r=r
            record.br=br
            record.bl=bl
            record.blr=blr
            record.blri=blri
            record.msg=0
            record.save()
            print(g,b,r,br)
            return render(request, 'alice2.html',{'g':g,'blr':blr,'b':b,'r':r,'br':br, 'bl':bl, 'x':0})
    else:
        return render(request, 'alice.html',{'x':0})

def alice2(request):
    x=int(request.POST.get('g'))
    blr=records.objects.values_list('blr').get(id=1)[0]
    g=records.objects.values_list('g').get(id=1)[0]
    b=records.objects.values_list('b').get(id=1)[0]
    r=records.objects.values_list('r').get(id=1)[0]
    br=records.objects.values_list('br').get(id=1)[0]
    bl=records.objects.values_list('bl').get(id=1)[0]
    print(x,blr,b,br,r,g)
    y=alice(x,blr,g)
    record=records.objects.get(id=1)
    record.msg=y
    record.save()
    return render(request,"alice2.html",{'g':g,'blr':blr,'b':b,'r':r,'bl':bl,'br':br,'x':1})

def bob1(request):
    y=records.objects.values_list('msg').get(id=1)[0]
    blri=records.objects.values_list('blri').get(id=1)[0]
    g=records.objects.values_list('g').get(id=1)[0]
    b=records.objects.values_list('b').get(id=1)[0]
    l=records.objects.values_list('l').get(id=1)[0]
    br=records.objects.values_list('br').get(id=1)[0]
    bl=records.objects.values_list('bl').get(id=1)[0]
    x=bob(y,blri,g)
    msg="Alice sent "+str(x)
    return render(request,"bob.html",{'b':b, 'blri':blri, 'l':l,'bl':bl, 'br':br, 'g': g, 'msg':msg})

def eve1(request):
    g=records.objects.values_list('g').get(id=1)[0]
    b=records.objects.values_list('b').get(id=1)[0]
    y=records.objects.values_list('msg').get(id=1)[0]
    br=records.objects.values_list('br').get(id=1)[0]
    bl=records.objects.values_list('bl').get(id=1)[0]
    blri=eve(g,b,bl,br)
    x=bob(y,blri,g)
    msg="Alice sent "+str(x)+" to Bob"
    return render(request,"eve.html",{'g':g,'b':b,'bl':bl,'br':br, 'blri':blri, 'msg':msg})