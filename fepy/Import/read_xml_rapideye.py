__author__ = 'pmagdon'

from datetime import *
from lxml import etree


class MetaData(object):
    """ A generic class for storing the remote sensing metadata information"""
    __version__ = "0.0.1"
    def __init__(self):
        self.orderID = None
        self.ProductVersion = None
        self.ProductType = None
        self.Acquisitiondate = None
        self.Day = None
        self.Month = None
        self.GmtDecimalHour = None
        self.DayOfYear = None
        self.SunElevation = None
        self.SunZenith = None
        self.SensorZenith = None
        self.SensorAzimuth = None
        self.RadianceScaleFactor = None
        self.CenterLatidue=None
        self.CenterLongitude=None
        # self.date = datetime.date(self.year, self.month, self.day)
        # self.day_of_year = self.date.timetuple().tm_yday

    def __str__(self):
        return ('Order ID: %s' % self.orderID + '\n'
                'Standard Product Version: %s' % self.ProductVersion + '\n'
                'Product Type: %s' % self.ProductType + '\n'
                'Acquisition Date: %s' % self.Acquisitiondate + '\n'
                'Day %s' %self.Day +'\n'
                'Month %s' %self.Month +'\n'
                'GMT Decimal Hour %s' %self.GmtDecimalHour +'\n'
                'Day of Year: %s' % self.DayOfYear + '\n'
                'Sun Elevation: %s' % self.SunElevation + '\n'
                'Sun Zenith: %s' % self.SunZenith + '\n'
                'Radiance Scale Factor: %s' % self.RadianceScaleFactor +'\n'
                'Center Latitude: %s' %self.CenterLatidue +'\n'
                'Center Longitude: %s' %self.CenterLongitude )


class MetaDataRapidEye:
    """ A class for importing and storing RapidEye Metadata"""

    @classmethod
    def import_rapideye_metadata(cls, o, filename):
        """ Imports Metadata from Rapideye metadata XML File"""
        try:
            import lxml
        except:
            raise ImportError("Can not find module lxml")
        try:
            tree = etree.parse(filename)
        except:
            raise ImportError("Metadata file", "Error reading RapidEye MetaDataFile - does it exist and contain data?")
        root = tree.getroot()
        o.ProductVersion = root.attrib['re_standard_product_version']
        AcceptedVersions = ['1.0', '3.0', '4.0']
        if o.ProductVersion in AcceptedVersions:
            o.orderID = root.find('.//re:orderId', root.nsmap).text
            o.ProductType = root.find('.//eop:productType', root.nsmap).text
            o.Acquisitiondate = datetime.strptime(root.find('.//eop:acquisitionDate', root.nsmap).text,'%Y-%m-%dT%H:%M:%S.%fZ')
            o.Day=o.Acquisitiondate.day
            o.Month=o.Acquisitiondate.month
            o.DayOfYear = o.Acquisitiondate.timetuple().tm_yday
            o.SunElevation = float(root.find('.//opt:illuminationElevationAngle', root.nsmap).text)
            o.SunZenith = 90 - o.SunElevation
            o.SensorAzimuth = float(root.find('.//re:azimuthAngle', root.nsmap).text)
            o.SensorZenith = float(root.find('.//re:spaceCraftViewAngle', root.nsmap).text)
            o.RadianceScaleFactor = float(root.find('.//re:radiometricScaleFactor', root.nsmap).text)
            o.CenterLatidue=float(str.split(root.find('.//gml:pos',root.nsmap).text)[0])
            o.CenterLongitude=float(str.split(root.find('.//gml:pos',root.nsmap).text)[1])
        else:
            raise StandardError("Standard Product Version %s is currently not supported by FEP" % o.ProductVersion)

# Adding this allows to run the code as module as well as a script
if __name__ == "__main__":
    import sys
    import os
    filename = os.path.normpath(str(sys.argv[1]))
    metadata = MetaData()
    MetaDataRapidEye.import_rapideye_metadata(metadata ,filename)
    print metadata


