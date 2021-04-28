import numpy as np
import math
import cvxpy as cp
import time
import re
from collections import Counter

ap_pos = np.array([[300, 500], [700, 500], [100, 100], [100, 900], [900, 100], [900, 900], [500, 500]])
m = 10
n = 7
dbm_lte = 18
dbm_wifi = -20
alpha_lte = 3.76
alpha_wifi = 3
tp_lte = 10
tp_wifi = 0.1
bw = 20
beta = 0.5
nch_lte = 25
nch_wifi = 25
kai = 5
rho = 1.3
h = 1
wn = 0
lamda = 1-math.exp(-1 / ( (kai-1)**(1/kai) + (kai-1)**((1-kai)/kai) ) )

prev_out_ap = np.ones(m)
out_ap = np.ones(m)
d = 1000*np.ones((m,n))
filepath = 'pos.txt'
count = 0

#for a in range(2):
while(1):
    rssi = -100*np.ones((m,n))
    out_ap = np.ones(m)
    fp = open(filepath,'r')
    lines = fp.readlines()

    if(len(lines)==m):
        for i in range(m):
            f = lines[i]
            pos = filter(None,re.split(' +', f.strip("\n").strip("[]")))
            #print(pos)
            if(len(pos)==3):
                pos = [float(j) for j in pos]
                pos = np.array(pos)
                for j in range(n):
                    d[i,j] = math.sqrt((pos[0]-ap_pos[j,0])**2 + (pos[1]-ap_pos[j,1])**2)

        for i in range(m):
            for j in range(n):
                if(j<2):
                    rssi[i,j] = max(min(dbm_lte - 10*alpha_lte*math.log10(d[i,j]),-30),-100)
                else:
                    rssi[i,j] = max(min(dbm_wifi - 10*alpha_wifi*math.log10(d[i,j]),-30),-100)

        dd = d
        for i in range(m):
            for j in range(n):
                if(dd[i,j]>800):
                    dd[i,j] = 800

        obj = (rssi+100)/70

        A1 = np.ones((1,m))
        b1 = np.array([nch_lte,nch_lte,nch_wifi,nch_wifi,nch_wifi,nch_wifi,nch_wifi]).reshape((1,n))

        A2 = dd
        b2 = np.hstack((800*np.ones((m,2)),100*np.ones((m,5))))

        Aeq1 = np.ones((1,n))
        beq1 = np.ones((1,m))

        Aeq2 = np.zeros((m,n))
        beq2 = np.zeros((m,n))
        for p in range(m):
            if(rssi[p,int(prev_out_ap[p]-1)] > -76):
                Aeq2[p,int(prev_out_ap[p]-1)] = 1
                beq2[p,int(prev_out_ap[p]-1)] = 1

        variables = cp.Variable((m,n), boolean=True)
        constraint1 = A1 * variables <= b1
        constraint2 = cp.multiply(A2, variables) <= b2
        constraint3 = Aeq1 * variables.T == beq1
        constraint4 = cp.multiply(Aeq2, variables) == beq2
        total_utility = cp.sum(cp.multiply(obj, variables)) - 0.5*cp.max(cp.sum(cp.reshape(variables, (m,n)), axis=0))
        if(count>0):
            problem = cp.Problem(cp.Maximize(total_utility), [constraint1, constraint2, constraint3, constraint4])
        else:
            problem = cp.Problem(cp.Maximize(total_utility), [constraint1, constraint2, constraint3])
        problem.solve(solver=cp.GLPK_MI)
        for p in range(m):
            ind = int(np.nonzero(variables.value[p,:])[0][0])
            out_ap[p] = ind+1

        print(out_ap)
        np.savetxt("out_ap.csv", out_ap, fmt="%d")
        prev_out_ap = out_ap
    fp.close()
    count = count+1
    time.sleep(10)

