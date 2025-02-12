// pages/_app.js
import "../styles/globals.css";
import "../styles/InterviewPanel.module.css"; // Add this line
import "../styles/ResumeViewer.module.css";


function MyApp({ Component, pageProps }) {
  return <Component {...pageProps} />;
}

export default MyApp;