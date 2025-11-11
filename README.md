# visualNetworking_erkai(二开视联网项目)
## 视觉模型
### 选用模型  ->  reid
### 模型输入  ->  视频流
### 模型输出
```json```
<br>{<br>
  &emsp;"timestamp": 1634567890.123,<br>
  &emsp;"camera_id": "cam_001",<br>
  &emsp;"detections": [<br>
    &emsp;&emsp;{<br>
     &emsp;&emsp;&emsp; "bbox": [100, 150, 200, 400], &ensp;//[x1, y1, x2, y2]<br>
      &emsp;&emsp;&emsp; "track_id": 101,<br>
      &emsp;&emsp;&emsp; "confidence": 0.95,<br>
      &emsp;&emsp;&emsp; "features": [0.12, -0.45, 0.88, ...], //&ensp;长达数百维的向量<br>
      &emsp;&emsp;&emsp; "attributes": {<br>
        &emsp;&emsp;&emsp;&emsp;"gender": "male",<br>
        &emsp;&emsp;&emsp;&emsp;"upper_color": "blue",<br>
        &emsp;&emsp;&emsp;&emsp;"has_backpack": true<br>
      &emsp;&emsp;&emsp; }<br>
    &emsp;&emsp;},<br>
    &emsp;&emsp;{<br>
      &emsp;&emsp;&emsp;"bbox": [300, 120, 380, 370],<br>
      &emsp;&emsp;&emsp;"track_id": 102,<br>
      &emsp;&emsp;&emsp;"confidence": 0.87,<br>
      &emsp;&emsp;&emsp;"features": [-0.34, 0.67, 0.11, ...],<br>
      &emsp;&emsp;&emsp;"attributes": {<br>
        &emsp;&emsp;&emsp;&emsp;"gender": "female",<br>
        &emsp;&emsp;&emsp;&emsp;"upper_color": "red",<br>
        &emsp;&emsp;&emsp;&emsp;"has_backpack": false<br>
      &emsp;&emsp;&emsp;}<br>
    &emsp;&emsp;}<br>
  &emsp;]<br>
}<br>
```json```
## 数据处理
