import styles from '../styles/ChatBubble.module.css';

export default function ChatBubble({ type, content }) {
  return (
    <div className={`${styles.bubble} ${styles[type]}`}>
      <p>{content}</p>
    </div>
  );
}