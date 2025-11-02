import tkinter as tk
import time
import colorsys

class HilbertCurve:
    def __init__(self, order=1, size=512):
        self.root = tk.Tk()
        self.root.title("Hilbert Curve Visualizer")

        self.size = size
        self.canvas = tk.Canvas(self.root, width=size, height=size, bg="black")
        self.canvas.pack()

        self.order = order
        self.N = 2 ** order
        self.total_points = self.N ** 2
        self.length = self.size / self.N
        print("Total Points: ", self.total_points)
    
    def hilbert(self, i):
        """ Method to return 2D coordinates from 1D index """

        # Base coordinates
        points = [
            [0, 0], [0, 1], [1, 1], [1, 0]
        ]

        index = i & 3
        coord = points[index]

        for j in range(1, self.order):
            i = i >> 2 # shift to get the quadrant location
            index = i & 3 # quadrant index

            # offset increases to the power of j
            offset = 2 ** j

            if index == 0: # first quadrant
                # Anti-clockwise rotation -> this swap only updates point 1 and 3 while point 0 and 2 remains unchanged
                coord[0], coord[1] = coord[1], coord[0]

            elif index == 1:
                coord[1] += offset
            
            elif index == 2:
                coord[0] += offset
                coord[1] += offset

            elif index == 3:
                # Clockwise rotation -> this swap with values subtracted from 1 udpates point 0 and 2, while keeping 1 and 3 unchanged
                coord[0], coord[1] = offset - 1 - coord[1], offset - 1 - coord[0]
                coord[0] += offset

        return coord

    def generate_curve(self):
        all_points = []

        for i in range(self.total_points):
            point = self.hilbert(i)
            # converting corner coords to center of quadrant coord
            coord = [coord * self.length + self.length / 2 for coord in point]
            all_points.append(coord)

        all_colors = self.generate_colors()

        for i in range(len(all_points) - 1):
            # self.draw_point(*all_points[i], i)
            self.draw_line(*all_points[i], *all_points[i + 1], line_color=all_colors[i])
        # self.draw_point(*all_points[-1], len(all_points) - 1)

    
    def generate_colors(self):
        colors = []

        for i in range(self.total_points):
            hue = i / self.total_points
            # full saturation and brightness
            r, g, b = colorsys.hsv_to_rgb(hue, 1.0, 1.0)

            # rbg to hex
            hex_color = f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"
            colors.append(hex_color)

        return colors

    def draw_point(self, x, y, name, text_offset=10):
        r = 3

        self.canvas.create_oval(x - r, y - r, x + r, y + r, fill="white", outline="white")
        self.canvas.create_text(x + text_offset, y - text_offset, text=f"{name}", fill="white", anchor="nw", font=("Courier", 8))
        self.root.update()

    def draw_line(self, x1, y1, x2, y2, line_color="white", delay=0):
        self.canvas.create_line(x1, y1, x2, y2, fill=line_color, width=2)

        self.root.update()
        if delay > 0:
            time.sleep(delay)

    def run(self):
        self.root.mainloop()



if __name__ == "__main__":
    app = HilbertCurve(order=8, size=1024)
    app.generate_curve()
    app.run()