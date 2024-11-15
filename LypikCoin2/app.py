
#####################################
import flet as ft
import asyncio
import time

import request0 as rq


rezistor = True
rezistor_register = "reg"

async def main(page: ft.Page) -> None:
    page.title = "Lypick Coin"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#00001a"
    page.font = {"Roboto-Black": r"assets\fonts\Roboto-Black.ttf"}
    page.theme = ft.Theme(font_family="Roboto-Black")
    
    
    async def register_users(event: ft.ContainerTapEvent):   
            global rezistor_register, ID
            username = username_input.value
            try:
                username = int(username)
            except ValueError: pass
            if await rq.get_id(username) == True:
                ID = int(username)
                rezistor_register = "play"
                page.update()
                
                page.clean()
                page.bgcolor = "#141221"
                await Play()
                page.update()
            else:
                pass  
                
    def on_tap_down0(event: ft.ContainerTapEvent):
        global tap_position
        tap_position = (event.local_x, event.local_y)
   
    # Реген энергии
    async def score_time():  
        global rezistor
        if rezistor == True:
            rezistor = False
            
            while progress_bar.value <= 1000 and await rq.get_energy(ID) <= 1000: 
                await asyncio.sleep(0.5)
                
                await rq.update_energy_plus(ID)               
                progress_bar.value += (1/1000)
                energy_score.data = await rq.get_energy(ID)
                energy_score.value = str(energy_score.data) + " / 1000 ⚡️"
                page.update()
                
            rezistor = True
                       
    # Действия при клике
    async def score_up(event: ft.ContainerTapEvent) -> None:
        if rezistor == True:
            await score_time()
            
        if await rq.get_energy(ID) > 0:
  
            score.data += 1
            score.value = str(score.data)   
                          
            image.scale = 0.6

            # +1 метка
            score_counter.opacity = 1.0
            score_counter.value = "+1"
            score_counter.right = 0
            score_counter.left = tap_position[0]
            score_counter.top = tap_position[1]
            score_counter.bottom = 0
          
            # energy and progress bar
            if progress_bar.value > 0:
                progress_bar.value -= (1/1000)
                await rq.update_energy(ID)
                energy_score.data = await rq.get_energy(ID)
                energy_score.value = str(energy_score.data) + " / 1000 ⚡️"
            
            if score.data == 100:
                score.data += 100
                page.snack_bar = ft.SnackBar(
                    content=ft.Text(
                        value="🪙 +100 от Лупика",
                        size=25,
                        color="#ff0000",
                        text_align=ft.TextAlign.CENTER
                    ),
                    bgcolor="#25223a"
                )
                page.snack_bar.open = True

            
            # Анимации
            page.update()
            await asyncio.sleep(0.01)
            score_counter.opacity = 0
            page.update()
            await asyncio.sleep(0.05)
            image.scale = 1   
            page.update()
                
            await rq.update_coin(score.data, ID)
            await rq.update_time(int(time.time()-1723288600), ID)
    
    # Переход на страницу статистики
    async def register_stat(event: ft.ContainerTapEvent):   
        global rezistor_register
        rezistor_register = "stat"
        
        page.clean()
        page.bgcolor = "#00001a"
        await Play()
        page.update()
        
    # Переход обратно   
    async def stating_exit(event: ft.ContainerTapEvent):   
        global rezistor_register
        rezistor_register = "play"
              
        page.clean()
        page.bgcolor = "#141221"
        await Play()
        page.update()
     
     
    username_input = ft.TextField(label="Ваше ID...", value="", border_color="#ffffff") 
    register_button = ft.ElevatedButton("Вход", on_click= register_users, color="#ffffff") 
        
    async def Play():
        global score, score_counter, image, progress_bar, energy_score
        
        if rezistor_register == "play":
            page.vertical_alignment = ft.MainAxisAlignment.CENTER
            page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
            
            button_stat = ft.ElevatedButton("🏆", on_click= register_stat)
            
            score = ft.Text(value=0, size=100, data=await rq.get_coin(ID))
            score_counter = ft.Text(
                size=50,
                animate_opacity=ft.Animation(
                duration=800, 
                curve=ft.AnimationCurve.BOUNCE_IN
                )
            )
            energy_score = ft.Text(value=0, size=35, data=await rq.get_energy(ID))


            # тап img
            image = ft.Image(
                src="photsdar.png",
                width= 450,
                height=450,
                fit=ft.ImageFit.CONTAIN,
                animate_scale=ft.Animation(duration=600, curve=ft.AnimationCurve.EASE)    
            )

            # прогресс бар
            progress_bar = ft.ProgressBar(
                value=(await rq.get_energy(ID)/1000),
                width=page.width - 100,
                bar_height=20,
                color="#ff0000",
                bgcolor="#990000"
            )
            
            page.add(        
                ft.Container(
                    content=ft.Stack(
                    controls=[button_stat]), 
                ), score,
                ft.Container(
                    content=ft.Stack(
                    controls=[image, score_counter]), 
                    on_click=score_up,
                    on_tap_down=on_tap_down0,
                    margin=ft.Margin(0, 0, 0, -50)
                ), energy_score,
                ft.Container(
                    content=progress_bar,
                    border_radius=ft.BorderRadius(10, 10, 10, 10)
                )
            )
        elif rezistor_register == "reg":
            previe = ft.Text(value="Регистрация", size=50)
            page.add(
                previe,
                username_input,
                ft.Container(
                    content=ft.Stack(
                    controls=[register_button])
                )
            )
            page.vertical_alignment = ft.MainAxisAlignment.CENTER
            page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
            
        elif rezistor_register == "stat":
            
            page.vertical_alignment = None
            page.horizontal_alignment = None
            
            top = ft.Text(value="TOP 10 🏆", size=35)
            
            stating_button = ft.ElevatedButton("⬅️", on_click= stating_exit, color="#ffffff" )
    
            s = await rq.get_stat(50)
            s.sort(reverse=True)
            times = (int(time.time())-1723288600) # - exit time
            tx_size = 20
            l = len(s)
            if l >= 1:
                stat1 = ft.Text(value=f"1. {s[0][1]} score: {s[0][0]}🪙 \nв сети {((times-s[0][2])//60) if (((times-s[0][2])//60) <= 60) else ((times-s[0][2])//60)//60} {"минут" if (((times-s[0][2])//60) <= 60) else "час"} назад", size=tx_size )
                if l >= 2:
                    stat2 = ft.Text(value=f"2. {s[1][1]} score: {s[1][0]}🪙 \nв сети {((times-s[1][2])//60) if (((times-s[1][2])//60) <= 60) else ((times-s[1][2])//60)//60} {"минут" if (((times-s[1][2])//60) <= 60) else "час"} назад", size=tx_size )
                else:
                    stat2 = ft.Text(value="", size=20)
                if l >= 3:
                    stat3 = ft.Text(value=f"3. {s[2][1]} score: {s[2][0]}🪙 \nв сети {((times-s[2][2])//60) if (((times-s[2][2])//60) <= 60) else ((times-s[2][2])//60)//60} {"минут" if (((times-s[2][2])//60) <= 60) else "час"} назад", size=tx_size )
                else:
                    stat3 = ft.Text(value="", size=20)
                if l >= 4:
                    stat4 = ft.Text(value=f"4. {s[3][1]} score: {s[3][0]}🪙 \nв сети {((times-s[3][2])//60) if (((times-s[3][2])//60) <= 60) else ((times-s[3][2])//60)//60} {"минут" if (((times-s[3][2])//60) <= 60) else "час"} назад", size=tx_size )
                else:
                    stat4 = ft.Text(value="", size=20)
                if l >= 5:
                    stat5 = ft.Text(value=f"5. {s[4][1]} score: {s[4][0]}🪙 \nв сети {((times-s[4][2])//60) if (((times-s[4][2])//60) <= 60) else ((times-s[4][2])//60)//60} {"минут" if (((times-s[4][2])//60) <= 60) else "час"} назад", size=tx_size )
                else:
                    stat5 = ft.Text(value="", size=20)
                if l >= 6:
                    stat6 = ft.Text(value=f"6. {s[5][1]} score: {s[5][0]}🪙 \nв сети {((times-s[5][2])//60) if (((times-s[5][2])//60) <= 60) else ((times-s[5][2])//60)//60} {"минут" if (((times-s[5][2])//60) <= 60) else "час"} назад", size=tx_size )
                else:
                    stat6 = ft.Text(value="", size=20)
                if l >= 7:
                    stat7 = ft.Text(value=f"7. {s[6][1]} score: {s[6][0]}🪙 \nв сети {((times-s[6][2])//60) if (((times-s[6][2])//60) <= 60) else ((times-s[6][2])//60)//60} {"минут" if (((times-s[6][2])//60) <= 60) else "час"} назад", size=tx_size )
                else:
                    stat7 = ft.Text(value="", size=20)
                if l >= 8:
                    stat8 = ft.Text(value=f"8. {s[7][1]} score: {s[7][0]}🪙 \nв сети {((times-s[7][2])//60) if (((times-s[7][2])//60) <= 60) else ((times-s[7][2])//60)//60} {"минут" if (((times-s[7][2])//60) <= 60) else "час"} назад", size=tx_size )
                else:
                    stat8 = ft.Text(value="", size=20)
                if l >= 9:
                    stat9 = ft.Text(value=f"9. {s[8][1]} score: {s[8][0]}🪙 \nв сети {((times-s[8][2])//60) if (((times-s[8][2])//60) <= 60) else ((times-s[8][2])//60)//60} {"минут" if (((times-s[8][2])//60) <= 60) else "час"} назад", size=25 )
                else:
                    stat9 = ft.Text(value="", size=20)
                if l >= 10:
                    stat10=ft.Text(value=f"10. {s[9][1]} score: {s[9][0]}🪙 \nв сети {((times-s[9][2])//60) if (((times-s[9][2])//60) <= 60) else ((times-s[9][2])//60)//60} {"минут" if (((times-s[9][2])//60) <= 60) else "час"} назад", size=25 )
                else:
                    stat10 = ft.Text(value="", size=20)
                    
            page.add(           
                top,
                stat1,
                stat2,
                stat3,
                stat4,
                stat5,
                stat6,
                stat7,
                stat8,
                stat9,
                stat10,
                ft.Container(
                    content=ft.Stack(
                    controls=[stating_button])
                )
            )
            
        page.update()
    await Play()

if __name__ == "__main__":
    ft.app(target=main, view=None, port=8000) # ft.WEB_BROWSER
    