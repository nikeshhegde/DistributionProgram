import sys
import random as rnd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

#select the distribution method
def myRNG(outputPrefix, n, seed, distribution, par1, par2):
    try:
        rnd.seed(seed)
        print()
        dist = {"kumaraswamy":"kumaraswamy", "logarithmic":"logarithmic"}
        dist_type =  dist.get(distribution.lower(), "No Such Distribution Available")
        if dist_type == "logarithmic":
            logarithmic(par1,n,outputPrefix)
        elif dist_type == "kumaraswamy":
        	kumaraswamy(par1, par2, n, outputPrefix)
        else:
            print("No Function as such is Found!")
    except:
        print(sys.exc_info())

#Write values to txt file
def write_to_txt(r, c, out):
    try:
        f = open('%s_rv.txt' %out,'w')
        for i in r:
            f.write(str(i)+'\n')
        f.close()
        f = open('%s_cdf.txt' %out,'w')
        for j in c:
            f.write(str(j)+'\n')
        f.close()
    except:
        print(sys.exc_info())

#Export diagram to pdf
def plot_to_file(x, y, out,distributionType):
	try:
		n_bins = 10
		with PdfPages('%s_cdf.pdf' % distributionType) as pdf:
			fig, ax = plt.subplots(figsize=(8,5))
			if distributionType == 'Kumaraswamy':
				ax.hist(x, n_bins, histtype='step',density=True,cumulative=True, label='Empirical')
				ax.plot(x, np.array(y) , 'k--', linewidth=1, label='Theoretical')
				ax.set_xlim(xmin=0 ,xmax=1)
				ax.text(0.8, 0.2, "p1: "+ sys.argv[5], color='green')
				ax.text(0.8, 0.1, "p2: "+ sys.argv[6], color='green')
			elif distributionType == 'Logarithmic':
				ax.hist(y, n_bins, histtype='step',density=True,cumulative=True, label='Empirical')
				ax.plot(x, y , 'k--', linewidth=1, label='Theoretical')
				ax.set_xlim(xmin=0 ,xmax=5)
				ax.text(4, 0.1, "p1: "+ sys.argv[5], color='green')
			ax.set_title('Cumulative step histograms')
			ax.set_xlabel('Random Numbers')
			ax.set_ylabel('Cumulative Distribution function' )
			ax.legend(loc='upper left')
			pdf.savefig(fig)

			fig, ax = plt.subplots(figsize=(8, 5))
			box_plot_data=[y]
			ax.boxplot(box_plot_data,patch_artist=True,labels=['Random Numbers'])
			ax.set_title('Box Plot')
			pdf.savefig(fig)
	except:
		print(sys.exc_info())

def uniform(a, b):
	try:
		return a + (b-a) * rnd.random()
	except:
		print(sys.exc_info())

#Kumaraswamy Distribution
def kumaraswamy(a,b,n,out):
	try:
		kum_rv = np.random.random(n)
		kum_rv.sort()
		cdf_kum = []
		inverse_cdf = []
		#for i in range(1,n+1):
		#	uni = rnd.random()
		#	kum_rv.append(uni)
		for i in range(len(kum_rv)):
			cdf_kum.append(1 - pow( (1 - pow(kum_rv[i] , a)) , b))
		plot_to_file(kum_rv,cdf_kum, out,'Kumaraswamy')
		write_to_txt(kum_rv,cdf_kum, out)
		#Inverse kumaraswamy cdf function
		for i in range(len(kum_rv)):
			inverse_cdf.append(np.power(1 - np.power( (1- cdf_kum[i]) , 1/b) , 1/a))
		#print("Inverse Values for Kumaraswamy Distribution are: ")
		#print(inverse_cdf)
	except:
		print(sys.exc_info())

#Logarithmic CDF Function
def logarithmic(p,n,out):
	try:
		log_pmf = []
		#log_rv = [1,2,3,4,5]
		log_rv = np.random.randint(1,5,n)
		log_rv.sort()
		for i in range(len(log_rv)):
			log_pmf.append((-1 * (p**log_rv[i])) / (np.log(1-p) * log_rv[i]))
		log_cdf = np.cumsum(log_pmf,dtype=float)
		log_cdf/=log_cdf[-1]
		#print("CDF Values for Logarithmic distribution are: ")
		#print(log_cdf)
		plot_to_file(log_rv,log_cdf, out,'Logarithmic')
		write_to_txt(log_rv,log_cdf, out)
	except:
		print(sys.exc_info())

if __name__ == "__main__":
    a = str(sys.argv[1])
    b = int(sys.argv[2])
    c = int(sys.argv[3])
    d = str(sys.argv[4]).lower()
    e = float(sys.argv[5])
    if len(sys.argv) > 6:
        f = float(sys.argv[6])
    else:
        f = "Not Found"
    if d == 'kumaraswamy':
    	if e <= 0 or f <= 0:
    		print("Please enter non-negative value")
    	else:
    		myRNG(a, b, c, d, e, f)
    elif d == 'logarithmic':
    	if e >= 1 or e <=0:
    		print("Please enter values between 0 and 1")
    	else:
    		myRNG(a, b, c, d, e, f)
    