import pygame
import numpy as np
import wave

pygame.init()
pygame.mixer.set_num_channels(2)
file = './music/payo.wav'
music = pygame.mixer.Sound(file)
wav_file = wave.open(file,'r')
channels = wav_file.getnchannels()
fs = wav_file.getframerate()
music_data = np.frombuffer(wav_file.readframes(-1), dtype=np.int16)
music_left_data, music_right_data = music_data[0::2], music_data[1::2]
 
display_width = 1200
display_height = 900
center = ((display_width/2),(display_height/2))

black = (0,0,0)
white = (255,255,255)

triangle_play_points = [(670,720),(630,745),(630,695)]

lines_play_points = [[(670,740),(670,700)],[(630,740),(630,700)]]

def draw_triange(points):
    return pygame.draw.polygon(gameDisplay, white, points)

def draw_lines(points) -> list[pygame.Rect]: 
    lines = []
    for point in points:
        lines.append(pygame.draw.line(gameDisplay, white, point[0], point[1], 5))
    return lines

def print_music(music_visual: list[float],channel:int):
    with_rect = display_width/len(music_visual)
    for i in range(len(music_visual)):
        height_rect = 0
        value = 0
        max_height = max(music_visual)

        if i%2 != 0:
            value = (abs(music_visual[i-1]) + abs(music_visual[i+1]))/2
            height_rect = abs(value/max_height * display_height)/2
        else:
            value = music_visual[i]
            height_rect = abs(music_visual[i]/max_height * display_height)/2

        if(channel == 0):
            color_rect = (255, 255, 255)
            if height_rect <= max_height/3:
                color_rect = (150, 150, 0)
        else:
            color_rect = (0, 0, 255)
            if height_rect <= max_height/3:
                color_rect = (0, 0, 150)

        pos_rect = display_height/2 - height_rect/2 # pos_rec = 0
        #if(value < 0):
        #    pos_rect = display_height/2
        #else:
        #    pos_rect = (display_height/2 - height_rect)
        pygame.draw.rect(gameDisplay, color_rect, (i*with_rect, pos_rect, with_rect, height_rect))
        # pygame.draw.rect(gameDisplay, white, (0, 100, 200, 300))

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Music player')
clock = pygame.time.Clock()

pause = False
 
def quitgame():
    pygame.quit()
    quit()

def game_loop():
    global pause
    gameDisplay.fill(black)
    gameExit = False
    channel = music.play()
    music_visual_left = []
    music_visual_right = []
    frame_rate = 10 # 200ms per frame
    frame_per_update = fs/frame_rate # 44 100 / 5 = 8820 par frame
    print(f'frames pour une seconde d\'audio {fs}')
    print(f'channels {channels}')
    frame = 0
    #len()/fs = second
    #second*fs = len()
    #fs = len()/second
    while not gameExit:
        gameDisplay.fill(black)
        if(pause):
            draw_lines(lines_play_points)
        else:
            draw_triange(triangle_play_points)
            # get music visual
            frame_per_update_start = int(frame_per_update * frame)
            frame_per_update_end = int(frame_per_update * (frame + 5))
            frame += 1
            music_visual_left = music_left_data[frame_per_update_start:frame_per_update_end:int(frame_per_update/40)]
            music_visual_right = music_right_data[frame_per_update_start:frame_per_update_end:int(frame_per_update/40)]
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
        print_music(music_visual_left,0)
        print_music(music_visual_right,1)
        pygame.display.update()
        clock.tick(frame_rate)
game_loop()
pygame.quit()
quit()