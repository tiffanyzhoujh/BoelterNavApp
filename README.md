# BoelterNavApp
navigation web app for ucla boelter hall

## Step 1: Verify physical layout
1. raw_floorplans/ 里面的图直接airdrop给ipad, 用goodnotes作为背景打开
2. 验证所有的门牌号&开门的方向
3. 标出所有电梯和楼梯间的出入口，注意每个电梯&楼梯能抵达的楼层范围 （后面个层电梯楼梯之间的edge不需要连）
4. 标出所有的外部出入口(e.g. 通向ms, science court等等)

## Step 2: Draw out the tentative dots (iPad)
- 每个教师/办公室只留一个门打点
- 走廊里的点居中，需要拐弯的地方要打点，使最终路径都是直角路径
- 标注好的文件由goodnotes导出image给电脑，所有文件在mark_dots/images和link_dots/images里各存一份

## Step 3: Mark dots (Web)
1. 进入directory
```bash
cd mark_dots
```
2. 修改`index.html`和`server.js`里标注`TODO: CHANGE`的地方，改变楼层的数值
3. Terminal运行网页
```bash
node server.js
```
4. Chrome打开localhost:3000，点击标点。标点时先把所有房间门口的点标出来。
5. 如果遇到问题需要停止网页运行修改代码，修改完之后：
```bash
lsof -i :3000 # 找到port 3000 server.js对应的PID
kill -9 [PID] # kill the process
node server.js # port 3000 released，可以重新正常跑了
```
6. 把`[X]f-coord.csv`复制到link_dots/
7. 标点之后截一个图，可以存在annotated_floorplans/里

## Step 4: Link dots
```bash
cd link_dots
node server.js # go to localhost:3001
```
和Step3同理，注意即使输入dot number有误edge.json里也还是会生成edge，可以用remove link撤销影响
注意保存Xf-edges.json