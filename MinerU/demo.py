import os
import sys
from mineru.cli.client import main as mineru_main

if __name__ == "__main__":
    # 1. 환경 변수에서 기본 옵션 읽기 (Docker Compose 연동용)
    input_path = os.getenv("INPUT_PATH", "demo/pdfs/demo1.pdf")
    output_dir = os.getenv("OUTPUT_DIR", "output_result")
    backend = os.getenv("BACKEND", "pipeline")
    method = os.getenv("METHOD", "auto")
    lang = os.getenv("LANG", "korean")

    # 2. 명령줄 인자가 아무것도 전달되지 않았을 때만 위 기본값들을 적용
    if len(sys.argv) == 1:
        sys.argv.extend([
            "-p", input_path,
            "-o", output_dir,
            "-b", backend,
            "-m", method,
            "-l", lang
        ])
    
    # 3. MinerU CLI 실행
    mineru_main()