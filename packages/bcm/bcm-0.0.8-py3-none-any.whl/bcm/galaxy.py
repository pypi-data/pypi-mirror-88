from vpython import *
import os
import sys

star_list = []
ring_list = []
name_list = [['水星','mercury','shuixing'],
             ['金星','venus','jinxing'],
             ['地球','earth','diqiu'],
             ['火星','mars','huoxing'],
             ['木星','jupiter','muxing'],
             ['土星','saturn','tuxing'],
             ['天王星','uranus','tianwangxing'],
             ['海王星','neptune','haiwangxing'],
             ['太阳','sun','taiyang'],
             ['月亮','moon','yueliang']
             ]

class star():
    def __init__(self, name=None, distance=0
                 , size=250, speed=0, round=0, angle=0, rotation=0.01,opacity=1,emissive=False,revolve=[0,0,0],shininess=0):
        self.name = name
        self.distance = distance
        self.angle = angle
        self.size = size/10
        self.speed = speed/10
        self.sphere = None
        self.ring = None
        self.rotation = rotation
        self.centre = vec(50, -100, 50)
        self.planet = True
        self.round = round
        self.opacity = opacity
        self.emissive = emissive
        self.revolve = revolve
        self.shininess = shininess

        # 公转速度
        self.revolution = radians(self.speed)
        self.setup()

    def setup(self):
        # 生成轨道
        ring(radius=self.distance, thickness=0.15, axis=vec(0, 0, 1), color=vec(0.4, 0.4, 0.4),emissive=True)
        # 生成环
        if self.name.split('-')[-1]=='ring':
            self.ring=cylinder(texture="外观图片/ring.jpg", pos=vec(self.distance, 0, 0), radius=self.size*2, length=0.01,shininess=0,opacity=0.7)
            ring_list.append(self)
            self.name = self.name[:-5]

        # 判断名称
        for i in name_list:
            if self.name in i:
                self.name = i[0]

        # 生成球体
        image_name=get_image(self.name)
        if not image_name:
            print('没有 '+self.name+' 图片！！','警告提示')
            sys.exit(0)
        self.sphere=sphere(texture=image_name, radius=self.size, pos=vec(self.distance, 0, 0),shininess=self.shininess,opacity=self.opacity,emissive=self.emissive)
        star_list.append(self)

        # 当球轨道为0时，发光
        if self.distance==0:
            self.sphere.emissive = True
            self.sphere.shininess = 1

        # self.sphere.rotate(angle=radians(i), axis=vec(0, 0, 1), origin=vec(0, 0, 0))
        self.sphere.pos=vec(self.distance*cos(self.angle*3.14159/180),    # 设置轨道位置
                            self.distance*sin(self.angle*3.14159/180),0)

        self.sphere.rotate(angle=radians(90), axis=vec(1, 0, 0))    # 球偏转朝向镜头
        if self.ring:
            self.ring.rotate(angle=radians(90), axis=vec(0, 1, 0))    # 环偏转
            self.ring.pos = vec(self.distance * cos(self.angle * 3.14159 / 180),        # 设置轨道位置
                                  self.distance * sin(self.angle * 3.14159 / 180), 0)

            #self.ring.rotate(angle=radians(self.angle), axis=vec(0, 0, 1), origin=vec(0, 0, 0))

        for i,e in enumerate(self.revolve):
            if i==0:
                self.sphere.rotate(angle=radians(e), axis=vec(1, 0, 0))
            elif i==1:
                self.sphere.rotate(angle=radians(e), axis=vec(0, 1, 0))
            elif i==2:
                #print(e)
                self.sphere.rotate(angle=radians(e), axis=vec(0, 0, 1))

bg_size=1000
def bg(image,size=1000):
    # 窗口
    scene.width, scene.height = 1500, 800
    scene.autoscale = False

    distant_light(direction=vec(-0.22,- 0.44, -0.88), color=color.gray(0.8))

    # 判断名称
    for i in name_list:
        if image in i:
            image = i[0]

    # 背景球体
    image_name = get_image(image)
    if not image_name:
        print('没有 ' + image + ' 图片！！', '警告提示')
        sys.exit(0)
        # return

    stars=sphere(texture=image_name, radius=size, shininess=0)
    stars.rotate(angle=radians(-90), axis=vec(1, 0, 0))
    stars.rotate(angle=radians(45), axis=vec(0, 1, 1))

    scene.camera.axis = vec(0, 450, -325)
    scene.camera.pos = vec(0,-450,200)
    scene.center = vec(0,50,-50)

# 初始化
def init():
    global change_centre

    # 更改状态
    for i in range(len(star_list)):
        # 有中心后其他球围绕中心公转
        if star_list[i].distance == 0:
            change_centre=True
            local_light(pos=vector(0, 0, 0), color=color.white)  # 设置中心光源

        # 第a个球 围绕 第b个球 公转
        if star_list[i].round != 0 and star_list[star_list[i].round].distance != 0:
            star_list[i].round -= 1
            star_list[i].planet = False
            star_list[i].sphere.pos = star_list[star_list[i].round].sphere.pos
            star_list[i].sphere.pos.x += star_list[star_list[i].round].sphere.radius + 10
            star_list[i].sphere.rotate(angle=radians(star_list[i].angle), axis=vec(0, 0, 1), origin=star_list[star_list[i].round].sphere.pos)
            star_list[i].centre = star_list[star_list[i].round]

forward=True
camera_pos=vec(0,0,0)
camera_axis=vec(0,0,0)
# 更新
def update():
    global forward
    global camera_pos
    global camera_axis
    scene.waitfor('draw_complete')
    for i in star_list:
        if change_centre and i.planet:
            i.centre = vec(0,0,0)   # 更改公转中心
        if not i.planet:
            i.sphere.rotate(angle=i.revolution, axis=vec(0, 0, 1), origin=i.centre.sphere.pos)  # 卫星公转
        else:
            i.sphere.rotate(angle=i.revolution, axis=vec(0, 0, 1), origin=i.centre)  # 行星公转
        i.sphere.rotate(angle=i.rotation, axis=vec(0, 0, 1))  # 球自转

    for i in ring_list:
        i.ring.rotate(angle=i.revolution, axis=vec(0, 0, 1), origin=i.centre)    # 环公转

    # 不让视角超出背景球体
    if mag(scene.camera.pos) > (bg_size-200):
        scene.camera.pos=camera_pos
    else:
        camera_pos=scene.camera.pos

    # 不让视角中心偏离
    if mag(scene.camera.axis) > 800:
        scene.camera.axis=camera_axis
    else:
        camera_axis=scene.camera.axis

# 视角跟随
def follow(index):
    if index<1:
        return
    scene.follow(star_list[index-1].sphere)

def get_image(image_name):
    images_ext = [".png", ".jpg", ".jpeg"]
    # 遍历检查是否存在指定名字的图片
    for ext in images_ext:
        image_file = os.path.join('外观图片', image_name+ext)
        if os.path.exists(image_file):
            image_file = os.path.join('外观图片', image_name + ext)
            return image_file
    # 不存在则返回 None，检查后弹窗提醒

dtheta=0.02
theta=0
def cameraMove(focus=0,speed=1,far=1):
    global theta
    scene.center = star_list[focus].sphere.pos
    scene.camera.rotate(angle=radians(speed),axis=vec(60*cos(theta),60*sin(theta),100*cos(theta)))
    scene.camera.pos += (sin(theta) * scene.camera.pos / far)
    theta+=dtheta

def cameraMove2(focus=0, speed=1):
    global theta
    scene.center = star_list[focus].sphere.pos
    scene.camera.pos+=vec(60*cos(theta)*speed,60*sin(theta)*speed,100*tan(theta)*speed)
    theta+=dtheta

change_centre=False
def run(focus=0,speed=1,far=1):
    init()
    while True:
        update()
        #cameraMove(focus,speed,far)
        rate(60)