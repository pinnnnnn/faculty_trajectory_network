from fuzzywuzzy import process

# this was just an affiliation list spit out using the preliminary
#    affiliation processing code
# in our code, we include that processing, so no need to read this in
import pickle
semiproc = pickle.load(open('semi-processed_author_institutions_91_10.pkl'))

# This is added to the preliminary institution processing code
# so it's not needed anymore
#f = open('AffiliationDups.fixed')
#inst_l = []
#for line in f:
#	ls = line.strip()
#	ls = ls.replace('institute of technology','iot')
#	inst_l.append(ls)
#f.close()


## One tokenizer
# 
# inst_d = {}
# for i in range(len(inst_l)):
# 	l = inst_l[i]
# 	others = list(inst_l)
# 	others.pop(i)
# 
# 	strln = 4
# 	tokened = False
# 	while( not tokened ):
# 		for starti in range(0,len(l)-strln+1):
# 			token = l[starti:starti+strln]
# 			if not any( [token in lo for lo in others] ):
# 				inst_d[token] = l
# 				tokened = True
# 		if strln < len(l):
# 			strln += 1
# 		else:
# 			if not tokened:
# 				print "No token for "+l
# 			break

# Simpler tokenizer


inst_d = {}
# take each entry in the existing list of institutions
#    (the one with basic replacements made)
for i in range(len(inst_l)):
	l = inst_l[i]
	others = list(inst_l)
	others.pop(i)

	strln = 4

	for starti in range(0,len(l)-strln+1):
		token = l[starti:starti+strln]
		if not any( [token in lo for lo in others] ):
			inst_d[token] = l
			tokened = True

# Fairly liberal matching -- hope that anything that *doesn't* match is truly different from what we have.


kl = semiproc.keys()
matchd = {}
unmatched = []
for k in kl:
	newinsts = semiproc[k]
	for j in range(len(newinsts)):
		ni = newinsts[j].replace('institute of technology','iot')
		if (' and ' in ni) or ('/' in ni) or (len(ni)<=2): continue
		found = False
		if ni in inst_l:
			found = True
			#print "exact match: "+ni
			continue
		for j in inst_d.keys():
			if j in ni:
				found = True
				#print "token match: "+ni+" , "+j+" , "+inst_d[j]
				try:
					if inst_d[j] not in matchd[ni]:
						matchd[ni].append( inst_d[j] )
				except KeyError:
					matchd[ni] = [ inst_d[j] ]
		if (not found) and (ni not in unmatched):
			unmatched.append(ni)

# Now, let's try some fuzzy matching
unmatched_clean = list(unmatched)
for i in range(len(unmatched)):
	rematch = list(unmatched)
	um = rematch.pop(i)
	testmatch = process.extractOne(um,inst_l)
	if testmatch[1] >= 94:
		print um,testmatch
		unmatched_clean.remove(um)

#And a little more.  This is super slow.
unmatched_reclean = list(unmatched_clean)
for i in range(len(unmatched_clean)):
	if (i+1) % 500 == 0:
		print i
	um = unmatched_clean[i]
	rematch = list(unmatched_reclean)
	rematch.remove(um)
	
	testmatch = process.extractOne(um,rematch)
	if testmatch[1] >= 94:
		print um,testmatch
		unmatched_reclean.remove(um)

candidates = list(unmatched_reclean)

#Save the results
f = open('InstCandidates.txt','w')
for l in candidates:
	f.write( l+'\n')
f.close()

# And a check
from random import sample
ri = sample(xrange(len(candidates)),100)
f = open('InstCandidates_Check100.txt','w')
for i in range(100):
	j = ri[i]
	f.write( candidates[j]+" "+str(process.extractOne(candidates[j],inst_l))+"\n" )
f.close()

#How about another?
ri = sample(xrange(len(inst_l)),40)
for i in range(40):
	j = ri[i]
	print inst_l[j]+" "+str(process.extractOne(inst_l[j],candidates)) 

#One more
closect = 0
for i in range(len(candidates)):
	um = candidates[i]
	testmatch = process.extractOne(um,inst_l)
	if testmatch[1] > 90:
		print um,testmatch
		closect += 1