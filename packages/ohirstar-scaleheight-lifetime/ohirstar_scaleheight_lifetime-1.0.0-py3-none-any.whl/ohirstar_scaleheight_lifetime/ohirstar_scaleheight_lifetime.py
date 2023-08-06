import numpy as np
from scipy.special import comb 
from scipy import stats
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class ScaleHeight:
    def __init__(self):
        return 

    def model(self, dist_func: dict, number: int, kinematic_dist: str):
        """
        dist_func: dict
            Distribution Function
            Horizontal Galactic distribution = Exponential
            Vertical Galactic distribution   = Gaussian
            dist_func = {'scale_length':XX[kpc], 'scale_height':XX[kpc]}
        number: int
            Total number of modeling stars
            number = 100000
        kinematic_dist: int
            Both Near and Far kinematic distance methods are supported. 
            kinematic_dist = 'near'
        """
        kpc_m     = 1000 * (3.0 * 10 ** 16)
        W_Jy      = 10 ** 26
        SUN       = np.array([0, -8.2, -0.017]) # location of the Sun in the Galaxy.
        luminosity_func = {'near':{'mean':15.3, 'std':0.531},'far':{'mean':15.5, 'std':0.531}}
        std       = dist_func['scale_height']/np.sqrt(2)
        np.random.seed(777)
        theta     = np.random.uniform(0, 2*np.pi, number)
        np.random.seed(778)
        r         = np.random.exponential(dist_func['scale_length'],number)
        mx, my    = r * np.cos(theta), r * np.sin(theta)
        np.random.seed(779)
        mz        = np.random.normal(loc=0, scale=std, size=number)
        np.random.seed(780)
        luminosity = np.random.normal(loc=luminosity_func[kinematic_dist]['mean'], scale=luminosity_func[kinematic_dist]['std'], size=number)
        # distance from the Sun
        r_xyz      =  np.sqrt((mx-SUN[0])**2 + (my-SUN[1])**2 + (mz-SUN[2])**2)  
        r_xyz2_m   = r_xyz ** 2 * kpc_m ** 2 # kpc -> m
        mflux      = np.array([float(i) for i in ((10 ** luminosity * W_Jy) / (4*np.pi*r_xyz2_m))])
        # Galactic Coordinate
        r_xy      = np.sqrt((mx-SUN[0])**2 + (my-SUN[1])**2)
        ml        = np.array([np.arccos((my-SUN[1])[i]/r_xy[i])*360/(2*np.pi) if (mx-SUN[0])[i]<0 else -np.arccos((my-SUN[1])[i]/r_xy[i])*360/(2*np.pi) for i in range(len(my)) ])
        mb        = np.arcsin((mz-SUN[2])/r_xyz) * 360/(2*np.pi)
        model_xyz = np.array([mx,my,mz])
        model_lb  = np.array([ml,mb])
        return model_xyz, model_lb, mflux

    def visualize(self, model, mflux):
        cmap = 'nipy_spectral'
        fig  = plt.figure(figsize=(10,4))
        if len(model) == 2:
            ax   = fig.add_subplot(111)
            sc   = ax.scatter(model[0], model[1], c=np.log10(mflux), cmap=cmap)
            ax.set_xlabel('Longitude (l)')
            ax.set_ylabel('Latitude (b)')
        if len(model) == 3:
            ax   = fig.add_subplot(111, projection='3d')
            sc   = ax.scatter(model[0], model[1], zs=model[2], zdir='z', c=np.log10(mflux),cmap=cmap)
            ax.set_xlabel('X [kpc]')
            ax.set_ylabel('Y [kpc]')
            ax.set_zlabel('Z [kpc]')
        plt.show()
        return

    def pvalue(self, data, model, mflux, detection_limit, region):
        observable_index = np.where(mflux > detection_limit)[0]
        model_test_index = []
        data_test_index  = []
        ml, mb = model[0], model[1] # l,b
        dl, db = np.array([float(x)-360 if float(x)>180 else float(x) for x in data[0]]), data[1]
        for field in region:
            for i in range(len(observable_index)):
                if field['l'][0] <= ml[observable_index][i] <= field['l'][1] and field['b'][0] <= mb[observable_index][i] <= field['b'][1]:
                    model_test_index.append(observable_index[i])
            for i in range(len(dl)):
                if field['l'][0] <= dl[i] <= field['l'][1]:
                    data_test_index.append(i)
        # for check
        fig = plt.figure(figsize=(5,5))
        ax = fig.add_subplot(211)
        ax.scatter(ml[model_test_index], mb[model_test_index],color='blue',s=30)
        ax.set_title('MODEL')
        ax_ = fig.add_subplot(212)
        ax_.scatter(dl[data_test_index], db[data_test_index], color='red', s=30)
        ax_.set_title('DATA')
        plt.show()

        # ks-test
        print('** number of stars **')
        print('real:',len(data_test_index),'model:',len(model_test_index))
        model_histogram = np.histogram(mb[model_test_index], bins=21, density='True') 
        data_histogram  = np.histogram(db[data_test_index],  bins=21, density='True')
        p_value = stats.ks_2samp(model_histogram[0], data_histogram[0]).pvalue
        return p_value


class LifeTime:

    def __init__(self, m, n, dT, span):
        self.m    = m
        self.n    = n
        self.dT   = dT
        self.span = span
        self.x    = np.arange(dT, span, 0.1) # year
        self.probability = comb(n,m) * (((dT/self.x)**m)*((1-(dT/self.x))**(n-m)))
        for m_ in range(self.m):
            if m_ == 0:
                probability =  comb(self.n,m_) *(((self.dT/self.x)**m_)*((1-(self.dT/self.x))**(n-m_)))
            else:
                probability +=  comb(self.n,m_) *(((self.dT/self.x)**m_)*((1-(self.dT/self.x))**(n-m_)))
        self.Qmn = 1 - probability

    def lifetime(self):
        x_at_probability_max = self.x[np.where(self.probability == self.probability.max())]
        return x_at_probability_max[0]

    def upper_limit(self):
        sigma3 = np.where(self.Qmn>0.003)[0][-1]
        sigma2 = np.where(self.Qmn>0.046)[0][-1]
        sigma1 = np.where(self.Qmn>0.318)[0][-1]
        return [self.x[sigma1], self.x[sigma2], self.x[sigma3]]
 
    def visualize(self, xscale, plot_type): # plot_type = 'lifetime' or 'upper_limit'
        fig = plt.figure(figsize=(5,5))
        ax = fig.add_subplot(111)
        if plot_type == 'lifetime':
            ax.plot(self.x, self.probability, label='m='+str(self.m),color='black')
        if plot_type == 'upper_limit':
            ax.plot(self.x, self.Qmn, label='m='+str(self.m), color='black')
        ax.set_xlabel('lifetime [yr]')
        ax.set_ylabel('Probability')
        plt.xscale(xscale)
        plt.legend()
        plt.show()
        return

def test_scaleheight():
    number          = 3990
    kinematic_dist  = 'near'
    dist_func       = {'scale_length':22,'scale_height':0.15} # kpc
    gc              = 4
    region          = [{'l':[-28, -gc], 'b':[-1.25, 1.25]},{'l':[gc, 10], 'b':[-1.25,1.25]},{'l':[14.35, 67.25], 'b':[-1.25, 1.25]}] # statistics region without GC
    path_to_data    = '/Users/astroimo/Desktop/research/ohir/experiments/data/stat.npy' 
    data            = np.load(path_to_data)
    data_lb         = np.array([[float(i) for i in data[1]],[float(i) for i in data[2]]])
    detection_limit = 0.122 # Jy 
    sh              = ScaleHeight()
    model_xyz, model_lb, mflux = sh.model(dist_func, number, kinematic_dist)
    sh.visualize(model_xyz, mflux)
    sh.visualize(model_lb, mflux)
    p_value      = sh.pvalue(data_lb, model_lb, mflux, detection_limit, region)
    print('p_value:', format(p_value,'.3f')) 
    return


def test_lifetime():
    m     = 30
    n     = 445
    dT    = 20
    span  = 1000
    xscale = 'linear' # 'log' *alternatively
    plot_type = 'lifetime' # 'lifetime' or 'upper_limit'
    lt = LifeTime(m,n,dT,span)
    print('The most plausible lifetime is:',format(lt.lifetime(),'.1f'),'year')
    print('The upper limits are:', [format(limit,'.1f')+' ('+str(i+1)+'sigma)' for i,limit in enumerate(lt.upper_limit())], 'yr')
    lt.visualize(xscale,plot_type)
    return

if __name__ == '__main__':
    test_lifetime()
    #test_scaleheight()
