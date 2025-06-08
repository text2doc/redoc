"""OCR processing functionality for Redoc."""

import logging
from pathlib import Path
from typing import Dict, Optional, Union, Any

from ..exceptions import OCRProcessingError

logger = logging.getLogger(__name__)

class OCRProcessor:
    """Handles OCR processing of documents and images."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the OCR processor.
        
        Args:
            config: Configuration options for the OCR processor
        """
        self.config = config or {}
        self.engine = self._initialize_engine()
    
    def _initialize_engine(self):
        """Initialize the OCR engine.
        
        Returns:
            An instance of the OCR engine
        """
        try:
            # Try to import Tesseract OCR
            import pytesseract
            from PIL import Image
            
            # Check if Tesseract is installed
            try:
                pytesseract.get_tesseract_version()
            except pytesseract.TesseractNotFoundError:
                logger.warning(
                    "Tesseract OCR is not installed. Please install it for OCR functionality. "
                    "On Ubuntu/Debian: sudo apt-get install tesseract-ocr"
                )
                return None
                
            return {
                'engine': 'tesseract',
                'pytesseract': pytesseract,
                'Image': Image
            }
            
        except ImportError:
            logger.warning(
                "OCR dependencies not found. Install with: "
                "pip install pytesseract pillow"
            )
            return None
    
    def process(
        self,
        source: Union[str, Path],
        output_file: Optional[Union[str, Path]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Process a document or image with OCR.
        
        Args:
            source: Path to the input file (image or PDF)
            output_file: Optional output file path for searchable PDF
            **kwargs: Additional OCR options
                - language: Language code (e.g., 'eng', 'pol')
                - dpi: DPI for processing
                - psm: Page segmentation mode
                - oem: OCR Engine mode
                
        Returns:
            Dictionary containing OCR results
            
        Raises:
            OCRProcessingError: If OCR processing fails
        """
        if not self.engine:
            raise OCRProcessingError("No OCR engine available. Please install required dependencies.")
        
        try:
            source_path = Path(source)
            if not source_path.exists():
                raise FileNotFoundError(f"Source file not found: {source_path}")
                
            # Handle PDF input
            if source_path.suffix.lower() == '.pdf':
                return self._process_pdf(source_path, output_file, **kwargs)
                
            # Handle image input
            return self._process_image(source_path, output_file, **kwargs)
            
        except Exception as e:
            raise OCRProcessingError(f"OCR processing failed: {str(e)}") from e
    
    def _process_image(
        self,
        image_path: Path,
        output_file: Optional[Path] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Process a single image with OCR.
        
        Args:
            image_path: Path to the image file
            output_file: Optional output file path for searchable PDF
            **kwargs: Additional OCR options
                
        Returns:
            Dictionary containing OCR results
        """
        if self.engine['engine'] == 'tesseract':
            return self._process_with_tesseract(image_path, output_file, **kwargs)
            
        raise OCRProcessingError(f"Unsupported OCR engine: {self.engine['engine']}")
    
    def _process_pdf(
        self,
        pdf_path: Path,
        output_file: Optional[Path] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Process a PDF document with OCR.
        
        Args:
            pdf_path: Path to the PDF file
            output_file: Optional output file path for searchable PDF
            **kwargs: Additional OCR options
                
        Returns:
            Dictionary containing OCR results
        """
        try:
            from pdf2image import convert_from_path
        except ImportError:
            raise OCRProcessingError(
                "PDF processing requires pdf2image. Install with: pip install pdf2image"
            )
            
        try:
            # Convert PDF to images
            images = convert_from_path(pdf_path)
            
            # Process each page
            results = []
            for i, image in enumerate(images):
                result = self._process_image(image, None, **kwargs)
                results.append({
                    'page': i + 1,
                    'text': result.get('text', ''),
                    'metadata': result.get('metadata', {})
                })
            
            # Create searchable PDF if output file is specified
            if output_file:
                self._create_searchable_pdf(images, output_file, **kwargs)
            
            return {
                'success': True,
                'pages': results,
                'output_file': str(output_file) if output_file else None
            }
            
        except Exception as e:
            raise OCRProcessingError(f"PDF processing failed: {str(e)}") from e
    
    def _process_with_tesseract(
        self,
        image,
        output_file: Optional[Path] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Process an image using Tesseract OCR.
        
        Args:
            image: Path to the image or PIL Image object
            output_file: Optional output file path for searchable PDF
            **kwargs: Additional Tesseract options
                
        Returns:
            Dictionary containing OCR results
        """
        config = {
            'lang': kwargs.get('language', 'eng'),
            'config': f'--psm {kwargs.get("psm", 3)} --oem {kwargs.get("oem", 3)}',
        }
        
        try:
            # If output file is specified, create a searchable PDF
            if output_file:
                if output_file.suffix.lower() != '.pdf':
                    output_file = output_file.with_suffix('.pdf')
                
                # Create searchable PDF
                self.engine['pytesseract'].image_to_pdf_or_hocr(
                    image, extension='pdf',
                    lang=config['lang'],
                    config=config['config']
                )
                
                return {
                    'success': True,
                    'output_file': str(output_file),
                    'text': self.engine['pytesseract'].image_to_string(
                        image, **config
                    )
                }
            
            # Otherwise, just extract text
            text = self.engine['pytesseract'].image_to_string(image, **config)
            
            return {
                'success': True,
                'text': text,
                'metadata': {
                    'language': config['lang'],
                    'engine': 'tesseract',
                    'config': config
                }
            }
            
        except Exception as e:
            raise OCRProcessingError(f"Tesseract processing failed: {str(e)}") from e
    
    def _create_searchable_pdf(
        self,
        images,
        output_path: Path,
        **kwargs
    ) -> None:
        """Create a searchable PDF from images.
        
        Args:
            images: List of PIL Image objects
            output_path: Path to save the searchable PDF
            **kwargs: Additional options
        """
        try:
            import io
            from reportlab.pdfgen import canvas
            from reportlab.lib.pagesizes import letter
            from reportlab.pdfbase import pdfmetrics
            from reportlab.pdfbase.ttfonts import TTFont
            
            # Create a new PDF with ReportLab
            packet = io.BytesIO()
            can = canvas.Canvas(packet, pagesize=letter)
            
            # Add text from OCR to the PDF
            for i, image in enumerate(images):
                # Process each image with OCR
                result = self._process_with_tesseract(image, **kwargs)
                
                # Add text to PDF (invisible but searchable)
                text = result.get('text', '')
                if text:
                    text_object = can.beginText(10, 10)
                    text_object.setFont('Helvetica', 1)  # Tiny, invisible text
                    text_object.textLines(text)
                    can.drawText(text_object)
                
                # Add the original image
                img_io = io.BytesIO()
                image.save(img_io, format='PNG')
                img_io.seek(0)
                
                # Add the image to the page
                can.drawImage(
                    img_io, 0, 0, width=letter[0], height=letter[1],
                    preserveAspectRatio=True, mask='auto'
                )
                
                # Add a new page for the next image
                if i < len(images) - 1:
                    can.showPage()
            
            # Save the PDF
            can.save()
            packet.seek(0)
            
            # Write to the output file
            with open(output_path, 'wb') as f:
                f.write(packet.read())
                
        except Exception as e:
            raise OCRProcessingError(f"Failed to create searchable PDF: {str(e)}") from e
