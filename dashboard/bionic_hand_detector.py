"""
Advanced Bionic Hand Detection and Validation System
Specialized ML model for accurate bionic hand recognition with image validation
"""

import cv2
import numpy as np
from PIL import Image, ImageEnhance
import io
import base64
from typing import Dict, List, Tuple, Optional, Union
from datetime import datetime
import json
import hashlib


class BionicHandDetector:
    """
    Advanced bionic hand detection system with image validation and preprocessing
    """
    
    def __init__(self):
        """Initialize the bionic hand detector with validation parameters"""
        
        # Image validation parameters
        self.min_image_size = (100, 100)
        self.max_image_size = (4000, 4000)
        self.supported_formats = ['JPEG', 'JPG', 'PNG', 'BMP', 'TIFF']
        self.max_file_size = 10 * 1024 * 1024  # 10MB
        
        # Hand detection parameters
        self.hand_cascade_features = self._initialize_hand_features()
        self.bionic_indicators = self._initialize_bionic_indicators()
        
        # Confidence thresholds
        self.confidence_thresholds = {
            'very_high': 0.95,
            'high': 0.85,
            'medium': 0.70,
            'low': 0.50
        }
        
        # Error messages
        self.error_messages = {
            'invalid_format': 'Invalid image format. Please upload JPG, PNG, BMP, or TIFF files only.',
            'file_too_large': f'File size exceeds {self.max_file_size // (1024*1024)}MB limit.',
            'file_too_small': 'Image resolution too low. Minimum size: 100x100 pixels.',
            'file_too_large_res': 'Image resolution too high. Maximum size: 4000x4000 pixels.',
            'no_hand_detected': 'No hand detected in the image. Please upload a clear image of a hand.',
            'corrupted_image': 'Image file appears to be corrupted or unreadable.',
            'no_bionic_features': 'This appears to be a natural/biological hand, not a bionic hand.',
            'unclear_image': 'Image quality too low for accurate analysis. Please upload a clearer image.',
            'multiple_hands': 'Multiple hands detected. Please upload an image with a single hand.',
            'partial_hand': 'Only partial hand visible. Please ensure the entire hand is in the frame.'
        }
    
    def validate_and_analyze_image(self, image_data: Union[bytes, str], 
                                 filename: str = None) -> Dict:
        """
        Complete image validation and bionic hand analysis pipeline
        
        Args:
            image_data: Image data (bytes or base64 string)
            filename: Optional filename for format validation
            
        Returns:
            Analysis results with validation status and detection results
        """
        
        analysis_start = datetime.now()
        
        try:
            # Step 1: Validate image format and data
            validation_result = self._validate_image_data(image_data, filename)
            if not validation_result['is_valid']:
                return {
                    'status': 'error',
                    'error_type': 'validation_error',
                    'message': validation_result['message'],
                    'timestamp': analysis_start.isoformat(),
                    'processing_time_ms': 0
                }
            
            # Step 2: Load and preprocess image
            processed_image = self._preprocess_image(validation_result['image'])
            if processed_image is None:
                return {
                    'status': 'error',
                    'error_type': 'preprocessing_error',
                    'message': self.error_messages['corrupted_image'],
                    'timestamp': analysis_start.isoformat(),
                    'processing_time_ms': 0
                }
            
            # Step 3: Hand detection and validation
            hand_detection_result = self._detect_and_validate_hand(processed_image)
            if not hand_detection_result['hand_detected']:
                return {
                    'status': 'error',
                    'error_type': 'detection_error',
                    'message': hand_detection_result['message'],
                    'timestamp': analysis_start.isoformat(),
                    'processing_time_ms': 0
                }
            
            # Step 4: Bionic hand analysis
            bionic_analysis = self._analyze_bionic_features(
                processed_image, 
                hand_detection_result['hand_region']
            )
            
            # Step 5: Generate comprehensive results
            processing_time = (datetime.now() - analysis_start).total_seconds() * 1000
            
            return self._generate_analysis_results(
                bionic_analysis, 
                hand_detection_result,
                validation_result['image_info'],
                processing_time
            )
            
        except Exception as e:
            return {
                'status': 'error',
                'error_type': 'system_error',
                'message': f'Analysis failed: {str(e)}',
                'timestamp': analysis_start.isoformat(),
                'processing_time_ms': 0
            }
    
    def _validate_image_data(self, image_data: Union[bytes, str], 
                           filename: str = None) -> Dict:
        """Validate image format, size, and basic properties"""
        
        try:
            # Handle base64 encoded data
            if isinstance(image_data, str):
                if image_data.startswith('data:image/'):
                    # Extract base64 data from data URL
                    header, data = image_data.split(',', 1)
                    image_data = base64.b64decode(data)
                else:
                    image_data = base64.b64decode(image_data)
            
            # Check file size
            if len(image_data) > self.max_file_size:
                return {
                    'is_valid': False,
                    'message': self.error_messages['file_too_large']
                }
            
            # Try to load image
            image = Image.open(io.BytesIO(image_data))
            
            # Validate format
            if image.format not in self.supported_formats:
                return {
                    'is_valid': False,
                    'message': self.error_messages['invalid_format']
                }
            
            # Validate dimensions
            width, height = image.size
            if width < self.min_image_size[0] or height < self.min_image_size[1]:
                return {
                    'is_valid': False,
                    'message': self.error_messages['file_too_small']
                }
            
            if width > self.max_image_size[0] or height > self.max_image_size[1]:
                return {
                    'is_valid': False,
                    'message': self.error_messages['file_too_large_res']
                }
            
            # Calculate image hash for duplicate detection
            image_hash = hashlib.md5(image_data).hexdigest()
            
            return {
                'is_valid': True,
                'image': image,
                'image_info': {
                    'format': image.format,
                    'size': image.size,
                    'mode': image.mode,
                    'file_size_bytes': len(image_data),
                    'hash': image_hash
                }
            }
            
        except Exception as e:
            return {
                'is_valid': False,
                'message': self.error_messages['corrupted_image']
            }
    
    def _preprocess_image(self, image: Image.Image) -> Optional[np.ndarray]:
        """Preprocess image for analysis"""
        
        try:
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Resize if too large (maintain aspect ratio)
            max_size = 1024
            if max(image.size) > max_size:
                ratio = max_size / max(image.size)
                new_size = tuple(int(dim * ratio) for dim in image.size)
                image = image.resize(new_size, Image.Resampling.LANCZOS)
            
            # Enhance image quality
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(1.2)
            
            enhancer = ImageEnhance.Sharpness(image)
            image = enhancer.enhance(1.1)
            
            # Convert to OpenCV format
            cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            
            return cv_image
            
        except Exception as e:
            return None
    
    def _detect_and_validate_hand(self, image: np.ndarray) -> Dict:
        """Detect and validate hand presence in image"""
        
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Use multiple detection methods
        detection_methods = [
            self._detect_hand_contours,
            self._detect_hand_skin_color,
            self._detect_hand_edges
        ]
        
        hand_regions = []
        confidence_scores = []
        
        for method in detection_methods:
            result = method(image, gray)
            if result['detected']:
                hand_regions.append(result['region'])
                confidence_scores.append(result['confidence'])
        
        if not hand_regions:
            return {
                'hand_detected': False,
                'message': self.error_messages['no_hand_detected']
            }
        
        # Select best detection result
        best_idx = np.argmax(confidence_scores)
        best_region = hand_regions[best_idx]
        best_confidence = confidence_scores[best_idx]
        
        # Validate hand region
        validation = self._validate_hand_region(image, best_region)
        
        return {
            'hand_detected': validation['is_valid'],
            'message': validation.get('message', 'Hand detected successfully'),
            'hand_region': best_region,
            'detection_confidence': best_confidence,
            'validation_details': validation
        }
    
    def _detect_hand_contours(self, image: np.ndarray, 
                            gray: np.ndarray) -> Dict:
        """Detect hand using contour analysis"""
        
        try:
            # Apply Gaussian blur
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            
            # Adaptive threshold
            thresh = cv2.adaptiveThreshold(
                blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                cv2.THRESH_BINARY, 11, 2
            )
            
            # Find contours
            contours, _ = cv2.findContours(
                thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
            )
            
            if not contours:
                return {'detected': False, 'confidence': 0}
            
            # Find largest contour (likely hand)
            largest_contour = max(contours, key=cv2.contourArea)
            
            # Filter by area
            area = cv2.contourArea(largest_contour)
            image_area = image.shape[0] * image.shape[1]
            area_ratio = area / image_area
            
            if area_ratio < 0.05:  # Too small
                return {'detected': False, 'confidence': 0}
            
            # Get bounding rectangle
            x, y, w, h = cv2.boundingRect(largest_contour)
            
            # Calculate confidence based on shape characteristics
            aspect_ratio = w / h if h > 0 else 0
            confidence = min(0.8, area_ratio * 10) * (1 - abs(aspect_ratio - 0.8))
            
            return {
                'detected': confidence > 0.3,
                'confidence': confidence,
                'region': (x, y, w, h),
                'method': 'contour_analysis'
            }
            
        except Exception:
            return {'detected': False, 'confidence': 0}
    
    def _detect_hand_skin_color(self, image: np.ndarray, 
                              gray: np.ndarray) -> Dict:
        """Detect hand using skin color detection"""
        
        try:
            # Convert to HSV
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            
            # Define skin color range in HSV
            lower_skin = np.array([0, 20, 70], dtype=np.uint8)
            upper_skin = np.array([20, 255, 255], dtype=np.uint8)
            
            # Create mask
            mask = cv2.inRange(hsv, lower_skin, upper_skin)
            
            # Morphological operations
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
            
            # Find contours in mask
            contours, _ = cv2.findContours(
                mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
            )
            
            if not contours:
                return {'detected': False, 'confidence': 0}
            
            # Get largest skin region
            largest_contour = max(contours, key=cv2.contourArea)
            area = cv2.contourArea(largest_contour)
            
            # Calculate confidence
            image_area = image.shape[0] * image.shape[1]
            area_ratio = area / image_area
            confidence = min(0.9, area_ratio * 8)
            
            if confidence < 0.4:
                return {'detected': False, 'confidence': confidence}
            
            x, y, w, h = cv2.boundingRect(largest_contour)
            
            return {
                'detected': True,
                'confidence': confidence,
                'region': (x, y, w, h),
                'method': 'skin_color_detection'
            }
            
        except Exception:
            return {'detected': False, 'confidence': 0}
    
    def _detect_hand_edges(self, image: np.ndarray, 
                         gray: np.ndarray) -> Dict:
        """Detect hand using edge detection"""
        
        try:
            # Apply Gaussian blur
            blurred = cv2.GaussianBlur(gray, (3, 3), 0)
            
            # Canny edge detection
            edges = cv2.Canny(blurred, 50, 150)
            
            # Find contours from edges
            contours, _ = cv2.findContours(
                edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
            )
            
            if not contours:
                return {'detected': False, 'confidence': 0}
            
            # Filter contours by size and shape
            valid_contours = []
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > 1000:  # Minimum area threshold
                    valid_contours.append(contour)
            
            if not valid_contours:
                return {'detected': False, 'confidence': 0}
            
            # Select best contour
            best_contour = max(valid_contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(best_contour)
            
            # Calculate confidence based on edge complexity
            perimeter = cv2.arcLength(best_contour, True)
            area = cv2.contourArea(best_contour)
            
            if area == 0:
                return {'detected': False, 'confidence': 0}
            
            circularity = 4 * np.pi * area / (perimeter * perimeter)
            confidence = min(0.85, (1 - circularity) * 2)  # Hands are not circular
            
            return {
                'detected': confidence > 0.3,
                'confidence': confidence,
                'region': (x, y, w, h),
                'method': 'edge_detection'
            }
            
        except Exception:
            return {'detected': False, 'confidence': 0}
    
    def _validate_hand_region(self, image: np.ndarray, region: Tuple) -> Dict:
        """Validate detected hand region"""
        
        x, y, w, h = region
        
        # Check if region is within image bounds
        if x < 0 or y < 0 or x + w > image.shape[1] or y + h > image.shape[0]:
            return {
                'is_valid': False,
                'message': self.error_messages['partial_hand']
            }
        
        # Check region size relative to image
        image_area = image.shape[0] * image.shape[1]
        region_area = w * h
        area_ratio = region_area / image_area
        
        if area_ratio < 0.1:
            return {
                'is_valid': False,
                'message': self.error_messages['partial_hand']
            }
        
        if area_ratio > 0.8:
            return {
                'is_valid': False,
                'message': self.error_messages['unclear_image']
            }
        
        # Check aspect ratio (hands are typically taller than wide)
        aspect_ratio = h / w if w > 0 else 0
        if aspect_ratio < 0.8 or aspect_ratio > 2.0:
            return {
                'is_valid': False,
                'message': self.error_messages['no_hand_detected']
            }
        
        return {
            'is_valid': True,
            'area_ratio': area_ratio,
            'aspect_ratio': aspect_ratio
        }
    
    def _analyze_bionic_features(self, image: np.ndarray, 
                               hand_region: Tuple) -> Dict:
        """Analyze bionic hand features in the detected hand region"""
        
        x, y, w, h = hand_region
        hand_roi = image[y:y+h, x:x+w]
        
        # Initialize feature scores
        feature_scores = {}
        
        # 1. Metallic surface detection
        feature_scores['metallic_surface'] = self._detect_metallic_surfaces(hand_roi)
        
        # 2. Joint articulation analysis
        feature_scores['joint_articulation'] = self._analyze_joint_articulation(hand_roi)
        
        # 3. Sensor detection
        feature_scores['sensor_presence'] = self._detect_sensors(hand_roi)
        
        # 4. Cable/wire detection
        feature_scores['cable_detection'] = self._detect_cables_wires(hand_roi)
        
        # 5. Surface texture analysis
        feature_scores['surface_texture'] = self._analyze_surface_texture(hand_roi)
        
        # 6. Color pattern analysis
        feature_scores['color_pattern'] = self._analyze_color_patterns(hand_roi)
        
        # 7. Geometric precision analysis
        feature_scores['geometric_precision'] = self._analyze_geometric_precision(hand_roi)
        
        # Calculate overall bionic confidence
        bionic_confidence = self._calculate_bionic_confidence(feature_scores)
        
        return {
            'is_bionic': bionic_confidence > self.confidence_thresholds['medium'],
            'confidence': bionic_confidence,
            'feature_scores': feature_scores,
            'classification': self._classify_hand_type(bionic_confidence, feature_scores),
            'detailed_analysis': self._generate_detailed_analysis(feature_scores)
        }
    
    def _detect_metallic_surfaces(self, hand_roi: np.ndarray) -> float:
        """Detect metallic surfaces in hand ROI"""
        
        try:
            # Convert to grayscale
            gray = cv2.cvtColor(hand_roi, cv2.COLOR_BGR2GRAY)
            
            # Detect high reflectance areas (metallic shine)
            _, bright_areas = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
            bright_ratio = np.sum(bright_areas == 255) / bright_areas.size
            
            # Detect metallic color ranges in HSV
            hsv = cv2.cvtColor(hand_roi, cv2.COLOR_BGR2HSV)
            
            # Silver/metallic color mask
            lower_metallic = np.array([0, 0, 180])
            upper_metallic = np.array([180, 30, 255])
            metallic_mask = cv2.inRange(hsv, lower_metallic, upper_metallic)
            metallic_ratio = np.sum(metallic_mask == 255) / metallic_mask.size
            
            # Combine scores
            metallic_score = (bright_ratio * 0.6 + metallic_ratio * 0.4) * 2
            return min(1.0, metallic_score)
            
        except Exception:
            return 0.0
    
    def _analyze_joint_articulation(self, hand_roi: np.ndarray) -> float:
        """Analyze joint articulation patterns typical of bionic hands"""
        
        try:
            gray = cv2.cvtColor(hand_roi, cv2.COLOR_BGR2GRAY)
            
            # Detect straight lines (artificial joint segments)
            edges = cv2.Canny(gray, 50, 150)
            lines = cv2.HoughLinesP(edges, 1, np.pi/180, 30, 
                                  minLineLength=20, maxLineGap=10)
            
            if lines is None:
                return 0.2
            
            # Count horizontal and vertical lines (artificial structure)
            horizontal_lines = 0
            vertical_lines = 0
            
            for line in lines:
                x1, y1, x2, y2 = line[0]
                angle = np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi
                
                if abs(angle) < 15 or abs(angle) > 165:  # Horizontal
                    horizontal_lines += 1
                elif abs(abs(angle) - 90) < 15:  # Vertical
                    vertical_lines += 1
            
            # More artificial lines = higher bionic score
            line_score = min(1.0, (horizontal_lines + vertical_lines) / 20)
            
            # Detect regular patterns (segmented fingers)
            circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20,
                                     param1=50, param2=30, minRadius=5, maxRadius=30)
            
            circle_score = 0
            if circles is not None:
                circle_score = min(1.0, len(circles[0]) / 10)
            
            return (line_score * 0.7 + circle_score * 0.3)
            
        except Exception:
            return 0.0
    
    def _detect_sensors(self, hand_roi: np.ndarray) -> float:
        """Detect electronic sensors and components"""
        
        try:
            # Look for small circular objects (sensors, LEDs)
            gray = cv2.cvtColor(hand_roi, cv2.COLOR_BGR2GRAY)
            
            circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 15,
                                     param1=50, param2=25, minRadius=3, maxRadius=15)
            
            sensor_score = 0
            if circles is not None:
                # Filter circles that might be sensors
                sensor_candidates = 0
                for circle in circles[0]:
                    x, y, r = map(int, circle)
                    if r < 10:  # Small radius typical of sensors
                        sensor_candidates += 1
                
                sensor_score = min(1.0, sensor_candidates / 8)
            
            # Look for rectangular components (circuit boards, connectors)
            contours, _ = cv2.findContours(gray, cv2.RETR_EXTERNAL, 
                                         cv2.CHAIN_APPROX_SIMPLE)
            
            rectangular_score = 0
            for contour in contours:
                area = cv2.contourArea(contour)
                if 50 < area < 500:  # Component-sized areas
                    perimeter = cv2.arcLength(contour, True)
                    if perimeter > 0:
                        circularity = 4 * np.pi * area / (perimeter * perimeter)
                        if circularity < 0.7:  # Non-circular (rectangular)
                            rectangular_score += 1
            
            rectangular_score = min(1.0, rectangular_score / 10)
            
            return (sensor_score * 0.6 + rectangular_score * 0.4)
            
        except Exception:
            return 0.0
    
    def _detect_cables_wires(self, hand_roi: np.ndarray) -> float:
        """Detect cables and wiring typical of bionic hands"""
        
        try:
            gray = cv2.cvtColor(hand_roi, cv2.COLOR_BGR2GRAY)
            
            # Detect thin lines (cables/wires)
            edges = cv2.Canny(gray, 30, 100)
            
            # Morphological operations to enhance thin lines
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 1))
            enhanced = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
            
            # Count edge pixels (more edges might indicate wiring)
            edge_density = np.sum(enhanced > 0) / enhanced.size
            
            # Look for parallel lines (cable bundles)
            lines = cv2.HoughLinesP(enhanced, 1, np.pi/180, 20,
                                  minLineLength=15, maxLineGap=5)
            
            cable_score = 0
            if lines is not None:
                # Group parallel lines
                parallel_groups = 0
                for i, line1 in enumerate(lines):
                    for line2 in lines[i+1:]:
                        x1, y1, x2, y2 = line1[0]
                        x3, y3, x4, y4 = line2[0]
                        
                        # Check if lines are roughly parallel
                        angle1 = np.arctan2(y2 - y1, x2 - x1)
                        angle2 = np.arctan2(y4 - y3, x4 - x3)
                        
                        if abs(angle1 - angle2) < 0.2:  # Parallel threshold
                            parallel_groups += 1
                
                cable_score = min(1.0, parallel_groups / 5)
            
            return min(1.0, edge_density * 3 + cable_score * 0.5)
            
        except Exception:
            return 0.0
    
    def _analyze_surface_texture(self, hand_roi: np.ndarray) -> float:
        """Analyze surface texture for artificial vs natural patterns"""
        
        try:
            gray = cv2.cvtColor(hand_roi, cv2.COLOR_BGR2GRAY)
            
            # Calculate texture features using Local Binary Pattern
            def local_binary_pattern(image, radius=3, n_points=24):
                """Simplified LBP implementation"""
                height, width = image.shape
                lbp = np.zeros_like(image)
                
                for i in range(radius, height - radius):
                    for j in range(radius, width - radius):
                        center = image[i, j]
                        binary_string = ""
                        
                        # Sample points in circle
                        for k in range(n_points):
                            angle = 2 * np.pi * k / n_points
                            x = i + radius * np.cos(angle)
                            y = j + radius * np.sin(angle)
                            
                            # Bilinear interpolation
                            x1, y1 = int(x), int(y)
                            x2, y2 = x1 + 1, y1 + 1
                            
                            if x2 < height and y2 < width:
                                pixel_value = (image[x1, y1] * (x2 - x) * (y2 - y) +
                                             image[x2, y1] * (x - x1) * (y2 - y) +
                                             image[x1, y2] * (x2 - x) * (y - y1) +
                                             image[x2, y2] * (x - x1) * (y - y1))
                                
                                binary_string += "1" if pixel_value >= center else "0"
                        
                        lbp[i, j] = int(binary_string, 2) if len(binary_string) == n_points else 0
                
                return lbp
            
            # Calculate LBP
            lbp_image = local_binary_pattern(gray)
            
            # Calculate texture uniformity (artificial surfaces are more uniform)
            hist, _ = np.histogram(lbp_image.flatten(), bins=256, range=(0, 256))
            hist = hist.astype(float) / np.sum(hist)  # Normalize
            
            # Calculate entropy (lower entropy = more uniform = more artificial)
            entropy = -np.sum(hist * np.log2(hist + 1e-10))
            max_entropy = 8  # Maximum possible entropy for 8-bit
            uniformity_score = 1 - (entropy / max_entropy)
            
            # Calculate variance in texture
            texture_variance = np.var(lbp_image)
            variance_score = min(1.0, texture_variance / 10000)  # Normalize
            
            # Artificial surfaces tend to be more uniform but with some texture
            artificial_score = uniformity_score * 0.7 + (1 - variance_score) * 0.3
            
            return min(1.0, artificial_score)
            
        except Exception:
            return 0.3  # Default moderate score
    
    def _analyze_color_patterns(self, hand_roi: np.ndarray) -> float:
        """Analyze color patterns typical of bionic hands"""
        
        try:
            # Convert to different color spaces
            hsv = cv2.cvtColor(hand_roi, cv2.COLOR_BGR2HSV)
            lab = cv2.cvtColor(hand_roi, cv2.COLOR_BGR2LAB)
            
            # Extract dominant colors
            pixels = hand_roi.reshape(-1, 3)
            
            # Calculate color variance
            color_variance = np.mean([np.var(pixels[:, i]) for i in range(3)])
            
            # Low variance = uniform color = more artificial
            variance_score = 1 - min(1.0, color_variance / 2000)
            
            # Check for typical bionic hand colors (grays, metallics, blacks)
            gray_pixels = 0
            total_pixels = len(pixels)
            
            for pixel in pixels[::10]:  # Sample every 10th pixel for efficiency
                b, g, r = pixel
                # Check if pixel is grayish (low saturation)
                if abs(b - g) < 30 and abs(g - r) < 30 and abs(b - r) < 30:
                    gray_pixels += 1
            
            gray_ratio = (gray_pixels * 10) / total_pixels  # Adjust for sampling
            
            # Check for metallic shine (high value, low saturation in HSV)
            h, s, v = cv2.split(hsv)
            metallic_pixels = np.sum((v > 180) & (s < 50))
            metallic_ratio = metallic_pixels / (hand_roi.shape[0] * hand_roi.shape[1])
            
            # Combine scores
            artificial_color_score = (variance_score * 0.4 + 
                                    gray_ratio * 0.4 + 
                                    metallic_ratio * 2 * 0.2)
            
            return min(1.0, artificial_color_score)
            
        except Exception:
            return 0.3
    
    def _analyze_geometric_precision(self, hand_roi: np.ndarray) -> float:
        """Analyze geometric precision typical of manufactured vs biological hands"""
        
        try:
            gray = cv2.cvtColor(hand_roi, cv2.COLOR_BGR2GRAY)
            
            # Detect edges
            edges = cv2.Canny(gray, 50, 150)
            
            # Find contours
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, 
                                         cv2.CHAIN_APPROX_SIMPLE)
            
            if not contours:
                return 0.3
            
            precision_scores = []
            
            for contour in contours:
                if cv2.contourArea(contour) < 100:  # Skip small contours
                    continue
                
                # Approximate contour to polygon
                epsilon = 0.02 * cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, epsilon, True)
                
                # Calculate how "geometric" the shape is
                # More vertices in approximation = more geometric precision
                area = cv2.contourArea(contour)
                perimeter = cv2.arcLength(contour, True)
                
                if perimeter > 0 and area > 0:
                    # Circularity (4π*area/perimeter²)
                    circularity = 4 * np.pi * area / (perimeter * perimeter)
                    
                    # Convexity
                    hull = cv2.convexHull(contour)
                    hull_area = cv2.contourArea(hull)
                    convexity = area / hull_area if hull_area > 0 else 0
                    
                    # Geometric shapes tend to have specific circularity and high convexity
                    if 0.7 < circularity < 1.3 or convexity > 0.9:
                        precision_scores.append(0.8)
                    elif len(approx) >= 4:  # Polygonal shape
                        precision_scores.append(0.7)
                    else:
                        precision_scores.append(0.3)
            
            if not precision_scores:
                return 0.3
            
            return min(1.0, np.mean(precision_scores))
            
        except Exception:
            return 0.3
    
    def _calculate_bionic_confidence(self, feature_scores: Dict) -> float:
        """Calculate overall bionic hand confidence from feature scores"""
        
        # Weighted importance of different features
        weights = {
            'metallic_surface': 0.25,
            'joint_articulation': 0.20,
            'sensor_presence': 0.15,
            'cable_detection': 0.15,
            'surface_texture': 0.10,
            'color_pattern': 0.10,
            'geometric_precision': 0.05
        }
        
        # Calculate weighted average
        total_score = 0
        total_weight = 0
        
        for feature, score in feature_scores.items():
            if feature in weights:
                total_score += score * weights[feature]
                total_weight += weights[feature]
        
        if total_weight == 0:
            return 0.0
        
        confidence = total_score / total_weight
        
        # Apply confidence adjustments
        # Minimum threshold for multiple features
        active_features = sum(1 for score in feature_scores.values() if score > 0.4)
        if active_features < 2:
            confidence *= 0.7  # Reduce confidence if few features detected
        
        return min(1.0, confidence)
    
    def _classify_hand_type(self, confidence: float, feature_scores: Dict) -> Dict:
        """Classify the type of hand based on confidence and features"""
        
        if confidence >= self.confidence_thresholds['very_high']:
            hand_type = 'advanced_bionic_hand'
            description = 'Advanced bionic prosthetic with multiple sensors and actuators'
        elif confidence >= self.confidence_thresholds['high']:
            hand_type = 'bionic_hand'
            description = 'Bionic prosthetic hand with electronic control systems'
        elif confidence >= self.confidence_thresholds['medium']:
            hand_type = 'mechanical_prosthetic'
            description = 'Mechanical prosthetic or simple bionic hand'
        elif confidence >= self.confidence_thresholds['low']:
            hand_type = 'prosthetic_device'
            description = 'Basic prosthetic device or assistive technology'
        else:
            hand_type = 'biological_hand'
            description = 'Natural biological hand'
        
        # Determine specific characteristics
        characteristics = []
        if feature_scores.get('sensor_presence', 0) > 0.6:
            characteristics.append('Multiple sensors detected')
        if feature_scores.get('metallic_surface', 0) > 0.6:
            characteristics.append('Metallic construction')
        if feature_scores.get('cable_detection', 0) > 0.6:
            characteristics.append('Visible wiring/cables')
        if feature_scores.get('joint_articulation', 0) > 0.6:
            characteristics.append('Articulated joints')
        
        return {
            'type': hand_type,
            'description': description,
            'characteristics': characteristics,
            'confidence_level': self._get_confidence_level(confidence)
        }
    
    def _get_confidence_level(self, confidence: float) -> str:
        """Convert numerical confidence to descriptive level"""
        
        if confidence >= self.confidence_thresholds['very_high']:
            return 'Very High'
        elif confidence >= self.confidence_thresholds['high']:
            return 'High'
        elif confidence >= self.confidence_thresholds['medium']:
            return 'Medium'
        elif confidence >= self.confidence_thresholds['low']:
            return 'Low'
        else:
            return 'Very Low'
    
    def _generate_detailed_analysis(self, feature_scores: Dict) -> Dict:
        """Generate detailed analysis breakdown"""
        
        analysis = {}
        
        # Metallic surface analysis
        metallic_score = feature_scores.get('metallic_surface', 0)
        if metallic_score > 0.7:
            analysis['surface'] = 'High reflectance metallic surface detected'
        elif metallic_score > 0.4:
            analysis['surface'] = 'Some metallic elements present'
        else:
            analysis['surface'] = 'No significant metallic surfaces detected'
        
        # Joint analysis
        joint_score = feature_scores.get('joint_articulation', 0)
        if joint_score > 0.6:
            analysis['joints'] = 'Artificial joint structures detected'
        elif joint_score > 0.3:
            analysis['joints'] = 'Some mechanical elements visible'
        else:
            analysis['joints'] = 'Natural joint appearance'
        
        # Sensor analysis
        sensor_score = feature_scores.get('sensor_presence', 0)
        if sensor_score > 0.6:
            analysis['sensors'] = 'Electronic sensors and components detected'
        elif sensor_score > 0.3:
            analysis['sensors'] = 'Possible sensor elements present'
        else:
            analysis['sensors'] = 'No electronic components visible'
        
        # Overall assessment
        avg_score = np.mean(list(feature_scores.values()))
        if avg_score > 0.7:
            analysis['overall'] = 'Strong indicators of bionic/prosthetic device'
        elif avg_score > 0.4:
            analysis['overall'] = 'Some artificial characteristics present'
        else:
            analysis['overall'] = 'Appears to be natural biological hand'
        
        return analysis
    
    def _generate_analysis_results(self, bionic_analysis: Dict, 
                                 hand_detection: Dict, image_info: Dict,
                                 processing_time: float) -> Dict:
        """Generate comprehensive analysis results"""
        
        # Determine if this is a valid bionic hand image
        is_bionic = bionic_analysis['is_bionic']
        confidence = bionic_analysis['confidence']
        
        if not is_bionic:
            if confidence < 0.3:
                return {
                    'status': 'error',
                    'error_type': 'detection_error',
                    'message': self.error_messages['no_bionic_features'],
                    'natural_hand_detected': True,
                    'confidence': confidence,
                    'suggestions': [
                        'This appears to be a natural/biological hand',
                        'Please upload an image of a bionic or prosthetic hand',
                        'Ensure the image clearly shows artificial/mechanical elements'
                    ],
                    'timestamp': datetime.now().isoformat(),
                    'processing_time_ms': round(processing_time, 2)
                }
        
        # Generate recommendations based on analysis
        recommendations = self._generate_bionic_recommendations(bionic_analysis)
        
        # Create comprehensive results
        results = {
            'status': 'success',
            'detection': {
                'bionic_detected': is_bionic,
                'confidence_percentage': round(confidence * 100, 1),
                'confidence_level': bionic_analysis['classification']['confidence_level'],
                'hand_type': bionic_analysis['classification']['type'],
                'description': bionic_analysis['classification']['description']
            },
            'analysis': {
                'characteristics': bionic_analysis['classification']['characteristics'],
                'detailed_analysis': bionic_analysis['detailed_analysis'],
                'feature_scores': {k: round(v, 3) for k, v in bionic_analysis['feature_scores'].items()}
            },
            'recommendations': recommendations,
            'technical_details': {
                'image_info': image_info,
                'hand_detection_confidence': round(hand_detection['detection_confidence'], 3),
                'processing_time_ms': round(processing_time, 2),
                'analysis_timestamp': datetime.now().isoformat()
            },
            'quality_metrics': {
                'image_quality': self._assess_image_quality(hand_detection),
                'detection_reliability': self._assess_detection_reliability(bionic_analysis),
                'overall_score': round((confidence * 0.7 + hand_detection['detection_confidence'] * 0.3) * 100, 1)
            }
        }
        
        return results
    
    def _generate_bionic_recommendations(self, analysis: Dict) -> List[Dict]:
        """Generate bionic hand model recommendations based on analysis"""
        
        recommendations = []
        confidence = analysis['confidence']
        features = analysis['feature_scores']
        hand_type = analysis['classification']['type']
        
        if hand_type == 'advanced_bionic_hand':
            recommendations.extend([
                {
                    'model': 'Quantumix Pro Advanced',
                    'reason': 'Detected advanced sensor array and sophisticated control systems',
                    'compatibility': 95,
                    'features': ['Neural interface', 'Multi-sensor feedback', 'AI-assisted control']
                },
                {
                    'model': 'Quantumix Elite Series',
                    'reason': 'High-end bionic hand with precision control capabilities',
                    'compatibility': 90,
                    'features': ['Precision grip', 'Force feedback', 'Wireless connectivity']
                }
            ])
        elif hand_type == 'bionic_hand':
            recommendations.extend([
                {
                    'model': 'Quantumix Standard Plus',
                    'reason': 'Matches detected bionic hand characteristics and sensor configuration',
                    'compatibility': 85,
                    'features': ['EMG control', 'Basic sensors', 'Durable construction']
                },
                {
                    'model': 'Quantumix Adaptive Model',
                    'reason': 'Flexible control system suitable for various bionic hand types',
                    'compatibility': 80,
                    'features': ['Adaptive learning', 'Custom grip patterns', 'Maintenance alerts']
                }
            ])
        elif confidence > 0.4:
            recommendations.append({
                'model': 'Quantumix Entry Model',
                'reason': 'Suitable for mechanical prosthetics with upgrade potential',
                'compatibility': 70,
                'features': ['Basic control', 'Upgrade ready', 'Cost effective']
            })
        else:
            recommendations.append({
                'model': 'Quantumix Assessment Kit',
                'reason': 'Evaluation kit for determining optimal bionic hand configuration',
                'compatibility': 60,
                'features': ['Assessment tools', 'Fitting analysis', 'Recommendation system']
            })
        
        return recommendations[:3]  # Return top 3 recommendations
    
    def _assess_image_quality(self, hand_detection: Dict) -> str:
        """Assess overall image quality for analysis"""
        
        confidence = hand_detection['detection_confidence']
        
        if confidence > 0.8:
            return 'Excellent'
        elif confidence > 0.6:
            return 'Good'
        elif confidence > 0.4:
            return 'Fair'
        else:
            return 'Poor'
    
    def _assess_detection_reliability(self, analysis: Dict) -> str:
        """Assess reliability of bionic detection"""
        
        confidence = analysis['confidence']
        active_features = sum(1 for score in analysis['feature_scores'].values() if score > 0.4)
        
        if confidence > 0.8 and active_features >= 3:
            return 'Very Reliable'
        elif confidence > 0.6 and active_features >= 2:
            return 'Reliable'
        elif confidence > 0.4:
            return 'Moderately Reliable'
        else:
            return 'Low Reliability'
    
    def _initialize_hand_features(self) -> Dict:
        """Initialize hand detection feature parameters"""
        
        return {
            'min_contour_area': 1000,
            'max_aspect_ratio': 2.0,
            'min_aspect_ratio': 0.5,
            'skin_color_ranges': {
                'hsv_lower': np.array([0, 20, 70]),
                'hsv_upper': np.array([20, 255, 255])
            }
        }
    
    def _initialize_bionic_indicators(self) -> Dict:
        """Initialize bionic hand detection indicators"""
        
        return {
            'metallic_colors': [(180, 180, 180), (200, 200, 200), (160, 160, 160)],
            'sensor_sizes': [(3, 15), (5, 20)],  # min_radius, max_radius ranges
            'joint_patterns': ['linear', 'segmented', 'articulated'],
            'surface_materials': ['metal', 'carbon_fiber', 'polymer']
        }


# Helper function for Django integration
def analyze_bionic_hand_image(image_data: Union[bytes, str], filename: str = None) -> Dict:
    """
    Standalone function for Django view integration
    
    Args:
        image_data: Image data (bytes or base64 string)
        filename: Optional filename
        
    Returns:
        Analysis results dictionary
    """
    
    detector = BionicHandDetector()
    return detector.validate_and_analyze_image(image_data, filename)