// pages/index.js
import { useState } from 'react';
import axios from 'axios';
import FileUpload from '../components/FileUpload';
import ResumeViewer from '../components/ResumeViewer';
import InterviewPanel from '../components/InterviewPanel';
import styles from '../styles/Home.module.css';

export default function Home() {
  const [resume, setResume] = useState(null);
  const [chatHistory, setChatHistory] = useState([]);
  const [currentQuestion, setCurrentQuestion] = useState('');
  const [currentAnswer, setCurrentAnswer] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);



  // Configure Axios to point to your Python backend
  // process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
  const api = axios.create({
    baseURL: 'http://localhost:8000',     
  });

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

      setResume(response.data);
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
      const response = await api.post('/api/start-interview', resume );
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

  const submitAnswer = async () => {
    // if (!userAnswer.trim()) return;
    
    setIsLoading(true);
    try {
      // Add user answer to history
      // setChatHistory(prev => [...prev, { type: 'answer', content: userAnswer }]);
      
      const response = await api.post('/api/submit-answer', 
        resume,
        // question: currentQuestion,
        // answer: currentAnswer
      );

      // Add evaluation and new question
      setChatHistory(prev => [
        ...prev,
        // { type: 'evaluation', content: response.data.evaluation },
        { type: 'question', content: response.data.question },
        { type: 'answer', content: response.data.answer }
      ]);
      
      setCurrentQuestion(response.data.question);
      setCurrentAnswer(response.data.answer);
    } catch (err) {
      setError('Failed to process answer');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className={styles.container}>
      <h1>AI Resume Interview Simulator</h1>
      
      <FileUpload onUpload={handleFileUpload} />
      
      {isLoading && <div className={styles.loading}>Processing...</div>}
      {error && <div className={styles.error}>{error}</div>}

      {resume && (
        <>
          <ResumeViewer resume={resume} />
          
          {!currentQuestion ? (
            <button 
              className={styles.startButton}
              onClick={startInterview}
            >
              Start Interview
            </button>
          ) : (
            <InterviewPanel
              question={currentQuestion}
              answer={currentAnswer}
              // onAnswerChange={setCurrentAnswer}
              // onSubmit={submitAnswer}
              onSubmit={startInterview}
              chatHistory={chatHistory}
              isLoading={isLoading}
            />
          )}
        </>
      )}
    </div>
  );
}