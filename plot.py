import os
import numpy as np
import cv2
from moviepy.editor import *
from natsort import natsorted
from matplotlib import pyplot as plt
from matplotlib import animation, image
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

def rotate_bound(image_h, angle):
    """ rotate png image (image_h) by given angle """
    
    # grab the dimensions of the image and then determine the
    # center
    (h, w) = image_h.shape[:2]
    (cX, cY) = (w // 2, h // 2)

    # grab the rotation matrix (applying the negative of the
    # angle to rotate clockwise), then grab the sine and cosine
    # (i.e., the rotation components of the matrix)
    M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])

    # compute the new bounding dimensions of the image
    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))

    # adjust the rotation matrix to take into account translation
    M[0, 2] += (nW / 2) - cX
    M[1, 2] += (nH / 2) - cY

    # perform the actual rotation and return the image
    return cv2.warpAffine(image_h, M, (nW, nH), borderValue=(255,255,255))


def create_animation(position, velocity, angles, iteration_str, xylimits=np.array([2000, 2000]), view='both'):
    """
        view: 'top', 'side' or 'both'(default)
        xylimits: size of single plot. default 2000*2000*2000
    """
    centre = xylimits / 2
    
    # read in our fly png file
    path_top = 'fly_top.png'
    path_side = 'fly_side.png'
    im_top = image.imread(path_top)
    im_side = image.imread(path_side)

    figsize = (9,4)
    if view == 'top':
        ax_side = plt.axes()
        fig, ax_top = plt.subplots(nrows=1, ncols=1, figsize=figsize)
    elif view == 'side':
        ax_top = plt.axes()
        fig, ax_side = plt.subplots(nrows=1, ncols=1, figsize=figsize)
    elif view == 'both':
        fig, [ax_top, ax_side] = plt.subplots(nrows=1, ncols=2, figsize=figsize, sharex=True)

    # ax = plt.axes(xlim=(0, limits[0]), ylim=(0, limits[1]), aspect='equal')
    
    for ax in [ax_top, ax_side]:
        
        ax.set_aspect('equal')

        ax.set_xticks([])
        ax.set_yticks([])
        
        ax.set_xlim([0, xylimits[0]])
        
    ax_top.set_ylim([0, xylimits[1]])
    ax_side.set_ylim([0, xylimits[2]])
    
    """ axes directions """
    arrow_x_start = xylimits[0] * 0.06
    arrow_y_start = xylimits[1] * 0.06
    arrow_z_start = xylimits[2] * 0.06
    
    arrow_length = 0.05 * xylimits[0]
    arrow_width = 0.005 * xylimits[0]
    
    ax_top.arrow(arrow_x_start, arrow_y_start, arrow_length , 0, width=arrow_width, length_includes_head=True, color='k')
    ax_top.arrow(arrow_x_start, arrow_y_start, 0, arrow_length, width=arrow_width, length_includes_head=True, color='k')
    
    ax_side.arrow(arrow_x_start, arrow_z_start, arrow_length , 0, width=arrow_width, length_includes_head=True, color='k')
    ax_side.arrow(arrow_x_start, arrow_z_start, 0, arrow_length, width=arrow_width, length_includes_head=True, color='k')

    """ hanging object """
    hanging_size = np.sqrt(np.product(xylimits)) * 0.1
    hanging_size = (np.product(xylimits) ** (1/3)) * 0.1
    hanging_radius = hanging_size
    hanging_points_N = 100
    hanging_theta = np.linspace(0, 2*np.pi, hanging_points_N, endpoint=False)
    hanging_x = hanging_radius * np.cos(hanging_theta) + centre[0]
    hanging_y = hanging_radius * np.sin(hanging_theta) + centre[1]
    hanging_z = (xylimits[2] * 0.75) * np.ones(hanging_points_N)
    ax_top.plot(hanging_x, hanging_y, 'k')
    ax_side.plot(hanging_x, hanging_z, 'k')

    """ flies """
    def plot_images(plot_x, plot_y, angle, input_image, ax=None):
        ax = ax or plt.gca()

        for xi, yi, theta in zip(plot_x, plot_y, angle):
            rotated = rotate_bound(input_image, theta)
            im = OffsetImage(rotated, zoom=0.03)
            im.image.axes = ax

            ab = AnnotationBbox(im, (xi,yi), frameon=False, pad=0.0)

            ax.add_artist(ab)

    
    for fly_idx in range(position.shape[1]):
        plot_images(position[0, :], position[1, :], angles[:], im_top, ax=ax_top)
        plot_images(position[0, :], position[2, :], angles[:], im_side, ax=ax_side)


    """ progress text """
    iteration_text = ax_top.text(0.06*xylimits[0], 0.91*xylimits[1], "Iteration " + iteration_str)
    
    """ axes directions text """
    xtext_loc = arrow_x_start + arrow_length*1.5
    ytext_loc = arrow_y_start + arrow_length*1.5
    arrow_offset = 0.2*arrow_length
    ax_top.text(xtext_loc, arrow_y_start - arrow_offset, 'x')
    ax_top.text(arrow_x_start - arrow_offset, ytext_loc, 'y')
    
    ax_side.text(xtext_loc, arrow_y_start - arrow_offset, 'x')
    ax_side.text(arrow_x_start - arrow_offset, ytext_loc, 'z')

    # def animate(frame, state, state_clock, flight_clock, turn_direction, position, velocity):
    #     state, state_clock, flight_clock, turn_direction, position, velocity = update_boids(state, state_clock, flight_clock, turn_direction, position, velocity)
    #     scatter.set_offsets(position.transpose())
    
    
    def animate(frame):
    
        return
    
    frame_interval = 50

    # anim = animation.FuncAnimation(fig, animate, fargs=(state, state_clock, flight_clock, turn_direction, position, velocity), frames=50, interval=frame_interval)
    anim = animation.FuncAnimation(fig, animate, frames=50, interval=frame_interval)


    fig.tight_layout()


    if not os.path.exists('results/'):
        os.mkdir('results/')
    anim.save('results/lesser_house_boids_'+ iteration_str + '.mp4', writer="ffmpeg")
    
    
def create_progress_animation(results_folder, iterations_list):

    L = []
    for root, dirs, files in os.walk(results_folder):
        files = natsorted(files)
        for file in files:
            if os.path.splitext(file)[1] == '.mp4':
                filePath = os.path.join(root, file)
                video = VideoFileClip(filePath)
                L.append(video)

    final_clip = concatenate_videoclips(L)
    final_clip.write_gif("progress.gif")
    
    return
    