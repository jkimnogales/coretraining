import os.path
import csv
import numpy
from matplotlib import pyplot as plt 
import math




###########################################################################
#  THIS IS FOR INTERACTIVE CLICK
###########################################################################

class AnnoteFinder(object):
    """callback for matplotlib to display an annotation when points are
    clicked on.  The point which is closest to the click and within
    xtol and ytol is identified.
    
    Register this function like this:
    
    scatter(xdata, ydata)
    af = AnnoteFinder(xdata, ydata, annotes)
    connect('button_press_event', af)
    """

    def __init__(self, xdata, ydata, annotes, ax=None, xtol=None, ytol=None):

        
        self.data = list(zip(xdata, ydata, annotes))
        if xtol is None:
            xtol = ((max(xdata) - min(xdata))/float(len(xdata)))/0.2
        if ytol is None:
            ytol = ((max(ydata) - min(ydata))/float(len(ydata)))/0.2
        self.xtol = xtol
        self.ytol = ytol
        if ax is None:
            self.ax = plt.gca()
        else:
            self.ax = ax
        self.drawnAnnotations = {}
        self.links = []

    def distance(self, x1, x2, y1, y2):
        """
        return the distance between two points
        """
       
        return(math.sqrt((x1 - x2)**2 + (y1 - y2)**2))
        

    def __call__(self, event):

        if event.inaxes:

            clickX = event.xdata
            clickY = event.ydata
            if (self.ax is None) or (self.ax is event.inaxes):
                annotes = []
                # print(event.xdata, event.ydata)
                for x, y, a in self.data:
                    # print(x, y, a)
                    if ((clickX-self.xtol < x < clickX+self.xtol) and
                            (clickY-self.ytol < y < clickY+self.ytol)):
                        annotes.append(
                            (self.distance(x, clickX, y, clickY), x, y, a))
                if annotes:
                    annotes.sort()
                    distance, x, y, annote = annotes[0]
                    self.drawAnnote(event.inaxes, x, y, annote)
                    for l in self.links:
                        l.drawSpecificAnnote(annote)

    def drawAnnote(self, ax, x, y, annote):
        """
        Draw the annotation on the plot
        """
        if (x, y) in self.drawnAnnotations:
            markers = self.drawnAnnotations[(x, y)]
            for m in markers:
                m.set_visible(not m.get_visible())
            self.ax.figure.canvas.draw_idle()
        else:
            t = ax.text(x, y, " - %s" % (annote),)
            m = ax.scatter([x], [y], marker='d', c='r', zorder=100)
            self.drawnAnnotations[(x, y)] = (t, m)
            self.ax.figure.canvas.draw_idle()

    def drawSpecificAnnote(self, annote):
        annotesToDraw = [(x, y, a) for x, y, a in self.data if a == annote]
        for x, y, a in annotesToDraw:
            self.drawAnnote(self.ax, x, y, a)


############################################################################################
# END OF INTERACTIVE CLICK PARK
############################################################################################



print "Make sure you are in the correct directory!"

# This program looks at two databases.  First one contains school information such as 
# tuition, SAT scores etc etc

# The second contains treasurey department reported mean income of alumni 8 years after graduation
# (amonste other things)

# The two tables are joined over the unique ID




# ####################################################################################
# DO NOT CHANGE THESE NUMBERS
# There are a few constants below this section that you can alter
# ######################################################################################

#CONSTANTS COLUMNS in Most-Recent-Cohorts-Scorecard-Elements.csv
elem_unit_id=0   # COLUMN for unique ID
elem_instnm=3    # Column for name of school
elem_sttabbr=5    #column for state of the school
elem_npt4_pub=96  #column for public school tuition
elem_npt4_priv=97 #column for private school tuition


# Most-Recent-Cohorts-Treasury-Elements.csv
MN_EARN_WNE_P10=19 # Mean earnings after 10 years
MD_EARN_WNE_P10=20 # Median earnings after 10 years



MN_init_id=0       # THE ID




##################################################################################################
#CHANGE the variables below to determine how the program reacts.  I should turn this into a menu
# system


#####################################################################
#   CHOose up to 3 states to compare.  If you add too many, your graph gets complicate
#####################################################################

STATE1='CA'     
STATE2='MA'
STATE3=''

# We will look at median earnings 10 years after graduation
EARNING_SELECT=MD_EARN_WNE_P10

# We will look at mean earnings of graduates 10 years after graduation
#EARNING_SELECT=MN_EARN_WNE_P10

########################################################################################




#################################################################
# PROGRAM Starts below


#Read from college earnings data - comes from treasury
with open('Most-Recent-Cohorts-Treasury-Elements.csv','r') as f:
    
    reader = csv.reader(f)
    college_list = list(reader)



#Read from college data
with open('Most-Recent-Cohorts-Scorecard-Elements.csv','r') as g:
    reader_elem = csv.reader(g)
    college_elem = list(reader_elem)




# I had to seperate these into public vs. private because I need to use two
# columns to differentiate the colors on the graph
# Only use circles as markers.  Any other symbol seems to confuse the
# onclick behavior
                            #ID
name_pub=[]                # name of institution              
tuition_pub=[]             #tuition
earnings_pub=[]            #mean earnings 8 years after graduation          


name_priv=[]
tuition_priv=[]
earnings_priv=[]


# Go through each row of the college data set.
for coll in college_elem:
    
    #What state is this college in?
    instate=coll[elem_sttabbr]
    
    
    #FILTER OUT UP TO 3 STATES
    if instate==STATE1 or instate==STATE2 or instate==STATE3:
        
        # Get the id for DB "join"
        id=coll[elem_unit_id]
        
        # name of the institution
        name=coll[elem_instnm]
        
        
        #cost of attendance.  Public school in one column, private school in another.  Nice (not)
        tuition_pub_l=coll[elem_npt4_pub]
        tuition_priv_l=coll[elem_npt4_priv]
        
        
        # Thisis where we do a DB "Join" to get the 10 year earnings for this college
        # We have the option of getting mean or midian.  Select from the section above.
        # EARNING_SELECT will determine which we do.
        

        
        # Go through each id in the second DB (Treasury data) and look for the row containing
        # the same college id.
        # I bet we can use the row number for the join, but I am using a for loop just in case
        # the college data are not in the same row.
        for coll_finance in college_list:
            

            # Found our match.  Get the earnings data.  Note EARNING_SELECT
            if coll_finance[MN_init_id]==id:
                earnings=coll_finance[EARNING_SELECT]


# Many schools hide their data with a "NULL" or "PrivacySuppressed" entry in the column.
# Can't really use these.
# If colleges have a tuition and an earnings report, add it to the list.
# We should get a tuition-earnings-name triple for private and public colleges
        if earnings!="PrivacySuppressed" and earnings!="NULL":
            
            # We have data in the public tuition column.  So place tuition, earning, name in
            # public university data.
            if (tuition_pub_l!="NULL"):
                name_pub.append(name)
                tuition_pub.append(int(tuition_pub_l))
                earnings_pub.append( int(earnings))
                
            # La meme chose.  But for private.
            elif (tuition_priv_l!="NULL"):
                name_priv.append(name)
                tuition_priv.append(int(tuition_priv_l)) 
                earnings_priv.append( int(earnings))
       


# I have no idea how this works.  It was provided in the onclick command.

fig, ax=plt.subplots()

# I lied.  I know how this works.  Public get color='r', private get color='b'.  
# If you change the marker from the default 'o', the onclick command to get the name
#will not work.
ax.scatter(tuition_pub,earnings_pub, color='r')
ax.scatter(tuition_priv,earnings_priv,color='b')
plt.xlabel('Title IV Average Cost of attendance (NOT TUITION) $ ')

if EARNING_SELECT==MD_EARN_WNE_P10:
    plt.ylabel('10 year median earnings')
else:
    plt.ylabel(' 10 year mean earnings')
    

# Send the (x,y) data points and the name to appear to the onclick() routine.
# Remember to combine the public and private schools because as far as the
# function is concerned, they are just one array of points.
af =  AnnoteFinder(tuition_pub+tuition_priv,earnings_pub+earnings_priv, name_pub+name_priv, ax=ax)
fig.canvas.mpl_connect('button_press_event', af)

#WHEW.
plt.show()




