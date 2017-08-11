# -*- encoding: utf-8 -*-
#
#  anasysdoc.py
#
#  Copyright 2017 Cody Schindler <cschindler@anasysinstruments.com>
#
#  This program is the property of Anasys Instruments, and may not be
#  redistributed or modified without explict permission of the author.

import anasysfile
import heightmap
import irspectra

class AnasysDoc(anasysfile.AnasysFile):
    """Object for holding document data in a file generated by Analysis Studio"""
    def __init__(self, ftree):
        self._special_tags = {'HeightMaps': self._get_height_maps,
                              'RenderedSpectra':self._get_rendered_spectra,
                              'SpectraChannelViews': {}}
        anasysfile.AnasysFile.__init__(self, ftree)
        # self.RenderedSpectra = self._get_rendered_spectra(ftree.find('RenderedSpectra'))

    def _get_rendered_spectra(self, spectra):
        """Returns a list of IRRenderedSpectra"""
        spectradict = {}
        for spectrum in spectra:
            #Mangle etree so DataChannels get stuck in a parent 'DataChannels' element
            #FIXME Not Working
            spectrum.makeelement('temp', {})
            print(list(spectrum))
            spectrum.find('temp').extend(spectrum.findall('DataChannels'))
            for dc in spectrum.findall('DataChannels'):
                spectrum.remove(dc)
            spectrum.makeelement('DataChannels', {})
            spectrum.find('DataChannels').extend(temp.findall('DataChannels'))
            spectrum.remove(spectrum.find('temp'))
            #End mangling
            self._attr_to_children(spectrum)
            key = spectrum.find('Label').text
            key = self._check_key(key, spectradict)
            spectradict[key] = irspectra.IRRenderedSpectra(spectrum)
        return spectradict

    def _get_height_maps(self, maps):
        """Takes an iterable of Height Maps, and returns a dict of HeightMap objects"""
        mapdict = {}
        for _map in maps:
            self._attr_to_children(_map)
            key = _map.find('Label').text
            key = self._check_key(key, mapdict)
            mapdict[key] = heightmap.HeightMap(_map)
        return mapdict