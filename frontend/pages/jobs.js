import Layout from "../components/Layout";
import { useEffect, useState } from "react";

const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function Jobs() {
  const [jobs, setJobs] = useState([]);
  useEffect(() => {
    async function load() {
      const res = await fetch(`${API}/jobs`);
      const d = await res.json();
      setJobs(d);
    }
    load();
  }, []);
  return (
    <Layout>
      <h2>Jobs</h2>
      <ul>
        {jobs.map(j => (
          <li key={j.id}>
            <b>{j.title}</b> at {j.company} — {j.location}
            <div>{j.description}</div>
            <div>Skills: {j.required_skills}</div>
          </li>
        ))}
      </ul>
    </Layout>
  );
}
