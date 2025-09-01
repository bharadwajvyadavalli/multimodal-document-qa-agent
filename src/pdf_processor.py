import fitz  # PyMuPDF
from PIL import Image
import io
import re

class PDFProcessor:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.doc = fitz.open(pdf_path)
        
    def extract_all(self):
        """Extract text, tables, and images from PDF"""
        content = {
            'text': [],
            'tables': [],
            'images': [],
            'num_pages': len(self.doc)
        }
        
        for page_num, page in enumerate(self.doc):
            # Extract text
            text = page.get_text()
            content['text'].append({
                'page': page_num + 1,
                'content': text
            })
            
            # Extract tables (simple approach - look for tabular patterns)
            tables = self._extract_tables(page, page_num + 1)
            content['tables'].extend(tables)
            
            # Extract images
            images = self._extract_images(page, page_num + 1)
            content['images'].extend(images)
            
        self.doc.close()
        return content
    
    def _extract_tables(self, page, page_num):
        """Simple table extraction using text patterns"""
        tables = []
        text = page.get_text()
        lines = text.split('\n')
        
        # Look for table-like patterns (multiple columns with alignment)
        table_lines = []
        for line in lines:
            # Check if line has multiple data points separated by spaces/tabs
            if len(line.split()) > 2 and any(char.isdigit() for char in line):
                table_lines.append(line)
            elif table_lines:
                # End of table
                if len(table_lines) > 2:
                    tables.append({
                        'page': page_num,
                        'type': 'table',
                        'content': '\n'.join(table_lines),
                        'bbox': None  # Could extract actual bbox if needed
                    })
                table_lines = []
        
        return tables
    
    def _extract_images(self, page, page_num):
        """Extract images from page"""
        images = []
        image_list = page.get_images()
        
        for img_index, img in enumerate(image_list):
            # Get image data
            xref = img[0]
            pix = fitz.Pixmap(self.doc, xref)
            
            if pix.n - pix.alpha < 4:  # GRAY or RGB
                # Convert to PIL Image
                img_data = pix.tobytes("png")
                img_pil = Image.open(io.BytesIO(img_data))
                
                # Get image position on page
                img_rect = page.get_image_bbox(img)
                
                images.append({
                    'page': page_num,
                    'type': 'image',
                    'index': img_index,
                    'image': img_pil,
                    'bbox': [img_rect.x0, img_rect.y0, img_rect.x1, img_rect.y1]
                })
            
            pix = None
        
        return images
    
    def get_page_text(self, page_num):
        """Get text from specific page"""
        page = self.doc[page_num]
        return page.get_text()