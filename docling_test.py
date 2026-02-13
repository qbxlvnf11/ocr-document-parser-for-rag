import sys
import os
from docling.document_converter import DocumentConverter
from docling.datamodel.pipeline_options import PdfPipelineOptions

def convert():
    # 1. 실행 인자로 파일 경로가 들어왔는지 확인
    if len(sys.argv) > 1:
        source = sys.argv[1]
    else:
        # 인자가 없을 경우 기본 파일명 지정 (또는 에러 메시지)
        source = "test.pdf" 
        print(f"입력된 파일 경로가 없어 기본 파일({source})로 진행합니다.")

    # 2. 파일 존재 여부 확인 (URL이 아닌 경우)
    if not source.startswith("http") and not os.path.exists(source):
        print(f"에러: 파일을 찾을 수 없습니다 -> {source}")
        return

    print(f"변환 시작: {source}...") 
    pipeline_options = PdfPipelineOptions()
    pipeline_options.do_ocr = True
    pipeline_options.ocr_options.lang = ["ko", "en"]
    
    try:
        
        # 출력 파일명 생성 (입력파일명.md)
        # output_filename = f"{os.path.splitext(os.path.basename(source))[0]}.md"
        source_dir = os.path.dirname(source)
        file_base_name = os.path.splitext(os.path.basename(source))[0]
        output_filename = f"{file_base_name}.md"
        output_filename = os.path.join(source_dir, output_filename)

        converter = DocumentConverter()
        result = converter.convert(source)
               
        md_output = result.document.export_to_markdown()
        
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(md_output)
        
        print(f"변환 완료! 결과 파일: {output_filename}")
        
    except Exception as e:
        print(f"변환 중 오류 발생: {e}")

if __name__ == "__main__":
    convert()