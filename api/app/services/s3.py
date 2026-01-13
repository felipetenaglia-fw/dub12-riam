import boto3
from botocore.exceptions import ClientError
from typing import Optional
from ..config import get_settings

settings = get_settings()


class S3Service:
    """Service for AWS S3 operations."""
    
    def __init__(self):
        """Initialize S3 client."""
        # Use profile for local development, credentials for production
        if hasattr(settings, 'aws_profile') and settings.aws_profile:
            # Use named profile
            session = boto3.Session(profile_name=settings.aws_profile, region_name=settings.aws_region)
            self.s3_client = session.client('s3')
        elif settings.aws_access_key_id:
            # Use explicit credentials
            self.s3_client = boto3.client(
                's3',
                region_name=settings.aws_region,
                aws_access_key_id=settings.aws_access_key_id,
                aws_secret_access_key=settings.aws_secret_access_key
            )
        else:
            # Use default credentials (IAM role, environment vars, etc.)
            self.s3_client = boto3.client('s3', region_name=settings.aws_region)
        
        self.bucket_name = settings.s3_bucket_name
    
    def generate_presigned_url(self, s3_key: str, expiration: int = 3600) -> Optional[str]:
        """
        Generate a presigned URL for downloading a file from S3.
        
        Args:
            s3_key: The S3 object key
            expiration: URL expiration time in seconds (default 1 hour)
        
        Returns:
            Presigned URL string or None if error
        """
        try:
            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket_name, 'Key': s3_key},
                ExpiresIn=expiration
            )
            return url
        except ClientError as e:
            print(f"Error generating presigned URL: {e}")
            return None
    
    def generate_presigned_upload_url(
        self, 
        s3_key: str, 
        content_type: str = "audio/mpeg",
        expiration: int = 3600
    ) -> Optional[dict]:
        """
        Generate a presigned URL for uploading a file to S3.
        
        Args:
            s3_key: The S3 object key
            content_type: MIME type of the file
            expiration: URL expiration time in seconds (default 1 hour)
        
        Returns:
            Dictionary with presigned URL and fields, or None if error
        """
        try:
            presigned_post = self.s3_client.generate_presigned_post(
                Bucket=self.bucket_name,
                Key=s3_key,
                Fields={"Content-Type": content_type},
                Conditions=[{"Content-Type": content_type}],
                ExpiresIn=expiration
            )
            return presigned_post
        except ClientError as e:
            print(f"Error generating presigned upload URL: {e}")
            return None
    
    def get_object_url(self, s3_key: str) -> str:
        """
        Get the public URL for an S3 object (non-presigned).
        
        Args:
            s3_key: The S3 object key
        
        Returns:
            Full S3 URL
        """
        return f"https://{self.bucket_name}.s3.{settings.aws_region}.amazonaws.com/{s3_key}"
    
    def delete_object(self, s3_key: str) -> bool:
        """
        Delete an object from S3.
        
        Args:
            s3_key: The S3 object key
        
        Returns:
            True if successful, False otherwise
        """
        try:
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=s3_key)
            return True
        except ClientError as e:
            print(f"Error deleting object: {e}")
            return False


# Singleton instance
s3_service = S3Service()
