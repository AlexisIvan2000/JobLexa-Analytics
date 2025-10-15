import os
from fastapi import UploadFile

UPLOAD_FOLDER = "uploads"

class Uploader:
    def __init__(self):
        self.allowed_extensions = {'pdf', 'docx'}
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)

    def allowed_file(self, filename: str) -> bool:
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in self.allowed_extensions

    async def upload_file(self, file: UploadFile):
        if not file:
            return None, "No file provided"
        if file.filename == "":
            return None, "No selected file"
        if not self.allowed_file(file.filename):
            return None, "Unsupported file type. Use PDF or DOCX."

        try:
            filename = os.path.basename(file.filename)
            save_path = os.path.join(UPLOAD_FOLDER, filename)

            with open(save_path, "wb") as buffer:
                content = await file.read()
                buffer.write(content)

            return save_path, "File uploaded successfully"
        except Exception as e:
            return None, f"File upload failed: {str(e)}"
