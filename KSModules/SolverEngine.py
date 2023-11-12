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


#This returns the values that could be possibly written into all cells - made possible by specific values written into cells
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
	
	for mcg in cgs:
		cl = mcg.clls
		tt = int(mcg.tot)
		mycl = set()
		for c in cl:
			if sudoku[c[0]][c[1]] == 0:
				mycl.add(c)
			else:
				tt -= sudoku[c[0]][c[1]]
		
		mylst = list()
		pl = list(posnum)
		
		if SingleOccurrence(mycl):
			for var in combinations(pl, len(mycl)):
				if sum(var) == tt:
					mylst.extend(var)
		else:
			for var in combinations_with_replacement(pl, len(mycl)):
				if sum(var) == tt:
					mylst.extend(var)
		
		for elemnt in mycl:
			fv[elemnt[0]][elemnt[1]] = set(mylst)
	
	return fv

#This returns the values that could actualy be written into all cells, both according to single values and sums in cages
def CheckSolutions():
	global sudoku
	global rows
	global cols
	
	ev = BasicSolutions()
	fv = CageSolutions()
	
	gv = [[set() for _ in range(cols)] for _ in range(rows)]
	
	for c in range(cols):
		for r in range(rows):
			for i in range(1, rows + 1):
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


#Looks for cells with the only possible occurence of a value in the given row, column or subrectangle
def IntermediateSolution(fv):
	global sudoku
	global cols
	global rows
	global div
	global posnum
	#fv = CheckSolutions()
	rv = 0
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
	return rv

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
		
		mylst = list()
		pl = list(posnum)
		
		if SingleOccurrence(mycl):
			for var in combinations(pl, len(mycl)):
				if sum(var) == tt:
					mylst.extend(var)
		
		#Case there is no uncertainity about the fact that all the given numbers are in the given cage
		if len(mylst) == len(mycl):
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
						for myelem in mylst:
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
						for myelem in mylst:
							rv[r][clv].discard(myelem)
			for scc in mycl:
				sr, sc =  scc[0] - scc[0] % div[1], scc[1] - scc[1] % div[0]
				scg.add((sr,sc))
				if len(scg) > 1:
					break
			else:
				for cntr in range(sr,sr+div[1]):
					for cntc in range(sc,sc + div[0]):
						if (cntr, cntc) not in mycl:
							for myelem in mylst:
								rv[cntr][cntc].discard(myelem)
	
	return rv


def EliminateSolutions(fv):
	global rows
	global cols
	global div
	global posnum
	#print(fv)
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

def HardSolution(fv):
	ev = EliminateSolutions(fv)
	t = SimpleSolution(ev)
	if t == 0:
		t = IntermediateSolution(ev)
	return t


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
	
	
	#Simple solution works for classic sudoku but is very unlikely to bring results for killer sudoku, therefore medium is also considered simple.
	#New, killer-sudoku-specific medium difficulty introduced, for the case where the boundary condition of sums will lead to a result.
	if ((ccn == 0 or CoherencyCheck(sudoku) == 1) and indeadend == 0):
		a = SimpleSolution(fv)
		if a == 0:
			a = 2*IntermediateSolution(fv)
			if a == 0:
				kv = KillerElimination(fv)
				a = 4*SimpleSolution(kv)
				if a == 0:
					a = 8*IntermediateSolution(kv)
					if a == 0:
						sv = EliminateSolutions(kv)
						a = 16*SimpleSolution(sv)
						if a == 0:
							a = 32*IntermediateSolution(sv)
							if a == 0:
								a = 64*GuessManager(sv)
								ccn = 1
	
	#If the current guess has brought to an incoherent status, do not waste loops on it
	else:
		sv = EliminateSolutions(fv)
		a = 64*GuessManager(sv)
	
	return SudokuTransmit(sudoku,cols,div,cgs), a

