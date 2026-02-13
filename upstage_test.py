import requests
import json
import sys
import os
from dotenv import load_dotenv

# .env 파일로부터 환경 변수를 불러옵니다.
load_dotenv()

def process_document(pdf_filename):
    # 1. 설정값 (환경 변수에서 가져오기)
    api_key = os.getenv("UPSTAGE_API_KEY")
    
    if not api_key:
        print("❌ Error: .env 파일에 'UPSTAGE_API_KEY'가 설정되어 있지 않습니다.")
        return

    url = "https://api.upstage.ai/v1/document-digitization"
    headers = {"Authorization": f"Bearer {api_key}"}

    if not os.path.exists(pdf_filename):
        print(f"❌ Error: 파일을 찾을 수 없습니다 -> {pdf_filename}")
        return

    try:
        print(f"🚀 1. Upstage API로 파일 전송 중: {pdf_filename}...")
        
        with open(pdf_filename, "rb") as f:
            files = {"document": f}
            data = {
                "model": "document-parse",
                "ocr": "force",
                "output_formats": "['html', 'markdown']"
            }
            response = requests.post(url, headers=headers, files=files, data=data)
        
        if response.status_code != 200:
            print(f"❌ API 오류: {response.status_code}\n{response.text}")
            return
        
        result = response.json()
        elements = result.get("elements", [])
        
        if not elements:
            print("⚠️ 추출된 데이터(elements)가 없습니다.")
            return

        base_name = os.path.splitext(pdf_filename)[0]
        
        # 2. HTML 병합 및 저장
        print("📝 2. HTML 결과물 생성 중...")
        html_parts = []
        for el in elements:
            h = el.get("content", {}).get("html", "")
            if h: html_parts.append(h)
        
        # 표 테두리 스타일 추가
        full_html = (
            "<html><head><meta charset='utf-8'>"
            "<style>table { border-collapse: collapse; width: 100%; margin-bottom: 20px; } "
            "th, td { border: 1px solid black; padding: 8px; text-align: left; }</style>"
            "</head><body>\n"
        )
        full_html += "\n".join(html_parts)
        full_html += "\n</body></html>"
        
        html_output = f"{base_name}_merged.html"
        with open(html_output, "w", encoding="utf-8") as f:
            f.write(full_html)
        print(f"   ✅ HTML 저장 완료: {html_output}")

        # 3. Markdown 병합 및 저장
        print("📝 3. 마크다운 결과물 생성 중...")
        md_parts = []
        for el in elements:
            content = el.get("content", {})
            md = content.get("markdown", "")
            if not md:
                md = content.get("text", "")
            if md:
                md_parts.append(md)
        
        full_md = "\n\n".join(md_parts)
        md_output = f"{base_name}_merged.md"
        with open(md_output, "w", encoding="utf-8") as f:
            f.write(full_md)
        print(f"   ✅ 마크다운 저장 완료: {md_output}")

        print("\n✨ 모든 변환 작업이 성공적으로 완료되었습니다!")

    except Exception as e:
        print(f"❗ 프로그램 실행 중 오류 발생: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("사용법: python upstage_converter.py <pdf_파일명>")
    else:
        process_document(sys.argv[1])