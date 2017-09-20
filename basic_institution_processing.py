#This code simply documents the limited processing I've subjected the insitution data to


processedauthorinst = {}

for a in authorinstdict:
    processedaffs = []
    for i in authorinstdict[a]:
        name = i
        
        # removing punctuation
        name = name.lower()
        name = name.replace(","," ")
        name = name.replace("." , "")
        name = name.replace("&" , " and ")
        name = name.replace('\"', "")
        name = name.replace('\'', "")
        name = name.replace('\\', " ")
        name = name.replace('\/', " ")
        name = name.replace('(',' ')
        name = name.replace(')',' ')
        name = name.replace('[',' ')
        name = name.replace(']',' ')
        name = name.replace('{',' ')
        name = name.replace('}',' ')
        name = name.replace("  "," ")
        name = name.replace("  "," ")
        name = name.replace("  "," ")
        name = name.replace("  "," ")
        name = name.replace("  "," ")
        name = name.replace("  "," ")
        
        # the following are issues identified using the list of the top ~560 institutions
        name = name.replace('london school of economics','london school of econ')
        name = name.replace('va polytechnic institute & state u','va polytechnic institute')
        name = name.replace('va polytechnic institute and state u','va polytechnic institute')
        name = name.replace('international monetary fund','imf')
        name = name.replace('bar-ilan u','bar ilan u')
        name = name.replace('birkbeck college u london','birkbeck college')
        name = name.replace('international food policy research institute','ifpri')
        name = name.replace('london school of econ and political science','london school of econ')
        name = name.replace('norwegian school of economics','norwegian school of econ')
        name = name.replace('norwegian school of econ & business administration','norwegian school of econ')
        name = name.replace('norwegian school of management','norwegian school of econ')
        name = name.replace('rand corporation','rand')
        name = name.replace('stockholm school of economics','stockholm school of econ')
        name = name.replace('tel-aviv u','tel aviv u')
        name = name.replace('u carlos iii de madrid','u carlos iii madrid')
        name = name.replace('u e anglia','u east anglia')
        name = name.replace('u new s wales','u new south wales')
        name = name.replace('us bureau of labor statistics', 'us bls')
        name = name.replace('us department of agriculture', 'usda')
        name = name.replace('aarhus school of business','aarhus u')
        name = name.replace('catholic u leuven','catholic u louvain')
        name = name.replace('cesifo munich','cesifo')
        name = name.replace('erasmus u rotterdam','erasmus u')
        name = name.replace('european u institute florence','european u institute')
        name = name.replace('hebrew u jerusalem','hebrew u')
        name = name.replace('hoover institution','hoover institution stanford u')
        name = name.replace('hoover institution stanford u stanford u','hoover institution stanford u')
        name = name.replace('institute for fiscal studies london','institute for fiscal studies')
        name = name.replace('ifs','institute for fiscal studies')
        name = name.replace('iza bonn','iza')
        name = name.replace('new school for social research','new school u')
        name = name.replace('queen s u kingston ontario','queen s u kingston')
        name = name.replace('u paris i pantheon-sorbonne','u paris i')
        name = name.replace('eurequa u paris i','u paris i')
        name = name.replace('u southern ca los angeles','u southern ca')
        name = name.replace('u toulouse i','u toulouse')
        name = name.replace('washington u in st louis','washington u')
        name = name.replace('gremaq','u toulouse')
        name = name.replace('ifpri washington dc','ifpri')
        name = name.strip()
        
        # there are three ways that different journals indicate missing affiliations
        if name == 'missing':
            name = ''
        elif name == 'unlisted':
            name = ''
        processedaffs.append(name)
    processedauthorinst[a] = processedaffs