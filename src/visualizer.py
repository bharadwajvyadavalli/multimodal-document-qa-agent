import fitz
from PIL import Image
import io

class PDFVisualizer:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        
    def highlight_area(self, page_num: int, bbox: list = None):
        """Highlight area on PDF page and return as image"""
        doc = fitz.open(self.pdf_path)
        page = doc[page_num]
        
        # Add highlight if bbox provided
        if bbox:
            # Create highlight annotation
            rect = fitz.Rect(bbox)
            highlight = page.add_highlight_annot(rect)
            highlight.set_colors(stroke=[1, 1, 0])  # Yellow
            highlight.update()
        
        # Render page as image
        mat = fitz.Matrix(2, 2)  # 2x zoom for clarity
        pix = page.get_pixmap(matrix=mat)
        img_data = pix.tobytes("png")
        
        # Convert to PIL Image
        img = Image.open(io.BytesIO(img_data))
        
        # Crop to highlighted area if bbox provided
        if bbox:
            # Convert bbox coordinates to image coordinates
            x0, y0, x1, y1 = [coord * 2 for coord in bbox]  # Account for 2x zoom
            
            # Add padding
            padding = 50
            x0 = max(0, x0 - padding)
            y0 = max(0, y0 - padding)
            x1 = min(img.width, x1 + padding)
            y1 = min(img.height, y1 + padding)
            
            # Crop image
            img = img.crop((x0, y0, x1, y1))
        
        doc.close()
        return img
    
    def get_page_thumbnail(self, page_num: int, size=(300, 400)):
        """Get thumbnail of PDF page"""
        doc = fitz.open(self.pdf_path)
        page = doc[page_num]
        
        # Calculate zoom to fit size
        rect = page.rect
        zoom_x = size[0] / rect.width
        zoom_y = size[1] / rect.height
        zoom = min(zoom_x, zoom_y)
        
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat)
        img_data = pix.tobytes("png")
        
        img = Image.open(io.BytesIO(img_data))
        doc.close()
        
        return img