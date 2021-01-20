import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches

def ploter(resultado):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    data1 = []
    data2 = []
    data3 = []
    ejey = []
    color = 'red'
    drasp1= []
    drasp2 = []
    drasp3= []
    xrasp1=[]
    xrasp2 = []
    xrasp3 = []
    for row in resultado:
        data1.append(float(row.content))
        if row.raspberry == 'RASP1':
            drasp1.append(float(row.content))
            xrasp1.append(str(row.date_created.strftime("%d %H:%M:%S")))
        # ax.plot(data1, marker='o', linestyle='none', color='red' if row.raspberry == 'RASP1' else (('green') if (row.raspberry == 'RASP2') else ('blue')),markersize=20)
        elif row.raspberry == 'RASP2':
            drasp2.append(float(row.content))
            xrasp2.append(str(row.date_created.strftime("%d %H:%M:%S")))
            # ax.plot(float(row.content), marker='v', linestyle='none', color='blue', markersize=20)
            # ax.plot(float(row.content), marker='v', linestyle='none', color='green', markersize=20)
            # ax.plot(float(row.content), marker='P', linestyle='none', color='red', markersize=20)
        else:
            drasp3.append(float(row.content))
            xrasp3.append(str(row.date_created.strftime("%d %H:%M:%S")))
        ejey.append(str(row.date_created.strftime("%d %H:%M:%S")))

    ## necessary variables
    ind = np.arange(len(data1))  # the x locations for the groups
    width = 0.5  # the width of the bars

    ## the bars
    rects1 = ax.bar(ind, data1, width,
                    color='black',
                    error_kw=dict(elinewidth=2, ecolor='red'))

    # axes and labels

    minimo = min(data1) - 0.25
    maximo = max(data1) + 0.25
    ax.set_xlim(-width, len(ind) + width)
    ax.set_ylim(minimo, maximo)

    ax.set_xticks(ind + width)
    xtickNames = ax.set_xticklabels(ejey)
    plt.setp(xtickNames, rotation=90, fontsize=0)

    fig.set_size_inches(50, 50)
    plt.plot(ejey, data1, color='k')
    plt.scatter(xrasp1, drasp1, color='r',s=800)
    plt.scatter(xrasp2, drasp2, color='g',s=800)
    plt.scatter(xrasp3, drasp3, color='b',s=800)
    ax.set_ylabel('TEMPERATURA',fontsize=200)
    ax.set_xlabel('FECHA',fontsize=200)
    ax.set_title('TEMP(t)',fontsize=200)

    lrasp1 = mpatches.Patch(color='red', label='RASP1')
    lrasp2 = mpatches.Patch(color='green', label='RASP2')
    lrasp3 = mpatches.Patch(color='blue', label='RASP3')

    plt.legend(handles=[lrasp1,lrasp2,lrasp3],fontsize=100)
    plt.yticks(fontsize=70)
    return fig
