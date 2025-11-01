import Link from "next/link";
import Layout from "../components/Layout";

export default function Home() {
  return (
    <Layout>
      <p>Welcome to TandemHire — a minimal AI-style recruiting MVP demo.</p>
      <ul>
        <li><Link href="/login">Login / Register</Link></li>
        <li><Link href="/candidate">Candidate Onboarding (Jack)</Link></li>
        <li><Link href="/jobs">Job Board</Link></li>
      </ul>
    </Layout>
  );
}
