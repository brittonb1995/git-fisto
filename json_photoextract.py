'''
-------
READ!!!
-------
This program allows for a user to extract Supernovae Photometry data from a complicated and long JSON file
This program features python methods, python classes and class inheritance
The user can then save the data into individually named .dat files in a newly created directory

JSON files are downloaded via the Open Supernovae Archive website https://sne.space/
Please cite the following paper if data from OSA was useful to you: [2017ApJ...835...64G] <--Bib code

Author: Britton Beeny
Email: brittonb1995@tamu.edu
'''
import json
import numpy as np
import os

filters = ['W1','W2','M2','U','B','V','R','I','J','H','K'] #any filter that exists can be added to this list

#-----For saving purposes-----------------------
def Make_dir(dir_name):
    current = os.getcwd()
    new_dir = current + '/' + dir_name
    os.mkdir(new_dir)
    return current,new_dir

def cd(Dir): #Might be superfluous, but eh
    os.chdir(Dir)

def length_match(mags,errs): #Sometimes, magnitude errors arent present for a given datapoint
    len1 = len(mags)         #Match the two lists in length
    len2 = len(errs)
    if len1 != len2:
        diff = len1-len2
        while diff > 0:
            errs.append(0.0) #<------Change this to add any value onto the end of mag errs list
            diff -= 1
    elif len1==len2:
        pass
#-----------------------------------------------
__metaclass__=type #<----Needed for class inheritance for Python 2.X

class FileOpen: #<-----Opens the .json file when instance is created
    
    def __init__(self, SNname):
        self.filename = SNname + ".json"
        self.SNname = SNname
        
    def json_open(self):
        self.f = open(self.filename,'r')
        self.json = json.load(self.f)
        self.f.close()
        return self.json

class Get_Index(FileOpen): #<-----Get_Index "inherits" the code from FileOpen
    
    def __init__(self,SNname,filterlist):
        super(Get_Index,self).__init__(SNname)
        super(Get_Index,self).json_open()
        self.filterlist = filterlist
        self.info = self.json[self.SNname]['photometry']
        
    def get_idx(self):
        total = len(self.info)
        all_idx = []
        for f in range(len(self.filterlist)):
            indexlist = []
            for x in range(total):
                try:
                    if(self.info[x]['band'] == self.filterlist[f])&('model' not in self.info[x]):
                        indexlist.append(x)
                except:
                    pass
            if len(indexlist) > 0:
                all_idx.append(indexlist)
        return all_idx

class Photo_Extract(Get_Index): #<-----This class "inherits" code from Get_index to be able to use get_idx()

    def __init__(self,SNname,filterlist):
        super(Photo_Extract,self).__init__(SNname,filterlist)
        self.idx = super(Photo_Extract,self).get_idx()
        
    def get_mags(self):
        allmags = {}       
        for f in range(len(self.idx)):
            maglist = []
            for i in self.idx[f]:
                maglist.append(float(self.info[i]['magnitude']))
            if len(maglist) > 0:
                allmags[self.filterlist[f]] = maglist

        return allmags

    def get_mag_errs(self):
        allmagerrs = {}
        for f in range(len(self.idx)):        
            magerr = []
            for i in self.idx[f]:
                if 'e_magnitude' in self.info[i]:
                    magerr.append(float(self.info[i]['e_magnitude']))
    
            if len(magerr) > 0:
                allmagerrs[self.filterlist[f]] = magerr
        return allmagerrs

    def get_time_data(self):
        alltimelist = {}
        for f in range(len(self.idx)):
            timelist = []
            for index in self.idx[f]:
                timelist.append(float(self.info[index]['time']))
            if len(timelist) > 0:
                alltimelist[self.filterlist[f]]=timelist
        return alltimelist
    
class Save: #<-----Saves the data into individual .dat files when called as an instance

    def __init__(self,snname,mags,errs,mjd):
        self.snname = snname
        self.mags = mags
        self.errs = errs
        self.mjd = mjd

    def save(self):

        current,new = Make_dir(self.snname)#<----Makes a new directory to save .dat files in. Can be commented out
        cd(new)#<----Changes into newly made directory. If above line is commented out, must comment out this line
        for key in range(len(self.mags)):
            length_match(self.mags.values()[key],self.errs.values()[key])
            savefile = '%s_phot_%s.dat' % (self.snname,self.mags.keys()[key])
            f = open(savefile,'w')
            f.write('#Magnitude    Error    MJD\n')
            for x in range(0,len(self.mags.values()[key])):
                line = str(self.mags.values()[key][x])+'  '+str(self.errs.values()[key][x])+'  '+str(self.mjd.values()[key][x])
                f.write(line+'\n')
            f.close()
        cd(current) #<----Changes back into original directory when done. If cd(new) commented out, must comment out this line

Object = raw_input("Enter Supernovae Name: ")#<-----User-inputted supernova name
File = FileOpen(Object) #<-----Creates an instance from FileOpen. Able to access variables within FileOpen.__init__()
Name = File.SNname #<-----Accesses SNname from FileOpen.__init__()
Mags = Photo_Extract(Name,filters).get_mags() #<-----Calls Photo_Extract in order to run get_mags()
Mag_errs = Photo_Extract(Name,filters).get_mag_errs()#<----Same, but for get_mag_errs()
MJD = Photo_Extract(Name,filters).get_time_data()#<-----Same for getting time data
Save(Name,Mags,Mag_errs,MJD).save()#<-----Saves
print "All done!"

            
