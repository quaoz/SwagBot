from discord import Embed


def draw_grid(grid):
	cols = len(grid[0])
	rows = len(grid)

	rendered_grid = '```┏'
	for i in range(0, cols - 1):
		rendered_grid += '━━━┳'
	rendered_grid += '━━━┓\n'

	for i in range(0, rows):
		rendered_grid += '┃'

		for j in range(0, cols):
			rendered_grid += f' {grid[i][j]} ┃'

		if i != rows - 1:
			rendered_grid += '\n┣'
			for k in range(0, cols - 1):
				rendered_grid += '━━━╋'
			rendered_grid += '━━━┫\n'

	rendered_grid += '\n┗'
	for i in range(0, cols - 1):
		rendered_grid += '━━━┻'
	rendered_grid += '━━━┛\n```'

	embed = Embed(title='Connect Four', description=rendered_grid)
	return embed


def has_won(grid, token):
	width = len(grid[0]) - 1  # cols
	height = len(grid) - 1    # rows

	# Horizontal check
	for j in range(0, height - 3):
		for i in range(0, width):
			if grid[i][j] == token and grid[i][j + 1] == token and grid[i][j + 2] == token and grid[i][j + 3] == token:
				return True

	# Vertical check
	for i in range(0, width - 3):
		for j in range(0, height):
			if grid[i][j] == token and grid[i + 1][j] == token and grid[i + 2][j] == token and grid[i + 3][j] == token:
				return True

	# Ascending diagonal check
	for i in range(3, width):
		for j in range(0, height - 3):
			if grid[i][j] == token and grid[i - 1][j + 1] == token and grid[i - 2][j + 2] == token and grid[i - 3][
				j + 3] == token:
				return True

	# Descending diagonal check
	for i in range(3, width):
		for j in range(3, height):
			if grid[i][j] == token and grid[i - 1][j - 1] == token and grid[i - 2][j - 2] == token and grid[i - 3][
				j - 3] == token:
				return True
