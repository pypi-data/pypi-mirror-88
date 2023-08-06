from math import *
def plot_sin(t=[*range(1000)],sampling = 1,frequency1 = 10,phase1=20,offset1=30,amplify1=10,
                            frequency2 = 1,phase2=200,offset2=3,amplify2=10):

    error = ''#@
    try:
        x,y1,y2 =[],[],[]
        for t_i in t:
            t_i+=1
            t_i = t_i/sampling
            x.append(t_i)
            y1.append(amplify1*sin((t_i+phase1)*frequency1*2*pi)+offset1)
            y2.append(amplify2*sin((t_i+phase2)*frequency2*2*pi)+offset2*log(t_i))

            # y3.append()
        plot = [t,y1,y2] #@
    except Exception as e:
        error = e #@

    return y1
if __name__ == "__main__":
    plot_sin()
# print(log(0))
