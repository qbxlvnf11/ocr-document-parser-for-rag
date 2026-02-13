### 🔍 Doc Parsers
* [Docling](https://github.com/docling-project/docling)
* [Upstage Doc Parser](https://www.upstage.ai/products/document-parse)
* [Upstage Doc Parser API Details](https://console.upstage.ai/api/document-digitization/document-parsing)
* [Google Document AI v1beta3](https://docs.cloud.google.com/document-ai/docs/reference/rpc/google.cloud.documentai.v1beta3)
* [Google Document AI Layout Parse](https://docs.cloud.google.com/document-ai/docs/layout-parse-quickstart#python)

### - Environment Configuration
* The script relies on a .env file located in the project root. Create a file named .env and include the following variables:

```ini
UPSTAGE_API_KEY=...
# Google Cloud or Document AI Settings
GCP_PROJECT_ID=...
GCP_LOCATION=...
GCP_PROCESSOR_ID=...
```

### - How to Run
* Docling Doc Parser

```bash
docker compose run docling-app python docling_test.py {pdf_file_path}
```

* Upstage Doc Parser

```bash
docker compose run upstage-app python upstage_test.py {pdf_file_path}
```

* Google Document AI Parser (Layout Parser v1.5)

```bash
docker compose run google-doc-ai-app python google_doc_ai_test.py {pdf_file_path}
```

---

## Author

#### - [LinkedIn](https://www.linkedin.com/in/taeyong-kong-016bb2154)

#### - [Blog URL](https://blog.naver.com/qbxlvnf11)

#### - Email: qbxlvnf11@google.com, qbxlvnf11@naver.com


