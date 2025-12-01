import cv2
import os
import math
import datetime

def extract_frames(video_path, output_dir, batch_size=20, frame_interval=1, quality=95):
    """
    高级版本：支持帧间隔和图片质量设置
    
    Args:
        video_path (str): 视频文件路径
        output_dir (str): 输出根目录
        batch_size (int): 每批处理的帧数量
        frame_interval (int): 帧间隔，1表示每帧都提取，2表示每隔一帧提取
        quality (int): 图片质量 (0-100)
    """
    if not os.path.exists(video_path):
        print(f"错误：视频文件 '{video_path}' 不存在")
        return False
    
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print("错误：无法打开视频文件")
        return False
    
    # 获取视频信息
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    # 创建输出目录
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    folder_name = f"{video_name}_{timestamp}"
    video_output_dir = os.path.join(output_dir, folder_name)
    os.makedirs(video_output_dir, exist_ok=True)
    
    print(f"开始提取帧...")
    print(f"视频: {video_name}")
    print(f"总帧数: {total_frames}")
    print(f"帧间隔: {frame_interval}")
    print(f"批次大小: {batch_size}")
    
    frame_count = 0
    saved_count = 0
    batch_index = 0
    success = True
    
    while success:
        success, frame = cap.read()
        
        if success:
            # 根据帧间隔决定是否保存当前帧
            if frame_count % frame_interval == 0:
                # 计算当前批次文件夹
                current_batch = saved_count // batch_size
                batch_folder = os.path.join(video_output_dir, f"batch_{current_batch+1:03d}")
                
                # 创建新批次文件夹
                if saved_count % batch_size == 0:
                    os.makedirs(batch_folder, exist_ok=True)
                
                # 保存图片
                frame_filename = os.path.join(batch_folder, f"frame_{saved_count:06d}.jpg")
                cv2.imwrite(frame_filename, frame, [cv2.IMWRITE_JPEG_QUALITY, quality])
                
                saved_count += 1
                
                # 显示进度
                if saved_count % 50 == 0:
                    progress = (frame_count / total_frames) * 100
                    print(f"进度: {frame_count}/{total_frames} 帧, 已保存 {saved_count} 张 ({progress:.1f}%)")
            
            frame_count += 1
    
    cap.release()
    
    print(f"\n提取完成!")
    print(f"处理了 {frame_count} 帧")
    print(f"保存了 {saved_count} 张图片")
    print(f"创建了 {math.ceil(saved_count / batch_size)} 个批次文件夹")
    print(f"输出位置: {video_output_dir}")
    
    return True

if __name__ == "__main__":
    # 设置视频路径和输出目录
    video_file = "E:\workplace\VSCodeWorkplace\\visualNetworking_erkai\static\\videos\\001.mp4"
    output_directory = "E:\workplace\VSCodeWorkplace\\visualNetworking_erkai\static\\videos\\output"  # 输出目录
    
    print("=== 逐帧提取 ===")
    extract_frames(
        video_path=video_file,
        output_dir=output_directory,
        batch_size=20,
        frame_interval=1,  # 每帧都提取
        quality=95         # 图片质量
    )