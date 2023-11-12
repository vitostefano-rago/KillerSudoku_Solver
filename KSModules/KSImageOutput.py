from PIL import Image, ImageDraw, ImageFont

solsteps = []
wt = 1000
dd = [3,3]
tl = 3
sl = 1
rs = 900
siz = 9
imig = []
bckgnd = 0
cgs = set()
cgtobrd = 5

class SudokuTransmit():
	def __init__(self, sdk, sz, dv, cg):
		self.sdk = sdk
		self.sz = sz
		self.dv = dv
		self.cg = cg


def GetWT(w):
	global wt
	
	wt = w


def AddNextStep(stp):
	global solsteps
	global dd
	global siz
	global cgs
	
	if stp == -1:
		solsteps = []
	
	else:
		if solsteps == []:
			dd = stp.dv
			siz = stp.sz
			cgs = stp.cg
		tmp = [[stp.sdk[cntr][cntc] for cntc in range(siz)] for cntr in range(siz)]
		solsteps.append(tmp)


def GenerateFrame(osdk, csdk):
	global tl
	global sl
	global rs
	global wt
	global dd
	global siz
	global bckgnd
	global imig
	global cgs
	
	ws = int(rs + tl + siz - (rs + tl) % siz)
	img = bckgnd.copy()
	imgdrw = ImageDraw.Draw(img)
	nsiz = int(rs*0.7/siz)
	rpos = int((ws/siz - nsiz)/2) + 2
	cpos = int((ws/siz - nsiz)/2 + nsiz/20)
	fnt = ImageFont.truetype("arial.ttf", nsiz)
	
	#In case the first image is being generated, add the original simbols to it, as well as the cage totals
	if len(imig) == 0:
		for cntr in range(siz):
			for cntc in range(siz):
				if csdk[cntr][cntc] != 0:
					imgdrw.text((ws*cntc/siz + cpos, ws*cntr/siz + rpos), str(csdk[cntr][cntc]), font = fnt, fill = (0,0,0))
		for mycg in cgs:
			csiz = int(rs*0.25/siz)
			rposc = 0 #int(nsiz * 1)
			cposc = 5 #int(nsiz * 1)
			scl = mycg.ShowingCell()
			cfont = ImageFont.truetype("arial.ttf", csiz)
			imgdrw.text((ws*scl[1]/siz + cposc, ws*scl[0]/siz + rposc), mycg.tot, font = cfont, fill = (0,0,0))
		bckgnd = img.copy()
	
	#Add only the simbols added as part of the solution
	else:
		for cntr in range(siz):
			for cntc in range(siz):
				if csdk[cntr][cntc] != 0 and osdk[cntr][cntc] == 0:
					imgdrw.text((ws*cntc/siz + cpos, ws*cntr/siz + rpos), str(csdk[cntr][cntc]), font = fnt, fill = (255,0,0))
	
	return img


def CreateCanvas():
	global tl
	global sl
	global rs
	global wt
	global dd
	global siz
	global bckgnd
	global cgtobrd
	global cgs
	
	ws = int(rs + tl + siz - (rs + tl) % siz)
	cgcolor = (80,80,80)
	
	img = Image.new("RGB", (ws, ws), (255, 255, 255))
	imgdrw = ImageDraw.Draw(img)
	
	#Draw vertical lines
	for cnt in range(siz):
		if cnt % dd[0] == 0:
			imgdrw.line([(int(cnt * ws/siz), 0),(int(cnt * ws/siz), ws)], fill = (0,0,0), width = tl)
		else:
			imgdrw.line([(int(cnt * ws/siz), 0),(int(cnt * ws/siz), ws)], fill = (0,0,0), width = sl)
	imgdrw.line([((ws-sl, 0)),(ws-sl, ws)], fill = (0,0,0), width = tl)
	
	#Draw horizontal lines
	for cnt in range(siz):
		if cnt % dd[1] == 0:
			imgdrw.line([(0,int(cnt * ws/siz)),(ws, int(cnt * ws/siz))], fill = (0,0,0), width = tl)
		else:
			imgdrw.line([(0,int(cnt * ws/siz)),(ws, int(cnt * ws/siz))], fill = (0,0,0), width = sl)
	imgdrw.line([((0,ws-sl)),(ws-tl, ws-sl)], fill = (0,0,0), width = tl)
	
	#Draw cages
	for cg in cgs:
		othclls = cg.clls.copy()
		for mycell in cg.clls:
			sc = [int(ws / siz) * mycell[1], int(ws / siz) * mycell[0]]
			#Check for being topmost at given position
			if (mycell[0] - 1, mycell[1]) not in othclls:
				#Draw horizontal line at the top
				#Case cells both to the left and the right are not part of the cage
				if (mycell[0], mycell[1] - 1) not in othclls and (mycell[0], mycell[1] + 1) not in othclls:
					imgdrw.line([(sc[0] + cgtobrd*sl, sc[1] + cgtobrd*sl), (sc[0] + int(ws / siz) - cgtobrd*sl, sc[1] + cgtobrd*sl)], fill = cgcolor, width = sl)
				#Case cells to the left are part of the cage but cells to the right are not
				elif (mycell[0], mycell[1] - 1) in othclls and (mycell[0], mycell[1] + 1) not in othclls:
					imgdrw.line([(sc[0] - cgtobrd*sl, sc[1] + cgtobrd*sl), (sc[0] + int(ws / siz) - cgtobrd*sl, sc[1] + cgtobrd*sl)], fill = cgcolor, width = sl)
				#Case cells to the right are part of the cage but cells to the left are not
				elif (mycell[0], mycell[1] - 1) not in othclls and (mycell[0], mycell[1] + 1) in othclls:
					imgdrw.line([(sc[0] + cgtobrd*sl, sc[1] + cgtobrd*sl), (sc[0] + int(ws / siz) + cgtobrd*sl, sc[1] + cgtobrd*sl)], fill = cgcolor, width = sl)
				#Cells both to the left and the right are part of the cage
				else:
					imgdrw.line([(sc[0] - cgtobrd*sl, sc[1] + cgtobrd*sl), (sc[0] + int(ws / siz) + cgtobrd*sl, sc[1] + cgtobrd*sl)], fill = cgcolor, width = sl)
			
			#Check for being lefmost at given position
			if (mycell[0], mycell[1] - 1) not in othclls:
				#Draw vertical line to the left
				#Case cells above and below are not part of the cage
				if (mycell[0] - 1, mycell[1]) not in othclls and (mycell[0] + 1, mycell[1]) not in othclls:
					imgdrw.line([(sc[0] + cgtobrd*sl, sc[1] + cgtobrd*sl), (sc[0] + cgtobrd*sl, sc[1] + int(ws / siz) - cgtobrd*sl)], fill = cgcolor, width = sl)
				#Case cell above is part and below is not part of the cage
				elif (mycell[0] - 1, mycell[1]) in othclls and (mycell[0] + 1, mycell[1]) not in othclls:
					imgdrw.line([(sc[0] + cgtobrd*sl, sc[1] - cgtobrd*sl), (sc[0] + cgtobrd*sl, sc[1] + int(ws / siz) - cgtobrd*sl)], fill = cgcolor, width = sl)
				#Case cell above is not part and below is part of the cage
				elif (mycell[0] - 1, mycell[1]) not in othclls and (mycell[0] + 1, mycell[1]) in othclls:
					imgdrw.line([(sc[0] + cgtobrd*sl, sc[1] + cgtobrd*sl), (sc[0] + cgtobrd*sl, sc[1] + int(ws / siz) + cgtobrd*sl)], fill = cgcolor, width = sl)
				#Both cells above and below are part of the cage
				else:
					imgdrw.line([(sc[0] + cgtobrd*sl, sc[1] - cgtobrd*sl), (sc[0] + cgtobrd*sl, sc[1] + int(ws / siz) + cgtobrd*sl)], fill = cgcolor, width = sl)
			
			#Check for being bottommost at given position
			if (mycell[0] + 1, mycell[1]) not in othclls:
				#Draw horizontal line at the bottom
				#Case cells both to the left and the right are not part of the cage
				if (mycell[0], mycell[1] - 1) not in othclls and (mycell[0], mycell[1] + 1) not in othclls:
					imgdrw.line([(sc[0] + cgtobrd*sl, sc[1]  + int(ws / siz) - cgtobrd*sl), (sc[0] + int(ws / siz) - cgtobrd*sl, sc[1] + int(ws / siz) - cgtobrd*sl)], fill = cgcolor, width = sl)
				#Case cell to the left is part of the cage and cage to the right is not
				elif (mycell[0], mycell[1] - 1) in othclls and (mycell[0], mycell[1] + 1) not in othclls:
					imgdrw.line([(sc[0] - cgtobrd*sl, sc[1]  + int(ws / siz) - cgtobrd*sl), (sc[0] + int(ws / siz) - cgtobrd*sl, sc[1] + int(ws / siz) - cgtobrd*sl)], fill = cgcolor, width = sl)
				#Case cell to the left is not part of the cage and cage to the right is
				elif (mycell[0], mycell[1] - 1) not in othclls and (mycell[0], mycell[1] + 1) in othclls:
					imgdrw.line([(sc[0] + cgtobrd*sl, sc[1]  + int(ws / siz) - cgtobrd*sl), (sc[0] + int(ws / siz) + cgtobrd*sl, sc[1] + int(ws / siz) - cgtobrd*sl)], fill = cgcolor, width = sl)
				#Cells both to the left and the right are part of the cage
				else:
					imgdrw.line([(sc[0] - cgtobrd*sl, sc[1]  + int(ws / siz) - cgtobrd*sl), (sc[0] + int(ws / siz) + cgtobrd*sl, sc[1] + int(ws / siz) - cgtobrd*sl)], fill = cgcolor, width = sl)
			
			#Check for being rightmost at given position
			if (mycell[0], mycell[1] + 1) not in othclls:
				#Draw vertical line to the rightmost
				#Case both cellse above and below are not part of the cage
				if (mycell[0] - 1, mycell[1]) not in othclls and (mycell[0] + 1, mycell[1]) not in othclls:
					imgdrw.line([(sc[0] + int(ws / siz) - cgtobrd*sl, sc[1] + cgtobrd*sl), (sc[0] + int(ws / siz) - cgtobrd*sl, sc[1] + int(ws / siz) - cgtobrd*sl)], fill = cgcolor, width = sl)
				#Case cell above is part and cell below is not
				elif (mycell[0] - 1, mycell[1]) in othclls and (mycell[0] + 1, mycell[1]) not in othclls:
					imgdrw.line([(sc[0] + int(ws / siz) - cgtobrd*sl, sc[1] - cgtobrd*sl), (sc[0] + int(ws / siz) - cgtobrd*sl, sc[1] + int(ws / siz) - cgtobrd*sl)], fill = cgcolor, width = sl)
				#Case cell above is not part and cell below is
				elif (mycell[0] - 1, mycell[1]) not in othclls and (mycell[0] + 1, mycell[1]) in othclls:
					imgdrw.line([(sc[0] + int(ws / siz) - cgtobrd*sl, sc[1] + cgtobrd*sl), (sc[0] + int(ws / siz) - cgtobrd*sl, sc[1] + int(ws / siz) + cgtobrd*sl)], fill = cgcolor, width = sl)
				#Case both cells above and below are part of the cage
				else:
					imgdrw.line([(sc[0] + int(ws / siz) - cgtobrd*sl, sc[1] - cgtobrd*sl), (sc[0] + int(ws / siz) - cgtobrd*sl, sc[1] + int(ws / siz) + cgtobrd*sl)], fill = cgcolor, width = sl)
	
	
	bckgnd = img.copy()


def UniteFrames(cst):
	global solsteps
	global wt
	global imig
	
	if cst < len(solsteps) and cst >= 0:
		imig.append(GenerateFrame(solsteps[0], solsteps[cst]))
		
		if cst == 0:
			ti = imig[0]
			imig.append(ti)
		
		if cst == len(solsteps) - 1:
			ti = imig[len(imig) - 1]
			imig.append(ti)
	
	elif cst >= len(solsteps):
		imig[0].save("Sudoku.gif", save_all=True, append_images = imig[1:], optimize = False, duration = 250 + wt * 0.5, loop = 0)
	
	elif cst == -1:
		imig = []
		CreateCanvas()