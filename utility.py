from fastapi import UploadFile, HTTPException, status


def validate_file(file: UploadFile):
    if file.content_type != 'application/pdf':
         raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail="Only .pdf files are allowed")
    
    if file.size>5242880: #5mb in bytes
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail="File size should be less than oe equals to 5 MB")