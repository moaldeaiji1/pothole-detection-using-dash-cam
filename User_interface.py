import tkinter as tk 
from PIL import ImageTk,Image,ImageDraw,ImageFont
from tkinterdnd2 import TkinterDnD, DND_FILES,DND_ALL
from tkinter import filedialog,Menu,Frame,Button,Label
import os
import mimetypes
import time
import threading
from ultralytics import YOLO
import cv2
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import  SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab import platypus
import numpy as np
import traceback
from functools import partial
import tempfile
from PIL import Image as PILImage
import datetime
import xml.etree.ElementTree as ET



global l,image,on_drop_file_path,file_path,inter_tk,change_text,image22,current,current_frame,model

global num_of_videos,frames_per_video
global track_page
global is_paused
global video_thread





global id_s
id_s=0
    
    
lock_writing = threading.Lock()

# %%


# %%
#make folders if notr exisit to save files in it
if os.path.exists("files_save") and os.path.isdir("files_save"):
    if(os.path.exists(r"files_save\detection") and os.path.isdir(r"files_save\detection")):
        pass
    else:
        os.makedirs(r"files_save\detection")
else:
    os.makedirs("files_save")
    os.makedirs("files_save\detection")
    
    


# %%
#load the model
def set_model():
    global model
    model = YOLO(r'resources\big_model.pt')

# %%

#check if the file is image or video , if it is somerhing else remove it
def get_file_type(file_path):
   

    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type and (mime_type.startswith('video') ):
        return True,"video"
    elif(mime_type and mime_type.startswith('image')):
        return True,"image"
    
    return False,"none"


#make the image look clickable when the mouse is in it
def make_image_transparent( alpha):
    global image
    image_with_alpha = image.copy()
    image_with_alpha.putalpha(alpha)
    return ImageTk.PhotoImage(image_with_alpha)

#set back the orignal image if the mouse is out of the inage
def or_image():
    global l,image
    image2=image.copy()
    image2=ImageTk.PhotoImage(image2)
    return image2

#event start when the mouse is in the image to make it look clickable
def on_enter(event):
    global image,l
    l.config(cursor="hand2")  # Change cursor to a hand when mouse enters
    # You can also change the image here if needed
    transparent_image = make_image_transparent(128)
    l.config(image=transparent_image)
    l.image = transparent_image

#event start when the mouse out of the image        
def on_leave(event):
    l.config(cursor="")
    untransparent_image = or_image()

    l.config(image=untransparent_image)
    l.image = untransparent_image


#event start when the mouse click the image  
def open_file_dialog():
    global file_path
    file_path = filedialog.askopenfilenames(
        filetypes = [
    ("Video Files", "*.mp4;*.avi"),
    ("Image Files", "*.jpg;*.jpeg;*.png;*.gif"),
    ("All Files", "*.*")
],
        multiple=True
    )
    
    if file_path:
        file_path=list(file_path)
        new_list=check_videos_or_image(file_path)
        print(f"Selected file: {file_path}")
        print("new list "+str(new_list))

        second_page(new_list)

#event start when the user drag files or folder
def on_drop(event):
    global on_drop_file_path
    on_drop_file_path = inter.tk.splitlist(event.data)

    
    if on_drop_file_path:
        on_drop_file_path=list(on_drop_file_path)
        for i in on_drop_file_path[:]:
            if(os.path.isdir(i)):
                items=os.listdir(i)
                items=[os.path.join(i,item) for item in items]
                on_drop_file_path+=items
                on_drop_file_path.remove(i)


        new_list=check_videos_or_image(on_drop_file_path)
        second_page(new_list)




def check_videos_or_image(li):
    li
    video_or_image=[]
    for i in li:
        type,_=get_file_type(i)
        if(type==False):
            pass
        else:
            if _=="video":
                video_or_image.append([i,0])        #0 for video
            else:
                video_or_image.append([i,1])        #1 for image


    return video_or_image
            




# %%
    
inter=TkinterDnD.Tk()
inter.title("Visual pollution")


#report window
def show_info():
    os.startfile(r"files_save\detection")
    


#when the user change to another model
def change_model(typ):
    global model_path,textbox,model

    if(typ=="c"):
        global model
        model_path = filedialog.askopenfilenames()
        
        if model_path:
            try:
                model=YOLO(model_path[0],task="detect")
                k=(str(model))
                if len(k)<=6:
                    tk.messagebox.showerror("Filed","The file you chose is not a model")
                    model = YOLO(r'resources\big_model.pt')
                else:
                    tk.messagebox.showinfo("Sucess","The Model has been changed")
            except:
                tk.messagebox.showerror("Filed","The file you chose is not a model")
                model = YOLO(r'resources\big_model.pt')

    elif(typ=="large_model"):
        model = YOLO(r'resources\big_model.pt')
        tk.messagebox.showinfo("Sucess","You chose the large model")
    elif(typ=="small_model"):
        model = YOLO(r'resources\small_model.pt')
        tk.messagebox.showinfo("Sucess","You chose the small model")
    else:
        model = YOLO(r'resources\big_model.pt')
        tk.messagebox.showinfo("Sucess","You chose the base model")



#menu
menu = Menu(inter)
option = Menu(menu, tearoff="off")

change_model_submenu = Menu(option, tearoff="off")
change_model_submenu.add_command(label="small_model",command=partial(change_model,"small_model" ))
change_model_submenu.add_command(label="large_model",command=partial(change_model,"large_model" ))
change_model_submenu.add_command(label="Custom Model ",command=partial(change_model,"c" ))


option.add_cascade(label="Change Model", menu=change_model_submenu)

option.add_command(label="Reports", command=show_info)

menu.add_cascade(label="Options", menu=option)

inter.config(menu=menu)





#reshow first page when cancel or finish procesasing
def reshow_page_one():
    global first_page_frame
    for widget in inter.winfo_children():
        if not isinstance(widget, Menu) and widget is not first_page_frame:
            widget.destroy()
    inter.geometry("400x125")
    first_page_frame.pack()



#first page details
def first_page():

    global t_img,l,image,inter,first_page_frame
    inter.geometry("400x125")

    first_page_frame=Frame(inter)
    
    image=Image.open("resources\doc-upload.jpg")
    image=image.resize((150,100))
    t_img=ImageTk.PhotoImage(image)


    drag_text=tk.Label(first_page_frame,text="Drag and drop or clik to upload video",font=("Helvetica",16))
    drag_text.pack(side="top")
    l=tk.Label(first_page_frame,image=t_img)
    l.pack(side=tk.TOP)
    first_page_frame.pack()

    l.bind("<Enter>", on_enter)

    l.bind("<Leave>", on_leave)

    l.bind("<Button-1>", lambda event: open_file_dialog())

    l.drop_target_register(DND_FILES)
    l.dnd_bind("<<Drop>>", on_drop)


# %%

def second_page(videos):
    global change_text,t_img2,change_image,video_thread
    
    print(videos)
    if(len(videos)==0):
        tk.messagebox.showerror("Filed","No image or video droped")
        return 

    
    else:
        second_page_interface()

        video_thread=threading.Thread(target=process_video,args=(videos,len(videos),))
        video_thread.start()
        


   




pause_event = threading.Event()

def process_video(videos,size):
    
    global is_paused
    is_paused=False
   

    for count,i in enumerate(videos,start=1):
        if(is_paused):
            pause_event.wait()

        update_text(count,size)
        if(i[1]==0):  
            video_capture = cv2.VideoCapture(i[0])
            length = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
            fps=video_capture.get(cv2.CAP_PROP_FPS) 
            print(fps)
            up=0
            gps_av=False
            gps="None"
            ski=0

            if(os.path.exists(i[0][0:-3]+"gpx")):
                gps_av=True
                tree = ET.parse(i[0][0:-3]+"gpx")
                root = tree.getroot()
                namespace = {'gpx': 'http://www.topografix.com/GPX/1/1'}
                trkpts = root.findall(".//gpx:trkpt", namespace)
                gps_info=[]
                for trkpt in trkpts:
                    temp=[]
                    lat = trkpt.attrib['lat']
                    lon = trkpt.attrib['lon']
                    temp.append(lat)
                    temp.append(lon)
                    gps_info.append(temp)

            try:
                while True:
                    if is_paused:
                        pause_event.wait()
                        
                    ret, frame = video_capture.read()
                    if not ret:  # Check if frame is successfully read
                        break  # Break the loop if there are no more frames
                    
                    up += 1
                    if(gps_av):
                        gps=f"https://www.google.com/maps?q={gps_info[ski.__round__()][0]},{gps_info[ski.__round__()][1]}"
                    model_usage(frame,gps)
                    

                    try:
                        for i in range(50):
                            ret, frame = video_capture.read()
                            if not ret:  # Check if frame is successfully read
                                break  # Break the loop if there are no more frames
                            up += 1
                        ski+=50/30
                    except Exception as e:
                        print("Error occurred while skipping frames:", e)

                    update_percetnage(int((up / length) * 100))
            except Exception as e:
                traceback.print_exc()
                print(e)
            
                

        else:
            update_percetnage(100)
            im=Image.open(i[0])
            model_usage(im,"None")

    proces_done()




def proces_done():
    dialog = tk.Toplevel()
    dialog.title("Sucess")

    label = tk.Label(dialog, text="The processing is done")
    label.pack(padx=10, pady=10)

    yes_button = tk.Button(dialog, text="show Repoer folder", command=lambda: report_folder(dialog))
    yes_button.pack(side="left", padx=10, pady=10)

    no_button = tk.Button(dialog, text="Ok", command=lambda: on_ok(dialog))
    no_button.pack(side="right", padx=10, pady=10)
    


def report_folder(dialog):
    dialog.destroy()
    os.startfile(r"files_save\detection")
    reshow_page_one()
    


def on_ok(dialog):
    dialog.destroy()
    reshow_page_one()


def update_percetnage(per):
    global change_text2
    change_text2.config(text=str(per)+"% completed")

            

def update_text(count,total):
    global change_text
    change_text.config(text=str(count)+" of "+str(total)+ " file")


def model_usage(frame,gps):
    global model,id_s
    
    res=model.predict([frame],conf=0.4,classes=[0])
    res=res[0]
    for i in res:
        tt=time.time()
        deteced=i.plot()
        update_image(deteced)
        deteced=cv2.cvtColor(deteced, cv2.COLOR_RGB2BGR)
        deteced=cv2.resize(deteced, (int(deteced.shape[0]/2), int(deteced.shape[1]/2)))
        cl=(res.boxes.cls.cpu().numpy()[0])
        tag=(res.names[cl])
        path_file=r"files_save\detection\\"+str(tag)+"-"+str(id_s)+"-"+str(tt)+".pdf"
        create_pdf(tag, deteced, gps, path_file)
        #threading.Thread(target=send_file,args=(path_file,)).start()

# def send_file(path_file):
#     global id_s
#     with open(path_file, 'rb') as file:
#         with lock_writing:
#             try:
#                 files = {'file': file}
#                 response = requests.post("http://127.0.0.1:5000/upload", files=files,data={"id":id_s})
#                 if("File uploaded successfully"!=response.text):
#                     f=open(r"files_save\detection\not_send.txt","a")
#                     f.write("\n"+path_file)
#                     f.close()         
#             except:
#                 f=open(r"files_save\detection\not_send.txt","a")
#                 f.write("\n"+path_file)
#                 f.close()


def update_image(frame):
    global change_image,t_img2
    try:
        image22=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    except:
        image22=frame
        pass
    image22=image22.resize((500,500))
    t_img2=ImageTk.PhotoImage(image22)
    change_image.config(image=t_img2)


# %%
def second_page_interface():
    global inter,pause_buuton
    global change_text,change_text2,change_image,change_bar,ff
    inter.geometry("600x600")
    for widget in inter.winfo_children():
        widget.pack_forget()

    ff=Frame(inter)
    buttons_fram=Frame(inter)
    

    change_image=Label(ff)
    change_image.pack(side="top")


    pause_buuton=Button(buttons_fram,text="pause",command=pause_but)
    pause_buuton.pack(side="right")

    cancel_buuton=Button(buttons_fram,text="Cancel",command=can_but)
    cancel_buuton.pack(side="left")

    change_text=Label(ff)
    change_text.pack(side="bottom")



    change_text2=Label(ff)
    change_text2.pack(side="top")

   

    ff.pack()
    buttons_fram.pack(side="bottom")


def pause_but():
    global is_paused,pause_buuton
    
    if(is_paused==False):
        is_paused=True
        pause_buuton.config(text="continue")
        pause_event.clear()

    else:
        is_paused=False
        pause_buuton.config(text="pause")
        pause_event.set()
   
    
    

def can_but():
    global video_thread,is_canceled
    response = tk.messagebox.askyesno("Confirmation", "Are you sure you want to proceed?")
    if response:
        is_canceled=True
        reshow_page_one()
        
    else:
        print("User clicked No")     
    


# %%
def create_pdf(title, image_path, gps_info, output_path):
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    styles = getSampleStyleSheet()
    title_style = styles["Title"]
    centered_style = ParagraphStyle("CenteredTitle", parent=title_style, alignment=1)
    clickable_style = ParagraphStyle(
        "Clickable", parent=styles["Normal"], textColor=colors.blue, underline=1
    )

    story = []

    # Adding current date and time to the story
    now = datetime.datetime.now()
    date_time_str = now.strftime("%Y-%m-%d %H:%M:%S")
    date_time_text = '<font size="10">{}</font>'.format(date_time_str)
    story.append(Paragraph(date_time_text, styles["Normal"]))

    # Adding title
    title_text = '<font size="24">{}</font>'.format(title)
    story.append(Paragraph(title_text, centered_style))
    story.append(Paragraph("<br/><br/>", styles["Normal"]))  # Adding some space

    # Adding GPS info as a clickable link
    gps_link_text = '<font size="12"><u><a href="{}">{}</a></u></font>'.format(
        gps_info, gps_info
    )
    story.append(Paragraph(gps_link_text, clickable_style))
    story.append(Paragraph("<br/><br/>", styles["Normal"]))  # Adding some space

    # Adding image
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
        temp_filename = temp_file.name
        pil_image = PILImage.fromarray(np.uint8(image_path))
        pil_image.save(temp_file, format='PNG')

    image = platypus.Image(temp_filename , width=350, height=350)
    story.append(image)
    doc.build(story)

# %%
set_model()
first_page()
is_paused=False
inter.mainloop()

# %%



