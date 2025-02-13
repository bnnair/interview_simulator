import styles from '../styles/InterviewPanel.module.css';

export default function InterviewPanel({
  question,
  answer,
  onSubmit,
  chatHistory,
  isLoading,
}) {
  return (
    <div className={styles.container}>
      <div className={styles.chatHistory}>
        {chatHistory.map((chat, i) => (
          <div
            key={i}
            className={`${styles.chatBubble} ${
              chat.type === 'question' ? styles.question : styles.answer
            }`}
          >
            <p>{chat.content}</p>
          </div>
        ))}
      </div>

      <div className={styles.inputArea}>{}
        <button onClick={onSubmit} disabled={isLoading}>
          {isLoading ? 'generating Question...' : 'Start Interview'}
        </button>
      </div>
    </div>
  );
}