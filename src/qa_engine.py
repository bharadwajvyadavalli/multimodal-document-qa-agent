import openai
from typing import Dict, List, Tuple
import base64
from io import BytesIO
import os

class QAEngine:
    def __init__(self, content: Dict):
        self.content = content
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
    def answer(self, question: str) -> Tuple[str, Dict]:
        """Answer question using document content"""
        # Search for relevant content
        relevant_content = self._find_relevant_content(question)
        
        # Generate answer based on content type
        if relevant_content['images']:
            # Use GPT-4 Vision for images/charts
            answer, source = self._answer_with_vision(question, relevant_content)
        else:
            # Use text-based answering
            answer, source = self._answer_with_text(question, relevant_content)
            
        return answer, source
    
    def _find_relevant_content(self, question: str) -> Dict:
        """Find relevant content for the question"""
        relevant = {'text': [], 'tables': [], 'images': []}
        question_lower = question.lower()
        
        # Simple keyword matching (can be improved with embeddings)
        keywords = question_lower.split()
        
        # Search text
        for text_block in self.content['text']:
            if any(kw in text_block['content'].lower() for kw in keywords):
                relevant['text'].append(text_block)
        
        # Search tables
        for table in self.content['tables']:
            if any(kw in table['content'].lower() for kw in keywords):
                relevant['tables'].append(table)
        
        # Include images if question mentions visual elements
        visual_keywords = ['chart', 'graph', 'image', 'figure', 'diagram', 'plot']
        if any(kw in question_lower for kw in visual_keywords):
            relevant['images'] = self.content['images'][:3]  # Limit to 3 images
        
        return relevant
    
    def _answer_with_text(self, question: str, relevant: Dict) -> Tuple[str, Dict]:
        """Answer using text and tables"""
        # Combine relevant content
        context = "Context from document:\n\n"
        source = {'type': 'general', 'page': 1}
        
        # Add text content
        for text in relevant['text'][:3]:  # Limit context size
            context += f"Page {text['page']}:\n{text['content'][:500]}\n\n"
            source = {'type': 'text', 'page': text['page']}
        
        # Add table content
        for table in relevant['tables'][:2]:
            context += f"Table on page {table['page']}:\n{table['content']}\n\n"
            source = {'type': 'table', 'page': table['page'], 'bbox': table.get('bbox')}
        
        # Generate answer
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Answer questions based on document context. Be concise."},
                    {"role": "user", "content": f"{context}\n\nQuestion: {question}"}
                ],
                max_tokens=200
            )
            answer = response.choices[0].message.content
        except:
            answer = "Please provide an OpenAI API key to generate answers."
            
        return answer, source
    
    def _answer_with_vision(self, question: str, relevant: Dict) -> Tuple[str, Dict]:
        """Answer using GPT-4 Vision for images"""
        source = {'type': 'image', 'page': 1}
        
        # Prepare image for API
        if relevant['images']:
            img = relevant['images'][0]
            source = {'type': 'image', 'page': img['page'], 'bbox': img['bbox']}
            
            # Convert image to base64
            buffered = BytesIO()
            img['image'].save(buffered, format="PNG")
            img_base64 = base64.b64encode(buffered.getvalue()).decode()
            
            try:
                response = self.client.chat.completions.create(
                    model="gpt-4-vision-preview",
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": f"Question about this image: {question}"},
                                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_base64}"}}
                            ]
                        }
                    ],
                    max_tokens=200
                )
                answer = response.choices[0].message.content
            except:
                # Fallback to text-based answer
                return self._answer_with_text(question, relevant)
        else:
            return self._answer_with_text(question, relevant)
            
        return answer, source