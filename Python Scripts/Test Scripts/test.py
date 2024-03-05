import fitz  # PyMuPDF 라이브러리

def extract_text_and_images(file_path):
    text = ""
    images = []

    with fitz.open(file_path) as pdf_document:
        for page_num in range(pdf_document.page_count):
            page = pdf_document[page_num]

            # 텍스트 추출
            text += page.get_text()

            # 이미지 추출
            image_list = page.get_images(full=True)
            for img_index, img_info in enumerate(image_list):
                img_index = img_info[0]
                base_image = pdf_document.extract_image(img_index)
                image_bytes = base_image["image"]
                image_extension = base_image["ext"]

                # 이미지를 파일로 저장하거나 리스트에 추가할 수 있습니다.
                # 여기서는 리스트에 추가한 예시입니다.
                images.append({
                    'index': img_index,
                    'image_bytes': image_bytes,
                    'extension': image_extension
                })

    return text, images

# PDF 파일 경로 지정
pdf_file_path = "example.pdf"

# 텍스트와 이미지 추출
pdf_text, pdf_images = extract_text_and_images(pdf_file_path)

# 결과 출력
print("텍스트:\n", pdf_text)
print("\n이미지 정보:\n", pdf_images)
