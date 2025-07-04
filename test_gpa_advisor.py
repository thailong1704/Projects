#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GPA Advisor System Test - Simplified version for testing
Tests the core functionality without requiring Chrome driver
"""

import json
import time
import logging
from typing import Dict, List, Any
from pathlib import Path

# Configure logging for debugging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('gpa_advisor_test.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class MockTranscriptCrawler:
    """Mock crawler for testing without selenium dependencies"""
    
    def __init__(self):
        logger.info("Mock TranscriptCrawler initialized")
    
    def crawl_transcript_data(self, student_id: str = "sample_student") -> Dict[str, Any]:
        """Create sample transcript data for testing"""
        logger.info(f"Creating sample transcript data for student: {student_id}")
        
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
        
        logger.info("Sample transcript data created successfully")
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
        """Clean up resources (no-op for mock)"""
        logger.info("Mock crawler cleanup completed")

# Import the DocumentKnowledgeBase and GPAAnalysisAgent from the main module
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gpa_advisor import DocumentKnowledgeBase, GPAAnalysisAgent

def test_gpa_advisor_system():
    """Test the GPA advisor system with mock data"""
    logger.info("Starting GPA Advisor System Test")
    
    crawler = None
    try:
        # Step 1: Initialize mock crawler
        logger.info("Initializing mock transcript crawler...")
        crawler = MockTranscriptCrawler()
        
        # Step 2: Create sample transcript data
        logger.info("Creating sample transcript data...")
        transcript_data = crawler.crawl_transcript_data()
        
        # Step 3: Save data to JSON with proper flushing
        logger.info("Saving data to ket_qua.json...")
        json_file = "ket_qua.json"
        save_success = crawler.save_data_to_json(transcript_data, json_file)
        
        if not save_success:
            logger.error("Failed to save data to JSON file")
            return False
        
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
            return False
        
        # Step 7: Initialize AI agent
        logger.info("Initializing AI agent...")
        agent = GPAAnalysisAgent(knowledge_base)
        
        # Step 8: Perform analysis
        logger.info("Performing transcript analysis...")
        analysis_result = agent.analyze_transcript()
        
        # Step 9: Verify results
        logger.info("Verifying analysis results...")
        success = verify_analysis_result(analysis_result)
        
        if success:
            # Step 10: Output results
            logger.info("Analysis completed successfully!")
            print("\n" + "="*50)
            print("KẾT QUẢ PHÂN TÍCH BẢNG ĐIỂM")
            print("="*50)
            print(json.dumps(analysis_result, ensure_ascii=False, indent=2))
            
            # Step 11: Save analysis result
            result_file = "analysis_result.json"
            with open(result_file, 'w', encoding='utf-8') as f:
                json.dump(analysis_result, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Analysis result saved to {result_file}")
            return True
        else:
            logger.error("Analysis result verification failed")
            return False
        
    except Exception as e:
        logger.error(f"Error in test execution: {e}")
        return False
    
    finally:
        # Cleanup
        if crawler:
            crawler.cleanup()
        logger.info("GPA Advisor System Test finished")

def verify_analysis_result(result: Dict[str, Any]) -> bool:
    """Verify that the analysis result has the expected structure and content"""
    
    # Check that all required fields are present
    required_fields = ["nhan_xet", "mon_can_cai_thien", "hoc_phan_uu_tien", "ke_hoach"]
    
    for field in required_fields:
        if field not in result:
            logger.error(f"Missing required field: {field}")
            return False
    
    # Verify that we have actual data (not the empty response)
    if not result["mon_can_cai_thien"] and "không có dữ liệu" in result["nhan_xet"].lower():
        logger.error("Analysis returned empty response - knowledge base not working properly")
        return False
    
    # Check that we found weak subjects
    if len(result["mon_can_cai_thien"]) == 0:
        logger.warning("No weak subjects identified - this may be unexpected for test data")
    
    # Check that assessment contains meaningful content
    if len(result["nhan_xet"]) < 50:
        logger.error("Assessment text is too short - may not contain proper analysis")
        return False
    
    # Verify ke_hoach structure
    if "ke_hoach" in result:
        ke_hoach = result["ke_hoach"]
        if "thoi_gian" not in ke_hoach or "chien_luoc" not in ke_hoach:
            logger.error("ke_hoach missing required subfields")
            return False
    
    logger.info("Analysis result verification passed")
    return True

if __name__ == "__main__":
    success = test_gpa_advisor_system()
    if success:
        print("\n✅ Test PASSED: GPA Advisor System working correctly!")
        print("The system successfully:")
        print("- Loaded transcript data")
        print("- Converted to DocumentKnowledgeBase format")
        print("- Analyzed data with AI agent") 
        print("- Generated meaningful recommendations")
    else:
        print("\n❌ Test FAILED: Issues found in GPA Advisor System")
        sys.exit(1)