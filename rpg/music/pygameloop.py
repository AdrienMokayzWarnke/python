import pygame
import numpy as np
import wave
import bisect

pygame.init()
pygame.mixer.set_num_channels(2)

#file = './music/pip_song.wav'
file = './music/payo.wav'
music = pygame.mixer.Sound(file)
wav_file = wave.open(file,'r')
channels = wav_file.getnchannels()
fs = wav_file.getframerate()
music_data = np.frombuffer(wav_file.readframes(-1), dtype=np.int16)
music_left_data, music_right_data = music_data[0::2], music_data[1::2]
 
display_width = 1200
display_height = 700
center = ((display_width/2),(display_height/2))

black = (0,0,0)
white = (255,255,255)
red = (255, 0, 0)
blue = (0, 0, 255)

x_offset = 10
y_offset = 20

triangle_play_points = [(display_width/2+x_offset, display_height/2), (display_width/2-x_offset, display_height/2+y_offset), (display_width/2-x_offset,display_height/2-y_offset)]

lines_play_points = [[(display_width/2-x_offset, display_height/2+y_offset),(display_width/2-x_offset, display_height/2-y_offset)],[(display_width/2+x_offset, display_height/2+y_offset),(display_width/2+x_offset, display_height/2-y_offset)]]

pause = False

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Music player')
clock = pygame.time.Clock()

def draw_triange(points):
    return pygame.draw.polygon(gameDisplay, white, points)

def draw_lines(points) -> list[pygame.Rect]: 
    lines = []
    for point in points:
        lines.append(pygame.draw.line(gameDisplay, white, point[0], point[1], 5))
    return lines

def get_color_by_channel(channel:int):
    if channel == 0:
        return red
    else:
        return blue
    
def print_music(music_visual: list[float], channel:int, ratio:float, position:float):
    width_rect = display_width/len(music_visual)
    max_height = display_height*ratio
    y_pos = display_height*position
    max_value = max(music_visual)
    #print(f'width rect {width_rect}')
    for i in range(len(music_visual)):
        value = 0
        color_rect = get_color_by_channel(channel)
        if i%2 != 0 and i+1 < len(music_visual):
            value = (abs(music_visual[i-1]) + abs(music_visual[i+1]))/2
        else:
            value = music_visual[i]
        height_rect = abs(value/max_value * max_height)
        y_pos_rect = y_pos - height_rect/2
        x_pos_rect = width_rect*i
        pygame.draw.rect(gameDisplay, color_rect, (x_pos_rect, y_pos_rect, width_rect*0.99, height_rect))

def print_music_frequency(music_visual: list[float], channel:int, ratio:int):
    frequencies = [0, 500, 1000, 2000, 3000, 4000, 5000, 7000, 9000, 11000, 13000, 15000, 30000]
    occurencies = count_values_between_milestones(frequencies, music_visual)
    if(channel == 0):
        occurencies.reverse()
    width_rect = display_width/(2*len(occurencies))
    max_height = display_height*ratio
    max_value = max(occurencies)
    x_offset = 0
    if channel == 1:
        x_offset = display_width/2
    #print(f'width rect {width_rect}')
    for i in range(len(occurencies)):
        color_rect = get_color_by_channel(channel)
        value = occurencies[i]
        height_rect = abs(value/max_value * max_height)
        y_pos_rect = display_height - height_rect
        x_pos_rect = x_offset + (width_rect*i)
        print(f'rectangle {i} drawned at position x:{x_pos_rect}, y:{y_pos_rect}, x_offset:{x_offset}, width:{width_rect}, height:{height_rect}')
        pygame.draw.rect(gameDisplay, color_rect, (x_pos_rect, y_pos_rect, width_rect*0.99, height_rect))
    

def count_values_between_milestones(milestones, values):
    # Initialize the solution array with zeros
    solution = [0] * (len(milestones) - 1)
    
    # Sort the values array for efficient processing
    sorted_values = np.copy(values)
    sorted_values.sort()
    
    # Iterate through each value
    for value in values:
        # Find the appropriate range using binary search
        index = bisect.bisect_right(milestones, abs(value)) - 1
        if 0 <= index < len(solution):
            solution[index] += 1
    
    return solution

def quitgame():
    pygame.quit()
    quit()

def game_loop():
    gameDisplay.fill(black)
    gameExit = False
    channel = music.play()
    music_visual_left = []
    music_visual_right = []
    frame_rate = 10
    global pause
    frame_per_update = fs/frame_rate
    print(f'frames pour une seconde d\'audio {fs}')
    print(f'channels {channels}')
    frame = 0
    ratio = 1/4
    skip_precision = 60 # 20 en 20
    skip_frequency = int(frame_per_update/skip_precision)

    while not gameExit:
        gameDisplay.fill(black)
        if(pause):
            draw_lines(lines_play_points)
        else:
            draw_triange(triangle_play_points)
            frame_per_update_start = int(frame_per_update * frame)
            frame_per_update_end = int(frame_per_update * (frame + 5))
            frame += 1
            music_visual_left = music_left_data[frame_per_update_start:frame_per_update_end:skip_frequency]
            music_visual_right = music_right_data[frame_per_update_start:frame_per_update_end:skip_frequency]
            print(f'frame n°: {frame}')
            print(f'nombre de données par frame {len(music_visual_left)}')
            print(f'frame start {frame_per_update_start}')
            print(f'frame end {frame_per_update_end}')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if pause:
                        channel.unpause()
                        pause = False
                    else:
                        channel.pause()
                        pause = True
        print_music(music_visual_left, 0, ratio, 1/8)
        print_music(music_visual_right, 1, ratio, 3/8)
        print_music_frequency(music_visual_left, 0, 1/3)
        print_music_frequency(music_visual_right, 1, 1/3)
        pygame.display.update()
        clock.tick(frame_rate)
game_loop()
pygame.quit()
quit()