
import math
class TOA:
    def __init__(self, EAI=None,RadScale=None):
        '''
        Class to caluclate TOA
        '''
        self.EAI = EAI
        self.RadScale=RadScale

#    EAI = [1997.8,1863.5,1560.4,1395.0,1124.4] #Exo Atmospheric Irradiance (EAI) as defined by RapidEye AG

    @classmethod
    def TOARad(cls,RadScaleFact,img):
        RadImag = RadScaleFactact*img
        return RadImage

    @classmethod
    def TOARefl(cls,EarthSunDist,SunZenith,EAI):
        ToaRefl = toa_rad*(math.pi*math.pow(EarthSunDist,2))/(EAI*math.cos(SunZenith))
        return ToaRefl

    @classmethod
    def SunZenith(cls,SunElev):
        SunZenith=(90-SunElev)*(math.pi/180)
        return SunZenith

    @classmethod
    def EarthSunDist(cls,doy):
        EsDist=1-0.016729*math.pow(math.cos((0.9856*(doy-4))*(math.pi/180)),2) #As defined here http://cwcaribbean.aoml.noaa.gov/bilko/module7/lesson3/
        print "Earth Sun distance:%f"%(EsDist)
