// pages/index.js
import { useState, useEffect } from 'react';
import axios from 'axios';
import FileUpload from '../components/FileUpload';
import ResumeViewer from '../components/ResumeViewer';
import InterviewPanel from '../components/InterviewPanel';
import styles from '../styles/Home.module.css';

export default function Home() {
  const [uploadedResume, setUploadedResume] = useState(null);
  const [chatHistory, setChatHistory] = useState([]);
  const [currentQuestion, setCurrentQuestion] = useState('');
  const [currentAnswer, setCurrentAnswer] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [resumes, setResumes] = useState([]); // Store all resumes
  const [selectedResume, setSelectedResume] = useState(null); // Store the selected resume
  const [userQuestion, setUserQuestion] = useState(""); // Store user-input question
  const [useUserQuestion, setUseUserQuestion] = useState(false); // Toggle between user and app-generated question


  // Configure Axios to point to your Python backend
  // process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
  const api = axios.create({
    baseURL: 'http://localhost:8000',     
  });

  // Fetch all resumes from the backend
  useEffect(() => {
    const fetchResumes = async () => {
      try {
        const response = await api.get("/api/get-all-resumes");
        console.log("response-----", response)
        setResumes(response.data);
      } catch (err) {
        console.error("Error fetching resumes:", err);
        setError("Failed to fetch resumes");
      }
    };
    fetchResumes();
  }, []);

  // Handle dropdown selection
  const handleResumeSelect = (event) => {
    const selectedId = event.target.value;
    console.log("selectedID------->", selectedId )
    if (selectedId === "uploaded") {
      // Show the uploaded resume
      console.log("uploaded REsume----->", uploadedResume)
      setSelectedResume(uploadedResume);
    } else {
      // Show the selected resume from the dropdown
      const resume = resumes.find((r) => r.id === parseInt(selectedId));
      console.log("resume------selected--->", resume)
      setSelectedResume(resume.resume_data);
    }
  };


  const handleFileUpload = async (file) => {
    setIsLoading(true);
    setError(null);
  
    try {
      const formData = new FormData();
      formData.append('file', file);
      
      const response = await api.post('/api/upload-resume', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });

      setUploadedResume(response.data);

      // Refresh the list of resumes
      const resumesResponse = await api.get("/api/get-all-resumes");
      setResumes(resumesResponse.data);


    } catch (err) {
      setError('Failed to process resume. Please try again.');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  const startInterview = async () => {
    console.log("inside start interview method in index.js");
    setIsLoading(true);
    try {
      console.log("inside try block in start interview method in index.js");
      console.log("user question ---->", userQuestion)
      console.log("selected REsume ------", selectedResume)

      const payload = {
        resume : selectedResume,
        user_question :  useUserQuestion ? userQuestion : null,
      };


      const response = await api.post('/api/start-interview',  payload,{
        params: {
          userQuestion: useUserQuestion ? userQuestion : null,
        },
      });

      if (useUserQuestion) {
        // Use the user's question
        setCurrentQuestion(userQuestion);
      } else {      
        setCurrentQuestion(response.data.question);
      }
       
      setCurrentAnswer(response.data.answer);
      setChatHistory(prev => [
        ...prev,
        { type: 'question', content: currentQuestion },
        { type: 'answer', content: currentAnswer },
      ]);
      setUseUserQuestion(false)
      setUserQuestion("")
    } catch (err) {
      setError('Failed to start interview');
      console.error('Error starting interview:', err.response?.data || err.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className={styles.container}>
      <h1>AI Resume Interview Simulator</h1>
        {/* File upload section */}
        <div>
          <FileUpload onUpload={handleFileUpload} />
          {isLoading && <div className={styles.loading}>Uploading...</div>}
        </div>
        {/* Dropdown to Select a Resume */}
        <div>
          <h2>Select Resume</h2>
          <select onChange={handleResumeSelect} defaultValue="">
            <option value="" disabled>
              Select a resume
            </option>
            {/* Option for the uploaded resume */}
            {uploadedResume && (
              <option value="uploaded">
                Uploaded Resume - {uploadedResume.name}
              </option>
            )}
            {/* Options for resumes from the database */}
            {resumes.map((resume) => (
              <option key={resume.id} value={resume.id}>
                Resume ID: {resume.id} - {resume.resume_data.name}
              </option>
            ))}
          </select>
          {error && <div className={styles.error}>{error}</div>}
        </div>
        {(
          <div>
            { selectedResume ? (
              <ResumeViewer resume={selectedResume} />
            ) : (
              <p>No resume selected.</p>
            )}
          </div>
        )}
      <div className = {styles.questionSection}>
        <h2>Question Input</h2>
        <label className={styles.checkboxLabel}>
          <input
            type="checkbox"
            checked={useUserQuestion}
            onChange={(e) => setUseUserQuestion(e.target.checked)}
          />
          Use my own question
        </label>

        { useUserQuestion && (
        <div className={styles.textareaContainer}>
          <textarea
            value={userQuestion}
            onChange={(e) => setUserQuestion(e.target.value)}
            placeholder="Type your question here..."
            rows={4}
            cols={50}
          />
        </div>
        )}
        {/* Start interview button */}
        <button 
          className={styles.startButton}
          onClick={startInterview} disabled={ isLoading }
          >
          {isLoading  ? 'Generating Question and Answer...' : 'Start Interview'}
        </button>
      </div>
      {/* Interview Panel */}
      <div className={styles.InterviewPanel}>
          <InterviewPanel
              question={currentQuestion}
              answer={currentAnswer}
              onSubmit={startInterview}
              chatHistory={chatHistory}
              isLoading={isLoading}
          />
      </div>
    </div>
  )
};