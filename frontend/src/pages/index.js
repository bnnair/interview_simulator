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
      const response = await api.post('/api/start-interview', selectedResume, {}  );
      setCurrentQuestion(response.data.question);
      setCurrentAnswer(response.data.answer);
      setChatHistory(prev => [
        ...prev,
        { type: 'question', content: response.data.question },
        { type: 'answer', content: response.data.answer },
      ]);
    } catch (err) {
      setError('Failed to start interview');
      console.error('Error starting interview:', err.response?.data || err.message);
    } finally {
      setIsLoading(false);
    }
  };

  // const submitAnswer = async () => {
  //   setIsLoading(true);
  //   try {
  //     const response = await api.post('/api/submit-answer', 
  //       resume,
  //     );
  //     // Add evaluation and new question
  //     setChatHistory(prev => [
  //       ...prev,
  //       { type: 'question', content: response.data.question },
  //       { type: 'answer', content: response.data.answer }
  //     ]);
      
  //     setCurrentQuestion(response.data.question);
  //     setCurrentAnswer(response.data.answer);
  //   } catch (err) {
  //     setError('Failed to process answer');
  //     console.error(err);
  //   } finally {
  //     setIsLoading(false);
  //   }
  // };

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
          {!currentQuestion ? (
            <button 
              className={styles.startButton}
              onClick={startInterview} disabled={ isLoading }
            >
              {isLoading ? 'Generating Question and Answer...' : 'Start Interview'}
            </button>
          ) : (
            <InterviewPanel
              question={currentQuestion}
              answer={currentAnswer}
              onSubmit={startInterview}
              chatHistory={chatHistory}
              isLoading={isLoading}
            />
          )}
        </div>
      )}
    </div>
  );
}