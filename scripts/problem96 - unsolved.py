# https://projecteuler.net/problem=96

# need to create each of the techniques
# https://www.kristanix.com/sudokuepic/sudoku-solving-techniques.php

from itertools import chain


def solveProblem():
   
# set initial sum value
   sum_value = 0

   # creat a grid list
   grids = []

   # convert text to a list
   soduku_list = list(soduku_text)
   
   # starting varialbles
   grid = []
   i = 8

   # convert the soduku text into grids 
   # for next stage
   while i < len(soduku_list):
      
      grid = []

      for j in range(0, 9):
         row = []
         for k in soduku_list[i+(j*10):i+(j*10)+9]:
            row.append(int(k))
         
         grid.append(row)
      
      grids.append(grid)
      i += 98


   # loop through each of the grids to solve
   for grid in grids[2:3]:

      p = Puzzle(grid=grid)
      p.setCells()
      # p.printGrid()
      
      p.solve()

      p.printCellsBySection()
      p.printGrid()

      print len(p.cells), p.legalSolution()



   #    # at this point the grid the puzzle should be solved so 
   #    # get the three digits needed.
   #    three_digit_number = '%s%s%s' % (p.grid[0][0], p.grid[0][1], p.grid[0][2])
   #    sum_value += int(three_digit_number)
   
   # print sum_value






class Puzzle:
   """
   A class to represet a soduku puzzle providing functionality
   to print the grid and obtain row, column and section missing
   values.
   """
   def __init__(self, grid):
      self.grid = grid
      self.cells = []

   def setCells(self):
      """
      This functions returns all the cells that have zero
      as the value, i.e. the ones we need to find.
      """
      cell_list = []
      for y in range(0, 9):
         for x in range(0, 9):
            target = self.grid[y][x]
            if target == 0:
               cell_list.append(Cell(x=x, y=y))
      self.cells = cell_list

   def printGrid(self):
      """
      Print the soduku grid
      """
      for y in range(0, 9):
         if y % 3 == 0:
            print '________________________'
         for x in range(0, 9):
            if x % 3 == 0:
               print '|',
            if self.grid[y][x] == 0:
               print ' ',
            else:
               print self.grid[y][x],
         print '|'
      print '________________________'

   def printCellsBySection(self):
      sections = self.getCellsBySection()
      for section in sections:
         print 'SECTION:', section
         for cell in sections[section]:
            cell.printCell()

         print '________________________'

   def printCellsByRow(self):
      rows = self.getCellsByRow()
      for key, row in rows.iteritems():
         print '[%s] ' % (key),
         for cell in row:
            print cell.x, cell.possible_values,
         print ''
         print '________________________'

   def printCellsByColumn(self):
      cols = self.getCellsByColumn()
      for key, col in cols.iteritems():
         print '[%s] ' % (key),
         for cell in col:
            print cell.y, cell.possible_values,
         print ''
         print '________________________'
  
   def getValuesNotInRow(self, cell):
      """
      Get the possible values that are not in the row
      """
      possible_values = range(1, 10)
      for elm in self.grid[cell.y]:
         if elm in possible_values:
            possible_values.remove(elm)
      return possible_values

   def getValuesNotInColumn(self, cell):
      """
      Get the possible values that are not in the column
      """
      possible_values = range(1, 10)
      for y in range(0, 9):
         elm = self.grid[y][cell.x]
         if elm in possible_values:
            possible_values.remove(elm)
      return possible_values

   def getValuesNotInSection(self, cell):
      """
      Get the possible values that are not in the section
      """
      possible_values = range(1, 10)
      x_starting_from = (cell.x // 3) * 3
      y_starting_from = (cell.y // 3) * 3
      for y in range(0, 3):
         for x in range(0, 3):
            elm = self.grid[y_starting_from + y][x_starting_from + x]
            if elm in possible_values:
               possible_values.remove(elm)
      return possible_values

   def solved(self):
      if len(self.cells) == 0:
         return True
      return False

   def legalSolution(self):
      legal_values = range(1, 10)
      # first check rows
      for y in range(0, 9):
         row_values = []
         for x in range(0, 9):
            row_values.append(self.grid[y][x])
         if not sorted(row_values) == legal_values:
            return False

      # then check cols
      for x in range(0, 9):
         col_values = []
         for y in range(0, 9):
            col_values.append(self.grid[y][x])
         if not sorted(col_values) == legal_values:
            return False

      # finally check sections
      sections = {k: [] for k in range(0, 9)}
      for y in range(0, 9):
         for x in range(0, 9):
            sections[self.calcSectionNumber(x, y)].append(self.grid[y][x])

      for key, value in sections.iteritems():
         if not sorted(value) == legal_values:
            return False

      return True

   def calcSectionNumber(self, x, y):
      x_starting_from = (x // 3) * 3
      y_starting_from = (y // 3) * 3

      return ((x_starting_from + 3) / 3) + y_starting_from - 1

   def checkCellsForSingles(self):
      updates = 0
      for cell in self.cells:
         if len(cell.possible_values) == 1:
            # set grid cell as the cell.
            self.grid[cell.y][cell.x] = cell.possible_values[0]
            # cell has been found so remove
            self.cells.remove(cell)
            updates += 1
      return updates

   def getCellsByRow(self):
      rows = {k: [] for k in range(9)}
      for cell in self.cells:
         rows[cell.y].append(cell)

      return rows

   def getCellsByColumn(self):
      cols = {k: [] for k in range(9)}
      for cell in self.cells:
         cols[cell.x].append(cell)

      return cols

   def getCellsBySection(self):
      # first split the possible cells into sections:
      sections = {k: [] for k in range(9)}

      # separate the cells into the sections they belong too
      for cell in self.cells:
         sections[self.calcSectionNumber(cell.x, cell.y)].append(cell)

      return sections

   def soleCandidate(self):

      # initial value to enter the while loop
      updates = 1 

      # want to loop until no more updates are made
      while updates > 0:
         for cell in self.cells:
            # get values for sets to compare
            notInRow = self.getValuesNotInRow(cell)
            notInColumn = self.getValuesNotInColumn(cell)
            notInSection = self.getValuesNotInSection(cell)
            possible_values = sorted(set(notInRow) & set(notInColumn) & set(notInSection))

            cell.possible_values = possible_values
         
         updates = self.checkCellsForSingles()

   def uniqueCandidate(self):
      changed = False

      # loop through each possible value in the section and find 
      # possible values only there once.
      sections = self.getCellsBySection()

      # loop through each section
      for section in sections:
         # going to identify unique values in each section
         # by assigning cells to a dict with their values
         values = {k: [] for k in range(1, 10)}

         # loop through each cell in the section
         for cell in sections[section]:

            # loop through each value in the possible values
            for value in cell.possible_values:
               # append to the dict list
               values[value].append(cell)

         # which values are only in the section once?
         for value in values:
            if len(values[value]) == 1:
               # only one possible value so update the grid and 
               # remove the cell from the possible values
               changed = True
               cell = values[value][0]
               self.grid[cell.y][cell.x] = value
               self.cells.remove(cell) 

      return changed      

   def checkCellsByRow(self):
      # Used this solution for identifying unique values
      # http://stackoverflow.com/questions/17035577/unique-features-between-multiple-lists
      
      changed = False

      # get the cells by rows
      rows = self.getCellsByRow()

      # set variables
      all_possible_value_lists = []

      # loop through each row
      for key, row in rows.iteritems():
         # skip empty rows
         if len(row) == 0:
            continue

         # first add all possible values to a list
         for cell in row:
            all_possible_value_lists.append(cell.possible_values)

         # loop again through row
         for cell in row:
            # Combine all the lists into one
            super_list = list(chain(*all_possible_value_lists))
            # Remove the items from the list under consideration
            for x in cell.possible_values:
               super_list.remove(x)
            # Get the unique items remaining in the combined list
            super_set = set(super_list)
            # Compute the unique items in this list and print them
            uniques = set(cell.possible_values) - super_set
            if len(uniques) == 1 and len(cell.possible_values) == 1:
               changed = True
               self.grid[cell.y][cell.x].possible_values = list(uniques)
               self.cells.remove(cell)

      return changed
         
   def checkCellsByColumn(self):
      # Used this solution for identifying unique values
      # http://stackoverflow.com/questions/17035577/unique-features-between-multiple-lists
      
      changed = False

      # get the cells by cols
      cols = self.getCellsByColumn()

      # set variables
      all_possible_value_lists = []

      # loop through each col
      for key, col in cols.iteritems():
         # skip empty cols
         if len(col) == 0:
            continue

         # first add all possible values to a list
         for cell in col:
            all_possible_value_lists.append(cell.possible_values)

         # loop again through col
         for cell in col:
            # Combine all the lists into one
            super_list = list(chain(*all_possible_value_lists))
            # Remove the items from the list under consideration
            for x in cell.possible_values:
               super_list.remove(x)
            # Get the unique items remaining in the combined list
            super_set = set(super_list)
            # Compute the unique items in this list and print them
            uniques = set(cell.possible_values) - super_set
            if len(uniques) == 1 and len(cell.possible_values) == 1:
               changed = True
               self.grid[cell.y][cell.x].possible_values = list(uniques)
               self.cells.remove(cell)

      return changed
         
   def nakedSubset(self):

      changed = False

      # loop through each cell and check against all other cells to identify duplicates
      # and assign to the duplicates list
      duplicates_list = []

      # assign puzzle cells to a temp variable so we can pop without effecting the original
      # list
      puzzle_cells = self.cells[:]

      for index, cell in enumerate(puzzle_cells):
         duplicate_list = []
         # only need to compare to the remainder of the list, as comparisons already
         # made with earlier cells.
         for i in range(index + 1, len(puzzle_cells)):
            try:
               # do the cells match?
               if cell.possible_values == puzzle_cells[i].possible_values:
                  # if so add to duplicate list
                  duplicate_list.append(puzzle_cells[i])
                  # remove the cells so it's not added twice
                  puzzle_cells.pop(i)
            
            except IndexError:
               # need to handle as the popping changes the length
               # of the list, so throws index out of range
               break

         # if there's been any duplicates
         if len(duplicate_list) > 0:
            # add the element we've compared to the list.
            # I like to add this to the front.
            duplicate_list.insert(0, cell)
            # append the list to the duplicates list.
            duplicates_list.append(duplicate_list)

      # loop through each of the duplicates
      for duplicate_list in duplicates_list:
         
         # get the length of the duplicates we're checking
         duplicate_values = duplicate_list[0].possible_values
         duplicate_length = len(duplicate_values)
         
         # list to mark the rows and columns of duplicates
         x_list = [[] for _ in xrange(9)]
         y_list = [[] for _ in xrange(9)]
         
         # loop through each cell in the list
         # and add to the x and y list.
         for cell in duplicate_list:
            x_list[cell.x].append(cell)
            y_list[cell.y].append(cell)

         # now need to loop through the x list
         # and find indexes where the length 
         # of the list is the same size as the duplicate
         # list.
         for index, sublist in enumerate(x_list):
            if len(sublist) == duplicate_length:
               # found what we're looking for, so need to 
               # remove the duplicate values from 
               # all other cells with x == index

               # loop through each of the duplicates
               for value in duplicate_values:
                  # loop through each cell
                  for cell in self.cells:
                     if cell.x == index and value in cell.possible_values and cell not in sublist:
                        changed = True
                        cell.possible_values.remove(value)

         # and repeat for y list
         for index, sublist in enumerate(y_list):
            if len(sublist) == duplicate_length:
               # found what we're looking for, so need to 
               # remove the duplicate values from 
               # all other cells with y == index

               # loop through each of the duplicates
               for value in duplicate_values:
                  # loop through each cell
                  for cell in self.cells:
                     if cell.y == index and value in cell.possible_values and cell not in sublist:
                        changed = True
                        cell.possible_values.remove(value)




      # now loop through and find any possible value lists that are length 
      # 1 and update the grid.
      self.checkCellsForSingles()

      return changed

   def xWing(self):
      # See www.sudokuwiki.org/x_wing_strategy
      # this is not working... getting unexpected results :s
      changed = False


      cells_by_row = list_to_iterate = self.getCellsByRow()
      cells_by_col = self.getCellsByColumn()

      # for each possible value 
      for value in range(1, 10):
         # reset variables
         value_list = []
         xwing = []
         xwing_found = False

         # loop through each row / col
         for index, sublist in list_to_iterate.iteritems():
            # reset variable
            cell_list = []
            # for each cell in the row / col
            for cell in sublist:
               if value in cell.possible_values:
                  # value is in cell
                  cell_list.append(cell)

            # if two elms in a row then add to value list
            if len(cell_list) == 2:
               value_list.append(cell_list)
         


         # is there an x wing?
         if len(value_list) > 1:

            j = 1

            # loop through each row/col in the value list
            for sublist in value_list:

               # assign top right and left to variables
               top_left = sublist[0]
               top_right = sublist[1]

               # just need to check values against rest of value list
               for i in range(j, len(value_list)):
                  next_row = value_list[i]

                  if next_row[0].x == top_left.x and next_row[1].x == top_right.x:
                     # we have an xwing!
                     xwing_found = True
                     # build the xwing grid
                     xwing.append([top_left, top_right])
                     xwing.append([next_row[0], next_row[1]])

               j += 1


         if xwing_found:
            # woo!
            # loop through all cells in both rows and remove the 
            # possible values of value
            top_row = xwing[0][0].y
            bottom_row = xwing[1][1].y
            left_col = xwing[0][0].x
            right_col = xwing[1][1].x
            
            for i, r in enumerate([left_col, right_col]):
               for c in cells_by_col[r]:
                  # don't touch a cell in the xwing
                  if c not in xwing[i]:
                     if value in c.possible_values:
                        # c.printCell()
                        changed = True
                        c.possible_values.remove(value)
            



      self.checkCellsForSingles()

      return changed

   def swordfish(self):
      # this needs some work. Need to improve my understanding
      # of this technique, as not 100% this is the correct approach.
      # Going to try an x-wing as this is an extension of that.

      # first need to identify the swordfish pattern.

      cells_by_row = self.getCellsByRow()
      cells_by_col = self.getCellsByColumn()

      # loop through each cell
      for cell in self.cells:
         # for each value in the possible values
         for value in cell.possible_values:
            # intialise variables
            cell_list = [cell]
            # failed_list = []
            value_found = True
            swordfish_found = False
            this_cell = cell

            while value_found and not swordfish_found:

               value_found = False

               # first check the row
               for row_cell in cells_by_row[this_cell.y]:
                  # skip if the same cell
                  if row_cell == this_cell:
                     continue

                  # is value in row cells values?
                  if value in row_cell.possible_values:
                     # move this cell along to next cell
                     this_cell = row_cell
                     # set value found as true
                     value_found = True
                     
                     # check to see if the swordfish has complete
                     if this_cell == cell:
                        swordfish_found = True
                     else:
                        cell_list.append(row_cell)

                     # break the loop
                     break

               if not value_found:
                  # todo: need to pop last element
                  # and try another route. For now
                  # ignoring this complication
                  continue
               
               if not swordfish_found:

                  # check column of new cell
                  for col_cell in cells_by_col[this_cell.x]:
                     # skip if the same cell 
                     if col_cell == this_cell:
                        continue

                     # is value in col cells values
                     if value in col_cell.possible_values:
                        # move this cell along to next cell
                        this_cell = col_cell
                        # set value found as true
                        value_found = True
                        
                        # check to see if the swordfish has complete
                        if this_cell == cell:
                           swordfish_found = True
                        else:
                           cell_list.append(col_cell)

                        # break the loop
                        break

                  if not value_found:
                     # same as above todo
                     continue
               

            if swordfish_found:

               print 'Value: %s and cell length: %s'  % (value, len(cell_list))
               for c in cell_list:
                  c.printCell()
               print '________________________'

   def solve(self, i=0):
      """
      Will execute each of the techniques
      and if changed will call itself
      """
      # increment recusion counter
      i+=1

      # set max recursion
      if i == 200:
         # safeguard to handle recusion error
         return False

      if self.solved():
         # base case for recursion
         # if solved terminate
         return True

      self.soleCandidate()

      if self.uniqueCandidate():
         self.solve(i)
      if self.nakedSubset():
         self.solve(i)
      if self.checkCellsByRow():
         self.solve(i)
      if self.checkCellsByColumn():
         self.solve(i)
      if self.xWing():
         self.solve(i)

      return False






class Cell:
   """
   A cell is an element that is yet to be found
   """
   def __init__(self, x, y):
      self.x = x
      self.y = y
      self.possible_values = []


   def printCell(self):
      print '[%s][%s] : %s' % (self.x, self.y, self.possible_values)






soduku_text = """Grid 01
003020600
900305001
001806400
008102900
700000008
006708200
002609500
800203009
005010300
Grid 02
200080300
060070084
030500209
000105408
000000000
402706000
301007040
720040060
004010003
Grid 03
000000907
000420180
000705026
100904000
050000040
000507009
920108000
034059000
507000000
Grid 04
030050040
008010500
460000012
070502080
000603000
040109030
250000098
001020600
080060020
Grid 05
020810740
700003100
090002805
009040087
400208003
160030200
302700060
005600008
076051090
Grid 06
100920000
524010000
000000070
050008102
000000000
402700090
060000000
000030945
000071006
Grid 07
043080250
600000000
000001094
900004070
000608000
010200003
820500000
000000005
034090710
Grid 08
480006902
002008001
900370060
840010200
003704100
001060049
020085007
700900600
609200018
Grid 09
000900002
050123400
030000160
908000000
070000090
000000205
091000050
007439020
400007000
Grid 10
001900003
900700160
030005007
050000009
004302600
200000070
600100030
042007006
500006800
Grid 11
000125400
008400000
420800000
030000095
060902010
510000060
000003049
000007200
001298000
Grid 12
062340750
100005600
570000040
000094800
400000006
005830000
030000091
006400007
059083260
Grid 13
300000000
005009000
200504000
020000700
160000058
704310600
000890100
000067080
000005437
Grid 14
630000000
000500008
005674000
000020000
003401020
000000345
000007004
080300902
947100080
Grid 15
000020040
008035000
000070602
031046970
200000000
000501203
049000730
000000010
800004000
Grid 16
361025900
080960010
400000057
008000471
000603000
259000800
740000005
020018060
005470329
Grid 17
050807020
600010090
702540006
070020301
504000908
103080070
900076205
060090003
080103040
Grid 18
080005000
000003457
000070809
060400903
007010500
408007020
901020000
842300000
000100080
Grid 19
003502900
000040000
106000305
900251008
070408030
800763001
308000104
000020000
005104800
Grid 20
000000000
009805100
051907420
290401065
000000000
140508093
026709580
005103600
000000000
Grid 21
020030090
000907000
900208005
004806500
607000208
003102900
800605007
000309000
030020050
Grid 22
005000006
070009020
000500107
804150000
000803000
000092805
907006000
030400010
200000600
Grid 23
040000050
001943600
009000300
600050002
103000506
800020007
005000200
002436700
030000040
Grid 24
004000000
000030002
390700080
400009001
209801307
600200008
010008053
900040000
000000800
Grid 25
360020089
000361000
000000000
803000602
400603007
607000108
000000000
000418000
970030014
Grid 26
500400060
009000800
640020000
000001008
208000501
700500000
000090084
003000600
060003002
Grid 27
007256400
400000005
010030060
000508000
008060200
000107000
030070090
200000004
006312700
Grid 28
000000000
079050180
800000007
007306800
450708096
003502700
700000005
016030420
000000000
Grid 29
030000080
009000500
007509200
700105008
020090030
900402001
004207100
002000800
070000090
Grid 30
200170603
050000100
000006079
000040700
000801000
009050000
310400000
005000060
906037002
Grid 31
000000080
800701040
040020030
374000900
000030000
005000321
010060050
050802006
080000000
Grid 32
000000085
000210009
960080100
500800016
000000000
890006007
009070052
300054000
480000000
Grid 33
608070502
050608070
002000300
500090006
040302050
800050003
005000200
010704090
409060701
Grid 34
050010040
107000602
000905000
208030501
040070020
901080406
000401000
304000709
020060010
Grid 35
053000790
009753400
100000002
090080010
000907000
080030070
500000003
007641200
061000940
Grid 36
006080300
049070250
000405000
600317004
007000800
100826009
000702000
075040190
003090600
Grid 37
005080700
700204005
320000084
060105040
008000500
070803010
450000091
600508007
003010600
Grid 38
000900800
128006400
070800060
800430007
500000009
600079008
090004010
003600284
001007000
Grid 39
000080000
270000054
095000810
009806400
020403060
006905100
017000620
460000038
000090000
Grid 40
000602000
400050001
085010620
038206710
000000000
019407350
026040530
900020007
000809000
Grid 41
000900002
050123400
030000160
908000000
070000090
000000205
091000050
007439020
400007000
Grid 42
380000000
000400785
009020300
060090000
800302009
000040070
001070500
495006000
000000092
Grid 43
000158000
002060800
030000040
027030510
000000000
046080790
050000080
004070100
000325000
Grid 44
010500200
900001000
002008030
500030007
008000500
600080004
040100700
000700006
003004050
Grid 45
080000040
000469000
400000007
005904600
070608030
008502100
900000005
000781000
060000010
Grid 46
904200007
010000000
000706500
000800090
020904060
040002000
001607000
000000030
300005702
Grid 47
000700800
006000031
040002000
024070000
010030080
000060290
000800070
860000500
002006000
Grid 48
001007090
590080001
030000080
000005800
050060020
004100000
080000030
100020079
020700400
Grid 49
000003017
015009008
060000000
100007000
009000200
000500004
000000020
500600340
340200000
Grid 50
300200000
000107000
706030500
070009080
900020004
010800050
009040301
000702000
000008006"""

   
if __name__ == '__main__':
   solveProblem()

