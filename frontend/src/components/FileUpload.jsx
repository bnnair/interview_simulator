import styles from '../styles/FileUpload.module.css';

export default function FileUpload({ onUpload }) {
  const handleFileChange = async (e) => {
    const file = e.target.files[0];
    if (file && file.type === 'application/pdf') {
      onUpload(file);
    } else {
      alert('Please upload a valid PDF file.');
    }
  };

  return (
    <div className={styles.container}>
      <label className={styles.label}>
        Upload Resume (PDF)
        <input
          type="file"
          accept="application/pdf"
          onChange={handleFileChange}
          className={styles.input}
        />
      </label>
    </div>
  );
}