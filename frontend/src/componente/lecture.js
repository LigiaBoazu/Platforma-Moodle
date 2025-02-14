import React from 'react';
import { useParams } from 'react-router-dom';

function LecturePage() {
  const { lectureId } = useParams();
  
  return (
    <div>
      <h1>Lecture Page</h1>
      <p>Lecture ID: {lectureId}</p>
    </div>
  );
}

export default LecturePage;