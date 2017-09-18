import pygame
import numpy as np
import random

SCR_DIM = (800, 600)
black = (0,0,0)
white = (250,250,250)

def main():
	pygame.init()
	
	screen = pygame.display.set_mode(SCR_DIM)
	clock = pygame.time.Clock()
	screen.fill((0,0,255))
	exit = False
	arr = np.zeros((80,60), dtype='int32')
	arr = rand_fill(arr)
	"""arr[11][10] = 1
	arr[12][10] = 1
	arr[13][10] = 1
	arr[10][11] = 1
	arr[11][11] = 1
	arr[12][11] = 1"""

	while not exit:
		clock.tick(25)
		screen.fill((200,0,0))
		for (x, row) in enumerate(arr):
			for (y, cell) in enumerate(row):
				if arr[x][y] == 0:
				    pygame.draw.rect(screen, (0,0,0), (x * 10, y * 10 ,10,10), 0)
				else:
					pygame.draw.rect(screen, white, (x * 10, y * 10 ,10,10), 0)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit = True
		arr = life_iter(arr)
		pygame.display.flip()

def rand_fill(a):
	f = a
	for (i, row) in enumerate(a):
		for (j, value) in enumerate(row):
			f[i][j] = random.randrange(2)
	return f

def life_iter(a):
	f = np.zeros((80,60), dtype='int32')
	for (i, row) in enumerate(f):
		for (j, value) in enumerate(row):
			live_count = 0
			live_count += check_n(a, i-1, j-1)
			live_count += check_n(a, i, j-1)
			live_count += check_n(a, i+1, j-1)
			live_count += check_n(a, i-1, j)
			live_count += check_n(a, i+1, j)
			live_count += check_n(a, i+1, j+1)
			live_count += check_n(a, i, j+1)
			live_count += check_n(a, i-1, j+1)
			live_count += 0

			if a[i][j] == 1 and live_count < 2 or live_count > 3:
				f[i][j] = 0
			elif a[i][j] == 1 and live_count == 2 or live_count == 2:
				pass
			elif a[i][j] == 0  and live_count == 3:
				f[i][j] = 1
	return f

def check_n(ar, x, y):
	try:
		return ar[x][y]
	except IndexError:
		return 0

if __name__ == "__main__":
    main()
