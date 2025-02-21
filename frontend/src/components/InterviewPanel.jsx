// import styles from '../styles/InterviewPanel.module.css';

// export default function InterviewPanel({
//   question,
//   answer,
//   onSubmit,
//   chatHistory,
//   isLoading,
// }) {
//   return (
//     <div className={styles.container}>
//       <h1>Interview Questions and Answers</h1>
//       <div className={styles.chatHistory}>
//         {chatHistory.map((chat, i) => (
//           <div
//             key={i}
//             className={`${styles.chatBubble} ${
//               chat.type === 'question' ? styles.question : styles.answer
//             }`}
//           >
//             <p>{chat.content}</p>
//           </div>
//         ))}
//       </div>

//       <div className={styles.inputArea}>{}
//         <button onClick={onSubmit} disabled={isLoading}>
//           {isLoading ? 'Generating Question and Answer...' : 'Next Question'}
//         </button>
//       </div>
//     </div>
//   );
// }

import React from "react";
import styles from "../styles/InterviewPanel.module.css";

const InterviewPanel = ({ question, answer, chatHistory, isLoading }) => {
  return (
    <div className={styles.panel}>
      <h2>Interview Session</h2>

      {/* Chat History */}
      <div className={styles.chatHistory}>
        {chatHistory.map((chat, index) => (
          <div
            key={index}
            className={`${styles.chatBubble} ${
              chat.type === "question" ? styles.question : styles.answer
            }`}
          >
            <p>{chat.content}</p>
          </div>
        ))}
      </div>

      {/* Current Question and Answer */}
      {isLoading && <p>Loading...</p>}
      {question && (
        <div className={styles.currentQuestion}>
          <h3>Question:</h3>
          <p>{question}</p>
        </div>
      )}
      {answer && (
        <div className={styles.currentAnswer}>
          <h3>Answer:</h3>
          <p>{answer}</p>
        </div>
      )}
    </div>
  );
};

export default InterviewPanel;