import os.path
import csv
import numpy
from matplotlib import pyplot as plt 
#

#datafile=open("college-data.csv",'r')



#Read from college earnings data
with open('college-data-2.csv','rb') as f:
    
    reader = csv.reader(f)
    college_list = list(reader)



rows= len(college_list)
cols= len(college_list[0])


#Read from college data
with open('college-data-elem.csv','rb') as g:
    reader_elem = csv.reader(g)
    college_elem = list(reader_elem)





mean_vals=[]



# Calculate the mean earnings 8 years after graduation of California Colleges
for i in range(1,rows):
   # print college_list[i][3]  #NAME
    mean = college_list[i][43]
    if mean!= "NULL" and mean!="PrivacySuppressed":
        mean_vals.append(int(mean))

               
my_hist, bins=numpy.histogram(mean_vals,10)

width = 1 * (bins[1] - bins[0])
center = (bins[:-1] + bins[1:]) / 2
plt.bar(center, my_hist, align='center', width=width)
plt.title('Mean earnings 8 years after graduation \nof California College Graduates')
plt.xlabel('Earnings in $')
plt.ylabel('Number of colleges')
plt.show()


#plt.bar(bin_edges[:-1], my_hist, width = 1)
#plt.xlim(min(bin_edges), max(bin_edges))
#plt.show()  
