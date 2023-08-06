"""Read funktion: OSM Data (pipelines) into K_Net Class"""

#######################################################################
#All functions are called from the makefile                           #
#######################################################################

from . M_PlotObjects            import routelength
#from Code.OSM.M_OSM_CreateElements import M_OSM_CreateElements
from . import OSM_Pipeline_CountryCode as OP


from unidecode                     import unidecode
#import configparser
#from  configparser import  ExtendedInterpolation
#from  pathlib            import Path
#import os
#import time

import json
#import Code.C_colors              as CC
from . import K_Netze               as K_Netze
from . import K_Component           as KC

def PipeLines2Nodes(Pipelines):
    lat_list=[]
    long_list=[]
    id_list=[]
    for pipe in Pipelines:
        for entry in zip(pipe.lat,pipe.long,pipe.node_id):
            lat_list.append(entry[0])
            long_list.append(entry[1])
            id_list.append(entry[2])
    return lat_list,long_list,id_list



def OSMways2net(elements,data,min_length=0):

    ''' Convert OSMways to plotable lines '''

    refs=[]
    lines=[]
    ids=[]
    lengths=[]
    tags=[]
    tagdicts=[]
    node_ids=[]
    if "Way" in elements.keys():
        node_id_list=[]
        for entry in elements["Way"]:
            refs=elements["Way"][entry]['refs']
            lonlat_array = []
            node_id_list=[]
            for ID in refs:
                lonlat_array.append(data["Node"][str(ID)]['lonlat'])
                node_id_list.append('OSM-'+str(ID))
            node_ids.append(node_id_list)
            long = []
            lat  = []
            line = []

            for coords in lonlat_array:
                long.append(coords[0])
                lat.append(coords[1])
            linelength=float(routelength(long,lat))
            tag = unidecode(json.dumps(elements["Way"][entry]["tags"],ensure_ascii=False,
                          indent=2)).replace('{','').replace('}','').replace('\\"','')
            tagdict=elements["Way"][entry]["tags"]
            line = [long,lat]
            # only lines longer than min_length
            if linelength>=min_length:
                lines.append(line)
                lengths.append(float(linelength))
                ids.append('OSM-'+entry)
                tags.append(tag)
                tagdicts.append(tagdict)
#                node_ids.append(refs)
    return lines, ids, lengths, tags, node_ids, tagdicts

def OSMnodes2net(elements):

    ''' Convert OSMways to plotable lines '''

    nodes=[]
    ids=[]
    tags=[]
    node_ids=[]
    tagdicts=[]

    if "Node" in elements.keys():
        for entry in elements["Node"]:
            idd=elements["Node"][entry]["id"]
            node_ids.append(idd)
            long = elements["Node"][entry]['lonlat'][0]
            lat  = elements["Node"][entry]['lonlat'][1]
            tag = unidecode(json.dumps(elements["Node"][entry]["tags"],
                                       ensure_ascii=False,       indent=2)).replace('{','').replace('}','').replace('\\"','')
            tagdict=elements["Node"][entry]["tags"]
            tagdicts.append(tagdict)
            node = [long,lat]
            nodes.append(node)
            ids.append(entry)
            tags.append(tag)

    return nodes,ids, tags, node_ids,tagdicts


def OSMways2nodes(elements,data,min_length=0):

    '''Convert OSM Pipeline endpoints to Nodes'''

    refs = set()
    if "Way" in elements:
        refs = set(
            ref
            for way_id, entry in elements['Way'].items()
            for ref in entry['refs']
        )

    refs=list(refs)
    new_ids=set('OSM-%s' % ref for ref in refs)
    points = {}

    for point in data['Node']:
        point_id='OSM-%s' % data['Node'][point]['id']
        if point_id in new_ids:
            data['Node'][point]['id']=point_id
            points[point_id] = data['Node'][point]

    return {'Node': points}


def RawData2ClassData(Data,elements,  JSON_outputfile, TM_World_Borders_file,countrycode,
                      CreateCountryCodeForLines=False,
                      LoadCountryCodeForLines=False, min_length=1,segment_length=100,verbose=False):
    from . import M_OSM_PipeSegmenting as PS
    Ret_Data           = K_Netze.NetComp_OSM()

    ########
    #Pipeline
    ########
    print('---Load Pipelines---')
    [lines, ids, lengths, tags, node_ids, tagdicts] = OSMways2net(elements["pipelines"],
                                                                  Data,
                                                                  min_length=min_length)
    # pipenodes_dict=OSMways2nodes(elements["pipelines"],Data,min_length=0)
    i=0
    for i,entry in enumerate(zip(lines,ids,lengths,tags)):
        PipeLine=KC.OSMComponent(id=ids[i],
                                 name=ids[i],
                                 node_id=node_ids[i],
                                 source_id=['OSM'],
                                 lat=lines[i][1],
                                 long=lines[i][0],
                                 country_code=countrycode,
                                 tags=tagdicts[i],
                                 param={'length_km':float(lengths[i])})
                                 # ,                                 length=lengths[i])

        Ret_Data.PipeLines.append(PipeLine)
    
    print('Count:',i+1)

    #here wieder rein
    Ret_Data.PipeLines=PS.OSM_PipelineSegmenting(Ret_Data.PipeLines,length=segment_length,minlength=min_length)
    print('---Load Nodes---')
    pipenodes=OSMways2nodes(elements['pipelines'], Data, min_length=min_length)
    # print(len(pipenodes['Node']))
    # print(pipenodes['Node'])
    [nodes, ids, tags, node_ids,tagdicts]=OSMnodes2net(pipenodes)

    for i,entry in enumerate(zip(nodes, ids, tags, node_ids, tagdicts)):
        Node=KC.OSMComponent(id=ids[i],
                              name=ids[i],
                              node_id=[node_ids[i]],
                              source_id=['OSM'],
                              lat=nodes[i][1],
                              long=nodes[i][0],
                              country_code=countrycode,
                              param={},
                              tags=tagdicts[i])

        Ret_Data.Nodes.append(Node)
    print('Count:',i+1)

    [lats,longs,ids]=PipeLines2Nodes(Ret_Data.PipeLines)

    for i,entry in enumerate(zip(lats,longs,ids)):
        PipePoint=KC.OSMComponent(id=ids[i],
                              name=ids[i],
                              node_id=[],
                              source_id=['OSM_Seq'],
                              lat=lats[i],
                              long=longs[i],
                              country_code=countrycode,
                              param={},
                              tags={})

        Ret_Data.PipePoints.append(PipePoint)

    if CreateCountryCodeForLines==True:
      
       OP.Create_Pipelines_CountryCodes(JSON_outputfile, TM_World_Borders_file,Ret_Data, countrycode,verbose=False)

    if LoadCountryCodeForLines==True:
        print('---Load Line Countrycodes--')
        OP.Load_Pipelines_Countrycodes(JSON_outputfile, Ret_Data, countrycode)

    return Ret_Data

