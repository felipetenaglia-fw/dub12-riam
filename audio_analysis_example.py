#!/usr/bin/env python3
"""
Example: Using AWS Bedrock Converse API for Audio Analysis

This script demonstrates how to analyze an audio file using AWS Bedrock's
Converse API with Claude models that support audio input.
"""

import boto3
import json
import base64
from pathlib import Path

# AWS Configuration
AWS_PROFILE = "FLY-Admin-Flywheel-Dev-803109464991"
AWS_REGION = "us-east-1"


def analyze_audio_with_bedrock(audio_file_path: str, prompt: str = None, profile: str = AWS_PROFILE):
    """
    Analyze an audio file using AWS Bedrock Converse API.

    Args:
        audio_file_path: Path to the audio file (mp3, wav, etc.)
        prompt: Optional custom prompt for analysis
        profile: AWS profile name to use

    Returns:
        dict: Response from Bedrock containing the analysis
    """
    # Initialize Bedrock client with profile
    session = boto3.Session(profile_name=profile)
    bedrock = session.client(
        service_name='bedrock-runtime',
        region_name=AWS_REGION
    )

    # Read and encode the audio file
    audio_path = Path(audio_file_path)
    with open(audio_path, 'rb') as audio_file:
        audio_bytes = audio_file.read()

    # Determine media type based on file extension
    extension = audio_path.suffix.lower()
    media_type_map = {
        '.mp3': 'audio/mpeg',
        '.wav': 'audio/wav',
        '.ogg': 'audio/ogg',
        '.flac': 'audio/flac',
        '.webm': 'audio/webm',
    }
    media_type = media_type_map.get(extension, 'audio/mpeg')

    # Default prompt if none provided
    if prompt is None:
        prompt = (
            "Please analyze this audio file and provide:\n"
            "1. A transcription of the speech\n"
            "2. Summary of key points discussed\n"
            "3. Speaker sentiment and tone\n"
            "4. Any notable background sounds or music"
        )

    # Construct the message with audio content
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "document": {
                        "format": extension[1:],  # Remove the dot
                        "name": audio_path.name,
                        "source": {
                            "bytes": audio_bytes
                        }
                    }
                },
                {
                    "text": prompt
                }
            ]
        }
    ]

    # Model configuration
    model_id = "anthropic.claude-sonnet-4-5-20250929-v1:0"  # Claude Sonnet 4.5 with audio support

    # Call Bedrock Converse API
    try:
        response = bedrock.converse(
            modelId=model_id,
            messages=messages,
            inferenceConfig={
                "maxTokens": 4096,
                "temperature": 0.7,
            }
        )

        return response

    except Exception as e:
        print(f"Error calling Bedrock: {e}")
        raise


def main():
    """Main function to demonstrate audio analysis."""

    # Path to your audio file
    audio_file = "input.mp3"

    print(f"Analyzing audio file: {audio_file}")
    print("-" * 60)

    # Custom prompt for analysis
    custom_prompt = """
    Please analyze this audio recording and provide:

    1. A detailed transcription
    2. Summary of the main topics
    3. Key insights or action items
    4. Sentiment analysis
    5. Any recommendations based on the content
    """

    try:
        # Analyze the audio
        response = analyze_audio_with_bedrock(audio_file, custom_prompt)

        # Extract the response text
        output_text = response['output']['message']['content'][0]['text']

        # Print results
        print("\nAnalysis Results:")
        print("=" * 60)
        print(output_text)
        print("=" * 60)

        # Print usage information
        usage = response.get('usage', {})
        print(f"\nToken Usage:")
        print(f"  Input tokens: {usage.get('inputTokens', 'N/A')}")
        print(f"  Output tokens: {usage.get('outputTokens', 'N/A')}")

        # Print metadata
        print(f"\nModel: {response.get('ResponseMetadata', {}).get('HTTPHeaders', {}).get('x-amzn-bedrock-model-id', 'N/A')}")
        print(f"Stop reason: {response['stopReason']}")

        return output_text

    except FileNotFoundError:
        print(f"Error: Audio file '{audio_file}' not found.")
        return None
    except Exception as e:
        print(f"Error during analysis: {e}")
        return None


# Alternative: Using streaming for real-time responses
def analyze_audio_streaming(audio_file_path: str, prompt: str = None, profile: str = AWS_PROFILE):
    """
    Analyze audio with streaming response for real-time output.

    Args:
        audio_file_path: Path to the audio file
        prompt: Optional custom prompt
        profile: AWS profile name to use
    """
    # Initialize Bedrock client with profile
    session = boto3.Session(profile_name=profile)
    bedrock = session.client(
        service_name='bedrock-runtime',
        region_name=AWS_REGION
    )

    # Read audio file
    with open(audio_file_path, 'rb') as f:
        audio_bytes = f.read()

    # Determine media type
    extension = Path(audio_file_path).suffix.lower()

    if prompt is None:
        prompt = "Please transcribe and analyze this audio."

    messages = [
        {
            "role": "user",
            "content": [
                {
                    "document": {
                        "format": extension[1:],
                        "name": Path(audio_file_path).name,
                        "source": {"bytes": audio_bytes}
                    }
                },
                {"text": prompt}
            ]
        }
    ]

    model_id = "anthropic.claude-sonnet-4-5-20250929-v1:0"  # Claude Sonnet 4.5 with audio support

    print("Streaming response:")
    print("-" * 60)

    try:
        # Use converse_stream for streaming responses
        response = bedrock.converse_stream(
            modelId=model_id,
            messages=messages,
            inferenceConfig={"maxTokens": 4096, "temperature": 0.7}
        )

        # Process the stream
        full_text = ""
        for event in response['stream']:
            if 'contentBlockDelta' in event:
                delta = event['contentBlockDelta']['delta']
                if 'text' in delta:
                    text_chunk = delta['text']
                    print(text_chunk, end='', flush=True)
                    full_text += text_chunk
            elif 'messageStop' in event:
                print("\n" + "-" * 60)
                print(f"Stop reason: {event['messageStop']['stopReason']}")

        return full_text

    except Exception as e:
        print(f"Error during streaming: {e}")
        raise


if __name__ == "__main__":
    # Example 1: Standard analysis
    print("=" * 60)
    print("EXAMPLE 1: Standard Audio Analysis")
    print("=" * 60)
    main()

    print("\n\n")

    # Example 2: Streaming analysis
    print("=" * 60)
    print("EXAMPLE 2: Streaming Audio Analysis")
    print("=" * 60)
    analyze_audio_streaming("input.mp3", "Please transcribe this audio and provide a brief summary.")
