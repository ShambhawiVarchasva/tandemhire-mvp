import { useState, useEffect } from "react";
import Layout from "../components/Layout";

const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function Candidate() {
  const [userId, setUserId] = useState("");
  const [title, setTitle] = useState("");
  const [years, setYears] = useState("");
  const [skills, setSkills] = useState("");
  const [location, setLocation] = useState("");
  const [salary, setSalary] = useState("");
  const [resumeFile, setResumeFile] = useState(null);
  const [summary, setSummary] = useState(null);

  useEffect(() => {
    const uid = localStorage.getItem("user_id");
    if (uid) setUserId(uid);
  }, []);

  async function onboard() {
    if (!userId) { alert("No user_id — register first"); return; }
    const body = {
      current_title: title,
      years_experience: years,
      skills,
      location,
      salary_expectation: salary
    };
    const res = await fetch(`${API}/jack/onboard/${userId}`, {
      method: "POST", headers: {"Content-Type":"application/json"}, body: JSON.stringify(body)
    });
    const d = await res.json();
    if (res.ok) setSummary(d.summary);
    else alert(JSON.stringify(d));
  }

  async function uploadResume() {
    if (!userId) { alert("No user_id"); return; }
    if (!resumeFile) { alert("Choose resume file"); return; }
    const form = new FormData();
    form.append("file", resumeFile);
    const res = await fetch(`${API}/jack/upload_resume/${userId}`, {
      method: "POST", body: form
    });
    const d = await res.json();
    if (res.ok) alert("Uploaded");
    else alert(JSON.stringify(d));
  }

  async function getMatches() {
    if (!userId) { alert("No user_id"); return; }
    const res = await fetch(`${API}/match/${userId}`);
    const d = await res.json();
    if (res.ok || res.status === 200) {
      alert(JSON.stringify(d, null, 2));
    } else alert(JSON.stringify(d));
  }

  return (
    <Layout>
      <h2>Candidate Onboarding — Jack (TandemHire)</h2>
      <p>user_id: <b>{userId || "not set (register first)"}</b></p>

      <input placeholder="Current title" value={title} onChange={e=>setTitle(e.target.value)} />
      <br/>
      <input placeholder="Years experience" value={years} onChange={e=>setYears(e.target.value)} />
      <br/>
      <input placeholder="Skills (comma separated)" value={skills} onChange={e=>setSkills(e.target.value)} />
      <br/>
      <input placeholder="Location" value={location} onChange={e=>setLocation(e.target.value)} />
      <br/>
      <input placeholder="Salary expectation" value={salary} onChange={e=>setSalary(e.target.value)} />
      <br/>
      <button onClick={onboard}>Run Jack Onboarding</button>
      <hr/>
      <h3>Resume Upload</h3>
      <input type="file" onChange={(e)=>setResumeFile(e.target.files[0])} />
      <button onClick={uploadResume}>Upload Resume</button>
      <hr />
      <button onClick={getMatches}>Get Matching Jobs</button>
      {summary && <div><h4>Summary</h4><pre>{summary}</pre></div>}
    </Layout>
  );
}
