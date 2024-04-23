import os
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1000, 600
DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, 5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (5, 0)
}


os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(obj_rct:pg.Rect) -> tuple[bool,bool]:
    """
    こうかとんRect，または，爆弾Rectの画面内外判定用の関数
    引数：こうかとんRect，または，爆弾Rect
    戻り値：横方向判定結果，縦方向判定結果（True：画面内/False：画面外）
    """
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate = False
    return yoko, tate


def hoko(obj_img) -> dict[tuple,pg.Surface]:
    """
    押下キーに対する移動量合計値タプルをキー
    rotozoomで回転させたSurfaceを値とした辞書
    引数：こうかとん画像
    戻り値：合計値のタプル:rotozoomしたSurface
    """
    flip_img = pg.transform.flip(obj_img, True, False)
    kaiten = {(-5, 0): pg.transform.rotozoom(obj_img, 0, 1.0),
              (-5, 5): pg.transform.rotozoom(obj_img, 45, 1.0),
              (0, 5): pg.transform.rotozoom(flip_img, 270, 1.0),
              (5, 5): pg.transform.rotozoom(flip_img, 315, 1.0),
              (5, 0): pg.transform.rotozoom(flip_img, 0, 1.0),
              (5, -5): pg.transform.rotozoom(flip_img, 45, 1.0),
              (0, -5): pg.transform.rotozoom(flip_img, 45, 1.0),
              (-5, -5): pg.transform.rotozoom(obj_img, 315, 1.0),
              (0, 0): pg.transform.rotozoom(obj_img, 0, 1.0),
              }
    return kaiten


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    bd_img = pg.Surface((20, 20))
    bd_img.set_colorkey((0, 0, 0))
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0)
    kk_imgs = hoko(kk_img)
    go_img = pg.image.load("fig/8.png") 
    go_rct1 = go_img.get_rect()
    go_rct2 = go_img.get_rect()
    go_rct1.center = WIDTH/2 - 200,HEIGHT/2
    go_rct2.center = WIDTH/2 + 200,HEIGHT/2
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400
    clock = pg.time.Clock()
    tmr = 0
    pg.draw.circle(bd_img, (255, 0, 0), (10, 10), 10)
    bd_rct = bd_img.get_rect()
    bd_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    vx, vy = +5, +5
    
    
        
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bd_rct):  # こうかとんと爆弾がぶつかったら
            shikaku = pg.Surface((WIDTH,HEIGHT))
            pg.draw.rect(shikaku,(0,0,0),(0,0,WIDTH,HEIGHT))
            shikaku.set_alpha(100)
            screen.blit(shikaku,(0,0))
            fonto = pg.font.Font(None, 80)
            txt = fonto.render("GameOver", True, (255,255,255))
            txt_rct = txt.get_rect()
            txt_rct.center = WIDTH/2,HEIGHT/2
            screen.blit(go_img,go_rct1)
            screen.blit(go_img,go_rct2)
            screen.blit(txt, txt_rct)
            pg.display.update()
            time.sleep(5)
            return
        screen.blit(bg_img,[0,0])
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k, v in DELTA.items():
            if key_lst[k]:
                sum_mv[0] += v[0]
                sum_mv[1] += v[1]
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])

        screen.blit(kk_imgs[tuple(sum_mv)], kk_rct)
        bd_rct.move_ip(vx, vy)
        screen.blit(bd_img, bd_rct)
        yoko, tate = check_bound(bd_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        pg.display.update()
        tmr += 1
        clock.tick(50)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
