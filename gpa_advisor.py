#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GPA Advisor System with AI Agent
Crawls student transcript data and provides academic recommendations
"""

import json
import time
import logging
from typing import Dict, List, Any
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# Configure logging for debugging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('gpa_advisor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class TranscriptCrawler:
    """Selenium-based crawler for student transcript data"""
    
    def __init__(self):
        self.driver = None
        self.setup_driver()
    
    def setup_driver(self):
        """Initialize Chrome driver with appropriate options"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            logger.info("Chrome driver initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Chrome driver: {e}")
            raise
    
    def crawl_transcript_data(self, student_id: str = "sample_student") -> Dict[str, Any]:
        """
        Crawl transcript data. For demo purposes, we'll create sample data
        In a real implementation, this would navigate to the student portal
        """
        logger.info(f"Starting transcript crawl for student: {student_id}")
        
        # Simulate crawling process with sample data
        # In real implementation, this would navigate to student portal and extract data
        sample_transcript_data = {
            "student_info": {
                "id": student_id,
                "name": "Nguyen Van A",
                "major": "Công nghệ thông tin",
                "year": "Năm 3"
            },
            "academic_records": [
                {
                    "semester": "Học kỳ 1 - Năm 2023",
                    "subjects": [
                        {"name": "Toán cao cấp", "credits": 3, "grade": "B+", "score": 8.5},
                        {"name": "Lập trình C++", "credits": 4, "grade": "A", "score": 9.0},
                        {"name": "Cơ sở dữ liệu", "credits": 3, "grade": "C+", "score": 6.5},
                        {"name": "Mạng máy tính", "credits": 3, "grade": "B", "score": 7.5}
                    ]
                },
                {
                    "semester": "Học kỳ 2 - Năm 2023", 
                    "subjects": [
                        {"name": "Thuật toán", "credits": 4, "grade": "B+", "score": 8.0},
                        {"name": "Hệ điều hành", "credits": 3, "grade": "C", "score": 6.0},
                        {"name": "Phân tích hệ thống", "credits": 3, "grade": "A-", "score": 8.7},
                        {"name": "Tiếng Anh chuyên ngành", "credits": 2, "grade": "B", "score": 7.0}
                    ]
                },
                {
                    "semester": "Học kỳ 1 - Năm 2024",
                    "subjects": [
                        {"name": "Trí tuệ nhân tạo", "credits": 3, "grade": "A", "score": 9.2},
                        {"name": "Kỹ thuật phần mềm", "credits": 4, "grade": "B", "score": 7.8},
                        {"name": "An toàn thông tin", "credits": 3, "grade": "C+", "score": 6.8},
                        {"name": "Quản lý dự án", "credits": 2, "grade": "B+", "score": 8.3}
                    ]
                }
            ],
            "gpa_summary": {
                "cumulative_gpa": 7.65,
                "total_credits": 33,
                "credits_completed": 33
            }
        }
        
        logger.info("Transcript data crawled successfully")
        return sample_transcript_data
    
    def save_data_to_json(self, data: Dict[str, Any], filepath: str = "ket_qua.json"):
        """Save crawled data to JSON file with proper flushing"""
        try:
            filepath = Path(filepath)
            
            # Ensure data is written and flushed properly
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                f.flush()  # Force flush to disk
            
            # Additional verification that file was written
            time.sleep(0.5)  # Small delay to ensure file system sync
            
            if filepath.exists() and filepath.stat().st_size > 0:
                logger.info(f"Data successfully saved to {filepath}")
                logger.debug(f"File size: {filepath.stat().st_size} bytes")
                return True
            else:
                logger.error(f"File {filepath} was not created properly")
                return False
                
        except Exception as e:
            logger.error(f"Error saving data to JSON: {e}")
            return False
    
    def cleanup(self):
        """Clean up resources"""
        if self.driver:
            try:
                self.driver.quit()
                logger.info("Driver cleanup completed")
            except Exception as e:
                logger.error(f"Error during driver cleanup: {e}")

class DocumentKnowledgeBase:
    """
    Document-based knowledge base for better control and debugging
    Replaces JSONKnowledgeBase with more reliable text-based approach
    """
    
    def __init__(self, knowledge_dir: str = "knowledge_base"):
        self.knowledge_dir = Path(knowledge_dir)
        self.knowledge_dir.mkdir(exist_ok=True)
        self.documents = []
        logger.info(f"DocumentKnowledgeBase initialized at: {self.knowledge_dir}")
    
    def load_from_json(self, json_filepath: str, recreate: bool = True) -> bool:
        """
        Load and convert JSON data to structured text documents
        Uses recreate=True to force reload of new data
        """
        try:
            json_path = Path(json_filepath)
            
            # Verify JSON file exists and has content
            if not json_path.exists():
                logger.error(f"JSON file not found: {json_filepath}")
                return False
            
            if json_path.stat().st_size == 0:
                logger.error(f"JSON file is empty: {json_filepath}")
                return False
            
            # Clear existing documents if recreating
            if recreate:
                self.documents = []
                logger.info("Cleared existing knowledge base for reload")
            
            # Load and parse JSON data
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            logger.info(f"Loaded JSON data from {json_filepath}")
            
            # Convert JSON to structured text documents
            self._convert_json_to_documents(data)
            
            # Save documents to knowledge base directory
            self._save_documents()
            
            logger.info(f"Successfully loaded {len(self.documents)} documents into knowledge base")
            return True
            
        except Exception as e:
            logger.error(f"Error loading JSON data to knowledge base: {e}")
            return False
    
    def _convert_json_to_documents(self, data: Dict[str, Any]):
        """Convert JSON transcript data to structured text documents"""
        
        # Document 1: Student Information
        if "student_info" in data:
            student_doc = self._create_student_info_document(data["student_info"])
            self.documents.append(student_doc)
        
        # Document 2: Academic Performance Summary
        if "gpa_summary" in data:
            gpa_doc = self._create_gpa_summary_document(data["gpa_summary"])
            self.documents.append(gpa_doc)
        
        # Documents 3-N: Semester-wise performance
        if "academic_records" in data:
            for record in data["academic_records"]:
                semester_doc = self._create_semester_document(record)
                self.documents.append(semester_doc)
        
        # Document N+1: Subject Analysis
        if "academic_records" in data:
            subject_analysis_doc = self._create_subject_analysis_document(data["academic_records"])
            self.documents.append(subject_analysis_doc)
    
    def _create_student_info_document(self, student_info: Dict[str, Any]) -> str:
        """Create structured document for student information"""
        return f"""THÔNG TIN SINH VIÊN:
Mã số sinh viên: {student_info.get('id', 'N/A')}
Họ và tên: {student_info.get('name', 'N/A')}
Ngành học: {student_info.get('major', 'N/A')}
Năm học: {student_info.get('year', 'N/A')}
"""
    
    def _create_gpa_summary_document(self, gpa_summary: Dict[str, Any]) -> str:
        """Create structured document for GPA summary"""
        return f"""TỔNG KẾT ĐIỂM:
GPA tích lũy: {gpa_summary.get('cumulative_gpa', 'N/A')}
Tổng số tín chỉ: {gpa_summary.get('total_credits', 'N/A')}
Tín chỉ hoàn thành: {gpa_summary.get('credits_completed', 'N/A')}
Tỷ lệ hoàn thành: {(gpa_summary.get('credits_completed', 0) / max(gpa_summary.get('total_credits', 1), 1) * 100):.1f}%
"""
    
    def _create_semester_document(self, semester_record: Dict[str, Any]) -> str:
        """Create structured document for semester performance"""
        semester = semester_record.get('semester', 'N/A')
        subjects = semester_record.get('subjects', [])
        
        doc = f"""HỌC KỲ: {semester}

DANH SÁCH MÔN HỌC VÀ ĐIỂM SỐ:
"""
        
        total_credits = 0
        total_weighted_score = 0
        
        for subject in subjects:
            name = subject.get('name', 'N/A')
            credits = subject.get('credits', 0)
            grade = subject.get('grade', 'N/A')
            score = subject.get('score', 0)
            
            doc += f"- {name}: {score} điểm ({grade}) - {credits} tín chỉ\n"
            
            total_credits += credits
            total_weighted_score += score * credits
        
        semester_gpa = total_weighted_score / max(total_credits, 1)
        doc += f"\nGPA học kỳ: {semester_gpa:.2f}"
        doc += f"\nTổng tín chỉ học kỳ: {total_credits}"
        
        return doc
    
    def _create_subject_analysis_document(self, academic_records: List[Dict[str, Any]]) -> str:
        """Create subject performance analysis document"""
        all_subjects = []
        
        # Collect all subjects across semesters
        for record in academic_records:
            for subject in record.get('subjects', []):
                all_subjects.append(subject)
        
        # Sort subjects by score to identify strengths and weaknesses
        sorted_subjects = sorted(all_subjects, key=lambda x: x.get('score', 0))
        
        doc = """PHÂN TÍCH HIỆU QUẢ HỌC TẬP:

MÔN HỌC CẦN CẢI THIỆN (Điểm thấp):
"""
        
        # Bottom 30% or subjects with score < 7.0
        weak_subjects = [s for s in sorted_subjects if s.get('score', 0) < 7.0]
        if not weak_subjects:
            weak_subjects = sorted_subjects[:max(1, len(sorted_subjects) // 3)]
        
        for subject in weak_subjects:
            doc += f"- {subject.get('name', 'N/A')}: {subject.get('score', 0)} điểm\n"
        
        doc += "\nMÔN HỌC ĐIỂM CAO (Thế mạnh):\n"
        
        # Top 30% or subjects with score >= 8.0
        strong_subjects = [s for s in sorted_subjects if s.get('score', 0) >= 8.0]
        if not strong_subjects:
            strong_subjects = sorted_subjects[-max(1, len(sorted_subjects) // 3):]
        
        for subject in strong_subjects:
            doc += f"- {subject.get('name', 'N/A')}: {subject.get('score', 0)} điểm\n"
        
        return doc
    
    def _save_documents(self):
        """Save all documents to knowledge base directory"""
        for i, doc in enumerate(self.documents):
            doc_path = self.knowledge_dir / f"document_{i+1}.txt"
            with open(doc_path, 'w', encoding='utf-8') as f:
                f.write(doc)
                f.flush()
        
        logger.info(f"Saved {len(self.documents)} documents to {self.knowledge_dir}")
    
    def search(self, query: str) -> List[str]:
        """Simple search functionality - returns all documents for analysis"""
        logger.info(f"Searching knowledge base with query: {query}")
        return self.documents

class GPAAnalysisAgent:
    """AI Agent for analyzing GPA data and providing recommendations"""
    
    def __init__(self, knowledge_base: DocumentKnowledgeBase):
        self.knowledge_base = knowledge_base
        logger.info("GPAAnalysisAgent initialized")
    
    def analyze_transcript(self) -> Dict[str, Any]:
        """
        Analyze transcript data from knowledge base and provide recommendations
        """
        try:
            logger.info("Starting transcript analysis")
            
            # Search knowledge base for all relevant documents
            documents = self.knowledge_base.search("transcript analysis")
            
            if not documents:
                logger.warning("No documents found in knowledge base")
                return self._create_empty_response()
            
            logger.info(f"Found {len(documents)} documents for analysis")
            
            # Analyze the documents to extract insights
            analysis_result = self._perform_analysis(documents)
            
            logger.info("Transcript analysis completed successfully")
            return analysis_result
            
        except Exception as e:
            logger.error(f"Error during transcript analysis: {e}")
            return self._create_error_response(str(e))
    
    def _perform_analysis(self, documents: List[str]) -> Dict[str, Any]:
        """Perform detailed analysis of transcript documents"""
        
        # Extract data from documents
        student_info = self._extract_student_info(documents)
        gpa_info = self._extract_gpa_info(documents)
        subject_performance = self._extract_subject_performance(documents)
        weak_subjects = self._identify_weak_subjects(documents)
        strong_subjects = self._identify_strong_subjects(documents)
        
        # Generate recommendations based on analysis
        recommendations = self._generate_recommendations(
            gpa_info, weak_subjects, strong_subjects, subject_performance
        )
        
        # Create structured response
        return {
            "nhan_xet": self._create_detailed_assessment(gpa_info, subject_performance),
            "mon_can_cai_thien": weak_subjects,
            "hoc_phan_uu_tien": self._prioritize_subjects(weak_subjects, subject_performance),
            "ke_hoach": recommendations,
            "analysis_metadata": {
                "student_info": student_info,
                "total_subjects_analyzed": len(subject_performance),
                "gpa_trend": self._analyze_gpa_trend(documents)
            }
        }
    
    def _extract_student_info(self, documents: List[str]) -> Dict[str, str]:
        """Extract student information from documents"""
        student_info = {}
        
        for doc in documents:
            if "THÔNG TIN SINH VIÊN" in doc:
                lines = doc.split('\n')
                for line in lines:
                    if "Mã số sinh viên:" in line:
                        student_info['id'] = line.split(':')[1].strip()
                    elif "Họ và tên:" in line:
                        student_info['name'] = line.split(':')[1].strip()
                    elif "Ngành học:" in line:
                        student_info['major'] = line.split(':')[1].strip()
                break
        
        return student_info
    
    def _extract_gpa_info(self, documents: List[str]) -> Dict[str, float]:
        """Extract GPA information from documents"""
        gpa_info = {}
        
        for doc in documents:
            if "TỔNG KẾT ĐIỂM" in doc:
                lines = doc.split('\n')
                for line in lines:
                    if "GPA tích lũy:" in line:
                        try:
                            gpa_info['cumulative_gpa'] = float(line.split(':')[1].strip())
                        except ValueError:
                            pass
                    elif "Tổng số tín chỉ:" in line:
                        try:
                            gpa_info['total_credits'] = float(line.split(':')[1].strip())
                        except ValueError:
                            pass
                break
        
        return gpa_info
    
    def _extract_subject_performance(self, documents: List[str]) -> List[Dict[str, Any]]:
        """Extract subject performance data from documents"""
        subjects = []
        
        for doc in documents:
            if "HỌC KỲ:" in doc and "DANH SÁCH MÔN HỌC" in doc:
                lines = doc.split('\n')
                for line in lines:
                    if line.startswith('- ') and ':' in line:
                        try:
                            # Parse subject line: "- Subject Name: score điểm (grade) - credits tín chỉ"
                            parts = line[2:].split(':')  # Remove "- " prefix
                            subject_name = parts[0].strip()
                            
                            score_part = parts[1].split(' điểm')[0].strip()
                            score = float(score_part)
                            
                            subjects.append({
                                'name': subject_name,
                                'score': score
                            })
                        except (ValueError, IndexError):
                            continue
        
        return subjects
    
    def _identify_weak_subjects(self, documents: List[str]) -> List[str]:
        """Identify subjects that need improvement"""
        weak_subjects = []
        
        for doc in documents:
            if "MÔN HỌC CẦN CẢI THIỆN" in doc:
                lines = doc.split('\n')
                in_weak_section = False
                
                for line in lines:
                    if "MÔN HỌC CẦN CẢI THIỆN" in line:
                        in_weak_section = True
                        continue
                    elif "MÔN HỌC ĐIỂM CAO" in line:
                        break
                    elif in_weak_section and line.startswith('- '):
                        subject_name = line[2:].split(':')[0].strip()
                        weak_subjects.append(subject_name)
                break
        
        return weak_subjects
    
    def _identify_strong_subjects(self, documents: List[str]) -> List[str]:
        """Identify subjects where student performs well"""
        strong_subjects = []
        
        for doc in documents:
            if "MÔN HỌC ĐIỂM CAO" in doc:
                lines = doc.split('\n')
                in_strong_section = False
                
                for line in lines:
                    if "MÔN HỌC ĐIỂM CAO" in line:
                        in_strong_section = True
                        continue
                    elif in_strong_section and line.startswith('- '):
                        subject_name = line[2:].split(':')[0].strip()
                        strong_subjects.append(subject_name)
                break
        
        return strong_subjects
    
    def _prioritize_subjects(self, weak_subjects: List[str], subject_performance: List[Dict[str, Any]]) -> List[str]:
        """Prioritize subjects for improvement based on importance and difficulty"""
        # Simple prioritization: return weak subjects in order of lowest scores
        subject_scores = {s['name']: s['score'] for s in subject_performance}
        
        prioritized = sorted(weak_subjects, 
                           key=lambda x: subject_scores.get(x, 0))
        
        return prioritized[:3]  # Return top 3 priorities
    
    def _generate_recommendations(self, gpa_info: Dict[str, float], 
                                weak_subjects: List[str], 
                                strong_subjects: List[str],
                                subject_performance: List[Dict[str, Any]]) -> Dict[str, str]:
        """Generate study plan and recommendations"""
        
        gpa = gpa_info.get('cumulative_gpa', 0)
        
        if gpa >= 8.0:
            time_frame = "1 học kỳ"
            strategy = "Duy trì phong độ, tập trung vào các môn chuyên sâu"
        elif gpa >= 7.0:
            time_frame = "2 học kỳ"
            strategy = "Cải thiện điểm các môn yếu, tăng cường ôn tập"
        else:
            time_frame = "3 học kỳ"
            strategy = "Học lại các môn điểm thấp, tham gia học nhóm, tìm gia sư"
        
        return {
            "thoi_gian": time_frame,
            "chien_luoc": strategy,
            "ghi_chu": f"Ưu tiên cải thiện {len(weak_subjects)} môn học có điểm thấp"
        }
    
    def _create_detailed_assessment(self, gpa_info: Dict[str, float], 
                                  subject_performance: List[Dict[str, Any]]) -> str:
        """Create detailed assessment text"""
        
        gpa = gpa_info.get('cumulative_gpa', 0)
        total_subjects = len(subject_performance)
        
        if gpa >= 8.0:
            assessment = f"Kết quả học tập tốt với GPA {gpa:.2f}. "
        elif gpa >= 7.0:
            assessment = f"Kết quả học tập khá với GPA {gpa:.2f}. "
        else:
            assessment = f"Kết quả học tập cần cải thiện với GPA {gpa:.2f}. "
        
        assessment += f"Đã phân tích {total_subjects} môn học. "
        
        # Count subjects by performance level
        excellent = len([s for s in subject_performance if s['score'] >= 8.5])
        good = len([s for s in subject_performance if 7.5 <= s['score'] < 8.5])
        average = len([s for s in subject_performance if 6.5 <= s['score'] < 7.5])
        below_average = len([s for s in subject_performance if s['score'] < 6.5])
        
        assessment += f"Trong đó: {excellent} môn xuất sắc, {good} môn tốt, "
        assessment += f"{average} môn trung bình, {below_average} môn yếu."
        
        return assessment
    
    def _analyze_gpa_trend(self, documents: List[str]) -> str:
        """Analyze GPA trend across semesters"""
        semester_gpas = []
        
        for doc in documents:
            if "GPA học kỳ:" in doc:
                lines = doc.split('\n')
                for line in lines:
                    if "GPA học kỳ:" in line:
                        try:
                            gpa = float(line.split(':')[1].strip())
                            semester_gpas.append(gpa)
                        except ValueError:
                            pass
        
        if len(semester_gpas) >= 2:
            if semester_gpas[-1] > semester_gpas[0]:
                return "Tăng"
            elif semester_gpas[-1] < semester_gpas[0]:
                return "Giảm"
            else:
                return "Ổn định"
        
        return "Không đủ dữ liệu"
    
    def _create_empty_response(self) -> Dict[str, Any]:
        """Create response when no data is available"""
        return {
            "nhan_xet": "Không có dữ liệu bảng điểm cụ thể nên không thể phân tích xu hướng học tập và đưa ra lời khuyên chính xác. Vui lòng cung cấp bảng điểm để có thể phân tích chi tiết.",
            "mon_can_cai_thien": [],
            "hoc_phan_uu_tien": [],
            "ke_hoach": {
                "thoi_gian": "2 học kỳ",
                "chien_luoc": "Học nhóm, tăng thời gian tự học, tôn tổt cấm nang học"
            }
        }
    
    def _create_error_response(self, error_message: str) -> Dict[str, Any]:
        """Create response when error occurs"""
        return {
            "nhan_xet": f"Lỗi trong quá trình phân tích: {error_message}",
            "mon_can_cai_thien": [],
            "hoc_phan_uu_tien": [],
            "ke_hoach": {
                "thoi_gian": "N/A",
                "chien_luoc": "Vui lòng kiểm tra lại dữ liệu và thử lại"
            },
            "error": error_message
        }

def main():
    """Main function to run the GPA advisor system"""
    logger.info("Starting GPA Advisor System")
    
    crawler = None
    try:
        # Step 1: Initialize and run transcript crawler
        logger.info("Initializing transcript crawler...")
        crawler = TranscriptCrawler()
        
        # Step 2: Crawl transcript data
        logger.info("Crawling transcript data...")
        transcript_data = crawler.crawl_transcript_data()
        
        # Step 3: Save data to JSON with proper flushing
        logger.info("Saving data to ket_qua.json...")
        json_file = "ket_qua.json"
        save_success = crawler.save_data_to_json(transcript_data, json_file)
        
        if not save_success:
            logger.error("Failed to save data to JSON file")
            return
        
        # Step 4: Wait to ensure file is completely written
        logger.info("Waiting for file system sync...")
        time.sleep(1.0)  # Additional safety delay
        
        # Step 5: Initialize DocumentKnowledgeBase with recreate=True
        logger.info("Initializing DocumentKnowledgeBase...")
        knowledge_base = DocumentKnowledgeBase()
        
        # Step 6: Load JSON data to knowledge base
        logger.info("Loading data to knowledge base...")
        load_success = knowledge_base.load_from_json(json_file, recreate=True)
        
        if not load_success:
            logger.error("Failed to load data to knowledge base")
            return
        
        # Step 7: Initialize AI agent
        logger.info("Initializing AI agent...")
        agent = GPAAnalysisAgent(knowledge_base)
        
        # Step 8: Perform analysis
        logger.info("Performing transcript analysis...")
        analysis_result = agent.analyze_transcript()
        
        # Step 9: Output results
        logger.info("Analysis completed successfully!")
        print("\n" + "="*50)
        print("KẾT QUẢ PHÂN TÍCH BẢNG ĐIỂM")
        print("="*50)
        print(json.dumps(analysis_result, ensure_ascii=False, indent=2))
        
        # Step 10: Save analysis result
        result_file = "analysis_result.json"
        with open(result_file, 'w', encoding='utf-8') as f:
            json.dump(analysis_result, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Analysis result saved to {result_file}")
        
    except Exception as e:
        logger.error(f"Error in main execution: {e}")
        raise
    
    finally:
        # Cleanup
        if crawler:
            crawler.cleanup()
        logger.info("GPA Advisor System finished")

if __name__ == "__main__":
    main()