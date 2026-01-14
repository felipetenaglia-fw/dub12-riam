"""
Bedrock Service - AWS Bedrock integration for AI music coaching.

This service combines Librosa audio analysis with Claude AI to provide
comprehensive music coaching feedback based on actual performance metrics.
"""

import boto3
import json
from botocore.exceptions import ClientError
from typing import Optional

from ..config import get_settings
from .audio_analysis import audio_analysis_service

settings = get_settings()


class BedrockService:
    """Service for AWS Bedrock operations with Claude."""
    
    def __init__(self):
        """Initialize Bedrock client."""
        # Use profile for local development, credentials for production
        if hasattr(settings, 'aws_profile') and settings.aws_profile:
            session = boto3.Session(profile_name=settings.aws_profile, region_name=settings.aws_region)
            self.bedrock_runtime = session.client('bedrock-runtime')
        elif settings.aws_access_key_id:
            self.bedrock_runtime = boto3.client(
                'bedrock-runtime',
                region_name=settings.aws_region,
                aws_access_key_id=settings.aws_access_key_id,
                aws_secret_access_key=settings.aws_secret_access_key
            )
        else:
            self.bedrock_runtime = boto3.client('bedrock-runtime', region_name=settings.aws_region)
        
        # Use Claude 3.5 Sonnet v2
        self.model_id = "us.anthropic.claude-3-5-sonnet-20241022-v2:0"
    
    def analyze_audio_performance(
        self, 
        audio_data: bytes,
        audio_format: str = "mp3",
        piece_name: Optional[str] = None,
        composer: Optional[str] = None,
        student_notes: Optional[str] = None
    ) -> Optional[dict]:
        """
        Analyze a student's musical performance using Librosa audio analysis
        and Claude AI for comprehensive coaching feedback.
        
        Args:
            audio_data: Raw audio file bytes
            audio_format: Audio file format (mp3, wav, etc.)
            piece_name: Optional name of the piece (helps with context)
            composer: Optional composer name (helps with context)
            student_notes: Optional notes or questions from the student
            
        Returns:
            Dictionary with audio analysis and coaching feedback
        """
        try:
            file_size_mb = len(audio_data) / 1024 / 1024
            print(f"🎵 Processing {file_size_mb:.2f}MB {audio_format} file for AI coaching...")
            
            # Step 1: Extract audio features using Librosa
            try:
                features = audio_analysis_service.extract_features(audio_data, audio_format)
            except Exception as e:
                print(f"⚠️ Audio analysis error: {e}")
                # If audio analysis fails, provide text-based feedback
                return self._provide_text_only_feedback(
                    file_size_mb, audio_format, piece_name, composer, student_notes
                )
            
            # Step 2: Generate coaching feedback with Claude using the extracted features
            feedback = self._generate_coaching_feedback(
                features, piece_name, composer, student_notes
            )
            
            return {
                "success": True,
                "feedback": feedback,
                "audio_analysis": features,
                "model": self.model_id
            }
            
        except ClientError as e:
            print(f"Error calling Bedrock: {e}")
            return {
                "success": False,
                "error": str(e),
                "feedback": None
            }
        except Exception as e:
            print(f"Unexpected error: {e}")
            return {
                "success": False,
                "error": str(e),
                "feedback": None
            }
    
    def _generate_coaching_feedback(
        self,
        features: dict,
        piece_name: Optional[str] = None,
        composer: Optional[str] = None,
        student_notes: Optional[str] = None
    ) -> str:
        """Generate comprehensive coaching feedback using Claude based on audio analysis."""
        
        # Build context section
        context_parts = []
        if piece_name:
            context_parts.append(f"🎵 **Piece:** {piece_name}")
        if composer:
            context_parts.append(f"👤 **Composer:** {composer}")
        if student_notes:
            context_parts.append(f"💭 **Student's Notes:** {student_notes}")
        
        context = "\n".join(context_parts) if context_parts else "No additional context provided."
        
        # Create the coaching prompt with actual metrics
        prompt = f"""You are a master music teacher at the Royal Irish Academy of Music (RIAM) with decades of experience coaching instrumentalists. A student has submitted a practice recording which has been analyzed.

## Student Context
{context}

## Audio Analysis Results

### Basic Information
- **Duration:** {features['basic_info']['duration_formatted']} ({features['basic_info']['duration_seconds']:.1f} seconds)
- **File Size:** {features['basic_info']['file_size_mb']:.2f} MB

### Tempo & Rhythm Analysis
- **Tempo:** {features['tempo_rhythm']['tempo_bpm']:.1f} BPM ({features['tempo_rhythm']['tempo_category']})
- **Tempo Stability:** {features['tempo_rhythm']['tempo_stability_score']:.0%} (higher = more stable)
- **Tempo Variation:** {features['tempo_rhythm']['tempo_variation_percent']:.1f}%
- **Rhythm Regularity:** {features['tempo_rhythm']['rhythm_regularity_score']:.0%}
- **Note Density:** {features['tempo_rhythm']['notes_per_second']:.1f} notes/second

### Pitch & Intonation
- **Estimated Key:** {features['pitch_intonation']['estimated_key']} (confidence: {features['pitch_intonation']['key_confidence']:.0%})
- **Pitch Stability:** {features['pitch_intonation']['pitch_stability_score']:.0%}
- **Pitch Range:** {features['pitch_intonation']['pitch_range_semitones']:.1f} semitones
- **Harmonic Content:** {features['pitch_intonation']['harmonic_content_ratio']:.0%}

### Dynamics
- **Dynamic Range:** {features['dynamics']['dynamic_range_db']:.1f} dB ({features['dynamics']['dynamic_range_category']})
- **Dynamic Contrast:** {features['dynamics']['dynamic_contrast_score']:.0%}
- **Expressiveness:** {features['dynamics']['dynamic_expressiveness']}
- **Crescendo Presence:** {features['dynamics']['crescendo_presence']:.0%}
- **Decrescendo Presence:** {features['dynamics']['decrescendo_presence']:.0%}

### Tone Quality
- **Brightness:** {features['tone_quality']['brightness_score']:.0%}
- **Warmth:** {features['tone_quality']['tone_warmth']:.0%}
- **Brightness Consistency:** {features['tone_quality']['brightness_consistency']:.0%}
- **Timbre Consistency:** {features['tone_quality']['timbre_consistency']:.0%}
- **Tone Character:** {features['tone_quality']['tonal_vs_noisy']}

### Articulation
- **Attack Clarity:** {features['articulation']['attack_clarity_score']:.0%}
- **Note Separation Consistency:** {features['articulation']['note_separation_consistency']:.0%}
- **Predominant Articulation:** {features['articulation']['predominant_articulation']}
- **Staccato Tendency:** {features['articulation']['staccato_tendency']:.0%}
- **Legato Tendency:** {features['articulation']['legato_tendency']:.0%}

### Musical Structure
- **Estimated Sections:** {features['musical_structure']['estimated_sections']}
- **Musical Development:** {features['musical_structure']['musical_development_score']:.0%}

### Overall Performance Scores
- **Technical Proficiency:** {features['performance_scores']['technical_proficiency']:.0%}
- **Expressiveness:** {features['performance_scores']['expressiveness']:.0%}
- **Overall Score:** {features['performance_scores']['overall_score']:.0%}
- **Difficulty Estimate:** {features['performance_scores']['difficulty_estimate']}
- **Performance Level:** {features['performance_scores']['performance_level']}

---

Based on these actual audio analysis metrics, provide comprehensive, **actionable** RIAM-standard coaching feedback that students can immediately apply in their practice. 

## CRITICAL INSTRUCTIONS FOR FEEDBACK:

### Feedback Philosophy:
- **BE SPECIFIC**: Instead of "work on rhythm," say "practice measures 5-8 with a metronome at 80 BPM, clapping the rhythm before playing"
- **BE ACTIONABLE**: Every criticism must include HOW to fix it with concrete steps
- **BE ENCOURAGING**: Start with genuine strengths, end with motivation
- **USE STUDENT LANGUAGE**: Avoid overly technical jargon; explain concepts clearly
- **PROVIDE EXAMPLES**: Reference specific techniques, exercises, or practice methods by name

### Score Interpretation Guidelines:
- **70%+ = Strong**: Acknowledge excellence, suggest refinement
- **50-69% = Developing**: Needs focused practice, provide clear exercises  
- **Below 50% = Priority**: Requires immediate attention with detailed practice plan

---

## 1. Opening: What You Did Well (2-3 sentences)
Start with genuine, specific praise based on highest metric scores. Make the student feel their effort is recognized.

## 2. Technical Breakdown (Be ULTRA-SPECIFIC)

### Rhythm & Tempo (Stability: {features['tempo_rhythm']['tempo_stability_score']:.0%} | Regularity: {features['tempo_rhythm']['rhythm_regularity_score']:.0%})

**What the data shows:** [Interpret scores in plain language]

**If below 70%, provide THIS level of detail:**
- **Exercise 1:** "Set metronome to [X] BPM. Play each passage 5 times perfectly before moving on. Record yourself."
- **Exercise 2:** "Practice with subdivisions: Count '1-e-and-a, 2-e-and-a' out loud while clapping the rhythm"
- **Daily goal:** "15 minutes of metronome work, focusing on [specific measure ranges or patterns]"

### Intonation & Pitch (Stability: {features['pitch_intonation']['pitch_stability_score']:.0%} | Harmonic Content: {features['pitch_intonation']['harmonic_content_ratio']:.0%})

**What the data shows:** [Interpret scores in plain language]

**If below 70%, provide actionable steps:**
- **Tuning Exercise:** "Play long tones on [specific notes] for 8 counts each with a tuner visible. Aim for steady needle at 0 cents."
- **Scale Practice:** "Practice [key] scale at 60 BPM, holding each note for 4 beats, checking intonation"
- **Drone Practice:** "Use a drone app set to [key note]. Play scales/passages against the drone to train your ear"

### Tone Quality (Brightness: {features['tone_quality']['brightness_score']:.0%} | Consistency: {features['tone_quality']['brightness_consistency']:.0%})

**What the data shows:** [Interpret scores in plain language - too bright? too dark? inconsistent?]

**Specific exercises:**
- "Long tone routine: 4-4-4-4 breathing (4 beats in, hold 4, out 4, rest 4). Focus on [fuller/brighter/warmer] tone."
- "Record yourself playing [exercise]. Listen for tone changes between registers."
- "Practice messa di voce (crescendo-decrescendo) on single notes to develop control"

### Articulation (Attack Clarity: {features['articulation']['attack_clarity_score']:.0%} | Style: {features['articulation']['predominant_articulation']})

**What the data shows:** [Are note starts clear? Too harsh? Too soft? Too uniform?]

**Exercises for variety and control:**
- "Practice THIS pattern: 4 notes staccato, 4 legato, 4 mixed. Start slow (60 BPM) and gradually increase."
- "Tongue position exercise: Say 'tah-tah-tah' vs 'dah-dah-dah' to develop articulation options"
- "Use a mirror: Watch your [embouchure/bow contact/finger position] to ensure consistency"

## 3. Musical Expression (Range: {features['dynamics']['dynamic_range_db']:.1f}dB | Contrast: {features['dynamics']['dynamic_contrast_score']:.0%} | Expression: {features['dynamics']['dynamic_expressiveness']})

**What the data shows:** [Do dynamics exist? Are they varied? Are they musical?]

**Actionable practice:**
- "Mark your score: pp, p, mp, mf, f, ff at 5-10 second intervals. Practice exaggerating each level."
- "Record yourself: Can you HEAR the difference between your p and f? If not, make it more extreme."
- "Practice crescendos: Start at whisper volume, gradually build to full volume over 16 beats. Reverse for decrescendos."

## 4. Your Biggest Strengths (3-4 specific)
[List actual strong points from highest scores, being specific about what they're doing RIGHT]

Example: "Your tempo stability (95%) is exceptional - you have an excellent internal sense of pulse that many students struggle to develop."

## 5. Priority Improvements (Top 3 most important)
[List lowest scoring areas, but ALWAYS paired with how to fix them]

Example: "Attack clarity (45%) - Your note starts are unclear. FIX: Practice scales with exaggerated tongue/bow/finger attacks for 10 minutes daily."

## 6. This Week's Practice Plan (Be ULTRA-SPECIFIC)

**Daily 40-Minute Routine:**
- **0-10 min:** [Exact warm-up with specific exercises]
- **10-25 min:** [Technical work addressing weakest metric]
- **25-35 min:** [Musical passages applying technical improvements]
- **35-40 min:** [Specific challenging sections, with practice method]

**Weekly Focus:** [One clear goal: "By Friday, play measures 12-24 with 70%+ rhythm accuracy"]

## 7. Recommended Next Pieces/Études
Suggest 2-3 specific pieces BY NAME that address the weakest areas:
- "[Piece Name] by [Composer]" - WHY: "This develops [specific skill] through [specific technical feature]"

## 8. Quick Technical Exercises (3-5 with EXACT instructions)
Format: **Exercise Name | Time | Purpose | Instructions**

Example: 
- **Drone Scale Practice | 5 min | Intonation | Set drone to [key]. Play scale 3x, adjusting each note to eliminate beats. Record progress.**

## 9. Encouragement & Next Recording Goals
End with:
- Specific praise for effort/improvement potential
- Clear goal for next recording: "Next time, focus on improving [specific metric] by [specific method]"
- Motivational closer referencing their current level ({features['performance_scores']['performance_level']})

---

**FINAL REMINDERS:**
✓ Every critique MUST have a "how to fix it" 
✓ Use numbers: "practice 5 times," "10 minutes," "at 80 BPM"
✓ Reference scores to show you're analyzing THEIR performance
✓ Make feedback feel personal and achievable
✓ If piece/composer provided, include piece-specific technical advice
"""

        # Call Claude
        print("🤖 Generating coaching feedback with Claude...")
        
        response = self.bedrock_runtime.converse(
            modelId=self.model_id,
            messages=[{"role": "user", "content": [{"text": prompt}]}],
            inferenceConfig={
                "maxTokens": 6000,
                "temperature": 0.7,
            }
        )
        
        return response['output']['message']['content'][0]['text']
    
    def _provide_text_only_feedback(
        self,
        file_size_mb: float,
        audio_format: str,
        piece_name: Optional[str],
        composer: Optional[str],
        student_notes: Optional[str]
    ) -> dict:
        """Fallback to text-only feedback if audio analysis fails."""
        
        if not piece_name and not composer:
            return {
                "success": True,
                "feedback": f"""# RIAM AI Music Coach

Thank you for uploading your {file_size_mb:.1f}MB {audio_format} recording!

Unfortunately, I couldn't analyze your audio file. To provide feedback, please include:

## Required Information:
- **Piece Name** - What are you playing?
- **Composer** - Who wrote it?

## Optional:
- **Your Level** - RIAM Grade level
- **Specific Questions** - Techniques you're working on?

Re-submit with this information for comprehensive coaching feedback!
""",
                "model": self.model_id
            }
        
        # Build context and provide text-based feedback
        context = []
        if piece_name:
            context.append(f"Piece: {piece_name}")
        if composer:
            context.append(f"Composer: {composer}")
        if student_notes:
            context.append(f"Student notes: {student_notes}")
        
        prompt = f"""You are a master music teacher at RIAM. A student submitted a recording but audio analysis failed.

Context provided:
{chr(10).join(context)}

Provide comprehensive coaching feedback for this piece including:
1. Historical context and significance
2. Key technical challenges
3. Interpretive guidance
4. Practice plan (2-4 weeks)
5. Recommended recordings
6. Exercises for common challenges
7. Encouragement

Be specific to the piece mentioned."""

        response = self.bedrock_runtime.converse(
            modelId=self.model_id,
            messages=[{"role": "user", "content": [{"text": prompt}]}],
            inferenceConfig={"maxTokens": 4000, "temperature": 0.7}
        )
        
        return {
            "success": True,
            "feedback": response['output']['message']['content'][0]['text'],
            "model": self.model_id,
            "note": "Audio analysis unavailable - feedback based on piece information only"
        }


# Singleton instance
bedrock_service = BedrockService()
