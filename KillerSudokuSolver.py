import pygame
import KSModules.SolverEngine
import KSModules.KSGUI
import KSModules.KSImageOutput


def main():
	row = -1
	col = -1
	KSModules.KSGUI.DrawRawGrid(1)
	loop = 0
	while True:
		tmp = KSModules.KSGUI.GUIEngine(row,col)
		row, col = tmp[0], tmp[1]
		if row < -5 or col < -5:
			cs = tmp[2].sdk
			if KSModules.SolverEngine.ReceiveSudoku(tmp[2]) == 0:
				KSModules.KSGUI.SendOutPut("Grid division not set properly.")
			elif KSModules.SolverEngine.ReceiveSudoku(tmp[2]) == 2:
				KSModules.KSGUI.SendOutPut("Too high input value added.")
			else:
				if row == -6 and col == -6:
					row, col = -1, -1
					if KSModules.SolverEngine.CoherencyCheck(tmp[2].sdk) == 0:
						KSModules.KSGUI.SendOutPut("Input does not comply with rules.")
					elif KSModules.SolverEngine.CoherencyCheck(tmp[2].sdk) == 2:
						KSModules.KSGUI.SendOutPut("Too small value in cage!")
					else:
						KSModules.KSGUI.SendOutPut("Input is coherent.")
				
				elif row == -7 and col == -7:
					row, col = -1, -1
					if KSModules.SolverEngine.CoherencyCheck(tmp[2].sdk) == 0:
						KSModules.KSGUI.SendOutPut("Input does not comply with rules.")
					elif KSModules.SolverEngine.CoherencyCheck(tmp[2].sdk) == 2:
						KSModules.KSGUI.SendOutPut("Too small value in cage!")
					else:
						loop = 0
						mxdff = 1
						lststp = 0
						wt = KSModules.KSGUI.GetWaitingTime()
						KSModules.KSImageOutput.GetWT(wt)
						KSModules.KSImageOutput.AddNextStep(-1)
						KSModules.KSImageOutput.AddNextStep(tmp[2])
						wit = ["Working on it", "Working on it.", "Working on it..", "Working on it..."]
						while KSModules.SolverEngine.CountBlanks() > 0 or KSModules.SolverEngine.CoherencyCheck(cs) == 0:
							#Give the possibility to exit
							KSModules.KSGUI.GUIMinimal()
							if pygame.time.get_ticks() > lststp + wt:
								lststp = pygame.time.get_ticks()
								#Move towards the solution after having waited the proper amount of time
								tmp = KSModules.SolverEngine.Solving()
								if tmp[1] < 0:
									#Case Sudoku is invalid
									mxdff = -1
									KSModules.KSGUI.SendOutPut("This Sudoku has no solution.")
									break
								else:
									#Sudoku is valid
									loop += 1
									mxdff = max(mxdff, tmp[1])
									KSModules.KSGUI.UpdateValues(tmp[0])
									KSModules.KSImageOutput.AddNextStep(tmp[0])
									cs = tmp[0].sdk
									if mxdff < 1024:
										KSModules.KSGUI.DspAllVals(1)
									else:
										KSModules.KSGUI.DspAllVals(2)
									KSModules.KSGUI.SendOutPut(wit[int(loop % 4)])
									KSModules.KSGUI.WriteDifficulty(mxdff)
									KSModules.KSGUI.DisplayLoop(loop)
						
						if mxdff > 0:
							KSModules.KSGUI.SendOutPut("Finished!")
				
				elif row == -8 and col == -8:
					row, col = -1, -1
					KSModules.KSImageOutput.UniteFrames(-1)
					if KSModules.SolverEngine.CountBlanks() == 0 and KSModules.SolverEngine.CoherencyCheck(cs) == 1:
						cit = ["Creating the GIF", "Creating the GIF.", "Creating the GIF..", "Creating the GIF..."]
						for cnt in range(loop + 2):
							#Give the possibility to exit
							KSModules.KSGUI.GUIMinimal()
							KSModules.KSImageOutput.UniteFrames(cnt)
							KSModules.KSGUI.SendOutPut(cit[int(loop % 4)])
						KSModules.KSGUI.SendOutPut("GIF created!")
					else:
						KSModules.KSGUI.SendOutPut("Please solve the Sudoku first.")


main()
