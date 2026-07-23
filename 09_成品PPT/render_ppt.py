# -*- coding: utf-8 -*-
"""
PPT渲染脚本：转PDF + 逐页PNG + 接触表
使用PowerPoint COM接口
"""
import os
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

import win32com.client
from PIL import Image

BASE_DIR = r"E:\仿真数据处理\答辩\PPT制作交付包\09_成品PPT"
PPTX_PATH = os.path.join(BASE_DIR, "S_T_VDMOS_TID_答辩完整版.pptx")
PDF_PATH = os.path.join(BASE_DIR, "S_T_VDMOS_TID_答辩完整版.pdf")
PNG_DIR = os.path.join(BASE_DIR, "逐页预览")
CONTACT_SHEET = os.path.join(BASE_DIR, "contact_sheet.png")

def ppt_to_pdf_and_png():
    """使用PowerPoint导出PDF和PNG"""
    print("启动PowerPoint...")
    powerpoint = win32com.client.Dispatch("PowerPoint.Application")
    powerpoint.Visible = True  # 必须可见才能导出
    
    try:
        print("打开PPT...")
        presentation = powerpoint.Presentations.Open(PPTX_PATH, WithWindow=False)
        print(f"共 {presentation.Slides.Count} 页")
        
        # 导出PDF
        print("导出PDF...")
        presentation.SaveAs(PDF_PATH, 32)  # 32 = ppSaveAsPDF
        print(f"PDF已保存: {PDF_PATH}")
        
        # 导出逐页PNG
        print("导出逐页PNG...")
        os.makedirs(PNG_DIR, exist_ok=True)
        
        # 设置导出分辨率
        # 先导出全部为PNG
        png_export_path = os.path.join(PNG_DIR, "slide.png")
        presentation.SaveAs(png_export_path, 18)  # 18 = ppSaveAsPNG
        
        # PowerPoint会自动命名为 slide1.png, slide2.png...
        # 重命名为更规范的名称
        count = 0
        for i in range(1, presentation.Slides.Count + 1):
            old_name = os.path.join(PNG_DIR, f"slide{i}.png")
            new_name = os.path.join(PNG_DIR, f"page_{i:02d}.png")
            if os.path.exists(old_name):
                if os.path.exists(new_name):
                    os.remove(new_name)
                os.rename(old_name, new_name)
                count += 1
        
        print(f"已导出 {count} 张PNG")
        
        presentation.Close()
        return count
        
    except Exception as e:
        print(f"导出出错: {e}")
        import traceback
        traceback.print_exc()
        return 0
    finally:
        try:
            powerpoint.Quit()
        except:
            pass

def make_contact_sheet(png_dir, output_path, cols=8, thumb_width=240):
    """生成接触表"""
    print("\n生成接触表...")
    
    png_files = sorted([f for f in os.listdir(png_dir) if f.endswith('.png') and f.startswith('page_')])
    if not png_files:
        print("没有找到PNG文件")
        return False
    
    # 读取第一张获取比例
    first_img = Image.open(os.path.join(png_dir, png_files[0]))
    orig_w, orig_h = first_img.size
    aspect = orig_h / orig_w
    thumb_height = int(thumb_width * aspect)
    
    rows = (len(png_files) + cols - 1) // cols
    
    sheet_width = cols * thumb_width + (cols + 1) * 5
    sheet_height = rows * thumb_height + (rows + 1) * 5 + 30
    
    sheet = Image.new('RGB', (sheet_width, sheet_height), (240, 240, 240))
    
    from PIL import ImageDraw, ImageFont
    draw = ImageDraw.Draw(sheet)
    
    # 标题
    try:
        font = ImageFont.truetype("msyh.ttc", 16)
    except:
        font = ImageFont.load_default()
    
    draw.text((10, 5), f"答辩PPT 接触表 - 共{len(png_files)}页", fill=(50, 50, 50), font=font)
    
    for idx, png_file in enumerate(png_files):
        row = idx // cols
        col = idx % cols
        
        x = 5 + col * (thumb_width + 5)
        y = 30 + row * (thumb_height + 5)
        
        img = Image.open(os.path.join(png_dir, png_file))
        img.thumbnail((thumb_width, thumb_height), Image.LANCZOS)
        sheet.paste(img, (x, y))
        
        # 页码
        page_num = png_file.replace('page_', '').replace('.png', '')
        draw.text((x + 3, y + 3), page_num, fill=(255, 100, 0), font=font)
    
    sheet.save(output_path, quality=90)
    print(f"接触表已保存: {output_path}")
    print(f"尺寸: {sheet_width} x {sheet_height}")
    return True

def main():
    print("=" * 60)
    print("PPT渲染与导出")
    print("=" * 60)
    
    # 1. 转PDF和PNG
    count = ppt_to_pdf_and_png()
    
    if count == 0:
        print("\nPowerPoint导出失败，尝试备用方案...")
        return
    
    # 2. 生成接触表
    make_contact_sheet(PNG_DIR, CONTACT_SHEET)
    
    # 3. 文件大小统计
    print("\n" + "=" * 60)
    print("产物统计:")
    if os.path.exists(PDF_PATH):
        print(f"  PDF: {os.path.getsize(PDF_PATH)/1024:.0f} KB")
    png_count = len([f for f in os.listdir(PNG_DIR) if f.endswith('.png')])
    print(f"  PNG: {png_count} 张")
    if os.path.exists(CONTACT_SHEET):
        print(f"  接触表: {os.path.getsize(CONTACT_SHEET)/1024:.0f} KB")
    print("=" * 60)

if __name__ == '__main__':
    main()
