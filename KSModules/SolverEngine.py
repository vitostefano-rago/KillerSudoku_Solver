from itertools import combinations, combinations_with_replacement

cols = 9
rows = 9
#size of subcell row, size of subcell culomn
div = [3,3]
posnum = {i+1 for i in range(div[0]*div[1])}
sudoku = [[0 for _ in range(cols)] for _ in range(rows)]
gl = []
ccn = 0
cgs = set()
indeadend = 0
mysinglecombos = dict()
mymulticombos = dict()


class MyCage:
	def __init__(self,clls,tot):
		self.clls = clls
		self.tot = tot
	
	def ShowingCell(self):
		r, c = 1000, 1000
		
		for itr in self.clls:
			if itr[0] < r:
				r = itr[0]
		
		for itrr in self.clls:
			if itrr[0] == r and itrr[1] < c:
				c = itrr[1]
		
		return (r,c)

class SudokuTransmit():
	def __init__(self, sdk, sz, dv, cg):
		self.sdk = sdk
		self.sz = sz
		self.dv = dv
		self.cg = cg

class SavedStatus():
	def __init__(self, sdk, row, col, vn):
		self.sdk = sdk
		self.row = row
		self.col = col
		self.vn = vn

def CoherencyCheck(sdk):
	global div
	global rows
	global cols
	global cgs
	
	#Check columns
	for cntr in range(rows):
		#initialise list of elements to be checked
		vl = set()
		for cntc in range(cols):
			#Check only nonblanks
			if sdk[cntr][cntc] != 0:
				if sdk[cntr][cntc] in vl:
					return 0
				else:
					vl.add(sdk[cntr][cntc])
	#Check rows
	for cntc in range(cols):
		#initialise list of elements to be checked
		vl = set()
		for cntr in range(rows):
			#Check only nonblanks
			if sdk[cntr][cntc] != 0:
				if sdk[cntr][cntc] in vl:
					return 0
				else:
					vl.add(sdk[cntr][cntc])
	#Check for cell groups
	for cnt in range(div[0]*div[1]):
		vl = set()
		ro, co = int((cnt - cnt % div[1]) / div[1]) , cnt % div[1]
		for cntr in range(div[1]*ro, div[1]*(ro + 1)):
			for cntc in range(div[0]*co, div[0]*(co + 1)):
				#Check only nonblanks
				#print(cntr,cntc)
				if sdk[cntr][cntc] != 0:
					if sdk[cntr][cntc] in vl:
						return 0
					else:
						vl.add(sdk[cntr][cntc])
	
	for mc in cgs:
		if mc.tot.isnumeric() == False:
			return 2
		if int(mc.tot) < len(mc.clls):
			return 2
	
	return 1


def CheckRow(row):
	global sudoku
	global cols
	rv = set()
	for cntc in range(cols):
		rv.add(sudoku[row][cntc])
	return rv


def CheckColumn(col):
	global sudoku
	global rows
	cv = set()
	for cntr in range(rows):
		cv.add(sudoku[cntr][col])
	return cv


def CheckCellGroup(row,col):
	global sudoku
	global div
	sr, sc =  row - row % div[1], col - col % div[0]
	gv = set()
	for cntr in range(sr,sr+div[1]):
		for cntc in range(sc,sc + div[0]):
			gv.add(sudoku[cntr][cntc])
	return gv

def GiveMeCombo(lngth, tot, mode):
	global mysinglecombos
	global mymulticombos
	global posnum
	
	#mode 0 means only one occurrence, mode 1 means multiple occurrences
	if mode == 0:
		if lngth in mysinglecombos.keys():
			if tot not in mysinglecombos[lngth].keys():
				mylst = list()
				pl = list(posnum)
				for var in combinations(pl, lngth):
					if sum(var) == tot:
						mylst.extend(var)
				sls = set(mylst)
				mysinglecombos[lngth][tot] = sls
			return mysinglecombos[lngth][tot]
		else:
			mysinglecombos[lngth] = dict()
			mylst = list()
			pl = list(posnum)
			for var in combinations(pl, lngth):
				if sum(var) == tot:
					mylst.extend(var)
			sls = set(mylst)
			mysinglecombos[lngth][tot] = sls
			return mysinglecombos[lngth][tot]
	else:
		if lngth in mymulticombos.keys():
			if tot not in mymulticombos[lngth].keys():
				mylst = list()
				pl = list(posnum)
				for var in combinations_with_replacement(pl, lngth):
					if sum(var) == tot:
						mylst.extend(var)
				sls = set(mylst)
				mymulticombos[lngth][tot] = sls
			return mymulticombos[lngth][tot]
		else:
			mymulticombos[lngth] = dict()
			mylst = list()
			pl = list(posnum)
			for var in combinations_with_replacement(pl, lngth):
				if sum(var) == tot:
					mylst.extend(var)
			sls = set(mylst)
			mymulticombos[lngth][tot] = sls
			return mymulticombos[lngth][tot]

#This returns the values that could be possibly written into all cells - made possible by specific values written into the other cells
def BasicSolutions():
	global sudoku
	global cols
	global rows
	global div
	global posnum
	
	ev = [[posnum.copy() for _ in range(cols)] for _ in range(rows)]
	#Check all cells
	for cntr in range(rows):
		for cntc in range(cols):
			if sudoku[cntr][cntc] == 0:
				#In blank cels, check possible solutions
				fc = CheckRow(cntr).union(CheckColumn(cntc).union(CheckCellGroup(cntr,cntc)))
				ev[cntr][cntc] = posnum.difference(fc)
			else:
				ev[cntr][cntc] = set()
	return ev

#This says if a cage is bound to contain different numbers only
#Input is set of cells in the cage
def SingleOccurrence(mcs):
	global div
	
	rs, cs, ds = set(), set(), set()
	for cg in mcs:
		rs.add(cg[0])
		cs.add(cg[1])
		ds.add((cg[0]//div[1],cg[1]//div[0]))
	
	if len(rs) == 1 or len(cs) == 1 or len(ds) == 1:
		return True
	return False

#This returns the values that could possibly be written into all cells - made possible by sums in cages
def CageSolutions():
	global cgs
	global sudoku
	global posnum
	fv = [[set() for _ in range(cols)] for _ in range(rows)]
	cgdclls = set()
	
	for mcg in cgs:
		cl = mcg.clls
		cgdclls.update(cl)
		tt = int(mcg.tot)
		mycl = set()
		for c in cl:
			if sudoku[c[0]][c[1]] == 0:
				mycl.add(c)
			else:
				tt -= sudoku[c[0]][c[1]]
		
		sls = set()
		pl = list(posnum)
		
		if SingleOccurrence(mycl):
			sls = GiveMeCombo(len(mycl),tt,0)
		
		else:
			sls = GiveMeCombo(len(mycl),tt,1)
		
		for elemnt in mycl:
			fv[elemnt[0]][elemnt[1]] = sls
	
	for row in range(rows):
		for col in range(cols):
			if(row, col) not in cgdclls:
				fv[row][col] = posnum
	
	return fv

#This returns the values that could actualy be written into all cells, both according to single values and sums in cages
def CheckSolutions():
	global sudoku
	global rows
	global cols
	global posnum
	
	ev = BasicSolutions()
	fv = CageSolutions()
	
	gv = [[set() for _ in range(cols)] for _ in range(rows)]
	
	for c in range(cols):
		for r in range(rows):
			for i in posnum:
				if i in ev[c][r] and i in fv[c][r]:
					gv[c][r].add(i)
	
	return gv


def CountBlanks():
	global sudoku
	global cols
	blanks = 0
	for cntc in range(cols):
		blanks += sudoku[cntc].count(0)
	return blanks


#In case there are cells where only one value can be written, this fills those cells with that value
def SimpleSolution(fv):
	global sudoku
	global cols
	global rows
	global div
	global posnum
	rv = 0
	#Check all cells
	for cntr in range(rows):
		for cntc in range(cols):
			#This means that only one number would fit the given cell
			if len(fv[cntr][cntc]) == 1:
					#Insert to the given cell of the sudoku the only possible number not in the given row, column and subcellgroup, and return ready flag
					sudoku[cntr][cntc] = min(fv[cntr][cntc])
					rv = 1
	return rv


#Looks for cells with the only possible occurence of a value in the given row, column nonet or cage
def IntermediateSolution(fv):
	global sudoku
	global cols
	global rows
	global div
	global posnum
	global cgs
	
	rv = 0
	#Check traditional sudoku parts
	for cntr in range(rows):
		for cntc in range(cols):
			if sudoku[cntr][cntc] == 0:
				#In every nonblank cell
				rl = set()
				cl = set()
				sl = set()
				#Get values from every other cell in the culomn
				for cntrr in range(rows):
					if cntrr != cntr:
						rl = rl.union(fv[cntrr][cntc])
				#Get values from every other cell in the row
				for cntcc in range(cols):
					if cntcc != cntc:
						cl = cl.union(fv[cntr][cntcc])
				#get values from every other cell in the subrectangle
				sr, sc =  cntr - cntr % div[1], cntc - cntc % div[0]
				for cntrr in range(sr, sr + div[1]):
					for cntcc in range(sc,sc + div[0]):
						if not (cntrr == cntr and cntcc == cntc):
							sl = sl.union(fv[cntrr][cntcc])
				#Check for all values occurrence
				for cnt in fv[cntr][cntc]:
					if cnt not in rl or cnt not in cl or cnt not in sl:
						#Case the given cell is the only place the current cnt value fits
						sudoku[cntr][cntc] = cnt
						rv = 1
						break
	
	if rv == 1:
		return rv
	
	#Check cages
	for cg in cgs:
		cl = cg.clls
		bc = 0
		allposs = set()
		
		for mc in cl:
			if sudoku[mc[0]][mc[1]] == 0:
				bc += 1
		
		if bc != 0:
			for sc in cl:
				for i in posnum:
					if i in fv[sc[0]][sc[1]]:
						allposs.add(i)
		
		#If, for how the cage is positioned, every number is guaranteed to be in it only once, and number of blank cells equals number of possible solutions
		if SingleOccurrence(cl) and bc == len(allposs) and bc != 0:
			for ccl in cl:
				mysls = set()
				for cccl in cl:
					if ccl != cccl:
						for i in fv[cccl[0]][cccl[1]]:
							mysls.add(i)
				for j in posnum:
					if j in fv[ccl[0]][ccl[1]] and j not in mysls:
						sudoku[ccl[0]][ccl[1]] = j
						rv = 1
	
	
	return rv

#If some numbers are guaranteed to be in given cells of the row/cage/nonet, eliminate them from the possibilities of the others
def KillerElimination(fv):
	global cgs
	global sudoku
	global posnum
	global rows
	global cols
	global div
	
	rv = fv[:][:]
	
	for mcg in cgs:
		cl = mcg.clls
		tt = int(mcg.tot)
		mycl = set()
		for c in cl:
			if sudoku[c[0]][c[1]] == 0:
				mycl.add(c)
			else:
				tt -= sudoku[c[0]][c[1]]
		
		sls = set()
		pl = list(posnum)
		
		if SingleOccurrence(mycl):
			sls = GiveMeCombo(len(mycl),tt,0)
		
		#Case there is no uncertainity about the fact that all the given numbers are in the given cage
		if len(sls) == len(mycl):
			rwv, clv, sr, sc = -10, -10, -10, -10
			rw, cl, scg = set(), set(), set()
			
			#Eliminate from row (if possible):
			for cll in mycl:
				rw.add(cll[0])
				rwv = cll[0]
				if len(rw) > 1:
					break
			else:
				for c in range(cols):
					if (rwv,c) not in mycl:
						for myelem in sls:
							rv[rwv][c].discard(myelem)
			
			#Eliminate from column (if possible)
			for rww in mycl:
				cl.add(rww[1])
				clv = rww[1]
				if len(cl) > 1:
					break
			else:
				for r in range(rows):
					if (r, clv) not in mycl:
						for myelem in sls:
							rv[r][clv].discard(myelem)
			
			#Eliminate from nonet
			for scc in mycl:
				sr, sc = scc[0] - scc[0] % div[1], scc[1] - scc[1] % div[0]
				scg.add((sr,sc))
				if len(scg) > 1:
					break
			else:
				for cntr in range(sr,sr+div[1]):
					for cntc in range(sc,sc + div[0]):
						if (cntr, cntc) not in mycl:
							for myelem in sls:
								rv[cntr][cntc].discard(myelem)
	
	return rv

def EliminateInvalid(fv):
	global cgs
	global sudoku
	global posnum
	
	rv = fv[:][:]
	
	for mcg in cgs:
		cl = mcg.clls
		tt = int(mcg.tot)
		mycl = set()
		mysols = set()
		tbe = set()
		for c in cl:
			if sudoku[c[0]][c[1]] == 0:
				mycl.add(c)
				for i in posnum:
					if i in rv[c[0]][c[1]]:
						mysols.add(i)
			else:
				tt -= sudoku[c[0]][c[1]]
		
		#Not to be replaced by the GiveMeCombo function! 
		#Used only seldomly and not combinations of all numbers inside posnum, GiveMeCombo does not handle this!
		for mynum in mysols:
			mysollst = list(mysols)
			if SingleOccurrence(mycl):
				mycmbs = combinations(mysollst, len(mycl))
			else:
				mycmbs = combinations_with_replacement(mysollst, len(mycl))
			for tr in mycmbs:
				if sum(tr) == tt and mynum in tr:
					break
			else:
				tbe.add(mynum)
		
		for elim in tbe:
			for ccl in mycl:
				rv[ccl[0]][ccl[1]].discard(elim)
	
	return rv


#Create cages from cell outside a given row/colum/nonet, eliminate elements from original cages based on them
def OutsideFortyFive(fv):
	global sudoku
	global cgs
	global posnum
	global rows
	global cols
	global div
	
	rv = fv[:][:]
	ff = -1*(cols+1)*cols*0.5
	ocg = set()
	
	for row in range(rows):
		mycls = {(row,i) for i in range(cols) if sudoku[row][i] == 0}
		ccg = MyCage(set(), ff)
		for i in range(cols):
			ccg.tot += sudoku[row][i]
		for cg in cgs:
			for cl in mycls:
				if cl in ccg.clls:
					continue
				if cl in cg.clls and cl not in ccg.clls:
					ccg.tot += int(cg.tot)
					for mc in cg.clls:
						if sudoku[mc[0]][mc[1]] == 0:
							ccg.clls.add((mc[0],mc[1]))
						else:
							ccg.tot -= sudoku[mc[0]][mc[1]]
					break
		for elim in mycls:
			ccg.clls.discard(elim)
		ocg.add(ccg)
	
	for col in range(cols):
		mycls = {(i,col) for i in range(rows) if sudoku[i][col] == 0}
		ccg = MyCage(set(), ff)
		for i in range(rows):
			ccg.tot += sudoku[i][col]
		for cg in cgs:
			for cl in mycls:
				if cl in ccg.clls:
					continue
				if cl in cg.clls and cl not in ccg.clls:
					ccg.tot += int(cg.tot)
					for mc in cg.clls:
						if sudoku[mc[0]][mc[1]] == 0:
							ccg.clls.add((mc[0],mc[1]))
						else:
							ccg.tot -= sudoku[mc[0]][mc[1]]
					break
		for elim in mycls:
			ccg.clls.discard(elim)
		ocg.add(ccg)
	
	for r in range(int(rows/div[1])):
		for c in range(int(cols/div[0])):
			mycls = {(r*div[1] + i,c*div[0] + j) for i in range(div[1]) for j in range(div[0]) if sudoku[r*div[1] + i][c*div[0] + j] == 0}
			ccg = MyCage(set(), ff)
			for i in range(div[1]):
				for j in range(div[0]):
					ccg.tot += sudoku[r*div[1] + i][c*div[0] + j]
			for cg in cgs:
				for cl in mycls:
					if cl in ccg.clls:
						continue
					if cl in cg.clls and cl not in ccg.clls:
						ccg.tot += int(cg.tot)
						for mc in cg.clls:
							if sudoku[mc[0]][mc[1]] == 0:
								ccg.clls.add((mc[0],mc[1]))
							else:
								ccg.tot -= sudoku[mc[0]][mc[1]]
						break
			for elim in mycls:
				ccg.clls.discard(elim)
			ocg.add(ccg)
	
	for myoc in ocg:
		sls = GiveMeCombo(len(myoc.clls),myoc.tot,1)
		for mc in myoc.clls:
			rv[mc[0]][mc[1]].intersection_update(sls)
	
	return rv

#Create subcages in line, column, nonet based on the fact that sum of all elements is known
def InsideFortyFive(fv):
	global sudoku
	global cgs
	global rows
	global posnum
	global cols
	global div
	
	rv = fv[:][:]
	
	ff = cols * (cols+1) * 0.5
	ocg = set()
	
	for row in range(rows):
		mycls = {(row,i) for i in range(cols) if sudoku[row][i] == 0}
		tt = ff
		imcg = set()
		for i in range(cols):
			tt -= sudoku[row][i]
		
		for cg in cgs:
			ct = int(cg.tot)
			cclp = cg.clls
			ccl = set()
			
			for cc in cclp:
				if sudoku[cc[0]][cc[1]] == 0:
					ccl.add(cc)
				else:
					ct -= sudoku[cc[0]][cc[1]]
			
			ce = ccl.intersection(mycls)
			
			
			if len(ce) == 0:
				continue
			
			if len(ce) == len(ccl):
				for elm in ce:
					mycls.discard(elm)
				tt -= ct
			else:
				imcg.update(ce)
		
		mycg = MyCage(imcg, tt)
		ocg.add(mycg)
		
	
	
	for col in range(cols):
		mycls = {(i,col) for i in range(rows) if sudoku[i][col] == 0}
		tt = ff
		imcg = set()
		for i in range(rows):
			tt -= sudoku[i][col]
		
		for cg in cgs:
			ct = int(cg.tot)
			cclp = cg.clls
			ccl = set()
			
			for cc in cclp:
				if sudoku[cc[0]][cc[1]] == 0:
					ccl.add(cc)
				else:
					ct -= sudoku[cc[0]][cc[1]]
			
			if len(ce) == 0:
				continue
			
			if len(ce) == len(ccl):
				for elm in ce:
					mycls.discard(elm)
				tt -= ct
			else:
				imcg.update(ce)
		
		mycg = MyCage(imcg, tt)
		ocg.add(mycg)
	
	
	for r in range(int(rows/div[1])):
		for c in range(int(cols/div[0])):
			mycls = {(r*div[1] + i,c*div[0] + j) for i in range(div[1]) for j in range(div[0]) if sudoku[r*div[1] + i][c*div[0] + j] == 0}
			tt = ff
			imcg = set()
			for i in range(div[1]):
				for j in range(div[0]):
					tt -= sudoku[r*div[1] + i][c*div[0] + j]
			
			for cg in cgs:
				ct = int(cg.tot)
				cclp = cg.clls
				ccl = set()
				
				for cc in cclp:
					if sudoku[cc[0]][cc[1]] == 0:
						ccl.add(cc)
					else:
						ct -= sudoku[cc[0]][cc[1]]
				
				if len(ce) == 0:
					continue
				
				if len(ce) == len(ccl):
					for elm in ce:
						mycls.discard(elm)
					tt -= ct
				else:
					imcg.update(ce)
			
			mycg = MyCage(imcg, tt)
			ocg.add(mycg)
	
	
	for myoc in ocg:
		sls = GiveMeCombo(len(myoc.clls),myoc.tot,0)
		for mc in myoc.clls:
			rv[mc[0]][mc[1]].intersection_update(sls)
	
	return rv

def EliminateSolutions(fv):
	global rows
	global cols
	global div
	global posnum
	doing = 1
	while doing == 1:
		doing = 0
		for cntg in range(div[0]*div[1]):
			ro, co = int((cntg - cntg % div[1]) / div[1]) , cntg % div[1]
			#Check for all possible values
			for cnt in posnum:
				rs = []
				cs = []
				#Check columnwise
				for cntr in range(div[1]*ro, div[1]*(ro + 1)):
					tv = 0
					for cntc in range(div[0]*co, div[0]*(co + 1)):
						if cnt in fv[cntr][cntc]:
							tv += 1
					rs.append(tv)
				#Check rowwise
				for cntc in range(div[0]*co, div[0]*(co + 1)):
					tv = 0
					for cntr in range(div[1]*ro, div[1]*(ro + 1)):
						if cnt in fv[cntr][cntc]:
							tv += 1
					cs.append(tv)
				#Eliminate rowwise
				#This means that value cnt can be found only in one row of the subcell
				if rs.count(0) == len(rs) - 1:
					for cntcc in range(cols):
						#This means outside the subcell
						if cntcc < div[0]*co or cntcc >= div[0]*(co + 1):
							if cnt in fv[div[1]*ro + rs.index(max(rs))][cntcc]:
								#If present, eliminate possible solution from all cells in the culomn that are not in the subrectangle
								fv[div[1]*ro + rs.index(max(rs))][cntcc] = fv[div[1]*ro + rs.index(max(rs))][cntcc].difference({cnt})
								doing = 1
				#Eliminate columnwise
				#This means that value cnt can be found only in one column of the subcell
				if cs.count(0) == len(cs) - 1:
					for cntrr in range(rows):
						#This means outside the subcell
						if cntrr < div[1]*ro or cntrr >= div[1]*(ro + 1):
							if cnt in fv[cntrr][div[0]*co + cs.index(max(cs))]:
								#If present, eliminate possible solution from all cells in the row that are not in the subrectangle
								fv[cntrr][div[0]*co + cs.index(max(cs))] = fv[cntrr][div[0]*co + cs.index(max(cs))].difference({cnt})
								doing = 1
	return fv


#Number of possible solutions in each cell
def GetPosSol(fv):
	global rows
	global cols
	global div
	global sudoku
	
	#Very high value means there is already a value in the given cell
	sols = [[10000000 for _ in range(cols)] for _ in range(rows)]
	for cntr in range(rows):
		for cntc in range(cols):
			#At least one solution can be fit in the given cell
			if len(fv[cntr][cntc]) != 0:
				sols[cntr][cntc] = len(fv[cntr][cntc])
			#No solutions can be fit into an empty cell
			elif sudoku[cntr][cntc] == 0:
				sols[cntr][cntc] = -1
	return sols


def GuessManager(sv):
	global sudoku
	global rows
	global cols
	global gl
	global indeadend
	
	indeadend = 0
	
	ps = GetPosSol(sv)
	mv = min(min(ps[cnt]) for cnt in range(cols))
	cntr, cntc = 0,0
	#create shallow copy of sudoku
	lc = [[sudoku[cntr][cntc] for cntc in range(cols)] for cntr in range(rows)]
	
	#Case there is a cell with multiple solution where a choice has to be made, pick the smallest value
	if mv >= 2 and mv < 999999 and CoherencyCheck(sudoku) == 1:
		for cntr in range(rows):
			for cntc in range(cols):
				if ps[cntr][cntc] == mv:
					tl = list(sv[cntr][cntc])
					tl.sort()
					gl.append(SavedStatus(lc,cntr,cntc,0))
					sudoku[cntr][cntc] = tl[0]
					return 1
	
	#Case algorithm got stuck, needs to go back.
	if mv == -1 or mv > 999999 or CoherencyCheck(sudoku) != 1:
		while True:
			if len(gl) > 0:
				lst = gl.pop()
				sudoku = lst.sdk
				fv = CheckSolutions()
				sv = EliminateSolutions(fv)
				rw = lst.row
				cl = lst.col
				if lst.vn <= len(sv[rw][cl]) - 2:
					#If there are still numbers to be tried in that position, do it (go to next smallest possible number not tried yet). Otherwise, do nothing(go one further step back in next iteration)
					lc = [[sudoku[cntr][cntc] for cntc in range(cols)] for cntr in range(rows)]
					tl = list(sv[rw][cl])
					tl.sort()
					gl.append(SavedStatus(lc,rw,cl,lst.vn+1))
					sudoku[rw][cl] = tl[lst.vn + 1]
					return 1
			else:
				return -1

def ReceiveSudoku(st):
	global sudoku
	global rows
	global cols
	global div
	global posnum
	global cgs
	
	#Not consistent size input
	if st.sz != st.dv[0] * st.dv[1]:
		return 0
	
	
	#Consistent size input
	else:
		rows = st.sz
		cols = st.sz
		div = st.dv
		cgs = st.cg
		posnum = {i+1 for i in range(div[0]*div[1])}
		sudoku = [[0 for _ in range(cols)] for _ in range(rows)]
		for r in range(rows):
			for c in range(cols):
				sudoku[r][c] = int(st.sdk[r][c])
				if sudoku[r][c] > rows:
					return 2
	
	return 1



def Solving():
	global sudoku
	global cols
	global div
	global ccn
	global cgs
	global indeadend
	
	fv = CheckSolutions()
	
	if ccn == 0:
		indeadend = 0
	else:
		ps = GetPosSol(fv)
		mv = min(min(ps[cnt]) for cnt in range(cols))
		if mv == -1:
			indeadend = 1
	
	kv = KillerElimination(fv)
	
	#Simple solution works for classic sudoku but is very unlikely to bring results for killer sudoku, therefore medium is also considered simple.
	#New, killer-sudoku-specific medium difficulty introduced, for the case where the boundary condition of sums will lead to a result.
	if ((ccn == 0 or CoherencyCheck(sudoku) == 1) and indeadend == 0):
		a = SimpleSolution(kv)
		if a == 0:
			a = 2*IntermediateSolution(kv)
			if a == 0:
				iv = InsideFortyFive(kv)
				a = 4*SimpleSolution(iv)
				if a == 0:
					a = 8*IntermediateSolution(iv)
					if a == 0:
						ov = OutsideFortyFive(iv)
						a = 16*SimpleSolution(ov)
						if a == 0:
							a = 32*IntermediateSolution(ov)
							if a == 0:
								iev = EliminateInvalid(ov)
								a = 64*SimpleSolution(iev)
								if a == 0:
									a = 128*IntermediateSolution(iev)
									if a == 0:
										sv = EliminateSolutions(iev)
										a = 256*SimpleSolution(sv)
										if a == 0:
											a = 512*IntermediateSolution(sv)
											if a == 0:
												a = 1024*GuessManager(sv)
												ccn = 1
	
	#If the current guess has brought to an incoherent status, do not waste loops on it
	else:
		sv = EliminateSolutions(fv)
		a = 64*GuessManager(sv)
	
	return SudokuTransmit(sudoku,cols,div,cgs), a

