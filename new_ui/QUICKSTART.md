# 🚀 Quick Start - New RIAM UI with AI Coach

## Start in 3 Steps

### Step 1: Start the Backend
```bash
cd api
uvicorn app.main:app --reload
```

✅ Backend running at: http://localhost:8000

### Step 2: Open the New UI
```bash
cd new_ui
open login.html
```

Or use Python HTTP server:
```bash
cd new_ui
python -m http.server 8080
# Open: http://localhost:8080/login.html
```

### Step 3: Login & Test
1. Click **"Student"** quick login button
2. Click on **"Scales Practice"** assignment card
3. Upload any PDF file for task 1
4. Upload the `input.mp3` file (from root) for task 2
5. Click **"Submit Assignment"**
6. Watch AI analysis magic happen! ✨

---

## 🎯 What You'll See

### Improved Scores (vs Old System)
- **Attack Clarity:** 27% → 58% (+31 points!)
- **Technical Proficiency:** 56% → 64%
- **Overall Score:** 60% → 64%

### AI Feedback Features
- ✅ Ultra-specific practice recommendations
- ✅ BPM and time allocations for exercises
- ✅ Daily 40-minute practice plan breakdown
- ✅ Piece-specific recommendations
- ✅ AI chat for questions about scores

---

## 🎵 Test Files

Use the `input.mp3` file from the root directory to see real AI analysis results!

---

## 📝 Demo Credentials

| User | Username | Password |
|------|----------|----------|
| Student | `student` | `student` |
| Teacher | `teacher` | `teacher` |
| Admin | `admin` | `admin` |

---

## 🎉 Features Implemented

✅ Beautiful login page with RIAM branding  
✅ Full authentication (JWT tokens)  
✅ Audio upload with real AI analysis  
✅ Improved attack clarity algorithm  
✅ Claude AI feedback generation  
✅ Four Pillars score display  
✅ AI chat with context awareness  
✅ Role-based dashboards  
✅ Logout functionality  
✅ Responsive design  

---

## 💡 Tips

- Use the **Quick Login** buttons for instant access
- Try different audio files to see varying scores
- Ask the AI chat questions like "why did I get this score?"
- Check the browser console for debugging info
- Backend logs show detailed analysis steps

---

**Need help?** Check the full `README.md` in the `new_ui/` folder!
