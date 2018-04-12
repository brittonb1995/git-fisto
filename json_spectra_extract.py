"""
----
READ
----

-This code will open a user downloaded json file from the Open Supernova Archive and parse
spectral data. 
-This code extracts the wavelength, flux, epoch, and sources data and saves the spectral
data to an npz file (special numpy data file), and the sources to an accompanying .dat for references.
-External libraries needed to run: json, numpy

Author: Britton Beeny 


"""


import json
import numpy as np

print "Make sure you're in the right directory before running!"
print ""



class File_Open:

    def json_open(self):
        f = open(self.filename,'r')
        self.json = json.load(f)
        f.close()
        return self.json

    def __init__(self,SNname):
        self.filename = SNname + ".json"
        self.SNname = SNname
        self.json_open


class Get_Data(File_Open):

    def __init__(self,SNname):
        File_Open.__init__(self,SNname)
        File_Open.json_open(self)
        self.info = self.json[self.SNname]['spectra']
        self.ref_info = self.json[self.SNname]['sources']
        self.totalspec = len(self.info)
        self.totalref = len(self.ref_info)
        
    def get_WL(self):
        WL_list = []
        for spectra in range(self.totalspec):
            data = self.info[spectra]['data']
            interiorwlarray = np.zeros(len(data))
            for x in range(len(data)):
                interiorwlarray[x] = data[x][0]
            WL_list.append(interiorwlarray)

        return WL_list


    def get_FLX(self):
        fluxlist = []
        for spectra in range(self.totalspec):
            data = self.info[spectra]['data']
            interiorflarray = np.zeros(len(data))
            for x in range(len(data)):
                interiorflarray[x] = data[x][1]
            fluxlist.append(interiorflarray)
        return fluxlist

    def get_time(self):
        epoch_list = []
        for spectra in range(self.totalspec):
            Times = self.info[spectra]['time']
            epoch_list.append(float(Times))
        return epoch_list
        

    def get_sources(self):
        spectra_source = []
        ref_list = []
        Sources = self.ref_info
        
        for spectra in range(self.totalspec):
            Source = self.info[spectra]['source']
            spectra_source.append(str(Source))

        for ref in range(self.totalref):
            try:
                ref_list.append(str(Sources[ref]['reference']))
            except:
                pass
        return ref_list
    
class Save:

	def save(self):
		src_filename = self.SNname + "_spec_src.dat"
		src_f = open(src_filename,"w")
		src_f.write("#Sources\n")
		for source in self.source_data:
			src_f.write("%s\n" % (source))
		src_f.close()

		savefile = self.SNname + "_spec"
		np.savez(savefile,wave_data=self.wave_data,flux_data=self.flux_data,epoch_data=self.epoch_data)

	def __init__(self,SNname,wave_data,flux_data,epoch_data,source_data):
		self.SNname = SNname
		self.wave_data = wave_data
		self.flux_data = flux_data
		self.epoch_data = epoch_data
		self.source_data = source_data

##Instantiate the classes into objects

Query = raw_input("Enter SN name: ")#<----User inputted query
File = File_Open(Query)#<----Instantiate the File_Open class into a File object
Name = File.SNname#<----Renaming by calling an object's attribute
WL = Get_Data(Name).get_WL()#<----Calling Get_Data's get_WL method
FLX = Get_Data(Name).get_FLX()#<----same
T = Get_Data(Name).get_time()#<----same
src = Get_Data(Name).get_sources()#<----same
Save(Name,WL,FLX,T,src).save()#<----Save to csv, .dat files


