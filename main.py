import flet as ft
import asyncio


async def main(page: ft.Page) -> None:
    
    page.title = "Lypick Coin"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#141221"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.font = {"Roboto-Black": r"assets\fonts\Roboto-Black.ttf"}
    page.theme = ft.Theme(font_family="Roboto-Black")
    
    def on_tap_down(event: ft.ContainerTapEvent):
        global tap_position
        tap_position = (event.local_x, event.local_y)
    
         
    async def score_up(event: ft.ContainerTapEvent) -> None:
        
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
        
        progress_bar.value -= (1/2000)
        
     
        if score.data % 100 == 0:
            score.data += 100
            page.snack_bar = ft.SnackBar(
                content=ft.Text(
                    value="🪙 +100",
                    size=25,
                    color="#ff0000",
                    text_align=ft.TextAlign.CENTER
                ),
                bgcolor="#25223a"
            )
            page.snack_bar.open = True
            
    
        
        await page.update_async()
        
        await asyncio.sleep(0.05)
        image.scale = 1
        score_counter.opacity = 0
        
        await page.update_async()
    
    score = ft.Text(value=0, size=100, data=0)
    score_counter = ft.Text(size=50, animate_opacity=ft.Animation(duration=600, curve=ft.AnimationCurve.BOUNCE_IN)
    )

    # тап img
    image = ft.Image(
        src="photsdar.png",
        width= 500,
        height=500,
        fit=ft.ImageFit.CONTAIN,
        animate_scale=ft.Animation(duration=600, curve=ft.AnimationCurve.EASE)    
    )
    # прогресс бар
    progress_bar = ft.ProgressBar(
        value=1,
        width=page.width - 100,
        bar_height=20,
        color="#ff0000",
        bgcolor="#990000"
    )
    await page.add_async(
        score, 
        ft.Container(
            content=ft.Stack(
            controls=[image, score_counter]), 
            on_click=score_up,
            on_tap_down=on_tap_down,
            margin=ft.Margin(0, 0, 0, 30)
        ),
        ft.Container(
            content=progress_bar,
            border_radius=ft.BorderRadius(10, 10, 10, 10)
        )
    )
    
if __name__ == "__main__":
    ft.app(target=main, view=ft.WEB_BROWSER, port=8000) # ft.WEB_BROWSER