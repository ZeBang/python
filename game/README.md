# 📚 火柴人防御游戏 - 教学指南

本指南将帮助你引导学生通过修改游戏代码来学习Python基础知识。

## 🎯 学习目标

通过这个游戏，学生将学习：
- **变量和常量** - 游戏配置参数
- **条件语句 (if/else)** - 游戏逻辑判断
- **循环 (for/while)** - 游戏循环和列表遍历
- **函数** - 代码组织和复用
- **类和方法** - 面向对象编程基础
- **列表操作** - 管理游戏对象

---

## 📖 教学路径（按难度分级）

### 🌱 第1级：变量和常量（最简单）

**位置：** 文件开头（第20-56行）

**学习内容：** 变量、常量、数字类型

**练习任务：**

1. **修改游戏难度**
   ```python
   # 让学生修改这些值，观察游戏变化
   PLAYER_SPEED = 6      # 改为 10，火柴人移动更快
   BULLET_SPEED = 10     # 改为 15，子弹更快
   MONSTER_SPEED_MIN = 1 # 改为 0.5，怪物更慢
   MAX_MONSTERS_IN_HOME = 5  # 改为 10，游戏更容易
   ```

2. **修改颜色**
   ```python
   # 让学生创建自己的颜色
   RED = (220, 20, 60)   # RGB值，让学生改成其他颜色
   # 例如：PURPLE = (128, 0, 128)
   ```

3. **修改屏幕大小**
   ```python
   SCREEN_WIDTH = 1200   # 改为 800，屏幕更小
   SCREEN_HEIGHT = 700   # 改为 600
   ```

**教学提示：**
- 解释什么是变量（可以改变的值）
- 解释RGB颜色系统（0-255）
- 让学生预测修改后的效果，然后运行验证

---

### 🌿 第2级：条件语句 (if/else)

**位置1：** `Stickman.update()` 方法（第72-108行）

**学习内容：** if语句、逻辑运算符

**练习任务：**

1. **添加新的移动键**
   ```python
   # 在 update() 方法中，让学生添加：
   if keys[pygame.K_q]:  # 按Q键向左上移动
       dx -= self.speed
       dy -= self.speed
   ```

2. **修改边界检查**
   ```python
   # 让学生修改边界限制
   # 原代码：
   self.x = max(self.size, min(SCREEN_WIDTH - self.size, self.x))
   # 改为允许超出屏幕：
   # self.x = self.x  # 不限制
   ```

3. **添加速度提升功能**
   ```python
   # 在 update() 方法中添加：
   if keys[pygame.K_LSHIFT]:  # 按住Shift加速
       speed_multiplier = 2
   else:
       speed_multiplier = 1
   dx *= speed_multiplier
   dy *= speed_multiplier
   ```

**位置2：** `Game.update()` 方法中的碰撞检测（第414-500行）

**练习任务：**

1. **修改游戏结束条件**
   ```python
   # 找到这行：
   if self.monsters_in_home >= MAX_MONSTERS_IN_HOME:
       self.game_over = True
   # 让学生改成：
   if self.monsters_in_home >= 3:  # 更难的难度
       self.game_over = True
   ```

2. **添加分数奖励**
   ```python
   # 在击中怪物后，让学生添加：
   if distance < bullet.size + monster.size:
       self.score += 10
       # 让学生改成：
       if distance < bullet.size + monster.size:
           self.score += 20  # 双倍分数
   ```

**教学提示：**
- 解释 if/else 的逻辑
- 解释比较运算符（==, <, >, >=, <=）
- 解释逻辑运算符（and, or, not）

---

### 🌳 第3级：循环 (for/while)

**位置1：** `Game.update()` 方法中的列表遍历（第414-500行）

**学习内容：** for循环、列表操作

**练习任务：**

1. **遍历子弹列表**
   ```python
   # 让学生理解这段代码：
   for bullet in self.bullets[:]:  # 为什么用 [:]？
       bullet.update()
       if not bullet.active:
           self.bullets.remove(bullet)
   ```

2. **添加子弹限制**
   ```python
   # 在 shoot() 方法中，让学生添加：
   if len(self.bullets) >= 10:  # 最多10发子弹
       return None  # 不能射击
   ```

3. **遍历怪物列表并添加特效**
   ```python
   # 让学生添加：给每个怪物添加闪烁效果
   for monster in self.monsters:
       # 添加闪烁逻辑
       if monster.x % 20 < 10:  # 简单的闪烁
           monster.color = RED
       else:
           monster.color = ORANGE
   ```

**位置2：** `Game.run()` 方法（第588-628行）

**学习内容：** while循环、游戏循环

**练习任务：**

1. **理解游戏循环**
   ```python
   # 让学生解释这段代码：
   while self.running:
       # 处理事件
       # 更新游戏
       # 绘制画面
   ```

2. **添加帧率显示**
   ```python
   # 在 draw_ui() 方法中，让学生添加：
   fps_text = self.font_small.render(f"FPS: {int(self.clock.get_fps())}", True, WHITE)
   self.screen.blit(fps_text, (10, 170))
   ```

**教学提示：**
- 解释 while 循环和 for 循环的区别
- 解释列表的遍历和修改
- 解释为什么用 `self.bullets[:]` 而不是 `self.bullets`

---

### 🌲 第4级：函数

**位置1：** `Stickman.can_shoot()` 方法（第110-112行）

**学习内容：** 函数定义、返回值

**练习任务：**

1. **创建简单的辅助函数**
   ```python
   # 让学生创建一个函数来计算距离：
   def calculate_distance(x1, y1, x2, y2):
       """计算两点之间的距离"""
       dx = x2 - x1
       dy = y2 - y1
       return math.sqrt(dx*dx + dy*dy)
   ```

2. **修改射击冷却时间**
   ```python
   # 让学生修改 can_shoot() 函数：
   def can_shoot(self):
       # 原代码：return self.shoot_cooldown == 0
       # 改成：允许连续射击但速度更快
       return self.shoot_cooldown <= 5
   ```

**位置2：** `Game.spawn_monster()` 方法（第409-412行）

**练习任务：**

1. **创建不同类型的怪物**
   ```python
   # 让学生修改 spawn_monster() 函数：
   def spawn_monster(self):
       y = random.randint(50, SCREEN_HEIGHT - 50)
       monster_type = random.choice(['normal', 'fast', 'slow'])
       if monster_type == 'fast':
           # 创建快速怪物
           monster = Monster(SPAWN_X, y)
           monster.speed = 5
       else:
           monster = Monster(SPAWN_X, y)
       self.monsters.append(monster)
   ```

2. **创建辅助函数**
   ```python
   # 让学生创建一个函数来检查碰撞：
   def check_collision(obj1_x, obj1_y, obj1_size, obj2_x, obj2_y, obj2_size):
       """检查两个圆形对象是否碰撞"""
       distance = math.sqrt((obj1_x - obj2_x)**2 + (obj1_y - obj2_y)**2)
       return distance < (obj1_size + obj2_size)
   ```

**教学提示：**
- 解释函数的作用（代码复用、组织代码）
- 解释参数和返回值
- 解释函数命名规范

---

### 🌴 第5级：类和对象（进阶）

**位置：** 各个类的定义（Stickman, Bullet, Monster, Home）

**学习内容：** 类、对象、方法、属性

**练习任务：**

1. **给火柴人添加新属性**
   ```python
   # 在 Stickman.__init__() 中，让学生添加：
   def __init__(self, x, y):
       # ... 原有代码 ...
       self.energy = 100  # 新属性：能量
       self.power_shot = False  # 新属性：强力射击
   ```

2. **创建新的方法**
   ```python
   # 让学生给 Stickman 类添加新方法：
   def use_power_shot(self):
       """使用强力射击"""
       if self.energy >= 50:
           self.energy -= 50
           self.power_shot = True
           return True
       return False
   ```

3. **修改 Monster 类**
   ```python
   # 让学生给 Monster 添加健康值：
   def __init__(self, x, y):
       # ... 原有代码 ...
       self.health = 2  # 需要击中2次
   
   # 修改碰撞检测，让怪物需要被击中多次
   ```

**教学提示：**
- 解释类和对象的区别
- 解释 self 的作用
- 解释 __init__ 方法（构造函数）

---

## 🎓 推荐教学顺序

### 第1周：基础变量和简单修改
1. 修改游戏配置（速度、颜色、大小）
2. 观察变化，理解变量作用

### 第2周：条件语句
1. 添加新的按键控制
2. 修改游戏规则（分数、难度）
3. 理解 if/else 逻辑

### 第3周：循环
1. 理解游戏循环
2. 遍历列表（子弹、怪物）
3. 添加列表操作（限制数量）

### 第4周：函数
1. 创建辅助函数
2. 修改现有函数
3. 理解函数参数和返回值

### 第5周：类和对象
1. 理解类的概念
2. 添加新属性和方法
3. 创建简单的类

---

## 💡 教学技巧

### 1. 渐进式学习
- 从最简单的变量修改开始
- 每次只教一个概念
- 让学生立即看到效果

### 2. 实验和观察
- 鼓励学生大胆修改
- 预测结果，然后验证
- 从错误中学习

### 3. 代码注释
- 让学生添加注释解释代码
- 理解每行代码的作用
- 培养代码阅读能力

### 4. 项目扩展
- 让学生添加新功能
- 鼓励创意和实验
- 分享和展示作品

---

## 🔧 常见问题解答

**Q: 学生修改代码后游戏崩溃怎么办？**
A: 这是学习的好机会！引导学生：
- 阅读错误信息
- 检查语法错误（拼写、缩进）
- 理解错误原因
- 学会调试

**Q: 如何让代码更易理解？**
A: 
- 添加详细注释
- 使用有意义的变量名
- 将复杂代码拆分成小函数
- 逐步解释每个部分

**Q: 学生进度不同怎么办？**
A:
- 提供不同难度的任务
- 让快的学生帮助慢的学生
- 鼓励学生互相学习
- 提供扩展挑战

---

## 📝 作业建议

### 初级作业
1. 修改游戏配置，让游戏更容易/更难
2. 改变所有颜色为主题色
3. 添加一个新的按键功能

### 中级作业
1. 添加分数倍数系统
2. 创建不同类型的怪物
3. 添加游戏音效提示

### 高级作业
1. 创建完整的升级系统
2. 添加多种武器类型
3. 实现保存/加载功能

---

## 🎯 学习成果评估

学生应该能够：
- ✅ 理解并修改变量和常量
- ✅ 使用 if/else 实现逻辑判断
- ✅ 使用循环遍历列表
- ✅ 创建和调用函数
- ✅ 理解类和对象的基本概念
- ✅ 独立添加简单的游戏功能

---

祝教学顺利！🎮📚

