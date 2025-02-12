import styles from '../styles/ResumeViewer.module.css';

export default function ResumeViewer({ resume }) {
  return (
    <div className={styles.container}>
      <h2>{resume.name}</h2>
      <p>{resume.contact_info}</p>
      <p>{resume.summary}</p>

      <h3>Experience</h3>
      {resume.experiences.map((exp, i) => (
        <div key={i} className={styles.experience}>
          <h4>{exp.company} - {exp.position}</h4>
          <p>{exp.duration}</p>
          <ul>
              {exp.responsibilities!=null && exp.responsibilities.map((resp, j) => (
                <li key={j}>{resp}</li>
            ))}
          </ul>
        </div>
      ))}

      <h3>Education</h3>
      {resume.education.map((edu, i) => (
        <div key={i} className={styles.education}>
          <h4>{edu.institution}</h4>
          <p>{edu.degree} in {edu.field_of_study}</p>
          <p>{edu.duration}</p>
        </div>
      ))}

      <h3>Certifications</h3>
      <div className={styles.skills}>
        {resume.certifications.map((cert, i) => (
          <span key={i} className={styles.skill}>
            {cert.name} 
          </span>
        ))}
      </div>
      
      <h3>Skills</h3>
      <div className={styles.skills}>
        {resume.skills.map((skill, i) => (
          <span key={i} className={styles.skill}>
            {skill.name} ({skill.description})
          </span>
        ))}
      </div>
    </div>
  );
}