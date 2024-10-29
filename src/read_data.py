import cv2
import pandas as pd
import re

ABS_MT_POSITION_Y_MAX = 21311
ABS_MT_POSITION_X_MAX = 9599

ABS_MT_POSITION_X_MAX_XU = 121999
ABS_MT_POSITION_Y_MAX_XU = 271199

def getdirection(df):
    dict = { 'frameid': [], 'attack': [], 'skill1': [], 'skill2': [], 'skill3': [], 'add_skill1': [], 'add_skill2': [], 'add_skill3': [], 'summon_skill': [], 'recover': [], 'return': [], 'buy': [], 'move_r': [], 'watch_map':[]}
    df_direct = pd.DataFrame(dict)
    i,j=0,0
    while i<10:
        while df["frameid"][j]<=i:
            print(df["frameid"][j])
            j+=1
        i+=1
    

def display(df, cap, fps):
    i,j=0,0
    ret,frame = cap.read()
    shape = frame.shape
    while 1:
        while df["frameid"][j]<i:
            x = df["x"][j]*shape[1]
            y = df["y"][j]*shape[0]
            center = (int(x),int(y))
            frame = cv2.circle(frame, center, 20, (0,255,0), 5)
            j+=1
        cv2.imshow("frame",frame)
        if cv2.waitKey(int(1000/fps)) & 0xff == ord('q'):
            break
        ret,frame = cap.read()
        if not ret: break
        i+=1

def read_xu(index, fps=15, dev_filter=4):

    dict = { 'time': [], 'x': [], 'y': [], 'ABS_MT_BLOB_ID': [], "frameid": []}

    df = pd.DataFrame(dict)
    cap = cv2.VideoCapture("../dataset/game%d-%dfps-xu/file.mp4"%(index,fps))

    with open("../dataset/game%d-%dfps-xu/log.txt"%(index,fps)) as log:
        lines = log.readlines()
        lines = lines[0:30000]
        i=0
        while "ABS_MT_POSITION_X" not in lines[i]:
            i+=1
        time0 = float(re.findall("\d+\.\d+",lines[i])[0]) + 0.5
        while i < len(lines):
            l = lines[i]
            time = float(re.findall("\d+\.\d+",l)[0]) - time0
            ABS_MT_POSITION_X = 0
            ABS_MT_POSITION_Y = 0
            j=i
            while j<len(lines) and "SYN_REPORT" not in lines[j]:
                if "ABS_MT_POSITION_X" in lines[j]:
                    pos = lines[j].split()[-1]
                    ABS_MT_POSITION_X = int(pos,16)
                elif "ABS_MT_POSITION_Y" in lines[j]:
                    pos = lines[j].split()[-1]
                    ABS_MT_POSITION_Y = int(pos,16)
                j+=1
            real_x = (ABS_MT_POSITION_Y)/ABS_MT_POSITION_Y_MAX_XU
            real_y = (ABS_MT_POSITION_X_MAX_XU - ABS_MT_POSITION_X)/ABS_MT_POSITION_X_MAX_XU
            if not (real_x < 0.01 or real_y < 0.01 or real_x > 0.99 or real_y > 0.99):
                df.loc[len(df.index)] = [time,real_x,real_y,-1,int(time*fps)]
            i=j+1
    print(df)
    getdirection(df)
    #df.to_csv("../dataset/game%d-%dfps-xu/out.csv"%(index,fps), index=False) 
    #print("csv saved!")
    display(df,cap, fps)

def read(index, fps=15, dev_filter=6):

    dev_filter="/dev/input/event%d"%dev_filter
    dict = { 'time': [], 'x': [], 'y': [], 'ABS_MT_BLOB_ID': [], "frameid": []}

    df = pd.DataFrame(dict)
    cap = cv2.VideoCapture("../dataset/game%d-%dfps/file.mp4"%(index,fps))

    with open("../dataset/game%d-%dfps/log.txt"%(index,fps)) as log:
        lines = log.readlines()
        #remove_l = []
        #for l in lines:
        #    if dev_filter not in l:
        #        remove_l.append(l)
        #for rl in remove_l:
        #    lines.remove(rl)
        #lines = lines[0:20000]
        # 
        i=0
        while "ABS_MT_POSITION_X" not in lines[i]:
            i+=1
        time0 = float(re.findall("\d+\.\d+",lines[i])[0]) - 0.5
        while i < len(lines):
            l = lines[i]
            time = float(re.findall("\d+\.\d+",l)[0]) - time0
            ABS_MT_POSITION_X = 0
            ABS_MT_POSITION_Y = 0
            ABS_MT_BLOB_ID = 0
            j=i
            while j<len(lines) and "SYN_MT_REPORT" not in lines[j]:
                if "ABS_MT_POSITION_X" in lines[j]:
                    pos = lines[j].split()[-1]
                    ABS_MT_POSITION_X = int(pos,16)
                elif "ABS_MT_POSITION_Y" in lines[j]:
                    pos = lines[j].split()[-1]
                    ABS_MT_POSITION_Y = int(pos,16)
                elif "ABS_MT_BLOB_ID" in lines[j]:
                    pos = lines[j].split()[-1]
                    ABS_MT_BLOB_ID = int(pos,16)
                j+=1
            real_x = (ABS_MT_POSITION_Y)/ABS_MT_POSITION_Y_MAX
            real_y = (ABS_MT_POSITION_X_MAX - ABS_MT_POSITION_X)/ABS_MT_POSITION_X_MAX
            df.loc[len(df.index)] = [time,real_x,real_y,ABS_MT_BLOB_ID,int(time*fps)]
            i=j+1
    print(df)
    df.to_csv("../dataset/game%d-%dfps/out.csv"%(index,fps), index=False) 
    print("csv saved!")
    #display(df,cap, fps)
        
read(6)