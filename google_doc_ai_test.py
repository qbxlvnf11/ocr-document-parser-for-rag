import os
import io
import sys
import logging
import time
from pathlib import Path
from dotenv import load_dotenv
from google.api_core.client_options import ClientOptions
from google.cloud import documentai_v1 as documentai
from pypdf import PdfReader, PdfWriter

# 1. 환경 변수 및 로깅 설정
load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def format_time(seconds: float) -> str:
    ms = seconds * 1000
    if ms < 1000:
        return f"{ms:.2f}ms"
    return f"{seconds:.2f}s"

def process_layout_parser(client, processor_name, pdf_bytes):
    """Document AI API 호출 로직 (Layout Parser v1.5)"""
    raw_document = documentai.RawDocument(content=pdf_bytes, mime_type="application/pdf")

    # RAG 전용 레이아웃 설정
    process_options = documentai.ProcessOptions(
        layout_config=documentai.ProcessOptions.LayoutConfig(
            chunking_config=documentai.ProcessOptions.LayoutConfig.ChunkingConfig(
                chunk_size=1024,
                include_ancestor_headings=True, # 문맥 보존을 위해 상위 제목 포함
            ),
        ),
    )

    request = documentai.ProcessRequest(
        name=processor_name,
        raw_document=raw_document,
        process_options=process_options,
    )

    result = client.process_document(request=request)
    return result.document

def run_pipeline(input_path: str):
    start_total = time.perf_counter()
    
    # 2. 환경 변수 로드
    project_id = os.getenv("GCP_PROJECT_ID")
    location = os.getenv("GCP_LOCATION", "us")
    processor_id = os.getenv("GCP_PROCESSOR_ID")
    
    if not all([project_id, processor_id]):
        logger.error("❌ .env 파일에 GCP_PROJECT_ID 또는 GCP_PROCESSOR_ID가 설정되지 않았습니다.")
        return

    # 3. 경로 설정
    pdf_file = Path(input_path)
    if not pdf_file.exists():
        logger.error(f"❌ 파일을 찾을 수 없습니다: {pdf_file.absolute()}")
        return

    # 출력 파일명: [파일명]_google_doc_ai_layout_parser.md
    output_file = pdf_file.with_name(f"{pdf_file.stem}_google_doc_ai_layout_parser.md")

    # 4. 클라이언트 초기화
    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")
    client = documentai.DocumentProcessorServiceClient(client_options=opts)
    
    # 레이아웃 파서 v1.5 고정 버전 설정
    processor_version_id = 'pretrained-layout-parser-v1.5-2025-08-25'
    processor_name = f"projects/{project_id}/locations/{location}/processors/{processor_id}/processorVersions/{processor_version_id}"

    # 5. PDF 읽기 및 설정
    reader = PdfReader(str(pdf_file))
    total_pages = len(reader.pages)
    chunk_page_limit = 15  # 안전한 처리를 위한 페이지 분할 단위
    merged_text = ""

    logger.info(f"🚀 분석 시작: {pdf_file.name} (총 {total_pages}p)")
    logger.info(f"📂 저장 경로: {output_file.absolute()}")

    # 6. 메인 처리 루프
    for start in range(0, total_pages, chunk_page_limit):
        end = min(start + chunk_page_limit, total_pages)
        chunk_start_time = time.perf_counter()
        logger.info(f"🔄 처리 중: {start+1} ~ {end} 페이지 / {total_pages}p")

        # 메모리 내에서 PDF 분할
        writer = PdfWriter()
        for i in range(start, end):
            writer.add_page(reader.pages[i])
        
        pdf_buffer = io.BytesIO()
        writer.write(pdf_buffer)
        pdf_bytes = pdf_buffer.getvalue()

        try:
            # 분리된 함수 호출
            document = process_layout_parser(client, processor_name, pdf_bytes)

            if hasattr(document, 'chunked_document'):
                # 각 청크의 텍스트를 하나의 문자열로 결합
                for chunk_id, chunk in enumerate(document.chunked_document.chunks):
                    logging.info(f"========> Chunk {chunk_id} content <========\n\n{chunk.content}")
                    merged_text += chunk.content + "\n\n"
                    logging.info(f"====================================================\n")
                
                chunk_duration = time.perf_counter() - chunk_start_time
                logger.info(f"   ✅ 성공! ({format_time(chunk_duration)})")
            else:
                logger.warning(f"   ⚠️ 페이지 {start+1}~{end}: 데이터가 비어있습니다.")

        except Exception as e:
            logger.error(f"   ❌ 에러 발생 (페이지 {start+1}~{end}): {e}")
        
        # API 쿼터 보호를 위한 대기
        time.sleep(0.5)

    # 7. 단일 마크다운 파일로 저장
    if merged_text.strip():
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(merged_text.strip())
        
        total_duration = time.perf_counter() - start_total
        logger.info(f"✨ 모든 작업 완료! 총 소요 시간: {format_time(total_duration)}")
        logger.info(f"📝 결과 확인: {output_file.name}")
    else:
        logger.error("❌ 추출된 데이터가 없습니다.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python layout_parser_merged.py <pdf_path>")
    else:
        run_pipeline(sys.argv[1])