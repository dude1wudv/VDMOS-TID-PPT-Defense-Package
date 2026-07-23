# -*- coding: utf-8 -*-
"""
PPT渲染脚本 v2：使用LibreOffice转PDF + 逐页PNG + 接触表
"""
import os
import sys
import io
import subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from PIL import Image

BASE_DIR = r"E:\仿真数据处理\答辩\PPT制作交付包\09_成品PPT"
PPTX_PATH = os.path.join(BASE_DIR, "S_T_VDMOS_TID_答辩完整版.pptx")
PDF_PATH = os.path.join(BASE_DIR, "S_T_VDMOS_TID_答辩完整版.pdf")
PNG_DIR = os.path.join(BASE_DIR, "逐页预览")
CONTACT_SHEET = os.path.join(BASE_DIR, "contact_sheet.png")

SOFFICE = r"C:\Program Files\LibreOffice\program\soffice.exe"

def ppt_to_pdf():
    """使用LibreOffice导出PDF"""
    print("使用LibreOffice转换PDF...")
    cmd = [
        SOFFICE,
        "--headless",
        "--convert-to", "pdf",
        "--outdir", BASE_DIR,
        PPTX_PATH
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    if result.returncode == 0 and os.path.exists(PDF_PATH):
        print(f"  PDF已生成: {os.path.getsize(PDF_PATH)/1024:.0f} KB")
        return True
    else:
        print(f"  转换失败: {result.stderr}")
        return False

def pdf_to_pngs():
    """使用LibreOffice将PDF转为逐页PNG"""
    print("导出逐页PNG...")
    os.makedirs(PNG_DIR, exist_ok=True)
    
    # 清空旧文件
    for f in os.listdir(PNG_DIR):
        if f.endswith('.png'):
            os.remove(os.path.join(PNG_DIR, f))
    
    cmd = [
        SOFFICE,
        "--headless",
        "--convert-to", "png",
        "--outdir", PNG_DIR,
        PDF_PATH
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    
    if result.returncode != 0:
        print(f"  PNG转换失败: {result.stderr}")
        return 0
    
    # LibreOffice会生成 S_T_VDMOS_TID_答辩完整版-1.png, -2.png 等
    # 重命名为 page_01.png, page_02.png
    count = 0
    png_files = sorted([f for f in os.listdir(PNG_DIR) if f.endswith('.png')])
    for i, f in enumerate(png_files, 1):
        old = os.path.join(PNG_DIR, f)
        new = os.path.join(PNG_DIR, f"page_{i:02d}.png")
        os.rename(old, new)
        count += 1
    
    print(f"  已导出 {count} 张PNG")
    return count

def make_contact_sheet(cols=8, thumb_width=240):
    """生成接触表"""
    print("\n生成接触表...")
    
    png_files = sorted([f for f in os.listdir(PNG_DIR) if f.endswith('.png') and f.startswith('page_')])
    if not png_files:
        print("  没有找到PNG文件")
        return False
    
    first_img = Image.open(os.path.join(PNG_DIR, png_files[0]))
    orig_w, orig_h = first_img.size
    aspect = orig_h / orig_w
    thumb_height = int(thumb_width * aspect)
    
    rows = (len(png_files) + cols - 1) // cols
    
    sheet_width = cols * thumb_width + (cols + 1) * 5
    sheet_height = rows * thumb_height + (rows + 1) * 5 + 30
    
    sheet = Image.new('RGB', (sheet_width, sheet_height), (240, 240, 240))
    
    from PIL import ImageDraw, ImageFont
    draw = ImageDraw.Draw(sheet)
    
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
        
        img = Image.open(os.path.join(PNG_DIR, png_file))
        img.thumbnail((thumb_width, thumb_height), Image.LANCZOS)
        sheet.paste(img, (x, y))
        
        page_num = png_file.replace('page_', '').replace('.png', '')
        draw.text((x + 3, y + 3), page_num, fill=(255, 100, 0), font=font)
    
    sheet.save(CONTACT_SHEET, quality=90)
    print(f"  接触表已保存: {os.path.getsize(CONTACT_SHEET)/1024:.0f} KB")
    return True

def main():
    print("=" * 60)
    print("PPT渲染与导出 (LibreOffice)")
    print("=" * 60)
    
    # 1. 转PDF
    if not ppt_to_pdf():
        print("\nPDF转换失败，终止")
        return
    
    # 2. 转PNG
    count = pdf_to_pngs()
    if count == 0:
        print("\nPNG导出失败")
        return
    
    # 3. 接触表
    make_contact_sheet()
    
    # 4. 统计
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
