import uuid


class StorageBackend:
    """
    A stubbed S3 interface for future-proofing.
    In production, this would use boto3 to upload files to an S3-compatible bucket.
    """
    
    def __init__(self, bucket_name: str = "openmcp-registry"):
        self.bucket_name = bucket_name
        self.base_url = f"https://{self.bucket_name}.s3.amazonaws.com"
        
    def upload_file(self, file_content: bytes, filename: str, content_type: str = "application/gzip") -> str:
        """
        Simulates an upload to S3 and returns the public URL.
        """
        # In reality, boto3.client('s3').put_object(...) goes here
        # We will just generate a pseudo-random URL to simulate a successful upload
        unique_key = f"{uuid.uuid4()}-{filename}"
        return f"{self.base_url}/packages/{unique_key}"

# Singleton instance
storage = StorageBackend()
