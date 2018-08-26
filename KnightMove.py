import threading
from queue import Queue

'''--------------------UI & User Input---------------------'''
print("Given the sample CHESS BOARD")
print()
print("-------------------------------------------------")
print("|  57 |  58 |  59 |  60 |  61 |  62 |  63 |  64 |")
print("-------------------------------------------------")
print("|  49 |  50 |  51 |  52 |  53 |  54 |  55 |  56 |")
print("-------------------------------------------------")
print("|  41 |  42 |  43 |  44 |  45 |  46 |  47 |  48 |")
print("-------------------------------------------------")
print("|  33 |  34 |  35 |  36 |  37 |  38 |  39 |  40 |")
print("-------------------------------------------------")
print("|  25 |  26 |  27 |  28 |  29 |  30 |  31 |  32 |")
print("-------------------------------------------------")
print("|  17 |  18 |  19 |  20 |  21 |  22 |  23 |  24 |")
print("-------------------------------------------------")
print("|  9  |  10 |  11 |  12 |  13 |  14 |  15 |  16 |")
print("-------------------------------------------------")
print("|  1  |  2  |  3  |  4  |  5  |  6  |  7  |  8  |")
print("-------------------------------------------------")
print()
print("Start Index - ", end="")
start_index = int(input())
print("End Index - ", end="")
last_index = int(input())
print("Max no. of allowed Moves(DEFAULT=6) - ", end="")
try:
	max_no_moves = int(input())
except:
	max_no_moves = 6
print("No. of Threads(DEFAULT=500) - ", end="")
try:
	no_of_threads = int(input())
except:
	no_of_threads = 500


possibilities = 0
state_queue = Queue()

'''--------------------Class wrapping Knight properties---------------------'''
class Knight():
	def __init__(self, start_index, last_index, path, move_no):
		self.start_index = start_index
		self.move_no = move_no
		self.last_index = last_index
		self.path = path

	def mv_fw_l(self):
		new_index = self.start_index + 16 - 1
		if new_index > 63 or new_index % 8 == 0:
			return None
		return new_index

	def mv_fw_r(self):
		new_index = self.start_index + 16 + 1
		if new_index > 64 or new_index % 8 == 1:
			return None
		return new_index

	def mv_lt_l(self):
		new_index = self.start_index - 2 - 8
		if new_index < 1 or new_index % 8 in [0, 7]:
			return None
		return new_index

	def mv_lt_r(self):
		new_index = self.start_index - 2 + 8
		if new_index > 62 or new_index % 8 in [0, 7]:
			return None
		return new_index

	def mv_rt_l(self):
		new_index = self.start_index + 2 + 8
		if new_index > 64 or new_index % 8 in [1, 2]:
			return None
		return new_index

	def mv_rt_r(self):
		new_index = self.start_index + 2 - 8
		if new_index < 3 or new_index % 8 in [1, 2]:
			return None
		return new_index

	def mv_bk_l(self):
		new_index = self.start_index - 16 + 1
		if new_index < 2 or new_index % 8 == 1:
			return None
		return new_index

	def mv_bk_r(self):
		new_index = self.start_index - 16 - 1
		if new_index < 1 or new_index % 8 == 0:
			return None
		return new_index

	#Create new Objects representing new moves/states on board
	def next_move(self):
		new_index = self.mv_fw_l()
		if new_index != None and new_index != self.last_index:
			state_queue.put(Knight(new_index, self.start_index, self.path + [new_index], (self.move_no+1)))
		new_index = self.mv_fw_r()
		if new_index != None and new_index != self.last_index:
			state_queue.put(Knight(new_index, self.start_index, self.path + [new_index], (self.move_no+1)))
		new_index = self.mv_lt_l()
		if new_index != None and new_index != self.last_index:
			state_queue.put(Knight(new_index, self.start_index, self.path + [new_index], (self.move_no+1)))
		new_index = self.mv_lt_r()
		if new_index != None and new_index != self.last_index:
			state_queue.put(Knight(new_index, self.start_index, self.path + [new_index], (self.move_no+1)))
		new_index = self.mv_rt_l()
		if new_index != None and new_index != self.last_index:
			state_queue.put(Knight(new_index, self.start_index, self.path + [new_index], (self.move_no+1)))
		new_index = self.mv_rt_r()
		if new_index != None and new_index != self.last_index:
			state_queue.put(Knight(new_index, self.start_index, self.path + [new_index], (self.move_no+1)))
		new_index = self.mv_bk_l()
		if new_index != None and new_index != self.last_index:
			state_queue.put(Knight(new_index, self.start_index, self.path + [new_index], (self.move_no+1)))
		new_index = self.mv_bk_r()
		if new_index != None and new_index != self.last_index:
			state_queue.put(Knight(new_index, self.start_index, self.path + [new_index], (self.move_no+1)))

	def run(self):
		global possibilities
		if self.start_index == last_index:
			possibilities += 1
			print(self.path)
		elif self.move_no < max_no_moves:
			self.next_move()

	def __str__(self):
		return ("Position -> " + str(self.start_index) + "     Move no -> " + str(self.move_no) + "     Path -> " + str(self.path))


#Initiation of code
start_game = Knight(start_index, None, [start_index], 0)
state_queue.put(start_game)

'''--------------------Function called by each Thread---------------------'''
def thread_function():
	while True:
		knight = state_queue.get()
		# print(knight)
		knight.run()
		state_queue.task_done()

'''--------------------Creating no. of Threads---------------------'''
for i in range(no_of_threads):
	 t = threading.Thread(target=thread_function)
	 t.daemon = True
	 t.start()

#Waiting for all Daemon Threads to stop
state_queue.join()
print("No. of ways - ", possibilities)
