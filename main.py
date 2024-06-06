import sqlite3 as sql
import pygame
import datetime
import button, databaseHandler 

pygame.init()

time_interval = 0
size = 800
screen = pygame.display.set_mode((size, size))
pygame.display.set_caption("Log _in")
clock = pygame.time.Clock()
run = True
loggedIn = False
black = (0, 0, 0)
delete_btns = []
delete_btns_built = False
num_of_tasks = 0
tasks_id_list = []
y_coor_tasks = 200
add_btn_y = 0
add_task_scene = False
task_input_complete = False

    
database = databaseHandler.DataBaseHandler("appData.db")
#database.selectAllData()

add_task_btn = button.Button(pygame.image.load("buttons/add_1.png"), pygame.image.load("buttons/add_2.png"), 0, 0, 0.55)

buttons_group = pygame.sprite.Group()

buttons_group.add(add_task_btn)


text_font_current_data = pygame.font.SysFont("Arial", 35, bold=True)
text_font_title = pygame.font.SysFont("Arial", 50, bold=True)

text_font_input_and_tasks = pygame.font.SysFont("Arial", 25, bold=True)

user_input_rect_1 = pygame.Rect(200, 80, 200, 35)
user_input_rect_2 = pygame.Rect(200, 120, 200, 35)
user_input_task_rect = pygame.Rect(450, 120, 200, 35)

user_input_1 = ""
user_input_2 = ""
user_input_task = ""

login_title_surface = text_font_title.render("Log In:", True, black)
text_input_1_label_surface = text_font_current_data.render("Username:", True, black)
text_input_2_label_surface = text_font_current_data.render("Password:", True, black)
text_input_task_label_surface = text_font_current_data.render("Input Task:", True, black)

active_input_1 = False
active_input_2 = False
active_input_task = False


def display_tasks(user):   
    global add_btn_y

    list_tasks = database.selectAllTasksByUser(user)
    
    multiplyier = 1
    y_coor = 200
    diff = 55
    
    for record in list_tasks:
        text_task_surface = text_font_input_and_tasks.render(f"{multiplyier} ----- {record[1]} ----- ({record[2]})", True, black) 
        screen.blit(text_task_surface, (20, y_coor+(diff*multiplyier)))
        multiplyier += 1

    add_btn_y = y_coor+(diff*multiplyier)

def create_ordered_id_list_and_count_tasks(user):
    global tasks_id_list
    global num_of_tasks
    
    tasks_id_list = []
    counter = 0
    list_tasks = database.selectAllTasksByUser(user)
 
    for record in list_tasks:
        tasks_id_list.append(record[0])
        counter += 1

    num_of_tasks = counter
    
def create_delete_btns():
    global tasks_id_list
    global num_of_tasks
    list_btns =[]

    multiplyier = 1
    y_coor = 200
    diff = 55
    
    for button_index in range(0, num_of_tasks):
        list_btns.append(button.Button(pygame.image.load("buttons/delete_1.png"), pygame.image.load("buttons/delete_2.png"), 600, y_coor + (diff*multiplyier), 0.35))
        list_btns[button_index].assignTaskID(tasks_id_list[button_index])
        buttons_group.add(list_btns[button_index])
        multiplyier += 1
        
    return list_btns
        
def lis_delete_btn_names(list):
    for i in list:
        print(i.task_id_refer)

while run:
    screen.fill((200, 200, 200))
       
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and add_task_scene == False:
            if user_input_rect_1.collidepoint(event.pos):
                active_input_1 = True
                active_input_2 = False
            elif user_input_rect_2.collidepoint(event.pos):
                active_input_2 = True
                active_input_1 = False
            else:
                active_input_1 = False
                active_input_2 = False

        if active_input_1 == True:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                        user_input_1 = user_input_1[:-1]
                else :
                        user_input_1 += event.unicode
        if active_input_2 == True:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    user_input_2 = user_input_2[:-1]
                else:
                    user_input_2 += event.unicode

        if event.type == pygame.KEYDOWN  and add_task_scene == False:
            if event.key == pygame.K_RETURN:
                #print("pressed", user_input_1, user_input_2, loggedIn)
                if database.authenticate(user_input_1.strip(), user_input_2.strip()):
                    currentUser = user_input_1
                    user_title_surface = text_font_current_data.render(f"{currentUser} tasks:", True, black)

                    user_input_1 = ""
                    user_input_2 = ""
                    loggedIn = True
                    delete_btns_built = False

    
    pygame.draw.rect(screen, black, user_input_rect_1, 2)
    pygame.draw.rect(screen, black, user_input_rect_2, 2)

    text_input_1_surface = text_font_input_and_tasks.render(user_input_1, True, black)
    text_input_2_surface = text_font_input_and_tasks.render(user_input_2, True, black)
    screen.blit(text_input_1_surface, (user_input_rect_1.x + 5, user_input_rect_1.y+5))
    screen.blit(text_input_2_surface, (user_input_rect_2.x + 5, user_input_rect_2.y+5))

    screen.blit(text_input_1_label_surface, (user_input_rect_1.x - 180, user_input_rect_1.y))
    screen.blit(text_input_2_label_surface, (user_input_rect_2.x - 180, user_input_rect_2.y))
    screen.blit(login_title_surface, (20, 10))

    pygame.draw.line(screen, black, (0, 180), (size, 180))


    if loggedIn == True:
        screen.blit(user_title_surface, (15, 200))
        display_tasks(currentUser)
        
        if delete_btns_built == False:
            create_ordered_id_list_and_count_tasks(currentUser)
            delete_btns = create_delete_btns()
            delete_btns_built = True
            
            print("---------")
            print("delete_btn_list:", delete_btns)

            print("---------")
            print("num_of_tasks:", num_of_tasks)
            #database.selectAllTasks(currentUser)
            print(tasks_id_list, "id_list")
            print("delete_btn_id_refers:")
            lis_delete_btn_names(delete_btns)
            print("---------")
            
            add_task_btn.setPos(40, add_btn_y)

        
        buttons_group.draw(screen)
        buttons_group.update()
        

        #if delete_btns[0].check_clicked():
            #print(delete_btns[0].rect.topleft)

        
        for btn in delete_btns:
            if btn.check_clicked() == True and time_interval > 3 and add_task_scene == False:
                database.deleteRecordInTaskById(btn.task_id_refer)
                delete_btns_built = False
                time_interval = 0
                for btn_to_clear in delete_btns:
                    btn_to_clear.unableDisplay()
        
        if add_task_btn.check_clicked() == True and time_interval > 3:
            add_task_scene = True
            task_input_complete = False
            time_interval = 0
        

        if add_task_scene == True:
            if task_input_complete == False:    
                pygame.draw.rect(screen, black, user_input_task_rect, 2)
                screen.blit(text_input_task_label_surface, (user_input_task_rect.x, user_input_task_rect.y-35))

                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_BACKSPACE:
                            user_input_task = user_input_task[:-1]
                        if event.key == pygame.K_RETURN and user_input_task.strip() != "":
                            task = user_input_task
                            user_input_task = ""
                            task_input_complete = True
                        else:
                            user_input_task += event.unicode

                text_input_task_surface = text_font_input_and_tasks.render(user_input_task, True, black)
                screen.blit(text_input_task_surface, (user_input_task_rect.x + 5, user_input_task_rect.y+5))


            else:
                database.addTask(task, currentUser)
                delete_btns_built = False
                for btn_to_clear in delete_btns:
                    btn_to_clear.unableDisplay()
                add_task_scene = False
    
    time_interval += 1
    pygame.display.update()
    clock.tick(60)
pygame.quit()