import matplotlib
matplotlib.rcParams['text.usetex'] = True
matplotlib.rcParams['text.latex.unicode'] = True
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from numpy import *
from matplotlib.lines import Line2D
from matplotlib.artist import Artist
from matplotlib.mlab import dist_point_to_segment
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection

def inside_shape(x,y,poly):
    n = len(poly)
    inside = False
    p1x,p1y = poly[0]
    for i in range(n+1):
        p2x,p2y = poly[i % n]
        if y > min(p1y,p2y):
            if y <= max(p1y,p2y):
                if x <= max(p1x,p2x):
                    if p1y != p2y:
                        xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xints:
                        inside = not inside
        p1x,p1y = p2x,p2y
    return inside

def geo_shape(center, size,len_c):
    len_c+=1
    theta = linspace(0.0, 2.0 * pi, len_c)
    r = sqrt(size)
    px = r * cos(theta)
    py = r * sin(theta)
    px = px + center[0]
    py = py + center[1]
    return px,py

def prep_lines(fac,dx0,dx1,dy0,dy1,xx1,yy1):
    len_l=1000
    slope = (dy1-dy0)/(dx1-dx0)
    b = dy0-slope*dx0
    newx = dx0 + fac * (dx1 - dx0)
    newy = slope * newx + b
    if arctan(slope)* 180./pi <= 0.0:
        newslope = tan(arctan(slope) + 90.0*pi/180.0 )
    else:
        newslope = tan(arctan(slope) - 90.0*pi/180.0 )
    newb = newy - newslope * newx
    if abs(arctan(slope)* 180./pi) <= 0.1:
        dnnx = zeros(len_l)
        dnnx[:] = newx
        dnny=linspace(min(yy1),max(yy1),len_l)
    else:
        dnnx = linspace(min(xx1),max(xx1),len_l)
        dnny = newslope * dnnx + newb
    x12d=column_stack((xx1,yy1))
    for i in range(len(dnnx)):
        tt = inside_shape(dnnx[i],dnny[i],x12d.tolist())
        if tt == False:
            dnnx[i] = 'NaN'
            dnny[i] = 'NaN'
    return dnnx,dnny

def main(fname):
    p1 = [0.0,0.0]
    p2 = [2.25,0.0]
    p3 = [4.5,0.0]
    p4 = [6.75,0.0]

    x1,y1 = geo_shape(p1,1.0,3)
    x2,y2 = geo_shape(p2,1.0,4)
    x3,y3 = geo_shape(p3,1.0,6)
    x4,y4 = geo_shape(p4, 1.0,1000)

    fracs = linspace(0.1,0.9,9)
    #plt.rcParams["font.family"] = "Times New Roman"
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(x1,y1,'k-',lw=0.5)
    ax.plot(x2,y2,'k-',lw=0.5)
    ax.plot(x3,y3,'k-',lw=0.5)
    ax.plot(x4,y4,'k-',lw=0.5)
    ax.scatter(p4[0],p4[1],facecolor='b')
    # Triagnle
    for j in range(len(x1)-1):
        for i in range(len(fracs)):
            #print()
            nnx1,nny1 = prep_lines(fracs[i],x1[j],x1[j+1],y1[j],y1[j+1],x1,y1)
            if fracs[i] == 0.5:
                ax.plot(nnx1,nny1,'r-',lw=0.5)
            else:
                ax.plot(nnx1,nny1,'k-',lw=0.25)
    # cube
    for j in range(len(x2)-1):
        for i in range(len(fracs)):
            #print()
            nnx1,nny1 = prep_lines(fracs[i],x2[j],x2[j+1],y2[j],y2[j+1],x2,y2)
            if fracs[i] == 0.5:
                ax.plot(nnx1,nny1,'r-',lw=0.5)
            else:
                ax.plot(nnx1,nny1,'k-',lw=0.25)
    #hexagon
    for j in range(len(x3)-1):
        for i in range(len(fracs)):
        #    print()
            nnx1,nny1 = prep_lines(fracs[i],x3[j],x3[j+1],y3[j],y3[j+1],x3,y3)
            if fracs[i] == 0.5:
                ax.plot(nnx1,nny1,'r-',lw=0.5)
            else:
                ax.plot(nnx1,nny1,'k-',lw=0.25)
    #circle
    for j in range(0,len(x4),25):
        px1 = [p4[0],x4[j]]
        py1 = [p4[1],y4[j]]
        ax.plot(px1,py1,'r-',lw=0.5)

    ax.scatter(p1[0],p1[1],facecolor='r')
    ax.scatter(p2[0],p2[1],facecolor='r')
    ax.scatter(p3[0],p3[1],facecolor='r')
    ax.scatter(p4[0],p4[1],facecolor='r')
    styles = ['<-']
    ax.add_patch(
        patches.FancyArrowPatch(
            (p1[0], -1.3),
            (p4[0], -1.3),
            arrowstyle='simple',   
            mutation_scale=30,
            linewidth=0.1
        )
    )
    ax.text(1.,-1.6,r'$\mathit{Increasing\;level\;of\;interdisciplinary\;capacity}$', size =10)
    plt.xlim(-1,7.8)
    plt.ylim(-1.7,1.1)
    ax.set_aspect(aspect=1.0)
    a=fig.gca()
    a.set_frame_on(False)
    a.set_xticks([]); a.set_yticks([])
    plt.axis('off')
    print("saving to file:",fname)
    plt.savefig(fname, dpi=300, bbox_inches='tight')

if __name__ == '__main__':
    print()
    print("\t \033[1m Making figure for proposal \033[0m")
    main('figure1.png')
    print("\t \033[1m DONE \033[0m")
    print()
