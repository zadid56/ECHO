import numpy as np
import math
import cvxpy as cp
import time
from scipy.stats import mode
from keras.models import load_model

ap_pos = np.array([[300, 300], [300, 700], [700, 300], [700, 700], [100, 100], [100, 500], [100, 900], [500, 100], [500, 500], [500, 900], [900, 100], [900, 500], [900, 900]])
m = 20
n = 13
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

steps = 15
prev_out_ap = np.ones(m)
out_ap = np.ones(m)
filepath = 'pos.txt'
count = 0
data = np.zeros((100000,int(m*2)))
model = load_model('lstm.h5')

#for a in range(2):
while(1):
    if(count>12):
        d = 1000*np.ones((steps,m,n))
        rssi = -100*np.ones((m,n))
        fp = open(filepath)
        lines = fp.readlines()
        out_ap_step = np.ones((m,steps))

        if(len(lines)==m):
            for i in range(m):
                f = lines[i]
                pos = f.strip("\n").strip("()").split(',')
                if(len(pos)==3):
                    pos = [float(j) for j in pos]
                    pos = np.array(pos)
                    data[count,i] = pos[0]
                    data[count,i+m] = pos[1]
                    x = data[count-4:count+1,[i,i+m]].reshape((1,1,10))
                    y = model.predict(x)
                    mpos = y.reshape((steps-1,2))
                    for q in range(steps-1):
                        for r in range(2):
                            if(mpos[q,r]>1000):
                                mpos[q,r] = 2000 - mpos[q,r]
                            if(mpos[q,r]<0):
                                mpos[q,r] = 0 - mpos[q,r]
                    
                    mpos = np.vstack((pos[0:2],mpos))
                    print(mpos)
                    for k in range(steps):
                        for j in range(n):
                            d[k,i,j] = math.sqrt((mpos[k,0]-ap_pos[j,0])**2 + (mpos[k,1]-ap_pos[j,1])**2)

            if(count%steps == 0):
                for k in range(steps):
                    for i in range(m):
                        for j in range(n):
                            if(j<4):
                                rssi[i,j] = max(min(dbm_lte - 10*alpha_lte*math.log10(d[k,i,j]),-30),-100)
                            else:
                                rssi[i,j] = max(min(dbm_wifi - 10*alpha_wifi*math.log10(d[k,i,j]),-30),-100)

                    dd = np.reshape(d[k,:,:],(m,n))
                    for i in range(m):
                        for j in range(n):
                            if(dd[i,j]>500):
                                dd[i,j] = 500


                    obj = (rssi+100)/70

                    A1 = np.ones((1,m))
                    b1 = np.array([nch_lte,nch_lte,nch_lte,nch_lte,nch_wifi,nch_wifi,nch_wifi,nch_wifi,nch_wifi,nch_wifi,nch_wifi,nch_wifi,nch_wifi]).reshape((1,n))

                    A2 = dd
                    b2 = np.hstack((500*np.ones((m,4)),100*np.ones((m,9))))

                    Aeq1 = np.ones((1,n))
                    beq1 = np.ones((1,m))

                    Aeq2 = np.zeros((m,n))
                    beq2 = np.zeros((m,n))
                    for p in range(m):
                        if(rssi[p,int(prev_out_ap[p]-1)] > -75):
                            Aeq2[p,int(prev_out_ap[p]-1)] = 1
                            beq2[p,int(prev_out_ap[p]-1)] = 1

                    variables = cp.Variable((m,n), boolean=True)
                    constraint1 = A1 * variables <= b1
                    constraint2 = cp.multiply(A2, variables) <= b2
                    constraint3 = Aeq1 * variables.T == beq1
                    constraint4 = cp.multiply(Aeq2, variables) == beq2
                    total_utility = cp.sum(cp.multiply(obj, variables)) - 0.5*cp.max(cp.sum(cp.reshape(variables, (m,n)), axis=0))
                    problem = cp.Problem(cp.Maximize(total_utility), [constraint1, constraint2, constraint3, constraint4])
                    problem.solve(solver=cp.GLPK_MI)
                    for p in range(m):
                        ind = int(np.nonzero(variables.value[p,:])[0][0])
                        out_ap_step[p,k] = ind+1
                    prev_out_ap = out_ap_step[:,k].reshape(m)

                out_ap = mode(out_ap_step,axis=1)[0].reshape(m)
                np.savetxt("out_ap.csv", out_ap, fmt="%d")
                prev_out_ap = out_ap

    else:
        d = 1000*np.ones((m,n))
        rssi = -100*np.ones((m,n))
        fp = open(filepath)
        lines = fp.readlines()

        if(len(lines)==m):
            for i in range(m):
                f = lines[i]
                pos = f.strip("\n").strip("()").split(',')
                if(len(pos)==3):
                    pos = [float(j) for j in pos]
                    pos = np.array(pos)
                    for j in range(n):
                        d[i,j] = math.sqrt((pos[0]-ap_pos[j,0])**2 + (pos[1]-ap_pos[j,1])**2)

            for i in range(m):
                for j in range(n):
                    if(j<4):
                        rssi[i,j] = max(min(dbm_lte - 10*alpha_lte*math.log10(d[i,j]),-30),-100)
                    else:
                        rssi[i,j] = max(min(dbm_wifi - 10*alpha_wifi*math.log10(d[i,j]),-30),-100)

            dd = d
            for i in range(m):
                for j in range(n):
                    if(d[i,j]>500):
                        dd[i,j] = 500

            obj = (rssi+100)/70

            A1 = np.ones((1,m))
            b1 = np.array([nch_lte,nch_lte,nch_lte,nch_lte,nch_wifi,nch_wifi,nch_wifi,nch_wifi,nch_wifi,nch_wifi,nch_wifi,nch_wifi,nch_wifi]).reshape((1,n))

            A2 = dd
            b2 = np.hstack((500*np.ones((m,4)),100*np.ones((m,9))))

            Aeq1 = np.ones((1,n))
            beq1 = np.ones((1,m))

            Aeq2 = np.zeros((m,n))
            beq2 = np.zeros((m,n))
            for p in range(m):
                if(rssi[p,int(prev_out_ap[p]-1)] > -75):
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

            np.savetxt("out_ap.csv", out_ap, fmt="%d")
            prev_out_ap = out_ap    

    print(out_ap)
    fp.close()
    count = count+1
    time.sleep(10)

