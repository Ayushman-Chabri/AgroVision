import matplotlib.pyplot as plt

def draw_line(x1, y1, x2, y2):
    plt.plot([x1, x2], [y1, y2], 'k-')

def draw_h_tree(x, y, length, level, factor=2):
    if level == 0:
        return
    
    # Calculate half-length
    half = length / 2
    
    # Coordinates of the H
    left_x = x - half
    right_x = x + half
    top_y = y + half
    bottom_y = y - half
    
    # Draw the H
    draw_line(left_x, top_y, left_x, bottom_y)   # left vertical
    draw_line(right_x, top_y, right_x, bottom_y) # right vertical
    draw_line(left_x, y, right_x, y)             # connecting horizontal
    
    # Recursive calls for 4 new H-trees
    draw_h_tree(left_x, top_y, length / factor, level - 1, factor)
    draw_h_tree(left_x, bottom_y, length / factor, level - 1, factor)
    draw_h_tree(right_x, top_y, length / factor, level - 1, factor)
    draw_h_tree(right_x, bottom_y, length / factor, level - 1, factor)

# Example: Draw H-tree of level 4
plt.figure(figsize=(6, 6))
draw_h_tree(0, 0, 100, 4)
plt.axis('equal')
plt.show()
